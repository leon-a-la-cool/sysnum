open Netlist_ast
open Graph

exception Combinational_cycle
exception Test


let read_exp eq = 
  let p = ref [] in
  let ajouter x = if List.mem x !p then () else p:=x::!p in

  let rec aux_arg = function
    |Avar x -> ajouter x
    |_->()
in
  let rec aux_eq = function
    | Earg arg -> aux_arg arg
    | Ereg  _ -> ()
    | Enot  arg -> aux_arg arg
    | Ebinop  (binop,arg1,arg2)-> aux_arg arg1; aux_arg arg2
    | Emux (arg1,arg2,arg3) -> aux_arg arg1;aux_arg arg2; aux_arg arg3
    | Erom (_,_,arg) -> aux_arg arg
    | Eram (_,_,arg1,arg2,arg3,arg4) -> () (*aux_arg arg1;aux_arg arg2;aux_arg arg3;aux_arg arg4;*)
    | Econcat (arg1,arg2)-> aux_arg arg1; aux_arg arg2
    | Eslice (_,_,arg) -> aux_arg arg
    | Eselect (_,arg) -> aux_arg arg
in aux_eq eq;!p



let schedule p = 
  let eqlist = p.p_eqs in 
  let eqtab = Array.of_list eqlist in 
  let deptab = Array.map (fun (ident,eq)-> read_exp eq) (Array.copy(eqtab)) in 
  let g = mk_graph () in
  List.iter (fun x-> add_node g x) eqlist ;
for i=0 to (Array.length eqtab -1) do
  let x = fst (eqtab.(i)) in
  for j=0 to (Array.length eqtab -1) do
    if List.mem x (deptab.(j)) then add_edge g (eqtab.(i)) (eqtab.(j))
    done
  done;
try begin let p_eqs = topological g in 
{p_eqs = p_eqs;p_inputs = p.p_inputs;p_outputs = p.p_outputs;p_vars = p.p_vars} end 
with Cycle -> raise Combinational_cycle