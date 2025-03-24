import customtkinter
from customtkinter import filedialog
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageEnhance
from customtkinter import ctk_tk
from tkinter import colorchooser

app = customtkinter.CTk()
app.geometry("1000x600")

#draw group

pen_color = "black"
pen_size = 5
file_path = ""

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]


def change_size(size):
    global pen_size
    pen_size = size/2


def draw(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline='')
    

def clear_canvas():
    canvas.delete("all")

#basic edit group

def light(bright):
    global canvas
    image = Image.open(file_path)
    image = ImageEnhance.Brightness(image).enhance(bright/50)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def adjust_temperature(factor):
    global canvas
    image = Image.open(file_path).convert("RGB")
    r, g, b = image.split()
    factor = factor/50

    if factor > 1:  # Tăng nhiệt độ (ấm hơn)
        r = r.point(lambda i: min(255, i * factor))
        b = b.point(lambda i: max(0, i / factor))
    else:  # Giảm nhiệt độ (lạnh hơn)
        r = r.point(lambda i: max(0, i * factor))
        b = b.point(lambda i: min(255, i / factor))
    
    image = Image.merge("RGB", (r, g, b))
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def freshness(factor):
    global canvas
    image = Image.open(file_path).convert("RGB")
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(factor/50)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")
    
# back button

def back_command():
    for widget in left_frame.winfo_children():
        widget.destroy()
    
    image_button = customtkinter.CTkButton(left_frame, text="Import Image",command=add_image, fg_color="black")
    image_button.place(x=55, y=25)

    draw_group_btn = customtkinter.CTkButton(master=left_frame, text="Open Draw", command=open_draw_group, fg_color="black")
    draw_group_btn.place(x=55, y=75)

    basic_edit_btn = customtkinter.CTkButton(master=left_frame, text="Edit Basic", command=open_edit_basic_group, fg_color="black")
    basic_edit_btn.place(x=55, y=135)

#main code

def add_image():
    global file_path, image
    file_path = filedialog.askopenfilename(
        initialdir="D:/codefirst.io/Tkinter Image Editor/Pictures")
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def open_draw_group():
    global color_button, pen_size_slider, clear_button

    for widget in left_frame.winfo_children():
        widget.destroy()

    color_button = customtkinter.CTkButton(left_frame, text="Change Pen Color", command=change_color, fg_color="black")
    color_button.place(x=55, y=10)

    pen_size_slider = customtkinter.CTkSlider(left_frame, from_=0, to=100, command=change_size)
    pen_size_slider.place(x=25, y=60)

    clear_button = customtkinter.CTkButton(left_frame, text="Clear", command=clear_canvas, bg_color="#FF9797")
    clear_button.place(x=55, y=120)

    back_button = customtkinter.CTkButton(left_frame, text="Back", command=back_command, bg_color="black")
    back_button.place(x=55, y=175)

def open_edit_basic_group():

    for widget in left_frame.winfo_children():
        widget.destroy()
    
    light_label = customtkinter.CTkLabel(left_frame, text="Light")
    light_label.place(x=25, y=20)

    light_slider = customtkinter.CTkSlider(left_frame, from_=0, to=100, command=light)
    light_slider.place(x=25, y=45)

    temperature_label = customtkinter.CTkLabel(left_frame, text="Temperature")
    temperature_label.place(x=25, y=65)

    temperature_slider = customtkinter.CTkSlider(left_frame, from_=0, to=100, command=adjust_temperature)
    temperature_slider.place(x=25, y=95)

    freshness_label = customtkinter.CTkLabel(left_frame, text="Tint")
    freshness_label.place(x=25, y=125)

    freshness_slider = customtkinter.CTkSlider(left_frame, from_=0, to=100, command=freshness)
    freshness_slider.place(x=25, y=165)

    back_button = customtkinter.CTkButton(left_frame, text="Back", command=back_command, bg_color="black")
    back_button.place(x=55, y=185)



def create_new_project():
    global create_project_btn, canvas, left_frame, image_button, draw_group_btn, basic_edit_btn
    
    create_project_btn.destroy()

    left_frame = customtkinter.CTkFrame(master=app, width=250, height=1200, fg_color="#1f1f1f")
    left_frame.pack(side="left", fill="y")

    canvas = customtkinter.CTkCanvas(master=app, width=750*2, height=1200, bg="white")
    canvas.pack()

    
    image_button = customtkinter.CTkButton(left_frame, text="Import Image",command=add_image, fg_color="black")
    image_button.place(x=55, y=25)

    draw_group_btn = customtkinter.CTkButton(master=left_frame, text="Open Draw", command=open_draw_group, fg_color="black")
    draw_group_btn.place(x=55, y=75)

    basic_edit_btn = customtkinter.CTkButton(master=left_frame, text="Edit Basic", command=open_edit_basic_group, fg_color="black")
    basic_edit_btn.place(x=55, y=135)

    canvas.bind("<B1-Motion>", draw)
    

customtkinter.set_appearance_mode("dark")

create_project_btn = customtkinter.CTkButton(master=app, text="Create Project", corner_radius=5, fg_color="#4158D0", hover_color="#C850C0", font=("Arial", 12, "bold"), command=create_new_project)
create_project_btn.place(relx = 0.05, rely=0.05)

app.mainloop()