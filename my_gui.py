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
import matplotlib.dates as mpl_dates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd
import numpy as nps

class Gui(customtkinter.CTk, GeckoFunctions):
    def __init__(self):
        super().__init__()

        # accessing crypto data
        self.gf = GeckoFunctions()
        self.mf = MyFunctions()
        self.dpf = DataProcessingFunctions()

        # dots per inch awareness - to fix blurry text on GUI
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        # hide initial window
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
        # self.navigation_frame.grid(row=0, column=0, padx=15, pady=15, sticky='news')
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

        # create background frame to host graph_frame - this allows for corner_radius to be applied
        self.back_frame = customtkinter.CTkFrame(master=self.window, corner_radius=8, fg_color='#2B2B2B')
        self.back_frame.grid_columnconfigure(0, weight=1)
        self.back_frame.grid_rowconfigure(0, weight=1)

        # create graph frame
        self.graph_frame = customtkinter.CTkFrame(master=self.back_frame, corner_radius=8, fg_color="#2B2B2B")
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)


# axes.labelpad: 4.0
# axes.labelsize: medium
# axes.labelweight: normal
# axes.linewidth: 0.8
# axes.titlecolor: auto
# axes.titlelocation: center
# axes.titlepad: 6.0
# axes.titlesize: large
# axes.titleweight: normal
# axes.titley: None
# axes.xmargin: 0.05
# axes.ymargin: 0.05
# axes.zmargin: 0.05
# figure.edgecolor: white
# figure.facecolor: white
# figure.figsize: [6.4, 4.8]
# figure.labelsize: large
# figure.labelweight: normal
# figure.titlesize: large
# figure.titleweight: normal
# font.size: 10.0
# font.style: normal
# font.variant: normal
# font.weight: normal
# grid.alpha: 1.0
# grid.color: #b0b0b0
# grid.linestyle: -
# grid.linewidth: 0.8
# lines.antialiased: True
# lines.color: C0
# lines.dash_capstyle: butt
# lines.dash_joinstyle: round
# lines.dashdot_pattern: [6.4, 1.6, 1.0, 1.6]
# lines.dashed_pattern: [3.7, 1.6]
# lines.dotted_pattern: [1.0, 1.65]
# lines.linestyle: -
# lines.linewidth: 1.5
# lines.marker: None
# lines.markeredgecolor: auto
# lines.markeredgewidth: 1.0
# lines.markerfacecolor: auto
# lines.markersize: 6.0
# lines.scale_dashes: True
# lines.solid_capstyle: projecting
# lines.solid_joinstyle: round
# text.antialiased: True
# text.color: black
# text.hinting: force_autohint
# text.hinting_factor: 8
# text.kerning_factor: 0
# text.latex.preamble:
# text.parse_math: True
# text.usetex: False
# timezone: UTC
# tk.window_focus: False
# toolbar: toolbar2
# xaxis.labellocation: center
# xtick.alignment: center
# xtick.bottom: True
# xtick.color: black
# xtick.direction: out
# xtick.labelbottom: True
# xtick.labelcolor: inherit
# xtick.labelsize: medium
# xtick.labeltop: False
# xtick.major.bottom: True
# xtick.major.pad: 3.5
# xtick.major.size: 3.5
# xtick.major.top: True
# xtick.major.width: 0.8
# xtick.minor.bottom: True
# xtick.minor.pad: 3.4
# xtick.minor.size: 2.0
# xtick.minor.top: True
# xtick.minor.visible: False
# xtick.minor.width: 0.6
# xtick.top: False
# yaxis.labellocation: center
# ytick.alignment: center_baseline
# ytick.color: black
# ytick.direction: out
# ytick.labelcolor: inherit
# ytick.labelleft: True
# ytick.labelright: False
# ytick.labelsize: medium
# ytick.left: True
# ytick.major.left: True
# ytick.major.pad: 3.5
# ytick.major.right: True
# ytick.major.size: 3.5
# ytick.major.width: 0.8
# ytick.minor.left: True
# ytick.minor.pad: 3.4
# ytick.minor.right: True
# ytick.minor.size: 2.0
# ytick.minor.visible: False
# ytick.minor.width: 0.6
# ytick.right: False


        print(plt.rcParams)

        # set plot theme for matplotlib
        with plt.rc_context({
                            'figure.facecolor':'#2B2B2B',
                            'axes.facecolor':'#2B2B2B',
                            'xtick.color':'white',
                            'ytick.color':'white',
                            'axes.titlecolor':'white',
                            'axes.labelcolor':'white',
                            'axes.edgecolor':'#333333',
                            'grid.color':'#333333',
                            'axes.titlelocation':'left',
                            'text.color': 'white',
                            }):


            # create embedded matplotlib graph - graph_frame <- canvas <- fig <- ax
            fig, ax = plt.subplots()
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            self.plotGraph(canvas, ax, self.gf, fig, self.mf)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.graph_button.configure(fg_color=("gray75", "gray25") if name == "graph" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, padx=(0,15), pady=10, sticky="news")
        else:
            self.home_frame.grid_forget()
        if name == "graph":
            self.back_frame.grid(row=0, column=1, padx=(0,15), pady=15, sticky="nsew")
            self.graph_frame.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")
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

    def plotGraph(self, canvas, ax, gf, fig, mf):
        data = gf.get_coin_data_days('bitcoin', 'usd', 10000)
        time = []
        price = []
        for i in data['prices']:
            time.append(i[0])
            price.append(i[1])

        ax.title.set_text('Bitcoin')
        ax.set_xlabel('Date')
        ax.set_ylabel('USD')
        ax.set_yscale('log')
        ax.grid(visible=True, which='major', axis='both')

        # for i in time:
        #     print(mf.human_time(i))

        #ax.plot(mf.human_time(time), price)
        ax.plot(time, price)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#fig, ax = plt.subplots()
#idx = pd.date_range('2013-12-07', '2023-01-09', freq='M')
# # generate a time range series with 10 min intervals
# idx = np.arange('2018-01-07T00', '2018-01-09T02', 10, dtype='datetime64[m]')
# # some random data
# y = np.sin(np.arange(idx.shape[0]) / 0.01)
#
# ax.plot_date(idx, y, '-')
#
# ax.xaxis.set_minor_locator(dates.HourLocator(interval=4))   # every 4 hours
# ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
# ax.xaxis.set_major_locator(dates.DayLocator(interval=1))    # every day
# ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d-%m-%Y'))



    def on_closing_event(self):
        print('on_closing_event ___________ destroyed self.window and initial window')
        self.window.destroy()
        self.destroy()
        exit()
        # "1968159393536check_dpi_scaling" on cmd after closing. This message was displayed when matplotlib graph was embedded.

if __name__ == "__main__":
    gui = Gui()
    gui.window.protocol("WM_DELETE_WINDOW", gui.on_closing_event)
    gui.mainloop()
