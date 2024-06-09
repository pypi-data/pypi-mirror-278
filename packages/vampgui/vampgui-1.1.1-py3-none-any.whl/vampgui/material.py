# -*- coding: utf-8 -*-
#
# Author: G. Benabdellah
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

import re
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext, messagebox,ttk
from vampgui.file_io import InputFileViewer 
from vampgui.helpkey import  show_help
class MainInputTab:
    def __init__(self, tab):
        self.setup_main_input(tab)
        # Create a canvas
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
# Add a horizontal scrollbar to the canvas
        h_scrollbar = tk.Scrollbar(tab, orient=tk.HORIZONTAL, command=canvas.xview, bg='black')
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.config(xscrollcommand=h_scrollbar.set)
# Bind the canvas scrolling to the mouse wheel
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta / 120), "units"))
        canvas.bind_all("<Shift-MouseWheel>", lambda event: canvas.xview_scroll(-1 * int(event.delta / 120), "units"))
# Bind a function to adjust the canvas scroll region when the frame size changes
        frame.bind("<Configure>", configure_scroll_region)
# Frame for buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)      
        tk.Button(button_frame, bg='cyan', text="Add Sample", command=lambda: self.add_sample(self.sample_tab)).grid(row=0, column=0, padx=5, pady=5,sticky="w")
        tk.Button(button_frame, bg='bisque', text="Import from file.mat", command=self.load_file).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(button_frame, bg='#99ff99', text="Save to sample.mat", command=self.save_to_file).grid(row=0, column=2, padx=5, pady=5,sticky="w")
        tk.Button(button_frame, bg='#ffff99', text="View/Edit sample.mat", command=self.open_sample_file).grid(row=0, column=3,padx=5, pady=5,sticky="w")
        tk.Button(button_frame, text="                      ",).grid(row=0, column=4, padx=4, pady=5, sticky="e")
        tk.Button(button_frame, bg='#ff9999', text="Deselect All", command=self.deselect_all_checkboxes).grid(row=0, column=5, padx=5, pady=5, sticky="e")
        tk.Button(button_frame, bg='#ff9999', text="Remove Last Sample", command=self.remove_sample).grid(row=0, column=6,padx=5, pady=5,sticky="e")
# Create a notebook for sub-tabs
        sub_notebook = ttk.Notebook(frame)
        sub_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
# load input values  from sample.mat file  
        #self.load_default_values()
        self.new_index=1
        self.new_indices = {}
        self.k_list = []
        self.load_input_values
        self.full_subkeywords = list(self.default_values.keys())
        self.sample_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(self.sample_tab, text="Sample")
        self.samples = []
        self.indx =0
        self.add_sample(self.sample_tab)


#==========================
    def add_sample(self, tab):
        index = len(self.samples) + 1
        
        self.indx += 1
        frame = tk.LabelFrame(tab, text=f"Sample {index} : Material attributes (Note: Before import the .mat file or add sample, ensure you add the necessary indexed subkeywords by clicking on the + button.)",font=("Helvetica", 12, "bold"))
        frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=(5, 5))
        entries = {}
        row = 0
        col = 0
        max_row = 13  # Set the maximum number of rows
        Padx = 0
        Wdth = 14
        shaps = []
        self.indexsky=[ "exchange-matrix[1]=", "biquadratic-exchange[1]=", "neel-anisotropy-constant[1]=", "alloy-fraction[1]=", "intermixing[1]="]

        for subkeys in self.full_subkeywords:
            ncol = 3 * col
            var = tk.BooleanVar()
            check = tk.Checkbutton(frame, text=subkeys, variable=var, font=13)
            check.config(command=lambda skw=subkeys, v=var, chk=check: self.selected_subky(skw, v, shaps, chk))
            check.grid(row=row, column=ncol+1, sticky="w")
            loaded_value = self.default_values[subkeys]
            subkeyword = subkeys.strip().strip("=").strip()

            if subkeyword == "num-materials":
                entry = tk.Entry(frame, width=Wdth, state='disabled')
                entry.grid(row=row, column=ncol+2, sticky="w", padx=Padx)
                entry.insert(0, loaded_value)
                var.set(True)
                entries[subkeys] = (var, entry, check)
            elif subkeyword == "non-magnetic":
                entry = ttk.Combobox(frame, values=["remove", "keep"], state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx  , sticky="e")
                if loaded_value.lower() in ["remove", "keep"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("remove")
                    entry.insert(0, "remove")
                entries[subkeys] = (var, entry, check)
                
                
            elif subkeyword == "alloy-distribution":
                entry = ttk.Combobox(frame, values=["native", "reciprocal" , "homogeneous"], state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx  , sticky="e")
                if loaded_value.lower() in ["native", "reciprocal" , "homogeneous"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("native")
                    entry.insert(0, "native")
                entries[subkeys] = (var, entry, check)
                
            elif loaded_value == "none":
                entry = tk.Entry(frame, width=Wdth, state='disabled')
                entry.grid(row=row, column=ncol+2, sticky="w", padx=Padx)
                entry.insert(0, loaded_value)
                entries[subkeys] = (var, entry, check)
            else:
                entry = tk.Entry(frame, bg='white', width=Wdth)
                entry.grid(row=row, column=ncol+2, sticky="w", padx=Padx)
                entry.insert(0, loaded_value)
                entries[subkeys] = (var, entry, check)

            help_button = tk.Button(frame, text="?", command=lambda kw=subkeys: show_help(kw)) 
            help_button.grid(row=row, column=ncol+3,padx=1, sticky="w")
            # Add a button to dynamically add more subkeys
            if subkeys in self.indexsky:
                add_subkey_button = tk.Button(frame, text="+", command=lambda   skw=subkeys: self.add_subkey(frame,skw))
                add_subkey_button.grid(row=row, column=ncol+3, padx=35, sticky="e")
            row += 1
            if row == max_row:
                row = 0
                col += 1
            
        self.lastrow=row
        self.colmax=col
        self.maxrow= max_row 
        self.samples.append((frame, entries))
        self.k_list.append((f'material[{index}]', entries))

    def add_subkey(self, frame, skw):
        subkey = skw.strip().strip("=").strip()
        subkey_base = subkey.split("[")[0]

        # Initialize the index for this subkey type if not already done
        if subkey_base not in self.new_indices:
            self.new_indices[subkey_base] = 2
        else:
            # Increment the index for this subkey type
            self.new_indices[subkey_base] += 1

        new_subkey = f"{subkey_base}[{self.new_indices[subkey_base]}]="
        if self.lastrow == self.maxrow:
            self.lastrow = 0
            self.colmax += 1

        row = self.lastrow
        col = self.colmax

        var = tk.BooleanVar()
        check = tk.Checkbutton(frame, text=new_subkey, variable=var, font=13)
        check.config(command=lambda skw=new_subkey, v=var, chk=check: self.selected_subky(skw, v, [], chk))
        check.grid(row=row, column=3 * col + 1, sticky="w")

        entry = tk.Entry(frame, bg='white', width=10)
        entry.grid(row=row, column=3 * col + 2, sticky="w")
        entry.insert(0, "0.0")
        self.full_subkeywords.append(new_subkey)

        # Add the new subkey to default_values with an initial default value
        self.default_values[new_subkey] = "0.0"  # Set the initial value as needed

        # Update self.samples and self.k_list
        self.samples[-1][1][new_subkey] = (var, entry, check)
        self.k_list[-1][1][new_subkey] = (var, entry, check)
        self.lastrow += 1
        
#==========================
    def selected_subky(self, subkeyword, var,shaps, check):
        if var.get():
            self.set_checkbox_color(check, 'blue')
            sub_key=subkeyword.strip().strip("=").strip() 
            #if self.last_selected.get():
                #if sub_key in shaps:
                    #self.set_checkbox_color(check, "green")
                    #self.deselect_checkbox(self.last_selected.get(), shaps)
        else:
            self.set_checkbox_color(check, 'black')
        #self.last_selected.set(subkeyword) 
#==========================
    def open_sample_file(self):
        InputFileViewer("sample.mat")
#==========================
    def deselect_checkbox(self, subkeyword, shaps):
        sub_key=subkeyword.strip().strip("=").strip()
        if sub_key in shaps:
            for keyword, entries in self.k_list:
                if subkeyword in entries:
                    entries[subkeyword][0].set(False)
#======================                
    def set_checkbox_color(self, checkbutton, color):
        checkbutton.config(fg=color) 
#==========================        
    def select_checkbox(self, subkeyword, shaps):
        sub_key=subkeyword.strip().strip("=").strip()
        if sub_key in shaps:
            for keyword, entries in self.k_list:
                if subkeyword in entries:
                    entries[subkeyword][0].set(True)
#==========================
# deselect all chekedbox
    def deselect_all_checkboxes(self):
        for keyword , entries in self.k_list:
            for var, _ , check in entries.values():
                var.set(False)      
                self.set_checkbox_color(check, 'black')
#==========================

    def remove_sample(self):
        if self.samples:
            frame, entries = self.samples.pop()
            if frame.winfo_exists():  # Check if the widget still exists
                frame.destroy()
                self.k_list.pop()
                self.indx -=1
##==========================
    #def load_input_values(self, file_path):
   
        #try:
            #with open(file_path, "r") as f:
                #self.deselect_all_checkboxes()  # Correctly call the method
                #lines = f.readlines()
                #Totkey=0
                #numkey=1
                #txtlog=""
                #stxtlog=""
                #index=0
                #lns =""
                
                #for line in lines:
                    #line = line.lstrip()
                    #str_line = line.strip()
                    #if ":" in line and not str_line.startswith('#'):
                        #keysubkey, value = re.split(r'\s|=', line, maxsplit=1)
                        #keysubkey=keysubkey.strip().strip("=").strip()
                        #skey = keysubkey.strip().split(":")[1]
                        
                        #if skey =="num-materials":
                            
                            #val =int(value.strip().strip("="))
                            #if val>1 and   val> int(self.indx):
                                #for i in range(val-1):
                                    #self.add_sample(self.sample_tab)
                            #break
                
                #for line in lines:
                    #line = line.lstrip()
                    #str_line = line.strip()
                    #if ":" in line and not str_line.startswith('#'):
                        #Totkey +=1
                        #keysubkey, value = re.split(r'\s|=', line, maxsplit=1)
                        #keysubkey=keysubkey.strip().strip("=").strip()
                        #skey = keysubkey.strip().split(":")[1]                            
                        #value = value.strip().strip("=")
                        #for keyword, entries in self.k_list:
                            
                            #for subkeyword, (var, entry, check) in entries.items():
                                #if keysubkey == f"{keyword}:{subkeyword.strip().strip('=').strip()}":
                                    #numkey +=1
                                    #var.set(True)
                                    #self.set_checkbox_color(check, 'blue')
                                    #if isinstance(entry, tk.Entry):
                                        #entry.delete(0, tk.END)
                                        #entry.insert(0, value)
                                    #if isinstance(entry, ttk.Combobox):                                       
                                        #if value in entry['values']:
                                            #entry.set(value)
                                            #entry.insert(0, value)
                                
                #self.inputfile = file_path
            
            #messagebox.showinfo("Success" ,f"File loaded successfully! \n Number of loaded keyword: {numkey} \n Number of Total keyword: {Totkey}\n")
                
        #except FileNotFoundError:
            #print(f"File {file_path} not found.")
        #except Exception as e:
            #print(f"An error occurred: {e}")   
    def load_input_values(self, file_path):
        skywd=[]
        for _, entries in self.k_list:
            for subkeyword, (var, entry, check) in entries.items():
                skywd.append(subkeyword.strip().strip("="))
        try:
            with open(file_path, "r") as f:
                self.deselect_all_checkboxes()  # Correctly call the method
                lines = f.readlines()
                Totkey=0
                numkey=0
                txtlog=""
                stxtlog=""
                for line in lines:
                    line = line.lstrip()
                    str_line = line.strip()
                    if ":" in line and not str_line.startswith('#'):
                        keysubkey, value = re.split(r'\s|=', line, maxsplit=1)
                        keysubkey=keysubkey.strip().strip("=").strip()
                        skey = keysubkey.strip().split(":")[1]
                        
                        if skey =="num-materials":
                            
                            val =int(value.strip().strip("="))
                            if val>1 and   val> int(self.indx):
                                for i in range(val-1):
                                    self.add_sample(self.sample_tab)
                            break
                
                for line in lines:
                    line = line.lstrip()
                    str_line = line.strip()
                    if ":" in line and not str_line.startswith('#'):
                        Totkey +=1
                        keysubkey, value = re.split(r'\s|=', line, maxsplit=1)
                        key = keysubkey.strip().split(":")[0]
                        key =key.split("[")[0]
                        sky = keysubkey.strip().split(":")[1]
                        sky =sky.strip().strip("=")
                        value = value.strip().strip("=").strip()
                        #print (value)
      
                        if key =="material":
                            if sky in skywd:
                                numkey +=1
                                subkey = keysubkey.strip().split(":")[1]
                                subkey = subkey.strip().strip("=")
                                if subkey =="alloy-host":
                                    subkey = "host-alloy"
                                value = value.strip().strip("=")
                                for keyword, entries in self.k_list:
                                    for subkeyword, (var, entry, check) in entries.items():
                                        if subkeyword.strip("=").strip() == subkey:
                                            var.set(True)
                                            self.set_checkbox_color(check, 'blue')
                                            if isinstance(entry, tk.Entry):
                                                entry.delete(0, tk.END)
                                                entry.insert(0, value)
                                            if isinstance(entry, ttk.Combobox):                                       
                                                if value in entry['values']:
                                                    entry.set(value)
                                                    entry.insert(0, value)
                            else:
                                stxtlog =  f" {stxtlog} \n {keysubkey}"
                        else:
                            txtlog =  f" {txtlog} \n {keysubkey}"
                if txtlog != "" or stxtlog != "":            
                    with open("keys_subkeys_errors.log", 'w') as flog:
                        flog.write("the list keywords  not found in List of VGUI\n")
                        flog.write("---------------------------------------------\n")
                        flog.write(f"{txtlog}")                
                self.inputfile = file_path
            if txtlog != "" or stxtlog != "":
                messagebox.showinfo("Echec !!",f"number of lines not loaded: {Totkey-numkey} \n Keyword error:\n{txtlog} \n Sub keyword error:\n  {stxtlog}"    )
            else:
                messagebox.showinfo("Success" ,f"File loaded successfully! \n Number of loaded keyword: {numkey} \n Number of Total keyword: {Totkey}\n")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")  
#============================================
    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select file", filetypes=[("input files", "*"), ("All files", "*.*")])
        if file_path:
            self.load_input_values(file_path)      
#=============================================    
    # Add other methods as needed"""
    def close_window(self):
        # Save the file before closing
        self.save_to_file()
        # Close the window
        # Add your code to close the window here
#==========================
    def save_to_file(self):
        filename = "sample.mat"
        with open(filename, 'w') as file:
            file.write("#===================================================\n")
            file.write("# Sample vampire material file .mat\n")
            file.write("#===================================================\n\n")
            file.write(f"material:num-materials={len(self.samples)}\n\n")
            for index, (frame, entries) in enumerate(self.samples, start=1):
                file.write(f"#---------------------------------------------------\n")
                file.write(f"# sample {index}\n")
                file.write(f"#---------------------------------------------------\n")
                for subkeys, (var, entry, _) in entries.items():
                    if subkeys.strip().strip("=") != "num-materials":
                        if var.get():
                            file.write(f"material[{index}]:{subkeys} {entry.get().strip()}\n")
                file.write("\n")
        messagebox.showinfo("Success", f"File '{filename}' saved successfully!")
#==========================
    def setup_main_input(self, tab):
            # Dictionary of default values
            self.default_values = {
            "num-materials=": "none",
            "material-name=": "Cobalt", 
            "damping-constant=": "1.0", 
            "exchange-matrix[1]=": "0.0 J/link",
            #"exchange-matrix[2]=": "0.0 J/link", 
            #"exchange-matrix[3]=": "0.0 J/link", 
            #"exchange-matrix-1st-nn[1]=": "0.0 J/link", 
            #"exchange-matrix-1st-nn[2]=": "0.0 J/link",
            #"exchange-matrix-2nd-nn[1]=": "0.0 J/link",
            #"exchange-matrix-2nd-nn[2]=": "0.0 J/link", 
            #"exchange-matrix-3rd-nn[1]=": "0.0 J/link",
            #"exchange-matrix-3rd-nn[2]=": "0.0 J/link", 
            #"exchange-matrix-4th-nn[1]=": "0.0 J/link",
            #"exchange-matrix-4th-nn[2]=": "0.0 J/link", 
            "biquadratic-exchange[1]=": "0.0 J/link", 
            #"biquadratic-exchange[2]=": "0.0 J/link",
            "atomic-spin-moment=": "1.72 !muB", 
            "surface-anisotropy-constant=": "0.0 J/atom", 
            "neel-anisotropy-constant[1]=": "0.0 J", 
            #"neel-anisotropy-constant[2]=": "0.0 J", 
            "lattice-anisotropy-constant=": "0.0 J/atom", 
            "relative-gamma=": "1",
            "initial-spin-direction=": "0, 0, 1",
            "material-element=": "Fe", 
             
            "alloy-fraction[1]=": "0.0",
            #"alloy-fraction[2]=": "0.0",  
            "minimum-height=": "0.0", 
            "maximum-height=": "1.0", 
            "core-shell-size=": "1.0", 
            "interface-roughness=": "1.0",
            "intermixing[1]=": "1.0",
            #"intermixing[2]=": "1.0", 
            "density=": "1.0",
            "unit-cell-category=": "0",
            "uniaxial-anisotropy-constant=": "0.0 J/atom",
            "uniaxial-anisotropy-direction=": "0,0,1",
            "cubic-anisotropy-constant=": "0.0 J/atom", 
            "second-order-uniaxial-anisotropy-constant=": "0.0  J/atom", 
            "fourth-order-uniaxial-anisotropy-constant=": "0.0  J/atom", 
            "sixth-order-uniaxial-anisotropy-constant" : "0.0 J/atom" ,
            "fourth-order-cubic-anisotropy-constant=" : "0.0 J/atom",
            "sixth-order-cubic-anisotropy-constant=" :  "0.0 J/atom",
            #"couple-to-phononic-temperature=": "off",
            "temperature-rescaling-exponent=": "1.0", 
            "temperature-rescaling-curie-temperature=": "0.0",
            
            "non-magnetic=": "remove",
            "host-alloy=": "none",
            "continuous ": "none",
            "fill-space=": "none",
            "geometry-file=": " ", 
            "lattice-anisotropy-file=": " ",
            "alloy-distribution" : " ",
            "alloy-variance" : "0.0",
            #"voltage-controlled-magnetic-anisotropy-coefficient=": "0.0 J/V"
        }

#def main():
    #root = tk.Tk()
    #app = MainInputTab (root)
    #root.mainloop()

#if __name__ == "__main__":
    #main()
    
  
