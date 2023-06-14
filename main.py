import tkinter
import tkinter.ttk
import event_window
import path


class main_window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(path.resource_path("Images\\Icon.ico"))
        self.title("Paint")
        self.geometry("200x100")
        self.minsize(200, 100)
        tkinter.ttk.Button(self, text="開始", command=self.start_paint).pack()
        self.mainloop()

    def start_paint(self):
        self.withdraw()
        self.window = event_window.e_window(self)
        self.busy_wait()

    def busy_wait(self):
        if self.window.is_done():
            self.deiconify()
        else:
            self.after(100, self.busy_wait)


if __name__ == "__main__":
    main_window()
