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
from tkinter import ttk, filedialog, messagebox
import subprocess
import platform
import os
import sys

class RunVampire:
    def __init__(self, tab):
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
# Create a canvas
        canvas = tk.Canvas(tab)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# Add a frame inside the canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)
# Add a vertical scrollbar to the canvas
        v_scrollbar = tk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview, bg='black')
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=v_scrollbar.set)
# Bind the canvas scrolling to the mouse wheel
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta / 120), "units"))
        canvas.bind_all("<Shift-MouseWheel>", lambda event: canvas.xview_scroll(-1 * int(event.delta / 120), "units"))
# Bind a function to adjust the canvas scroll region when the frame size changes
        frame.bind("<Configure>", configure_scroll_region)
        
        
        # Get the home directory
        home_dir = os.path.expanduser("~")
        # Determine the .vampire directory based on the operating system
        if sys.platform == "win32":
            vampire_dir = os.path.join(home_dir, "vampire_tmp")
        else:
            vampire_dir = os.path.join(home_dir, ".vampire")
        # Create the .vampire directory if it doesn't exist
        if not os.path.exists(vampire_dir):
            os.makedirs(vampire_dir)
        # Attribute to track command execution
        self.command_running = False 
        serial="serial"
        para="para"
        # Use this path for your base path
        self.tmp_path = vampire_dir
        # serial run
        self.mode = tk.LabelFrame(frame, text="Serial mode: ", font=("Helvetica", 14, "bold"))
        self.mode.pack(side=tk.TOP, fill=tk.BOTH, expand=True,padx=8, pady=(8, 8))
        
        self.path_label = tk.Label(self.mode, text="Vampire serial Program Path:", font=("Helvetica", 12, "bold"))
        
        self.path_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.path_entry = ttk.Entry(self.mode, width=50)
        
        self.path_entry.grid(row=0, column=1, padx=20, pady=5)
        
        self.browse_button = tk.Button(self.mode, text="Browse", command=self.browse_vampire_serial)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        self.file_label = tk.Label(self.mode, text="Input file name:" , font=("Helvetica", 12, "bold"))
        self.file_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.file_entry = ttk.Entry(self.mode, width=50)
        self.file_entry.grid(row=1, column=1, padx=20, pady=5)
        
        #self.file_button = ttk.Button(self.mode, text="Browse", command=self.browse_input_serial)
        #self.file_button.grid(row=1, column=3, padx=10, pady=5)
        
        self.run_serial_button = tk.Button(self.mode, text="Run vampire-serial", command=lambda: self.run_vampire(serial))
        self.run_serial_button.grid(row=2, column=0, columnspan=3, pady=5)
        
# Parallel run        
        
        self.mode = tk.LabelFrame(frame, text="Parallel mode:  ", font=("Helvetica", 14, "bold"))
        self.mode.pack(side=tk.TOP, fill=tk.BOTH, expand=True ,padx=8, pady=(8, 8))
        
        self.path_para = tk.Label(self.mode, text="mpirun -np n  vampire_parallel  --input_file input ", font=("Helvetica", 12))
        self.path_para.grid(row=0, column=1, padx=10, pady=5,columnspan=2, sticky="w")
        
        
        self.path_para = tk.Label(self.mode, text="Vampire Program Path:", font=("Helvetica", 12, "bold"))
        self.path_para.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.path_para_entry = ttk.Entry(self.mode, width=70)
        self.path_para_entry.grid(row=1, column=1,columnspan=3, padx=10, pady=5)
        
        self.browse_button_para = tk.Button(self.mode, text="Browse", command=self.browse_vampire_para)
        self.browse_button_para.grid(row=1, column=4, padx=10, pady=5)

        self.n_label =  tk.Label(self.mode, text="Number of Processes (n):", font=("Helvetica", 12, "bold"))
        self.n_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.n_entry = ttk.Entry(self.mode, width=20)
        self.n_entry.grid(row=2, column=1, padx=10, pady=5 )

        self.file_label = tk.Label(self.mode, text="Input file name:", font=("Helvetica", 12, "bold"))
        self.file_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        
        self.file_para_entry = ttk.Entry(self.mode, width=30)
        self.file_para_entry.grid(row=2, column=3, padx=20, pady=5)
         

        #self.file_button = ttk.Button(self.mode, text="Browse", command=self.browse_input_para)
        #self.file_button.grid(row=1, column=3, padx=10, pady=5)

        self.run_para_button = tk.Button(self.mode, text="Run vampire_parallel" , command=lambda: self.run_vampire(para))
        self.run_para_button.grid(row=3, column=0, columnspan=4, pady=5)

        ## Load configuration
        self.load_config_serial()
        self.load_config_para()
        
        self.mode = tk.LabelFrame(frame, text="LOG file: ", font=("Helvetica", 14, "bold"))
        self.mode.pack(side=tk.TOP, fill=tk.BOTH, expand=True ,padx=8, pady=(8, 8))
        
        self.run_para_button = tk.Button(self.mode, text="LOG file ", command=self.log_file)
        self.run_para_button.grid(row=10, column=0, columnspan=4, pady=5)
        
        self.text_output = tk.Text(self.mode, height=40, width=150, wrap='none', bg="white")
        self.text_output.grid(row=11, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

        # Ensure the columns expand properly
        self.mode.grid_rowconfigure(4, weight=1)
    
    
#--------------------------    
    def browse_vampire_serial(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.path_entry.delete(0, tk.END)  # Clear any existing text in the entry
            self.path_entry.insert(0, file_path)
#--------------------------            
    def browse_vampire_para(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.path_para_entry.delete(0, tk.END)  # Clear any existing text in the entry
            self.path_para_entry.insert(0, file_path)
            
#--------------------------
    def browse_input_serial(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)  # Clear any existing text in the entry
            self.file_entry.insert(0, file_path)
#--------------------------            
    def browse_input_para(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_para_entry.delete(0, tk.END)  # Clear any existing text in the entry
            self.file_para_entry.insert(0, file_path)
    
 #--------------------------   
    def save_config_serial(self):
        #base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        base_path=self.tmp_path
        try:
            with open(os.path.join(base_path, "config_serial.txt"), "w")  as file:
                file.write(self.path_entry.get() + "\n")
                file.write(self.file_entry.get() + "\n")
        except FileNotFoundError:
            pass
#--------------------------
    def save_config_para(self):
        base_path=self.tmp_path
        try:
            with open(os.path.join(base_path, "config_para.txt"), "w")  as file:
                file.write(self.path_para_entry.get() + "\n")
                file.write(self.n_entry.get() + "\n")
                file.write(self.file_para_entry.get() + "\n") 
        except FileNotFoundError:
            pass
            
#--------------------------            
    def load_config_serial(self):
        #base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        base_path=self.tmp_path
        try:
            with open(os.path.join(base_path, "config_serial.txt"), "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    self.path_entry.insert(0, lines[0].strip())
                    self.file_entry.insert(0, lines[1].strip())
        except FileNotFoundError:
            pass
#--------------------------    
    def load_config_para(self):
        base_path=self.tmp_path
        try:
            with open(os.path.join(base_path, "config_para.txt"), "r")  as file:
                    lines = file.readlines()
                    if len(lines) >= 3:
                        self.path_para_entry.insert(0, lines[0].strip())
                        self.n_entry.insert(0, lines[1].strip())
                        self.file_para_entry.insert(0, lines[2].strip())
        except FileNotFoundError:
            pass

#--------------------------
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            return file_path
#--------------------------
    def log_file(self):
        try:
            with open("log", 'r') as file:
                data = file.readlines()
                self.text_output.delete(1.0, tk.END)  # Clear previous data
                for line in data:
                    self.text_output.insert(tk.END, line)
        except Exception as e:
            print("Error:", e)
#--------------------------
    def detect_terminal(self):
        system = platform.system()
        if system == 'Windows':
            return 'cmd'  # Default terminal in Windows
        elif system == 'Darwin':
            return 'open -a Terminal'  # Default terminal in macOS
        else:  # Assume a Linux system
            # Check for various common terminal emulators
            terminals = ['gnome-terminal', 'konsole', 'xterm', 'xfce4-terminal', 'mate-terminal', 'tilix']
            for term in terminals:
                if subprocess.call(['which', term], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
                    return term
            return 'xterm'  # Fallback to xterm if no other terminal is found

#--------------------------
    
    def run_vampire(self, run_mode):
        print ("-*************")
        #check command execution 
        file_state = os.path.exists("running.txt")
        if self.command_running or file_state:  # Check if a command is already running
            messagebox.showinfo("Already Running", "Mybe the command is already running. \n or not remove the file 'running.txt' then run the command again")
            return
        if run_mode=="para":
            path = self.path_para_entry.get()
            n = self.n_entry.get()
            input_file = self.file_para_entry.get()
            n = self.n_entry.get()
            if not path or not n or not input_file:
                messagebox.showerror("Input file name", " Please insert vampire path and the input file name")
                return
            try:
                n = int(n)
            except ValueError:
                messagebox.showerror("Input Error", "Number of processes (n) must be an integer.")
                return
            command = f"mpirun -np {n} {path} --input-file {input_file}"
            terminal = self.detect_terminal()
        elif run_mode=="serial":
            path = self.path_entry.get()
            input_file = self.file_entry.get()
            if not path or not input_file:
                messagebox.showerror("Input Error", "Please insert vampire path and the input file name")
                return
            command = f"{path} --input-file {input_file}"
            terminal = self.detect_terminal()
        else:
             messagebox.showerror("Mode", "run mode not known")
             return

        # Get the initial state of the file
        if terminal == 'cmd':
            terminal_command = f'start cmd /k "{command}"'
        elif terminal == 'open -a Terminal':
            terminal_command = f'open -a Terminal.app -n --args bash -c "{command}; exec bash"'
        elif terminal == 'gnome-terminal':
            terminal_command = f'gnome-terminal -- bash -c "{command}; exec bash"'
        elif terminal == 'konsole':
            terminal_command = f'konsole -e bash -c "{command}; exec bash"'
        elif terminal == 'xterm':
            terminal_command = f'xterm -e bash -c "{command}; exec bash"'
        elif terminal == 'xfce4-terminal':
            terminal_command = f'xfce4-terminal --command="{command}; exec bash"'
        elif terminal == 'mate-terminal':
            terminal_command = f'mate-terminal -- bash -c "{command}; exec bash"'
        elif terminal == 'tilix':
            terminal_command = f'tilix -- bash -c "{command}; exec bash"'
        else:
            messagebox.showerror("Error", "No suitable terminal found.")
            return
        
        try:
            with open("running.txt", "w") as file:
                file.write("...vampire is running... it should be remove to run the command again")
        except FileNotFoundError:
            pass
        initial_file_state = os.path.exists("running.txt")
        try:
            ## Disable the "Run" button while the command is running
            self.command_running = True
            self.run_serial_button.config(state=tk.DISABLED)
            self.run_para_button.config(state=tk.DISABLED)
            # rn the command
            process = subprocess.Popen(terminal_command, shell=True, executable='/bin/bash')
            messagebox.showinfo("Running", f"Command :\n '{command}' \nis running in a new terminal.")
            # Wait for the command to finish
            process.wait()
            os.remove("running.txt")  # Corrected typo here
            # Get the final state of the file
            file_state = os.path.exists("running.txt")
            #If the file was removed, enable the "Run" button again
            if  not file_state:
                self.run_serial_button.config(state=tk.NORMAL)
                self.run_para_button.config(state=tk.NORMAL)
                self.command_running = False
                #messagebox.showinfo("File Removed", "The input file was removed at the terminal end.")
        except Exception as e:
            # Reset the state of the "Run" button and command_running flag after command execution
            self.run_serial_button.config(state=tk.NORMAL)
            self.run_para_button.config(state=tk.NORMAL)
            self.command_running = False
            messagebox.showerror("Execution Error", str(e))
        # Save configuration
        if run_mode=="serial":
            self.save_config_serial()
        if run_mode=="para":
            self.save_config_para()
 
    
 
        
    

