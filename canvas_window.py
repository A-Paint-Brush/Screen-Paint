import tkinter
import path


class c_window(tkinter.Toplevel):
    def __init__(self, root, event_w, tools_w):
        super().__init__(root)
        self.iconbitmap(path.resource_path("Images/Icon.ico"))
        self.event_w = event_w
        self.tools_w = tools_w
        self.canvas = tkinter.Canvas(self, bg="#DDDDDD", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.attributes("-transparentcolor", "#DDDDDD")
        self.attributes("-topmost", True)
        self.attributes("-fullscreen", True)
        self.protocol("WM_DELETE_WINDOW", lambda: None)

    def close(self):
        self.destroy()
