from tkinter import Canvas,Tk

def show_noise(noiseFunction):
    size = [500,500]
    pas = 3
    windows = Tk()
    windows.geometry(str(size[0])+'x'+str(size[1]))
    canvas = Canvas(width=size[0], height=size[1])
    canvas.pack()
    for y in range(0, size[1], pas):
        for x in range(0, size[0], pas):
            c = (noiseFunction(x, y)+1)/2
            c = hex(int(255*c))[2:]
            if len(c) == 1: c = "0"+c
            c = "#"+c*3
            canvas.create_rectangle(x, y, x+pas, y+pas, width = 0, fill = c)
    windows.mainloop()