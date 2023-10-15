import fitz  # MuPDF library
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import io


signature_placement_mode = False

current_page_number = 0

def on_configure(event):
    canvas.config(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def display_images(imgs1, imgs2):
    global images1, images2
    images1, images2 = imgs1, imgs2

    for widget in inner_frame.winfo_children():
        widget.destroy()

    for img1, img2 in zip(images1, images2):
        image_frame = tk.Frame(inner_frame)
        image_frame.pack(fill="both", expand=True)

        label1 = tk.Label(image_frame, image=img1)
        label1.img = img1
        label1.pack(side="left", fill="both", expand=True)

        label2 = tk.Label(image_frame, image=img2)
        label2.img = img2
        label2.pack(side="right", fill="both", expand=True)

        
def update_scroll_region():
    canvas.config(scrollregion=canvas.bbox("all"))

def select_file():
    global images1, images2, current_page_number
    simulator = selected_simulator.get()
    test_file_path = filedialog.askopenfilename()
    current_page_number = 0 

    test_name_with_extension = os.path.basename(test_file_path)

    if simulator == "787#2":
        master_folder = "C:/Users/abenh/Documents/Results-Combined-with-updates"

    master_file_path = os.path.join(master_folder, test_name_with_extension)

    test_doc = fitz.open(test_file_path)
    master_doc = fitz.open(master_file_path)

    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    window_width = root.winfo_screenwidth()

    images1 = []
    images2 = []

    for page_num in range(len(test_doc)):
        test_page = test_doc.load_page(page_num)
        master_page = master_doc.load_page(page_num)

        test_image = Image.frombytes("RGB", [test_page.get_pixmap().width, test_page.get_pixmap().height], test_page.get_pixmap().samples)
        master_image = Image.frombytes("RGB", [master_page.get_pixmap().width, master_page.get_pixmap().height], master_page.get_pixmap().samples)

        new_width = window_width // 2
        new_height_test = int(test_image.height * (new_width / test_image.width))
        new_height_master = int(master_image.height * (new_width / master_image.width))

        test_image = test_image.resize((new_width, new_height_test))
        master_image = master_image.resize((new_width, new_height_master))

        images1.append(ImageTk.PhotoImage(image=test_image))
        images2.append(ImageTk.PhotoImage(image=master_image))

    display_images(images1, images2)

    # Delay the update of the canvas's scroll region
    root.after(100, update_scroll_region)

#--------------------------------------------------------------------------------------pass or fail
def mark_as_pass():
    # Code to mark the PDF as a pass will go here
    print("Marked as Pass")

def mark_as_fail():
    # Code to mark the PDF as a fail will go here
    print("Marked as Fail")

#------------------------------------------------------------------------------------------- Main GUI Setup
root = tk.Tk()
root.state('zoomed')

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack()

selected_simulator = tk.StringVar()
selected_simulator.set("787#2")
simulator_options = ["787#2", "Simulator 2"]
dropdown = tk.OptionMenu(button_frame, selected_simulator, *simulator_options)
dropdown.pack(side="left")

select_file_button = tk.Button(button_frame, text="Select File", command=select_file)
select_file_button.pack(side="left")

pass_button = tk.Button(button_frame, text="Pass", command=mark_as_pass)
pass_button.pack(side="left")

fail_button = tk.Button(button_frame, text="Fail", command=mark_as_fail)
fail_button.pack(side="left")

frame = tk.Frame(root)
frame.pack(side="top", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
canvas.bind("<Configure>", on_configure)
canvas.bind_all("<MouseWheel>", on_mousewheel)

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")


scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

root.mainloop()