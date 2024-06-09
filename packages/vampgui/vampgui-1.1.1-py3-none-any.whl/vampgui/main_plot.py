# -*- coding: utf-8 -*-
#
# copyright (c) 06-2024 G. Benabdellah
# Departement of physic
# University of Tiaret , Algeria
# E-mail ghlam.benabdellah@gmail.com
#
# this program is part of VAMgui 
# first creation 28-05-2024
#  
#
# License: GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#  log change:
#
#


import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt
#import subprocess

class Plotmain:
    def __init__(self, tab):
        self.tab = tab
        canvas = tk.Canvas(tab)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a frame inside the canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)
        
        self.mode = tk.LabelFrame(frame, text="Plot output file:", font=("Helvetica", 14, "bold"))
        self.mode.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(8, 8))
        
        self.open_label = tk.Label(self.mode, text="Output Vampire file", font=("Helvetica", 12, "bold"))
        self.open_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        # Create and position widgets
        self.open_button = tk.Button(self.mode, text="Open File", command=self.plot_data)
        self.open_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.x_label = tk.Label(self.mode, text="X Axis:")
        self.x_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.x_var = tk.StringVar()
        self.x_var.set("Select X Axis")
        self.x_optionmenu = tk.OptionMenu(self.mode, self.x_var, *[f"Column {i}" for i in range(1, 10)])
        self.x_optionmenu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.x_plot_label = tk.Label(self.mode, text="X-Label:")
        self.x_plot_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.x_lab = ttk.Entry(self.mode, width=25)
        self.x_lab.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.y_label = tk.Label(self.mode, text="Y Axis:")
        self.y_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.y_var = tk.StringVar()
        self.y_var.set("Select Y Axis")
        self.y_optionmenu = tk.OptionMenu(self.mode, self.y_var, *[f"Column {i}" for i in range(1, 10)])
        self.y_optionmenu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.y_plot_label = tk.Label(self.mode, text="Y-Label:")
        self.y_plot_label.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.y_lab = ttk.Entry(self.mode, width=25)
        self.y_lab.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        self.plot_button = tk.Button(self.mode, text="Plot", command=self.plot_graph)
        self.plot_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="e")

        self.text_output = tk.Text(self.mode, height=40, width=120, wrap='none', bg="white")
        self.text_output.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Ensure the columns expand properly
        self.mode.grid_columnconfigure(0, weight=1)
        self.mode.grid_columnconfigure(1, weight=1)
        self.mode.grid_columnconfigure(2, weight=1)
        self.mode.grid_columnconfigure(3, weight=1)
        self.mode.grid_rowconfigure(4, weight=1)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            return file_path

    def plot_data(self):
        file_path = self.open_file()
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    data = file.readlines()
                    self.text_output.delete(1.0, tk.END)  # Clear previous data
                    for line in data:
                        self.text_output.insert(tk.END, line)

            except Exception as e:
                print("Error:", e)


    #def plot_graph(self):
        #x_column = self.x_var.get()
        #y_column = self.y_var.get()
        #x_label = self.x_lab.get()
        #y_label = self.y_lab.get()
        #file_data = self.text_output.get("1.0", tk.END)

        #if x_column != "Select X Axis" and y_column != "Select Y Axis" and file_data:
            #try:
                #x_values = []
                #y_values = []
                #lines = file_data.split('\n')
                #for line in lines:
                    #if line.strip() and not line.startswith('#'):  # Skip empty lines and comments
                        #line_data = line.split()
                        #x_values.append(float(line_data[int(x_column.split()[-1]) - 1]))
                        #y_values.append(float(line_data[int(y_column.split()[-1]) - 1]))

                ## Write data to a temporary file
                #with open('temp.dat', 'w') as f:
                    #for x, y in zip(x_values, y_values):
                        #f.write(f"{x} {y}\n")

                ## Gnuplot command
                #gnuplot_script = f"""
                #set xlabel "{x_label}"
                #set ylabel "{y_label}"
                #plot 'temp.dat' with lines
                
                #pause -1
                
                #"""

                ## Execute Gnuplot
                #gnuplot_process = subprocess.Popen(['gnuplot'], stdin=subprocess.PIPE)
                #gnuplot_process.communicate(gnuplot_script.encode())

            #except Exception as e:
                #print("Error:", e)


    def plot_graph(self):
        plt.close('all')  # Close any existing plot windows
        x_column = self.x_var.get()
        y_column = self.y_var.get()
        x_label = self.x_lab.get()
        y_label = self.y_lab.get()
        file_data = self.text_output.get("1.0", tk.END)

        if x_column != "Select X Axis" and y_column != "Select Y Axis" and file_data:
            try:
                x_values = []
                y_values = []
                lines = file_data.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):  # Skip empty lines and comments
                        line_data = line.split()
                        x_values.append(float(line_data[int(x_column.split()[-1]) - 1]))
                        y_values.append(float(line_data[int(y_column.split()[-1]) - 1]))

                plt.plot(x_values, y_values)
                plt.xlabel(x_label)
                plt.ylabel(y_label)
                plt.title('Plot from File Data')
                plt.show()

            except Exception as e:
                print("Error:", e)

### Create GUI instance
##root = tk.Tk()
##tab = tk.Frame(root)
##tab.pack(fill=tk.BOTH, expand=True)
##app = Plotmain(tab)
##root.mainloop()
