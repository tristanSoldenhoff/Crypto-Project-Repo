
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import os
from PIL import Image

# load images
#======== tool bar image
# image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
# wrench_image_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "wrench_icon.png")), size=(26, 26))
#===============================================================================

# window
window = tk.Tk()
window.title('Crypto Project')
window.geometry('1000x600')
customtkinter.set_appearance_mode('Light')

# configure grid
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=10)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=10)
# window.grid_rowconfigure(2, weight=1)

# create navigation frame
navigation_frame = customtkinter.CTkFrame(master=window, corner_radius=0)
navigation_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')
navigation_frame.grid_rowconfigure(2, weight=1)



# navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text='Tool Bar', image=wrench_image_icon,
#                                 compound='left', font=customtkinter.CTkFont(size=15, weight='bold'))
navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text='Tool Bar',
                                compound='left', font=customtkinter.CTkFont(size=15, weight='bold'))
navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

home_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home", fg_color="transparent",
        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
home_button.grid(row=1, column=0, sticky="ew")



# define widgets
label1 = ttk.Label(window, text = 'Row 0    Column 0', background = 'red')
label2 = ttk.Label(window, text = 'Row 0    Column 1', background = 'blue')
label3 = ttk.Label(window, text = 'Row 1    Column 0', background = 'green')
label4 = ttk.Label(window, text = 'Row 1    Column 1', background = 'yellow')
label5 = ttk.Label(window, text = 'Row 2    Column 0', background = 'orange')
label6 = ttk.Label(window, text = 'Row 2    Column 1', background = 'grey')


# place widget
# label1.grid(row = 0, column = 0, sticky = 'nsew')
# label2.grid(row = 0, column = 1, sticky = 'nsew')
# label3.grid(row = 1, column = 0, sticky = 'nsew')
# label4.grid(row = 1, column = 1, sticky = 'nsew')
# label5.grid(row = 2, column = 0, sticky = 'nsew')
# label6.grid(row = 2, column = 1, sticky = 'nsew')




window.mainloop()
