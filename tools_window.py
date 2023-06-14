import tkinter
import tkinter.ttk
import tkinter.colorchooser
import functools
import path


class tools(tkinter.Toplevel):
    def __init__(self, root, event_w):
        super().__init__(root)
        self.iconbitmap(path.resource_path("Images\\Icon.ico"))
        self.title("Tools")
        self.event_w = event_w
        self.canvas_w = None
        self.chooser = tkinter.colorchooser.Chooser(self)
        self.result = "#000000"
        self.tools = ["Brush",
                      "Line",
                      "Rect",
                      "Triangle",
                      "Right Triangle",
                      "Circle",
                      "Eraser",
                      "Undo",
                      "Clear"]
        self.btn_list = []
        self.selected_tool = 0
        self.images = []
        self.check_box = tkinter.BooleanVar()
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", lambda: None)

    def get_canvas_w(self, canvas_w):
        self.canvas_w = canvas_w

    def iconify_all(self):
        self.withdraw()
        self.canvas_w.withdraw()
        self.event_w.iconify()

    def deiconify_all(self, event):
        self.event_w.deiconify()
        self.canvas_w.deiconify()

    def set_pos(self, resolution):
        self.geometry("70x600+{}+{}".format(resolution[0] - 70, 0))
        self.overrideredirect(True)

    def set_tools(self, images, callback, quit_callback):
        for btn in range(0, len(images)):
            self.images.append(tkinter.PhotoImage(file=path.resource_path(".\\Images\\{}".format(images[btn]))))
            self.btn_list.append(tkinter.Button(self,
                                                image=self.images[btn],
                                                command=functools.partial(callback, images[btn][0:-4])))
            self.btn_list[btn].pack()
        self.btn_list[0].config(background="#33FFFF")
        tkinter.ttk.Checkbutton(self, text="填充", variable=self.check_box, command=self.toggle_filled).pack()
        self.check_box.set(False)
        tkinter.Label(self, text="筆寬").pack()
        self.width_scale = tkinter.Scale(self, from_=1, to=20, orient="vertical")
        self.width_scale.set(1)
        self.width_scale.pack()
        tkinter.ttk.Button(self, text="選擇顏色", command=self.choose_color).pack()
        tkinter.Label(self, text="顏色：").pack()
        self.color = tkinter.Frame(self, width=20, height=20, background="#000000")
        self.color.pack()
        tkinter.ttk.Button(self, text="最小化", command=self.iconify_all).pack()
        tkinter.ttk.Button(self, text="關閉", command=functools.partial(self.register_quit, quit_callback)).pack()

    def get_width(self):
        return self.width_scale.get()

    def toggle_filled(self):
        self.event_w.toggle_filled()

    def choose_color(self):
        self.withdraw()
        self.event_w.withdraw()
        self.canvas_w.withdraw()
        temp = self.chooser.show()
        if temp != (None, None):
            self.result = temp[1]
        if self.result == "#dddddd":
            self.result = "#d5d5d5"
        self.color.config(background=self.result)
        self.deiconify()
        self.deiconify_all(None)

    def get_color(self):
        return self.result

    def change_selected_tool(self, tool):
        self.btn_list[self.selected_tool].config(background="SystemButtonFace")
        self.selected_tool = self.tools.index(tool)
        self.btn_list[self.selected_tool].config(background="#33FFFF")

    def register_quit(self, quit_callback):
        self.destroy()
        quit_callback()
