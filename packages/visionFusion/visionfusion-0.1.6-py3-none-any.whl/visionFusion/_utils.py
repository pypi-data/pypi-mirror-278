import tkinter as tk
import pyperclip


class ScreenGrabber():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Screen Grabber')
        self.root.geometry('400x400')

        self.main_frame = tk.Frame(self.root, bg='#0D1B2A')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.dim_clip_button_coords = tk.Button(
            self.main_frame,
            text='Clip with Selection (Coords only)',
            command=self.clip_screen_coords,
            bg='#1B263B',
            fg='#E0E1DD',
            padx=10,
            font=('Sans Serif', 9),
        )
        self.dim_clip_button_coords.grid(
            row=1, column=0, pady=(10, 1), padx=20, sticky=tk.W
        )

        self.copy_clipboard_button = tk.Button(
            self.main_frame,
            text='Copy to Clipboard',
            command=self.copy_to_clipboard,
            bg='#1B263B',
            fg='#E0E1DD',
            padx=10,
            font=('Sans Serif', 9),
        )
        self.copy_clipboard_button.grid(
            row=2, column=0, pady=10, padx=20, sticky=tk.W
        )

        # Coordenadas
        self.x1_entry = self.create_coord_entry('x1', 3)
        self.y1_entry = self.create_coord_entry('y1', 4)
        self.x2_entry = self.create_coord_entry('x2', 5)
        self.y2_entry = self.create_coord_entry('y2', 6)

        self.label = tk.Label(
            self.main_frame,
            text='',
            bg='#0D1B2A',
            fg='#E0E1DD',
            font=('helvetica', 10),
        )
        self.label.grid(row=7, column=0, pady=(10, 0), padx=20, sticky=tk.W)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        self.selection_window = None

        # Inicia o loop principal do tkinter
        self.root.mainloop()

    def create_coord_entry(self, label, row):
        frame = tk.Frame(self.main_frame, bg='#0D1B2A')
        frame.grid(row=row, column=0, pady=5, padx=10, sticky=tk.W)
        lbl = tk.Label(
            frame,
            text=f'{label}:',
            bg='#0D1B2A',
            fg='#E0E1DD',
            font=('helvetica', 10),
        )
        lbl.pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=15)
        entry.pack(side=tk.LEFT, padx=5)
        return entry

    def clip_screen_coords(self):
        self.dim_clip_button_coords.grid_forget()  # Remove o botão temporariamente
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes('-fullscreen', True)
        self.selection_window.attributes('-alpha', 0.3)
        self.selection_window.configure(bg='gray')

        self.selection_window.bind(
            '<ButtonPress-1>', self.on_button_press_coords
        )
        self.selection_window.bind('<B1-Motion>', self.on_mouse_drag_coords)
        self.selection_window.bind(
            '<ButtonRelease-1>', self.on_button_release_coords
        )

    def on_button_press_coords(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.rect = tk.Canvas(self.selection_window, width=1, height=1)
        self.rect.place(x=self.start_x, y=self.start_y)
        self.rect.config(highlightthickness=2, highlightbackground='red')

    def on_mouse_drag_coords(self, event):
        curX, curY = (event.x_root, event.y_root)
        width, height = (curX - self.start_x, curY - self.start_y)
        self.rect.config(width=width, height=height)

    def on_button_release_coords(self, event):
        self.curX = event.x_root
        self.curY = event.y_root
        self.selection_window.destroy()
        self.update_coordinates()
        self.label.configure(
            text=f'Coordinates: ({self.start_x}, {self.start_y}) - ({self.curX}, {self.curY})'
        )
        self.dim_clip_button_coords.grid(
            row=1, column=0, pady=(10, 1), padx=20, sticky=tk.W
        )  # Coloca o botão de volta em sua posição original

    def update_coordinates(self):
        self.x1_entry.delete(0, tk.END)
        self.x1_entry.insert(0, str(self.start_x))
        self.y1_entry.delete(0, tk.END)
        self.y1_entry.insert(0, str(self.start_y))
        self.x2_entry.delete(0, tk.END)
        self.x2_entry.insert(0, str(self.curX))
        self.y2_entry.delete(0, tk.END)
        self.y2_entry.insert(0, str(self.curY))

    def copy_to_clipboard(self):
        if (
            self.start_x is not None
            and self.start_y is not None
            and self.curX is not None
            and self.curY is not None
        ):
            coordinates = (
                f'({self.start_x}, {self.start_y}, {self.curX}, {self.curY})'
            )
            pyperclip.copy(coordinates)
            self.label.configure(text='Coordinates copied to clipboard.')
