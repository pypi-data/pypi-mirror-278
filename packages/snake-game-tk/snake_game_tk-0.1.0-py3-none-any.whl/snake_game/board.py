import tkinter as tk


class Board:

    COLOR = 'black'

    def __init__(self, master: tk.Tk, width: int, height: int, cell_size: int) -> None:
        self.canvas: tk.Canvas = tk.Canvas(master, width=width, height=height, bg=self.COLOR)
        self.canvas.pack()
        self.width = width
        self.height = height
        self.cell_size = cell_size

    def clear(self) -> None:
        self.canvas.delete("all")
