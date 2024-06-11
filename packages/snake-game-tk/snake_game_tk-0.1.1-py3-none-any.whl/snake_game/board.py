import tkinter as tk


class Board:

    COLOR = 'black'

    def __init__(self, master: tk.Tk, width: int, height: int, cell_size: int) -> None:
        self.master: tk.Tk = master
        self.width: int = width
        self.height: int = height
        self.cell_size: int = cell_size
        self.create_canvas()
        self.center_window()
    
    def create_canvas(self) -> None:
        self.canvas = tk.Canvas(
            self.master,
            width=self.width,
            height=self.height,
            bg=self.COLOR,
        )
        self.canvas.pack()

    def center_window(self) -> None:
        # Get the screen width and height
        screen_width: int = self.master.winfo_screenwidth()
        screen_height: int = self.master.winfo_screenheight()

        # Calculate the position for the window to be centered
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        # Set the window position
        self.master.geometry(f'{self.width}x{self.height}+{x}+{y}')

    def clear(self) -> None:
        self.canvas.delete("all")
