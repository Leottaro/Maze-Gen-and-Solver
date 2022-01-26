from random import randint
import tkinter as tk

class Maze:
    def __init__(self, width, height, canv):
        self.W = width -width%2 +1
        self.H = height -height%2 +1
        self.__grid = [[0 for x in range(self.W)] for y in range(self.H)]

        self.__generated = False
        self.__genState = 2

        self.__resolved = False

        self.Canvas = canv
        self.__rectangles = []

        """
        size:  w,h
        walls: 0.5(wh +w +h) -1.5
        ways:  0.5(wh -w -h) +1.5
        """

    def __str__(self):
        return "\n".join([" ".join(["#" if obj==0 else "." if obj==2 else " " for obj in line]) for line in self.__grid])
        #return "\n".join([" ".join([str(obj) for obj in line]) for line in self.__grid])

    def getgrid(self):
        return self.__grid    

    def getcell(self, x, y, warn = True):
        if 0 <= x < self.W and 0 <= y < self.H:
            return self.__grid[y][x]
        elif warn: print("getcell out of range")
    
    def setcell(self, x, y, obj, warn = True):
        if x < self.W and y < self.H:
            self.__grid[y][x] = obj
        elif warn: print("setcell out of range")

    def getRect(self, x, y):
        return( MyCanvas.itemcget(x+1 +y*self.W, "fill") )

    def setRect(self, x, y, color, update = True):
        self.Canvas.itemconfig(x+1 +y*self.W, fill=color, outline=color)
        if update:    self.Canvas.update()


    def Generate_v2(self):
        i = 0
        for y in range(self.H):
            for x in range(self.W):
                if x%2 != 0 and y%2 != 0: 
                    i += 1
                    self.setcell(x, y, i)
                    self.__rectangles.append(self.Canvas.create_rectangle(x*wall_size, y*wall_size, (x+1)*wall_size, (y+1)*wall_size, fill="#EEEEEE", outline="#EEEEEE", width=1))
                else:
                    self.setcell(x, y, 0)
                    self.__rectangles.append(self.Canvas.create_rectangle(x*wall_size, y*wall_size, (x+1)*wall_size, (y+1)*wall_size, fill="#111111", outline="#111111", width=1))
                
        self.setcell(0, 1, self.getcell(1, 1))
        self.setRect(0, 1, self.getRect(1, 1), False)
        self.setcell(self.W-1, self.H-2, self.getcell(self.W-2, self.H-2))
        self.setRect(self.W-1, self.H-2, self.getRect(self.W-2, self.H-2))
        

        total_ways = 0.5*(self.W*self.H - self.W - self.H) + 1.5
        while self.__genState != total_ways:
            cell1 ,cell2 = 0, 0

            while cell1 == cell2:
                x = randint(1,self.W-2)
                y = x
                while x%2 == y%2:
                    y = randint(1,self.H-2)

                if x%2 == 0:
                    cell1 = self.getcell(x-1, y)
                    cell2 = self.getcell(x+1, y)
                else:
                    cell1 = self.getcell(x, y-1)
                    cell2 = self.getcell(x, y+1)
                
            if cell1 > cell2:
                cell1, cell2 = cell2, cell1
            
            self.__Unify__(x, y, cell2, cell1)
            self.setRect(x, y, "#EEEEEE")
        
        self.__generated = True
    
    def __Unify__(self, x, y, form, to):
        if to == 1: self.__genState += 1

        self.setcell(x, y, to)

        if self.getcell(x+1, y, warn=False) == form: 
            self.__Unify__(x+1, y, form, to)
        if self.getcell(x, y+1, warn=False) == form: 
            self.__Unify__(x, y+1, form, to)
        if self.getcell(x, y-1, warn=False) == form: 
            self.__Unify__(x, y-1, form, to)
        if self.getcell(x-1, y, warn=False) == form: 
            self.__Unify__(x-1, y, form, to)


    def Resolve(self):
        if not self.__generated: print("can't resolve a not generated maze !")
        else:
            self.__Res__(0, 1)
    
    def __Res__(self, x, y):
        if not self.__resolved:
            if x == self.W-1 and y == self.H-2: self.__resolved = True

            self.setcell(x, y, 2)
            self.setRect(x, y, "#1111EE")

            if self.getcell(x+1, y, warn=False) == 1: 
                self.__Res__(x+1, y)
            if self.getcell(x, y+1, warn=False) == 1: 
                self.__Res__(x, y+1)
            if self.getcell(x, y-1, warn=False) == 1: 
                self.__Res__(x, y-1)
            if self.getcell(x-1, y, warn=False) == 1: 
                self.__Res__(x-1, y)
            
            if not self.__resolved:
                self.setcell(x, y, 1)
                self.setRect(x, y, "#EEEEEE")
            else:
                self.setRect(x, y, "#11AA11")


if __name__ == "__main__":
    while True:
        size = input("size ('widht'x'height') or 'size': ")
        if len([i for i in size.split("x") if i.isdigit()]) == 2:
            Width, Height = [int(i) if int(i)%2==1 else int(i)+1 for i in size.split("x")]
            break
        elif size.isdigit():
            Width = int(size)
            Height = Width
            break
        elif len(size.split("x")) != 2:
            print("I need a 'width'x'height' format like '51x25' or '51'\n")
    print("width:%s, height:%s" %(Width, Height))



    MyWindow = tk.Tk()
    window_height = int(Height*((MyWindow.winfo_screenheight()*0.9)//Height))
    wall_size = window_height // Height
    window_width = wall_size*Width

    MyWindow.title("Maze gen and solver")
    MyWindow.geometry("%sx%s" % (window_width, window_height))
    MyWindow.configure(background="#EEEEEE")
    MyWindow.resizable(width=False, height=False)

    MyCanvas = tk.Canvas(background="#EEEEEE", width=window_width, height=window_height, borderwidth=0, highlightthickness=0)
    MyCanvas.pack()

    MyMaze = Maze(Width, Height, MyCanvas)
    MyMaze.Generate_v2()
    MyMaze.Resolve()

    MyWindow.mainloop()
