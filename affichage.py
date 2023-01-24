
import tkinter as tk

nbtruc=7
file=open("time.txt","w")
file.close()
root=tk.Tk()
root.title("Horloge")

c=tk.Canvas(root,width=360,height=140,background="lightgray")
def color(n,k):
    if k%8==6 or k%8==7:
        dec=1
    else:
        dec=0 
    L=[[15,35,35,40],[10,15,15,35],[10,40,15,60],[15,60,35,65],[35,40,40,60],[35,15,40,35],[15,10,35,15]]
    nb=n
    for i in range(7):
        if nb%10:
            col="black"
        else:
            col="lightgrey"
        c.create_rectangle(L[i][0]+(k%8)*40+((k+1)%2)*5-dec*10,L[i][1]+(k//8)*60,L[i][2]+(k%8)*40+((k+1)%2)*5-dec*10,L[i][3]+(k//8)*60,fill=col,outline=col)
        nb=nb//10

c.create_oval(163,80,172,89,fill="black")
c.create_oval(163,106,172,115,fill="black")
c.create_oval(83,80,92,89,fill="black")
c.create_oval(83,106,92,115,fill="black")
c.create_line(83,60,92,15,fill="black",width=4,capstyle="round")
c.create_line(163,60,172,15,fill="black",width=4,capstyle="round")

M=[0 for i in range(2*nbtruc)]

def updateEvryticks():
    file=open("time.txt","r")
    try:
        for b in range (nbtruc):
            nb=str(file.readline())
            for k in range(2):
                n=int(nb[0+k*7:7+k*7])
                if n!=M[2*b+k]:
                    color(n,2*b+k)
                    M[2*b+k] = n
    except ValueError:
        pass

    file.close()
    root.after(100,updateEvryticks)

c.pack()

updateEvryticks()
root.mainloop()