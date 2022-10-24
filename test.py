"""test"""

import tkinter


def ende():
    main.destroy()

main= tkinter.Tk()
main.title("Spiel")
main.geometry("600x600")

x1=50
y1=50

tsv=tkinter.Label(main,text="SV")
tsv.place(x=x1,y=y1)

tsp = tkinter.Label(main, text="Spieler A")
tsp.place(x=x1,y=y1+50)

lh=tkinter.Label(main,text= "A   B   C   D   E   F   G   H   I   J")
lh.place(x=x1+50, y=y1+80)

i=0
for z in range(10):
    lv=tkinter.Label(main, text=z)
    lv.place(x=x1+30, y=y1+100+z*30)
    for s in range(10):
        btn=tkinter.Button(main, text=i)
        btn.place(x=x1+50+s*30, y=y1+100+z*30, width=28, height=28)
        i=i+1

b=tkinter.Button(main, text="Ende", command=ende)
b["anchor"]="center"
b.place(x=x1+50, y=y1+450)

main.mainloop()
