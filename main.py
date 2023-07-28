import tkinter
import os
from tkinter import filedialog

from PIL import Image, ImageTk


class WaterMark(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.mark_entry = None
        self.mark_label = None
        self.apply_button = None
        self.position_label = None
        self.size_label = None
        self.font_label = None
        self.position_list = None
        self.size_list = None
        self.font_list = None
        self.waterm_option_window_widget = None
        self.text_canvas = None
        self.ow_add_watermark_button = None
        self.ow_chose_image_button = None
        self.image = None
        self.new_image_file = None
        self.option_window_widget = None
        self.xscrollbar_canvas = None
        self.canvas_in_frame = None
        self.yscrollbar_canvas = None
        self.main_frame = None
        self.welcome_title = None
        self.option_button = None

        self.title("Water Mark Creator")
        self.main_window_size = (700, 670)
        self.option_window_size = (200, 70)
        self.waterm_option_window_size = (610, 125)
        self.welcome_font = ("Calibre lights", 14, 'bold')
        self.pick_font = ("Calibre body", 12, 'bold')
        self.font_in_text = ("Calibre body", 10, 'normal')
        self.bg_color = "#b9f0c8"
        self.columnconfigure(0, weight=1)
        self.fonts_list = ['Calibre', 'Arial', 'Abadi', 'Agency FB']
        self.sizes_list = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]

        self.w_positions = {
            "Top-Left": (0, 0),
            "Top-Mid": (0, 0),
            "Top-Right": (0, 0),
            "Mid-Left": (0, 0),
            "Mid-Center": (0, 0),
            "Mid-Right": (0, 0),
            "Bottom-Left": (0, 0),
            "Bottom-Center": (0, 0),
            "Bottom-Right": (0, 0)
        }

        self.my_NSWE_positions = {
            "Top-Left": "nw",
            "Top-Mid": "n",
            "Top-Right": "ne",
            "Mid-Left": "nw",
            "Mid-Center": "center",
            "Mid-Right": "ne",
            "Bottom-Left": "sw",
            "Bottom-Center": "s",
            "Bottom-Right": "se",
        }

        self.config(background=self.bg_color)
        self.photo_button_option = tkinter.PhotoImage(file="images/gear2.png").subsample(10, 10)

        self.label_image = None
        self.label_photo = None

        self.program()

    def window_position(self, window_widget):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_width = screen_width / 2 - window_widget[0] / 2
        position_height = screen_height / 2 - window_widget[1] / 2
        return int(position_width), int(position_height)

    def creating_geometry_root_window(self, width, height):
        self.geometry(f"{self.main_window_size[0]}x{self.main_window_size[1]}+{width}+{height}")

    def creating_geometry_window_option(self, width, height):
        self.option_window_widget.geometry(
            f"{self.option_window_size[0]}x{self.option_window_size[1]}+{width}+{height}")

    def creating_geometry_window_watermark_option(self, width, height):
        self.waterm_option_window_widget.geometry(
            f"{self.waterm_option_window_size[0]}x{self.waterm_option_window_size[1]}+{width}+{height}")

    def create_main_widgets(self):
        self.welcome_title = tkinter.Label(text="Welcome to Water Mark App.\n"
                                                "To start process use button int he right corner.",
                                           bg=self.bg_color, font=self.welcome_font)
        self.welcome_title.grid(row=0, column=0)

        self.option_button = tkinter.Button(self, image=self.photo_button_option, width=25, height=25,
                                            command=self.option_window)
        self.option_button.grid(row=0, column=1)

        # First we create frame in our tkinter and place it using grid
        self.main_frame = tkinter.Frame(self)
        self.main_frame.grid(row=1, column=0, columnspan=2)

        # Second we create canvas but in our new frame, position is new, so we start from row and column 0
        self.canvas_in_frame = tkinter.Canvas(self.main_frame, width=680, height=600)
        self.canvas_in_frame.grid(row=0, column=0)
        # Third we place a test image
        self.label_image = Image.open("images/test.jpg")
        self.label_photo = ImageTk.PhotoImage(self.label_image)

        self.w_positions["Top-Mid"] = (int(self.label_image.width / 2), 0)
        self.w_positions["Top-Right"] = (int(self.label_image.width), 0)

        self.w_positions["Mid-Left"] = (0, int(self.label_image.height / 2))
        self.w_positions["Mid-Center"] = (int(self.label_image.width / 2), int(self.label_image.height / 2))
        self.w_positions["Mid-Right"] = (int(self.label_image.width), int(self.label_image.height / 2))

        self.w_positions["Bottom-Left"] = (0, int(self.label_image.height))
        self.w_positions["Bottom-Center"] = (int(self.label_image.width / 2), int(self.label_image.height))
        self.w_positions["Bottom-Right"] = (int(self.label_image.width), int(self.label_image.height))

        self.image = self.canvas_in_frame.create_image(0, 0, anchor=tkinter.NW, image=self.label_photo)

        # Fourth we create two scrollbars to our canvases, in each we establish the orientation and command
        # for canvas x and y view
        self.yscrollbar_canvas = tkinter.Scrollbar(self.main_frame, orient='vertical',
                                                   command=self.canvas_in_frame.yview)
        self.xscrollbar_canvas = tkinter.Scrollbar(self.main_frame, orient='horizontal',
                                                   command=self.canvas_in_frame.xview)

        self.yscrollbar_canvas.grid(row=0, column=1, sticky="NS")
        self.xscrollbar_canvas.grid(row=1, column=0, sticky="EW")

        self.canvas_in_frame.configure(yscrollcommand=self.yscrollbar_canvas.set,
                                       xscrollcommand=self.xscrollbar_canvas.set)
        self.canvas_in_frame.bind("<Configure>", lambda e: self.canvas_in_frame.configure(
            scrollregion=self.canvas_in_frame.bbox("all")))

    def option_window(self):
        position = self.window_position(self.option_window_size)
        self.option_window_widget = tkinter.Toplevel(self)
        self.creating_geometry_window_option(position[0], position[1])
        self.option_window_widget.title("Option window")
        self.option_window_widget.config(bg=self.bg_color)
        self.option_window_widget.attributes("-alpha", 1.0)

        self.ow_chose_image_button = tkinter.Button(self.option_window_widget, text="Chose image to place watermark",
                                                    command=self.chose_image_function)
        self.ow_chose_image_button.grid(row=0, column=0, pady=5, padx=7)

        self.ow_add_watermark_button = tkinter.Button(self.option_window_widget, text="Add water mark",
                                                      command=self.water_mark_window_options)
        self.ow_add_watermark_button.grid(row=1, column=0, pady=5)

    def water_mark_window_options(self):
        position = self.window_position(self.waterm_option_window_size)
        self.waterm_option_window_widget = tkinter.Toplevel(self)
        self.creating_geometry_window_watermark_option(position[0], position[1])
        self.waterm_option_window_widget.title("Water mark window options")
        self.waterm_option_window_widget.config(bg=self.bg_color)
        self.waterm_option_window_widget.attributes("-alpha", 1.0)

        # Font box
        self.font_label = tkinter.Label(self.waterm_option_window_widget, text="Chose font:", bg=self.bg_color)
        self.font_label.grid(row=0, column=0)
        self.font_list = tkinter.Listbox(self.waterm_option_window_widget, height=6,
                                         selectmode="single", exportselection=False)
        self.font_list.grid(row=1, column=0)

        scroll_font_list = tkinter.Scrollbar(self.waterm_option_window_widget, orient='vertical',
                                             command=self.font_list.yview)

        scroll_font_list.grid(row=1, column=1, sticky="NS")
        self.font_list.configure(yscrollcommand=scroll_font_list.set)

        break_label = tkinter.Label(self.waterm_option_window_widget, bg=self.bg_color)
        break_label.grid(row=1, column=2)

        for position in range(len(self.fonts_list)):
            self.font_list.insert(position, self.fonts_list[position])

        # Size box
        self.size_label = tkinter.Label(self.waterm_option_window_widget, text="Chose size:", bg=self.bg_color)
        self.size_label.grid(row=0, column=3)
        self.size_list = tkinter.Listbox(self.waterm_option_window_widget, height=6,
                                         selectmode="single", exportselection=False)
        self.size_list.grid(row=1, column=3)

        scroll_size_list = tkinter.Scrollbar(self.waterm_option_window_widget, orient='vertical',
                                             command=self.size_list.yview)

        scroll_size_list.grid(row=1, column=4, sticky="NS")
        self.size_list.configure(yscrollcommand=scroll_size_list.set)

        break_label = tkinter.Label(self.waterm_option_window_widget, bg=self.bg_color)
        break_label.grid(row=1, column=5)

        for position in range(len(self.sizes_list)):
            self.size_list.insert(position, self.sizes_list[position])

        # Position box
        self.position_label = tkinter.Label(self.waterm_option_window_widget, text="Chose position:", bg=self.bg_color)
        self.position_label.grid(row=0, column=5)
        self.position_list = tkinter.Listbox(self.waterm_option_window_widget, height=6, selectmode="single",
                                             exportselection=False)
        self.position_list.grid(row=1, column=5)

        scroll_position_list = tkinter.Scrollbar(self.waterm_option_window_widget, orient='vertical',
                                                 command=self.position_list.yview)

        scroll_position_list.grid(row=1, column=6, sticky="NS")
        self.position_list.configure(yscrollcommand=scroll_position_list.set)

        break_label = tkinter.Label(self.waterm_option_window_widget, bg=self.bg_color)
        break_label.grid(row=1, column=7)

        for key, value in self.w_positions.items():
            self.position_list.insert(tkinter.END, key)

        # Entry Mark
        self.mark_label = tkinter.Label(self.waterm_option_window_widget, text="Write watermark:",
                                        bg=self.bg_color)
        self.mark_label.grid(row=0, column=8)
        self.mark_entry = tkinter.Entry(self.waterm_option_window_widget)
        self.mark_entry.grid(row=1, column=8)

        break_label = tkinter.Label(self.waterm_option_window_widget, bg=self.bg_color)
        break_label.grid(row=1, column=9)

        # Apply button   
        self.apply_button = tkinter.Button(self.waterm_option_window_widget, text="Apply",
                                           command=self.add_water_mark_function)
        self.apply_button.grid(row=1, column=10)

    def chose_image_function(self):
        file_type = [
            ("Image file", ".jpg")
        ]

        self.new_image_file = filedialog.askopenfilename(title="Chose Image File:", filetypes=file_type)
        just_name = os.path.basename(self.new_image_file)

        if just_name != "":
            self.label_image = Image.open(self.new_image_file)
            self.label_photo = ImageTk.PhotoImage(self.label_image)

            self.canvas_in_frame.itemconfig(self.image, image=self.label_photo)
            self.canvas_in_frame.configure(scrollregion=self.canvas_in_frame.bbox("all"))
            self.option_window_widget.attributes('-topmost', 1)
            self.canvas_in_frame.itemconfig(self.text_canvas, text="")

            self.w_positions["Top-Mid"] = (int(self.label_image.width / 2), 0)
            self.w_positions["Top-Right"] = (int(self.label_image.width), 0)

            self.w_positions["Mid-Left"] = (0, int(self.label_image.height / 2))
            self.w_positions["Mid-Center"] = (int(self.label_image.width / 2), int(self.label_image.height / 2))
            self.w_positions["Mid-Right"] = (int(self.label_image.width), int(self.label_image.height / 2))

            self.w_positions["Bottom-Left"] = (0, int(self.label_image.height))
            self.w_positions["Bottom-Center"] = (int(self.label_image.width / 2), int(self.label_image.height))
            self.w_positions["Bottom-Right"] = (int(self.label_image.width), int(self.label_image.height))
            print(self.w_positions)
        else:
            self.option_window_widget.destroy()

    def add_water_mark_function(self):
        font = None
        size = None
        position = None
        anchor_sign = None
        water_mark_input = self.mark_entry.get()

        for i in self.font_list.curselection():
            font = self.font_list.get(i)

        for i in self.size_list.curselection():
            size = self.size_list.get(i)

        for i in self.position_list.curselection():
            position_to_find = self.position_list.get(i)
        position = self.w_positions[position_to_find]

        anchor_sign = self.my_NSWE_positions[position_to_find]

        print(font, size, position, water_mark_input, anchor_sign)

        self.text_canvas = self.canvas_in_frame.create_text(position[0],
                                                            position[1], anchor=anchor_sign, font=(font, int(size)))
        self.canvas_in_frame.itemconfig(self.text_canvas, text=water_mark_input)

    def program(self):
        window_params = self.window_position(self.main_window_size)
        self.creating_geometry_root_window(window_params[0], window_params[1])
        self.create_main_widgets()


water_mark = WaterMark()
water_mark.mainloop()
