import tkinter
import functools
import canvas_window
import tools_window
import path


class e_window(tkinter.Toplevel):
    def __init__(self, root):
        self.tools = tools_window.tools(root, self)
        super().__init__(root)
        self.iconbitmap(path.resource_path("Images/Icon.ico"))
        self.done = False
        self.line_list = []
        self.id_list = []
        self.temp_id = None
        self.temp_pos = (0, 0)
        self.resolution = (self.winfo_screenwidth(), self.winfo_screenheight())
        self.filled = False
        self.thickness = 1
        self.shift_down = False
        self.eraser = False
        self.tools.set_pos(self.resolution)
        self.tools.set_tools(
            ["Brush.png",
             "Line.png",
             "Rect.png",
             "Triangle.png",
             "Right Triangle.png",
             "Circle.png",
             "Eraser.png",
             "Undo.png",
             "Clear.png"],
            self.change_tool,
            self.register_quit)
        self.tool_bindings = {"Brush": functools.partial(self.set_bindings,
                                                         self.move_paint,
                                                         self.start_paint,
                                                         self.end_paint),
                              "Line": functools.partial(self.set_bindings, self.move_line),
                              "Rect": functools.partial(self.set_bindings, self.move_rect),
                              "Triangle": functools.partial(self.set_bindings, self.move_triangle),
                              "Right Triangle": functools.partial(self.set_bindings, self.move_right_triangle),
                              "Circle": functools.partial(self.set_bindings, self.move_circle),
                              "Eraser": functools.partial(self.set_bindings, lambda event: None)}
        self.attributes("-alpha", 0.01)
        self.attributes("-topmost", True)
        self.attributes("-fullscreen", True)
        self.draw = canvas_window.c_window(root, self, self.tools)
        self.tools.get_canvas_w(self.draw)
        self.bind("<Button-1>", self.start_paint)
        self.bind("<B1-Motion>", self.move_paint)
        self.bind("<ButtonRelease-1>", self.end_paint)
        self.bind("<Shift_L>", self.shiftdown)
        self.bind("<KeyRelease-Shift_L>", self.shiftup)
        self.bind("<Shift_R>", self.shiftdown)
        self.bind("<KeyRelease-Shift_R>", self.shiftup)
        self.bind("<Map>", self.deiconify_all)
        self.protocol("WM_DELETE_WINDOW", lambda: None)

    def shiftdown(self, event):
        self.shift_down = True

    def shiftup(self, event):
        self.shift_down = False

    def deiconify_all(self, event):
        self.draw.deiconify()
        self.tools.deiconify()
        self.lift()

    def set_color(self, color):
        self.color = color

    def toggle_filled(self):
        self.filled = not self.filled

    def start_func(self, event):
        if event.x >= self.tools.winfo_rootx() and event.x <= self.tools.winfo_rootx() + self.tools.winfo_width() and \
                event.y >= self.tools.winfo_rooty() and event.y <= self.tools.winfo_rooty() + self.tools.winfo_height():
            self.tools.focus()
        self.temp_pos = (event.x, event.y)

    def end_func(self, event):
        if self.temp_id is not None:
            self.id_list.append(self.temp_id)
        self.temp_id = None

    def start_paint(self, event):
        if event.x >= self.tools.winfo_rootx() and event.x <= self.tools.winfo_rootx() + self.tools.winfo_width() and \
                event.y >= self.tools.winfo_rooty() and event.y <= self.tools.winfo_rooty() + self.tools.winfo_height():
            self.tools.focus()
        self.line_list.append([(event.x, event.y)])
        self.id_list.append([])

    def move_paint(self, event):
        self.line_list[-1].append((event.x, event.y))
        self.id_list[-1].append(self.draw.canvas.create_line(self.line_list[-1][-2][0],
                                                             self.line_list[-1][-2][1],
                                                             self.line_list[-1][-1][0],
                                                             self.line_list[-1][-1][1],
                                                             fill=[self.tools.get_color(), "#dddddd"][self.eraser],
                                                             width=self.tools.get_width()))

    def end_paint(self, event):
        self.line_list.clear()
        if len(self.id_list[-1]) == 0:
            self.id_list.pop()

    def move_line(self, event):
        if self.temp_id is not None:
            self.draw.canvas.delete(self.temp_id)
        if self.shift_down:
            temp1 = abs(event.x - self.temp_pos[0])
            temp2 = abs(event.y - self.temp_pos[1])
            if temp1 > temp2:
                if event.x > self.temp_pos[0]:
                    self.temp_id = self.draw.canvas.create_line(self.temp_pos[0],
                                                                self.temp_pos[1],
                                                                self.temp_pos[0] + temp1,
                                                                self.temp_pos[1],
                                                                fill=self.tools.get_color(),
                                                                width=self.tools.get_width())
                elif event.x < self.temp_pos[0]:
                    self.temp_id = self.draw.canvas.create_line(self.temp_pos[0],
                                                                self.temp_pos[1],
                                                                self.temp_pos[0] - temp1,
                                                                self.temp_pos[1],
                                                                fill=self.tools.get_color(),
                                                                width=self.tools.get_width())
                else:
                    self.temp_id = None
            else:
                if event.y > self.temp_pos[1]:
                    self.temp_id = self.draw.canvas.create_line(self.temp_pos[0],
                                                                self.temp_pos[1],
                                                                self.temp_pos[0],
                                                                self.temp_pos[1] + temp2,
                                                                fill=self.tools.get_color(),
                                                                width=self.tools.get_width())
                elif event.y < self.temp_pos[1]:
                    self.temp_id = self.draw.canvas.create_line(self.temp_pos[0],
                                                                self.temp_pos[1],
                                                                self.temp_pos[0],
                                                                self.temp_pos[1] - temp2,
                                                                fill=self.tools.get_color(),
                                                                width=self.tools.get_width())
                else:
                    self.temp_id = None
        else:
            self.temp_id = self.draw.canvas.create_line(self.temp_pos[0],
                                                        self.temp_pos[1],
                                                        event.x,
                                                        event.y,
                                                        fill=self.tools.get_color(),
                                                        width=self.tools.get_width())

    def move_rect(self, event):
        if self.temp_id is not None:
            self.draw.canvas.delete(self.temp_id)
        self.temp_id = self.draw.canvas.create_rectangle(self.temp_pos[0],
                                                         self.temp_pos[1],
                                                         event.x,
                                                         event.y,
                                                         outline=self.tools.get_color(),
                                                         fill=["", self.tools.get_color()][self.filled],
                                                         width=self.tools.get_width())

    def move_triangle(self, event):
        if self.temp_id is not None:
            self.draw.canvas.delete(self.temp_id)
        if event.x > self.temp_pos[0]:
            self.temp_id = self.draw.canvas.create_polygon(self.temp_pos[0],
                                                           self.temp_pos[1],
                                                           self.temp_pos[0] - abs(event.x - self.temp_pos[0]),
                                                           event.y,
                                                           event.x,
                                                           event.y,
                                                           outline=self.tools.get_color(),
                                                           fill=["", self.tools.get_color()][self.filled],
                                                           width=self.tools.get_width())
        elif event.x < self.temp_pos[0]:
            self.temp_id = self.draw.canvas.create_polygon(self.temp_pos[0],
                                                           self.temp_pos[1],
                                                           self.temp_pos[0] + abs(event.x - self.temp_pos[0]),
                                                           event.y,
                                                           event.x,
                                                           event.y,
                                                           outline=self.tools.get_color(),
                                                           fill=["", self.tools.get_color()][self.filled],
                                                           width=self.tools.get_width())
        else:
            self.temp_id = None

    def move_right_triangle(self, event):
        if self.temp_id is not None:
            self.draw.canvas.delete(self.temp_id)
        self.temp_id = self.draw.canvas.create_polygon(self.temp_pos[0],
                                                       self.temp_pos[1],
                                                       self.temp_pos[0],
                                                       event.y,
                                                       event.x,
                                                       event.y,
                                                       outline=self.tools.get_color(),
                                                       fill=["", self.tools.get_color()][self.filled],
                                                       width=self.tools.get_width())

    def move_circle(self, event):
        if self.temp_id is not None:
            self.draw.canvas.delete(self.temp_id)
        temp1 = abs(event.x - self.temp_pos[0])
        temp2 = abs(event.y - self.temp_pos[1])
        if temp1 > temp2:
            diameter = temp1
        else:
            diameter = temp2
        if event.x > self.temp_pos[0] and event.y > self.temp_pos[1]:
            self.temp_id = self.draw.canvas.create_oval(self.temp_pos[0],
                                                        self.temp_pos[1],
                                                        self.temp_pos[0] + diameter,
                                                        self.temp_pos[1] + diameter,
                                                        outline=self.tools.get_color(),
                                                        fill=["", self.tools.get_color()][self.filled],
                                                        width=self.tools.get_width())
        elif event.x > self.temp_pos[0] and event.y < self.temp_pos[1]:
            self.temp_id = self.draw.canvas.create_oval(self.temp_pos[0],
                                                        self.temp_pos[1] - diameter,
                                                        self.temp_pos[0] + diameter,
                                                        self.temp_pos[1],
                                                        outline=self.tools.get_color(),
                                                        fill=["", self.tools.get_color()][self.filled],
                                                        width=self.tools.get_width())
        elif event.x < self.temp_pos[0] and event.y > self.temp_pos[1]:
            self.temp_id = self.draw.canvas.create_oval(self.temp_pos[0] - diameter,
                                                        self.temp_pos[1],
                                                        self.temp_pos[0],
                                                        self.temp_pos[1] + diameter,
                                                        outline=self.tools.get_color(),
                                                        fill=["", self.tools.get_color()][self.filled],
                                                        width=self.tools.get_width())
        elif event.x < self.temp_pos[0] and event.y < self.temp_pos[1]:
            self.temp_id = self.draw.canvas.create_oval(self.temp_pos[0],
                                                        self.temp_pos[1],
                                                        self.temp_pos[0] - diameter,
                                                        self.temp_pos[1] - diameter,
                                                        outline=self.tools.get_color(),
                                                        fill=["", self.tools.get_color()][self.filled],
                                                        width=self.tools.get_width())
        else:
            self.temp_id = None

    def change_tool(self, tool):
        if tool != "Eraser":
            self.eraser = False
        if tool == "Undo":
            if not len(self.id_list):
                return None
            elif isinstance(self.id_list[-1], list):
                for line in range(0, len(self.id_list[-1])):
                    self.draw.canvas.delete(self.id_list[-1][line])
                self.id_list.pop(-1)
            else:
                self.draw.canvas.delete(self.id_list[-1])
                self.id_list.pop(-1)
        elif tool == "Eraser":
            self.eraser = True
            self.tools.change_selected_tool(tool)
            self.tool_bindings["Brush"]()
        elif tool == "Clear":
            self.draw.canvas.delete("all")
            self.id_list.clear()
        else:
            self.tools.change_selected_tool(tool)
            self.tool_bindings[tool]()

    def set_bindings(self, move_func, start_func=None, end_func=None):
        self.unbind("<Button-1>")
        self.unbind("<B1-Motion>")
        self.unbind("<ButtonRelease-1>")
        if start_func is None:
            self.bind("<Button-1>", self.start_func)
        else:
            self.bind("<Button-1>", start_func)
        self.bind("<B1-Motion>", move_func)
        if end_func is None:
            self.bind("<ButtonRelease-1>", self.end_func)
        else:
            self.bind("<ButtonRelease-1>", end_func)

    def is_done(self):
        return self.done

    def register_quit(self):
        self.draw.close()
        self.line_list.clear()
        self.id_list.clear()
        self.destroy()
        self.done = True
