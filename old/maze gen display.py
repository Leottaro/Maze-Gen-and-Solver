from time import sleep
import tkinter as tk
from random import randrange

def Rectangle(x, y, size, id="", type=0, color="#E1E1E1", width=1):
    canvas.create_rectangle(x, y, x+size, y+size, outline=color, fill=color, width=width, tags=id)
    return [type, color, id]



size = int(input("quelle taille ?\n"))
if size%2==0: size+=1    # il faut un nombre impair
window = tk.Tk()
window_size = size*((window.winfo_screenheight()*0.8)//size)
wall_size = window_size / size

window.title("ez")
window.geometry(str(int(window_size))+"x"+str(int(window_size)))
window.configure(background="#EEEEEE")
window.resizable(width=False, height=False)



cells = []
canvas = tk.Canvas(background="#EEEEEE", width=window_size, height=window_size, borderwidth=0, highlightthickness=0)
canvas.pack()

####$$$$????ééééiiii++++::::----....    générer la grille    ....----::::++++iiiiéééé????$$$$####
i, j = 0, 0
for y in range(size):
    line = []
    for x in range(size):
        i += 1
        if x%2 == 0 or y%2 == 0:
            line.append(Rectangle(x*wall_size, y*wall_size, wall_size, color="#111111", id=str(i)))
        else:
            j += 1
            line.append(Rectangle(x*wall_size, y*wall_size, wall_size, color="#EEEEEE", id=str(i), type=j))
    cells.append(line)
    
# faire entrée + sortie
canvas.itemconfig(cells[1][0][2], fill=cells[1][1][1], outline=cells[1][1][1])
cells[1][0][0], cells[1][0][1] = cells[1][1][0], cells[1][1][1]
canvas.itemconfig(cells[size-2][size-1][2], fill=cells[size-2][size-2][1], outline=cells[size-2][size-2][1])
cells[size-2][size-1][0], cells[size-2][size-1][1] = cells[size-2][size-2][0], cells[size-2][size-2][1]



canvas.update()
sleep(0.5)
####$$$$????ééééiiii++++::::----....    générer le labyrinthe    ....----::::++++iiiiéééé????$$$$####
count = 0
while count < (size**2):
    count = 0
    cell1 ,cell2 = [-1, '#111111', '-1'], [-1, '#111111', '-1']

    while cell1[0] == cell2[0]:
        x = randrange(1,size-1)
        y = x
        while x%2 == y%2:
            y = randrange(1,size-1)

        if x%2 == 0:        # le mur est vertical, cases à gauche et à droite
            cell1 = cells[y][x-1]
            cell2 = cells[y][x+1]
        else:               # le mur est horizontal, cases en haut es en bas
            cell1 = cells[y-1][x]
            cell2 = cells[y+1][x]
            
    if cell1[0] > cell2[0]:    # pour qu'il ne reste que des uns à la fin
        cell1, cell2 = cell2, cell1
        
    canvas.itemconfig(cells[y][x][2], fill=cell1[1], outline=cell1[1])
    cells[y][x][0], cells[y][x][1] = cell1[0], cell1[1]
    count += 1
    for j in range(size):    # on unifie les cases des deux cotés du mur
        for i in range(size):
            if cells[j][i][0] == cell2[0] and cells[j][i][2] != cell2[2]:
                canvas.itemconfig(cells[j][i][2], fill=cell1[1], outline=cell1[1])
                cells[j][i][0], cells[j][i][1] = cell1[0], cell1[1]
            if cells[j][i][0] == 1 or cells[j][i][0] == 0:
                count += 1
    canvas.itemconfig(cell2[2], fill=cell1[1], outline=cell1[1])
    cell2[0], cell2[1] = cell1[0], cell1[1]
    canvas.update()

sleep(0.5)
i = size//8
while i != 0:    # on casse des murs pour créer un labyrinthe complexe (a plusieurs chemins)
    x = randrange(1,size-1)
    y = x
    while x%2 == y%2:
        y = randrange(1,size-1)
        
    if cells[y][x][0] == 0:
        canvas.itemconfig(cells[y][x][2], fill="#EEEEEE", outline="#EEEEEE")
        cells[y][x][0], cells[y][x][1] = 1, "#EEEEEE"
        i -= 1



canvas.update()
sleep(0.5)
####$$$$????ééééiiii++++::::----....    résoudre le labyrinthe    ....----::::++++iiiiéééé????$$$$####
canvas.itemconfig(cells[size-2][size-1][2], fill="#1111EE", outline="#1111EE")
cells[size-2][size-1][0] = -1
canvas.itemconfig(cells[size-2][size-2][2], fill="#1111EE", outline="#1111EE")
cells[size-2][size-2][0] = -2
i = -1
temp = []
while cells[1][0][0] == 1:    # on part de la sortie et on compte les cases jusqu'au départ
    i -= 1
    for y in range(1, size-1):
        for x in range(1, size-1):
            if cells[y][x][0] == i:
                if cells[y][x-1][0] == 1: 
                    canvas.itemconfig(cells[y][x-1][2], fill="#1111EE", outline="#1111EE")
                    cells[y][x-1][0] = i-1
                if cells[y][x+1][0] == 1: 
                    canvas.itemconfig(cells[y][x+1][2], fill="#1111EE", outline="#1111EE")
                    cells[y][x+1][0] = i-1
                if cells[y-1][x][0] == 1: 
                    canvas.itemconfig(cells[y-1][x][2], fill="#1111EE", outline="#1111EE")
                    cells[y-1][x][0] = i-1
                if cells[y+1][x][0] == 1: 
                    canvas.itemconfig(cells[y+1][x][2], fill="#1111EE", outline="#1111EE")
                    cells[y+1][x][0] = i-1
    canvas.update()

i = cells[1][0][0] -2
canvas.itemconfig(cells[1][0][2], fill="#11EE11", outline="#11EE11")
cells[1][0][0] = 0.1
while cells[size-2][size-1][0] != 0.1:    # on rebrousse chemin en suivant les cases comptées
    i += 1
    for y in range(0, size):
        for x in range(0, size-1):
            if cells[y][x][0] == 0.1: 
                if cells[y][x-1][0] == i: 
                    canvas.itemconfig(cells[y][x-1][2], fill="#11EE11", outline="#11EE11")
                    cells[y][x-1][0] = 0.1
                if cells[y][x+1][0] == i: 
                    canvas.itemconfig(cells[y][x+1][2], fill="#11EE11", outline="#11EE11")
                    cells[y][x+1][0] = 0.1
                if cells[y-1][x][0] == i: 
                    canvas.itemconfig(cells[y-1][x][2], fill="#11EE11", outline="#11EE11")
                    cells[y-1][x][0] = 0.1
                if cells[y+1][x][0] == i: 
                    canvas.itemconfig(cells[y+1][x][2], fill="#11EE11", outline="#11EE11")
                    cells[y+1][x][0] = 0.1
            if size<51 and cells[y][x][0] < i: 
                #canvas.itemconfig(cells[y][x][2], fill="#EEEEEE", outline="#EEEEEE")
                cells[y][x][0] = 1
    canvas.update()



####$$$$????ééééiiii++++::::----....    FINITOOOOOO    ....----::::++++iiiiéééé????$$$$####
print("FINITOOOOOO")
window.mainloop()
