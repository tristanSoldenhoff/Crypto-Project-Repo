"""
 Customtkinter documentation:  https://customtkinter.tomschimansky.com/documentation/widgets/button
 Appearance: customtkinter
 forest-ttk-theme     (used for treeview table)
"""

import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import Image
import os
import ctypes                                                                   # dots per inch awareness
from my_functions import MyFunctions
from data_processing_functions import DataProcessingFunctions
#import tkinter.messagebox

# loading data into treeview
def load_data():
    list = dpf.tree_view_data('usd',1,2)
    for i in list:
        treeview.insert('', tk.END, values=i)

# accessing crypto data
mf = MyFunctions()
dpf = DataProcessingFunctions()

# dots per inch awareness - to fix blurry text on GUI
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# window
window = tk.Tk()
window.title('Crypto Project')
window.geometry('1000x600')
window['background'] = '#1A1A1A'
window.state('zoomed')
customtkinter.set_appearance_mode('Dark')

# configure grid
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=5)
window.grid_rowconfigure(0, weight=1)

# create navigation frame
navigation_frame = customtkinter.CTkFrame(master=window, corner_radius=8)
navigation_frame.grid(row=0, column=0, padx=15, pady=15, sticky='news')
navigation_frame.grid_columnconfigure(0, weight=1)
navigation_frame.grid_rowconfigure(10, weight=1)

navigation_frame_label_0 = customtkinter.CTkLabel(navigation_frame, text='Tool Bar', anchor='center',
                                font=customtkinter.CTkFont(size=25, weight='bold'))
navigation_frame_label_0.grid(row=0, column=0, padx=20, pady=20, sticky='news')

# navigation_frame_label_1 = customtkinter.CTkLabel(navigation_frame, text='Label 1',
#                                 compound='left', font=customtkinter.CTkFont(size=15, weight='bold'))
# navigation_frame_label_1.grid(row=1, column=0, padx=20, pady=20)
#
# navigation_frame_label_2 = customtkinter.CTkLabel(navigation_frame, text='Label 2',
#                                 compound='left', font=customtkinter.CTkFont(size=15, weight='bold'))
# navigation_frame_label_2.grid(row=2, column=0, padx=20, pady=20)

home_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, text="Home",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
home_button.grid(row=1, column=0, sticky="ew")

graph_button = customtkinter.CTkButton(navigation_frame, corner_radius=0, height=40, text="Graphs",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
graph_button.grid(row=2, column=0, sticky="ew")

# create home frame
home_frame = customtkinter.CTkFrame(master=window, corner_radius=8, fg_color=('gray70', 'gray15'))
home_frame.grid(row=0, column=1, padx=(0,15), pady=15, sticky="news")
home_frame.grid_columnconfigure(0, weight=1)
home_frame.grid_rowconfigure(0, weight=1)

# create tree frame
tree_frame = customtkinter.CTkFrame(master=home_frame, corner_radius=8)
tree_frame.grid_columnconfigure(0, weight=1)
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid(row=0, column=0, padx=5, pady=5, sticky="news")
treeScroll = ttk.Scrollbar(tree_frame)
treeScroll.pack(side='right', fill='y')

# apply Azure theme to tree_frame
style = ttk.Style(tree_frame)
tree_frame.tk.call('source', 'Azure/azure.tcl')
tree_frame.tk.call('set_theme', 'dark')

# set up column and data into treeview
cols = ('Rank', 'ID', 'Symbol', 'Market Cap', 'Total Volume', '24h', 'Price' )
treeview = ttk.Treeview(tree_frame, show='headings', yscrollcommand=treeScroll.set, columns=cols, height=100)
treeview.heading('Rank', text='Rank', anchor=tk.W)
treeview.heading('ID', text='ID', anchor=tk.W)
treeview.heading('Symbol', text='Symbol', anchor=tk.W)
treeview.heading('Market Cap', text='Market Cap', anchor=tk.W)
treeview.heading('Total Volume', text='Total Volume', anchor=tk.W)
treeview.heading('24h', text='24h', anchor=tk.W)
treeview.heading('Price', text='Price', anchor=tk.W)

treeview.column('Rank', width=50)
treeview.column('Symbol', width=80)
treeview.column('Market Cap', width=150)
treeview.column('Total Volume', width=150)
treeview.column('24h', width=80)

treeview.pack()
treeScroll.config(command=treeview.yview)
load_data()



window.mainloop()
