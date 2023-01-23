
import tkinter as tk

nbtruc=7

root=tk.Tk()
root.title("Horloge")

c=tk.Canvas(root,width=600,height=80)


def color(n,k):
    nb=n
    if nb%10:
        c.create_rectangle(15+k*40,35,35+k*40,40,fill="red")
    else:
        c.create_rectangle(15+k*40,35,35+k*40,40,fill="white")
    nb=nb//10
    if nb%10:
        c.create_rectangle(10+k*40,15,15+k*40,35,fill="red")
    else:
        c.create_rectangle(10+k*40,15,15+k*40,35,fill="white")
    nb=nb//10
    if nb%10:
       c.create_rectangle(10+k*40,40,15+k*40,60,fill="red")
    else:
       c.create_rectangle(10+k*40,40,15+k*40,60,fill="white")
    nb=nb//10
    if nb%10:
        c.create_rectangle(15+k*40,60,35+k*40,65,fill="red")
    else:
        c.create_rectangle(15+k*40,60,35+k*40,65,fill="white")
    nb=nb//10
    if nb%10:
        c.create_rectangle(35+k*40,40,40+k*40,60,fill="red")
    else:
        c.create_rectangle(35+k*40,40,40+k*40,60,fill="white")
    nb=nb//10
    if nb%10:
        c.create_rectangle(35+k*40,15,40+k*40,35,fill="red")
    else:
        c.create_rectangle(35+k*40,15,40+k*40,35,fill="white")
    nb=nb//10
    if nb%10:
        c.create_rectangle(15+k*40,10,35+k*40,15,fill="red")
    else:
        c.create_rectangle(15+k*40,10,35+k*40,15,fill="white")


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