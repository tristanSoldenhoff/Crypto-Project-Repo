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

        # configure grid 2x2
        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=8)
        self.window.grid_rowconfigure(0, weight=0)
        self.window.grid_rowconfigure(1, weight=5)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8)
        self.navigation_frame.grid_columnconfigure(0, weight=1)
        self.navigation_frame.grid_rowconfigure(10, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text='Navigation Bar', anchor='center',
                                        font=customtkinter.CTkFont(size=25, weight='bold'))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20, sticky='news')

        self.treeview_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Treeview", fg_color="transparent",
                            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=self.treeview_button_event)
        self.treeview_button.grid(row=1, column=0, sticky="ew")

        self.chart_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Chart", fg_color="transparent",
                            text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=self.chart_button_event)
        self.chart_button.grid(row=2, column=0, sticky="ew")

        # create toolbar
        self.toolbar_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8)
        self.toolbar_frame.grid_columnconfigure(0, weight=1)
        self.toolbar_frame.grid_rowconfigure(10, weight=1)

        self.toolbar_frame_label = customtkinter.CTkLabel(self.toolbar_frame, text='Toolbar', anchor='center',
                                        font=customtkinter.CTkFont(size=25, weight='bold'))
        self.toolbar_frame_label.grid(row=0, column=0, padx=20, pady=20, sticky='news')

        # create home frame which hosts:    window <-- home_frame <-- tree_frame OR chart_frame
        self.home_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8, fg_color=('gray70', 'gray17'))
        self.home_frame.grid(row=0, column=1, rowspan=2, padx=(7.5 ,15), pady=15, sticky="news")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        # create treeview:  home_frame <-- background_frame <-- treeview + tree_scroll
        self.tree_frame = TreeFrame(master=self.home_frame, dpf=self.dpf)

        # create price chart and modify navigation_frame
        self.chart_frame = ChartFrame(master=self.home_frame, dpf=self.dpf, gf=self.gf)

        # select default frame
        self.select_frame_by_name("treeview")

    # show navigation_frame or navigation_frame & toolbar_frame
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.treeview_button.configure(fg_color=("gray75", "gray25") if name == "treeview" else "transparent")
        self.chart_button.configure(fg_color=("gray75", "gray25") if name == "chart" else "transparent")

        if name == 'treeview':
            self.navigation_frame.grid(row=0, column=0, rowspan=2, padx=(15, 7.5), pady=15, sticky='news')
            self.tree_frame.grid(row=0, column=0, padx=(7.5 ,15), pady=15)
        else:
            self.navigation_frame.grid_forget()
            self.tree_frame.grid_forget()
        if name == 'chart':
            self.navigation_frame.grid(row=0, column=0, padx=(15, 7.5), pady=(15, 7.5), sticky='news')
            self.toolbar_frame.grid(row=1, column=0, padx=(15, 7.5), pady=(7.5, 15), sticky='news')
            self.chart_frame.grid(row=0, column=0, padx=5, pady=5, sticky='news')
        else:
            self.toolbar_frame.grid_forget()
            self.chart_frame.grid_forget()

    def treeview_button_event(self):
        self.select_frame_by_name("treeview")

    def chart_button_event(self):
        self.select_frame_by_name("chart")

    def on_closing_event(self):
        exit()


class TreeFrame(customtkinter.CTkFrame):
    def __init__(self, master, dpf, **kwargs):
        super().__init__(master, **kwargs)

        self.dpf = dpf

        #  create scroll bar
        self.tree_scroll = ttk.Scrollbar(master=self)
        self.tree_scroll.pack(side='right', fill='y')

        # create treeview and set up treeview columns and theme
        self.cols = ('Rank', 'ID', 'Symbol', 'Market Cap', 'Total Volume', '24h', 'Price' )
        self.treeview = ttk.Treeview(master=self, show='headings', yscrollcommand=self.tree_scroll.set, columns=self.cols, height=100)
        self.tree_scroll.config(command=self.treeview.yview)
        self.set_tree_frame_theme(self.treeview)
        self.set_treeview_data(self.treeview)

    # apply Azure theme to tree_frame
    def set_tree_frame_theme(self, treeview):
        style = ttk.Style(self.treeview)
        self.treeview.tk.call('source', 'Azure/azure.tcl')
        self.treeview.tk.call('set_theme', 'dark')

    # set up treeview column headings and load data
    def set_treeview_data(self, treeview):
        self.treeview = treeview
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

        # load data into treeview
        list = self.dpf.tree_view_data('usd',1,2)
        for i in list:
            self.treeview.insert('', tk.END, values=i)


class ChartFrame(customtkinter.CTkFrame):
    def __init__(self, master, dpf, gf, **kwargs):
        super().__init__(master, **kwargs)

        #print(plt.rcParams)

        # set plot theme for matplotlib
        with plt.rc_context({
                            'axes.labelpad': '8.0',
                            'font.size': '10.0',
                            'axes.xmargin': '0.1',
                            'axes.ymargin': '0.1',
                            'grid.linewidth': '1.5',
                            'grid.color': '#F7F7F7',
                            'axes.linewidth': '1.5',
                            'xtick.major.width': '1.5',
                            'xtick.major.size': '4.0',
                            'xtick.minor.width': '1.0',
                            'xtick.minor.size': '2.0',
                            'ytick.major.width': '1.5',
                            'ytick.major.size': '4.0',
                            }):

            self.dpf = dpf
            self.gf = gf

            # create embedded matplotlib graph - window <-- home_frame <-- self <- canvas <- fig <- ax
            self.fig, self.ax = plt.subplots()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.plotGraph(self.ax, self.fig, self.canvas, self.dpf, self.gf)

    # def plotGraph(self, ax, fig, canvas, gf, dpf):
    def plotGraph(self, ax, fig, canvas, dpf, gf):
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



if __name__ == "__main__":
    gui = Gui()
    gui.window.protocol("WM_DELETE_WINDOW", gui.on_closing_event)
    gui.mainloop()
