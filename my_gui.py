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

class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # accessing crypto data
        self.mf = MyFunctions()
        self.dpf = DataProcessingFunctions()

        # dots per inch awareness - to fix blurry text on GUI
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        #hide initial window
        self.iconify()

        # window
        self.title('initial window i would like to close')
        self.geometry('800x600')
        self.window = tk.Tk()
        self.window.title('Crypto Project')
        self.window.geometry('1000x600')
        self.window['background'] = '#1A1A1A'
        self.window.state('zoomed')
        customtkinter.set_appearance_mode('Dark')

        # configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=5)
        self.window.grid_rowconfigure(0, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8)
        self.navigation_frame.grid(row=0, column=0, padx=15, pady=15, sticky='news')
        self.navigation_frame.grid_columnconfigure(0, weight=1)
        self.navigation_frame.grid_rowconfigure(10, weight=1)

        self.navigation_frame_label_0 = customtkinter.CTkLabel(self.navigation_frame, text='Tool Bar', anchor='center',
                                        font=customtkinter.CTkFont(size=25, weight='bold'))
        self.navigation_frame_label_0.grid(row=0, column=0, padx=20, pady=20, sticky='news')

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.graph_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Graphs",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   command=self.graph_button_event)
        self.graph_button.grid(row=2, column=0, sticky="ew")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8, fg_color=('gray70', 'gray10'))
        self.home_frame.grid(row=0, column=1, padx=(0,15), pady=10, sticky="news")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        # create tree frame
        self.tree_frame = customtkinter.CTkFrame(master=self.home_frame, corner_radius=8)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid(row=0, column=0, padx=5, pady=5, sticky="news")

        self.treeScroll = ttk.Scrollbar(self.tree_frame)
        self.treeScroll.pack(side='right', fill='y')

        # apply Azure theme to tree_frame
        style = ttk.Style(self.tree_frame)
        self.tree_frame.tk.call('source', 'Azure/azure.tcl')
        self.tree_frame.tk.call('set_theme', 'dark')

        # set up column and data into treeview
        cols = ('Rank', 'ID', 'Symbol', 'Market Cap', 'Total Volume', '24h', 'Price' )
        self.treeview = ttk.Treeview(self.tree_frame, show='headings', yscrollcommand=self.treeScroll.set, columns=cols, height=100)
        self.treeview.heading('Rank', text='Rank', anchor=tk.W)
        self.treeview.heading('ID', text='ID', anchor=tk.W)
        self.treeview.heading('Symbol', text='Symbol', anchor=tk.W)
        self.treeview.heading('Market Cap', text='Market Cap', anchor=tk.W)
        self.treeview.heading('Total Volume', text='Total Volume', anchor=tk.W)
        self.treeview.heading('24h', text='24h', anchor=tk.W)
        self.treeview.heading('Price', text='Price', anchor=tk.W)
        self.treeview.column('Rank', width=50)
        self.treeview.column('Symbol', width=80)
        self.treeview.column('Market Cap', width=150)
        self.treeview.column('Total Volume', width=150)
        self.treeview.column('24h', width=80)
        self.treeview.pack()
        self.treeScroll.config(command=self.treeview.yview)
        self.load_data()

        # create graph frame
        self.graph_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")






    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.graph_button.configure(fg_color=("gray75", "gray25") if name == "graph" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "graph":
            self.graph_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.graph_frame.grid_forget()

    def graph_button_event(self):
        self.select_frame_by_name("graph")

    def home_button_event(self):
        self.select_frame_by_name("home")

    # loading data into treeview
    def load_data(self):
        list = self.dpf.tree_view_data('usd',1,2)
        for i in list:
            self.treeview.insert('', tk.END, values=i)

    def on_closing_event(self):
        print('on_closing_event ___________ destroyed self.window and initial window')
        self.window.destroy()
        self.destroy()


if __name__ == "__main__":
    gui = Gui()
    gui.window.protocol("WM_DELETE_WINDOW", gui.on_closing_event)
    gui.mainloop()
