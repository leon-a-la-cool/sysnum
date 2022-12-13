
open Netlist_ast



let print_only = ref false
let number_steps = ref (-1)

(* fonctions de calcul*)


let rec enot = function 
  |VBit b -> VBit (not b)
  |VBitArray t ->  VBitArray (Array.map (fun x->not x) t)


let rec ebinop binop arg1 arg2 = 
  let aux () = match binop with
    |Or -> (||)
    |Xor -> fun x -> fun y -> (x||y)&&(not(x&&y))
    |And -> (&&)
    |Nand -> fun x -> fun y -> not (x&&y)
  in 
  match arg1,arg2 with
    | VBit x1, VBit x2 -> VBit (aux () x1 x2)
    | VBitArray t1, VBitArray t2 -> let n = Array.length t1
      in let t = Array.make n false in 
      for i =0 to (n-1) do 
        t.(i)<-aux () (t1.(i)) (t2.(i))
      done; VBitArray t
    | VBit x1, VBitArray [|x2|]| VBitArray [|x1|], VBit x2 -> VBit (aux () x1 x2)
    | _ -> failwith "taille invalide1"

(*let rec emux (choix,a,b) = 
    match choix with
      |VBit c |VBitArray [|c|] -> 
        begin match a,b with
          |VBit a0,VBitArray [|b0|]|VBitArray [|a0|],VBit b0|VBit a0,VBit b0 | VBitArray [|a0|], VBitArray [|b0|] -> if not c then VBit a0 else VBit b0 
          |_ -> failwith "taille invalide2" end
      |VBitArray tc ->
        begin match a,b with
          |VBitArray ta, VBitArray tb -> (let n = Array.length tc in let t = Array.make n false in 
            for i = 0 to (n-1) do 
              t.(i)<-if tc.(i) then tb.(i) else ta.(i)
            done; VBitArray t)
          |_ -> failwith "taille invalide3" end*)
   
let rec emux outputname (choix,a,b) = 
  match choix with
    |VBit c |VBitArray [|c|] -> 
      begin match a,b with
        |VBit a0,VBitArray [|b0|]|VBitArray [|a0|],VBit b0|VBit a0,VBit b0 -> if not c then VBit a0 else VBit b0 
        |VBitArray ta, VBitArray tb -> (let n = Array.length ta in let t = Array.make n false in 
          for i = 0 to (n-1) do 
            t.(i)<-if c then tb.(i) else ta.(i)
          done; VBitArray t) 
        |_ ->failwith ("taille invalide 2 "^outputname) end
    |_ -> failwith "taille invalide3" 


(*conversion*)

let int_of_bits x = match x with
    |VBit b -> if b then 1 else 0
    |VBitArray t -> let n = ref ((Array.length t) - 1) in let valeur = ref 0 in Array.iter (fun b -> (if b then valeur := !valeur + 1 lsl !n; decr n)) t; !valeur  


(****************)


let simulator program number_steps = 
  print_newline();

  (*Initialisation de la mémoire et de l'environement*)
  let memoiresROM = Hashtbl.create 0 in
  let memoiresRAM = Hashtbl.create 0 in
  let env = ref Env.empty in
  let envprecedent = ref Env.empty in
  let ecritureRAM = Stack.create () in
  
  let initialiser_mem eq = match eq with
  | outname,Erom (addr_size,word_size,adr) -> print_string ("Choisissez un fichier pour initialiser la ROM associée à " ^ outname ^ " (laisser vide pour initialiser à 0 ):\n");

    let rom = Array.make (1 lsl addr_size) (VBitArray [||]) in 
    for i = 0 to ((1 lsl addr_size) - 1) do
      rom.(i)<-VBitArray (Array.make word_size false)
    done;

    let rompath = read_line() in begin
      if rompath <> "" then
        try (
          let ic = open_in rompath  in 
          for i = 0 to ((1 lsl addr_size) - 1) do
            let mot = Array.make word_size false in
            let ligne = input_line ic in
            for j = 0 to (word_size - 1) do 
              mot.(j)<- ligne.[j] = '1'
            done;
            rom.(i) <- VBitArray mot 
          done
        ) 
        with _ -> failwith "Invalid Input.\n"
      else
        for i = 0 to ((1 lsl addr_size)-1) do
          rom.(i) <- VBitArray (Array.make word_size false)
        done end;
    Hashtbl.add memoiresROM outname rom
    

  | outname,Eram (addr_size,word_size,read_addr,write_enable,write_addr,data) -> print_string ("Choisissez un fichier pour initialiser la RAM associée à " ^ outname ^ " (laisser vide pour initialiser à 0 ):\n");
    
    let ram = Array.make (1 lsl addr_size) (VBitArray [||]) in 
    for i = 0 to ((1 lsl addr_size) - 1) do
      ram.(i)<-VBitArray (Array.make word_size false)
    done;

    let rampath = read_line() in begin
      if rampath <> "" then
        try (
          let ic = open_in rampath  in 
          for i = 0 to ((1 lsl addr_size) - 1) do
            let mot = Array.make word_size false in
            let ligne = input_line ic in
            for j = 0 to (word_size - 1) do 
              mot.(j)<- ligne.[j] = '1'
            done;
            ram.(i) <- VBitArray mot 
          done
        ) 
        with _ -> failwith "Invalid Input.\n"
      else
        for i = 0 to ((1 lsl addr_size)-1) do
          ram.(i) <- VBitArray (Array.make word_size false)
        done end;
    Hashtbl.add memoiresRAM outname ram
  | _ -> ()
  in
  List.iter initialiser_mem (program.p_eqs);

  (*Fonction de calcul*)

  let rec calcularg = function
    |Avar ident -> Env.find ident (!env) 
    |Aconst value -> value

  in

  let rec calcul outputname= function
    | Earg arg -> calcularg arg
    | Ereg  ident -> (try Env.find ident (!envprecedent) with Not_found -> match (Env.find ident (program.p_vars)) with 
                                                                            |TBitArray n -> VBitArray (Array.make n false)
                                                                            |TBit -> VBit false)
    | Enot  arg -> enot (calcularg arg)
    | Ebinop  (binop,arg1,arg2)-> ebinop binop (calcularg arg1) (calcularg arg2)
    | Emux (arg1,arg2,arg3) -> emux outputname ((calcularg arg1),(calcularg arg2),(calcularg arg3))
    | Erom (addrsize,wordsize,adr) -> 
          let rom = Hashtbl.find memoiresROM outputname in
          let n = int_of_bits (calcularg adr) in 
          rom.(n)
    | Eram (addrsize,wordsize,read_addr,write_enable,write_addr,data) -> begin
          let ram = Hashtbl.find memoiresRAM outputname in 
          let x = (let n = int_of_bits (calcularg read_addr) in ram.(n)) in
          if (calcularg write_enable) = VBit true then Stack.push (outputname,write_addr,data) ecritureRAM ;
          x end
    | Econcat (arg1,arg2)-> begin match calcularg arg1,calcularg arg2 with 
          |VBitArray t1, VBitArray t2 -> VBitArray (Array.concat [t1;t2])
          |VBit v1, VBitArray t2 -> VBitArray (Array.concat [[|v1|];t2])
          |VBitArray t1, VBit v2 -> VBitArray (Array.concat [t1;[|v2|]])
          |VBit v1, VBit v2 -> VBitArray [|v1;v2|] end
    | Eslice (i,j,arg) -> begin match calcularg arg with 
          |VBitArray t -> VBitArray (Array.sub t i (j-i+1))
          |VBit v -> VBit v end 
    | Eselect (i,arg) -> begin match calcularg arg with 
          |VBitArray t -> VBit (t.(i))
          |VBit v -> VBit v end 
  in


  let ecrireram () = while not (Stack.is_empty ecritureRAM) do let outname,write_addr,data = Stack.pop ecritureRAM in let n = int_of_bits (calcularg write_addr) in (Hashtbl.find memoiresRAM outname).(n) <- (calcularg data) done in

  let traitereq eq = 
    let outputident,expression = eq in env := (Env.add outputident (calcul outputident expression ) (!env)) 
  in


  
  
  let prog_ordre = Scheduler.schedule program in
  let compteur = ref number_steps in 
  let step = ref 1 in



  let rec traiter_input ident = 
    print_string (ident ^ "=? ");
    let x = read_line () in 
    let ty = Env.find ident (prog_ordre.p_vars) in
    match ty with
      |TBit -> begin
        match x with 
          |"0"|"1" -> env:=Env.add ident (VBit (x="1")) (!env)
          |_ -> print_string ("Wrong Input.\n"); traiter_input ident end
      |TBitArray n -> 
        if String.length x = n then (
          let t =(Array.make n false ) and b = ref false in 
          for i = 0 to (n-1) do
            match x.[i] with
              |'0'|'1' -> t.(i)<- x.[i] = '1' 
              |_ -> b:= true
          done;
          if !b then (
            print_string ("Wrong Input.\n"); traiter_input ident)
          else 
            env:=Env.add ident (VBitArray t) (!env))
        else
          (print_string ("Wrong Input Size.\n"); traiter_input ident)

  in  




  (*boucle d'éxécution*)

  while (!compteur = -1) || (!compteur > 0) do
    print_string "Step ";print_int (!step);print_string ":\n";incr step;
    List.iter traiter_input prog_ordre.p_inputs;
    List.iter (*(fun e -> (match (Env.find (fst e) prog_ordre.p_vars) with |TBitArray n ->print_string (fst e); print_int n;print_newline () |_-> print_string (fst e); print_int (-1);print_newline () ); traitereq e)*) traitereq (prog_ordre.p_eqs);
    ecrireram ();
    List.iter (fun ident ->(  print_string (ident ^ "= ");match (Env.find ident (!env)) with 
      |VBit v -> (print_string (if v then "1\n" else "0\n")) 
      |VBitArray t -> (Array.iter (fun x -> print_string (if x then "1" else "0")) t; print_string "\n")))
    prog_ordre.p_outputs;


    envprecedent := !env;
    env := Env.empty;
    compteur := if (!compteur) <> (-1) then !compteur - 1 else !compteur;
    


  done




let compile filename =
  try
    let p = Netlist.read_file filename in
    begin try
        let p = Scheduler.schedule p in
        print_int !number_steps;
        simulator p !number_steps
      with
        | Scheduler.Combinational_cycle ->
            Format.eprintf "The netlist has a combinatory cycle.@.";
    end;
  with
    | Netlist.Parse_error s -> Format.eprintf "An error accurred: %s@." s; exit 2

let main () =
  Arg.parse
    ["-n", Arg.Set_int number_steps, "Number of steps to simulate"]
    compile
    ""
;;

main ()
