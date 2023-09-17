"""
 Customtkinter documentation:  https://customtkinter.tomschimansky.com/documentation/widgets/button
 Appearance: customtkinter
 forest-ttk-theme     (used for treeview table)
"""

import tkinter as tk
from tkinter import ttk
import customtkinter
import ctypes                                                                   # dots per inch awareness
from my_functions import MyFunctions
from gecko_functions import GeckoFunctions
from data_processing_functions import DataProcessingFunctions
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd
import numpy as nps

class Gui(customtkinter.CTk, GeckoFunctions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # accessing crypto data
        self.gf = GeckoFunctions()
        self.mf = MyFunctions()
        self.dpf = DataProcessingFunctions()

        # dots per inch awareness - to fix blurry text on GUI
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        # hide initial window
        self.iconify()

        # window
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

        self.navigation_frame_label_0 = customtkinter.CTkLabel(self.navigation_frame, text='Navigation Bar', anchor='center',
                                        font=customtkinter.CTkFont(size=25, weight='bold'))
        self.navigation_frame_label_0.grid(row=0, column=0, padx=20, pady=20, sticky='news')

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Home", fg_color="transparent",
                            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.graph_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Graphs", fg_color="transparent",
                            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=self.graph_button_event)
        self.graph_button.grid(row=2, column=0, sticky="ew")

        # create home frame             home_frame <- tree_frame <- tree_scroll + tree_view
        # self.home_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8, fg_color=('gray70', 'gray10'))
        self.home_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8, fg_color=('gray70', 'gray17'))
        self.home_frame.grid(row=0, column=1, padx=(0,15), pady=10, sticky="news")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        # create tree frame
        self.tree_frame = customtkinter.CTkFrame(master=self.home_frame, corner_radius=8)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid(row=0, column=0, padx=5, pady=5)

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

        # create background frame to host chart_frame - this allows for corner_radius to be applied
        self.back_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8, fg_color='#2B2B2B')
        self.back_frame.grid_columnconfigure(0, weight=1)
        self.back_frame.grid_rowconfigure(0, weight=1)

        # create graph frame
        self.graph_frame = customtkinter.CTkFrame(master=self.back_frame, corner_radius=8, fg_color="#2B2B2B")
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)

        #print(plt.rcParams)

        # set plot theme for matplotlib
        with plt.rc_context({
                            # 'figure.facecolor':'#2B2B2B',
                            # 'axes.facecolor':'#2B2B2B',
                            # 'xtick.color':'white',
                            # 'ytick.color':'white',
                            # 'axes.titlecolor':'white',
                            # 'axes.labelcolor':'white',
                            # 'axes.edgecolor':'#333333',
                            # 'grid.color':'#333333',
                            # 'axes.titlelocation':'left',
                            # 'text.color': 'white',
                            'axes.labelpad': '8.0',
                            'font.size': '10.0',
                            'axes.xmargin': '0.1',
                            'axes.ymargin': '0.1',
                            'grid.linewidth': '1.5',
                            'axes.linewidth': '1.5',
                            'xtick.major.width': '1.5',
                            'xtick.major.size': '4.0',
                            'xtick.minor.width': '1.0',
                            'xtick.minor.size': '2.0',
                            'ytick.major.width': '1.5',
                            'ytick.major.size': '4.0',

                            }):

            # create embedded matplotlib graph - graph_frame <- canvas <- fig <- ax
            self.fig, self.ax = plt.subplots()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
            self.plotGraph(self.ax, self.fig, self.canvas, self.gf, self.dpf)

        self.toplevel_toolbar_window = None

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.graph_button.configure(fg_color=("gray75", "gray25") if name == "graph" else "transparent")

        # show selected frame or frame and toplevel window
        if name == "home":
            self.home_frame.grid(row=0, column=1, padx=(0,15), pady=10, sticky="news")
        else:
            self.home_frame.grid_forget()
        if name == "graph":
            self.back_frame.grid(row=0, column=1, padx=(0,15), pady=15, sticky="nsew")
            self.graph_frame.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")
            self.open_toplevel_graph_toolbar()
        else:
            self.back_frame.grid_forget()
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

    def plotGraph(self, ax, fig, canvas, gf, dpf):
        data = gf.get_coin_data_days('bitcoin', 'usd', 10000)
        human_time, price = ([] for i in range(2))
        for i in data['prices']:
            human_time.append(dpf.human_time(i[0]))
            price.append(i[1])
        self.ax.title.set_text('Bitcoin')
        self.ax.set_ylabel(r'Price [\$]')

        self.ax.plot(human_time, price)
        #ax.set_yscale('log')
        self.ax.grid(visible=True, which='major', axis='both')

        # Major ticks every half year, minor ticks every month,
        self.ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1)))
        self.ax.xaxis.set_minor_locator(mdates.MonthLocator())

        self.ax.set_title('Manual DateFormatter', loc='left', y=0.85, x=0.02, fontsize='medium')

        # Text in the x-axis will be displayed in 'YYYY' format.
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def open_toplevel_graph_toolbar(self):
        if self.toplevel_toolbar_window is None or not self.toplevel_toolbar_window.winfo_exists():
            self.toplevel_toolbar_window = ToplevelGraphToolBar(self)  # create window if its None or destroyed
        else:
            self.toplevel_toolbar_window.focus()  # if window exists focus it

    def on_closing_event(self):
        print('on_closing_event ___________ destroyed self.window and initial window')
        self.window.destroy()
        self.destroy()
        exit()
        # "1968159393536check_dpi_scaling" on cmd after closing. This message was displayed when matplotlib graph was embedded.

class ToplevelGraphToolBar(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(8, weight=1)

        self.geometry("400x300")
        self.title('Toolbar')

        self.toolbar_frame = customtkinter.CTkLabel(master=self)
        self.toolbar_frame.grid(row=0, column=0, sticky='news')

        self.toolbarLabel = customtkinter.CTkLabel(self.toolbar_frame, text='Toolbar', anchor='center',
                                        font=customtkinter.CTkFont(size=25, weight='bold'))
        self.toolbarLabel.grid(row=0, column=0, sticky='news')

        self.switch_var_yscale_on = customtkinter.StringVar(value="on")
        self.switch_var_yscale_off = customtkinter.StringVar(value="off")
        self.switch_yscale = customtkinter.CTkSwitch(master=self.toolbar_frame, text="Log", command=self.switch_yscale_event,
                        variable=self.switch_var_yscale_on, onvalue="on", offvalue="off")
        self.switch_yscale.grid(row=0, column=1, sticky='news')




    def switch_yscale_event(self):
        if self.switch_var_yscale_on.get() == 'on':
            print('switch is on')
            self.ax.set_yscale('log')
        elif self.switch_var_yscale_off.get() == 'off':
            print('switch if off')



if __name__ == "__main__":
    gui = Gui()
    gui.window.protocol("WM_DELETE_WINDOW", gui.on_closing_event)
    gui.mainloop()
