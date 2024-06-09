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
# Vampire input:  kyeword:subkeyword = value

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from vampgui.file_io import   InputFileViewer
from vampgui.helpkey import  show_help
from tkinter import scrolledtext, messagebox
from tkinter import filedialog
import re
import os

class InputTab:
    def __init__(self, tab):


# keywords list & tab header 
# the changement of the order of keyword will change the order of the subtab 
        headers={"create" :"Creation",
                "material" : "Material attributes",
                "dimensions" :"Dimensions System",
                "sim" : "Simulation",
                "montecarlo" :"Montecarlo",
                "exchange" : "Exchange cal.",
                "anisotropy"  :"Anisotropy cal.",
                "dipole" :"Dipole field cal.",
                "hamr" :"HAMR cal.",
                "output" : "Output" , 
                "config"  : "Configuration", 
                "screen" :"Screen" ,
                "cells" : "Cells",
                }
        
        self.headerkeywrds = list(headers.values())
        self.tabkeywords = list(headers.keys())
     

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
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=8)
# Buttons   
        tk.Button(button_frame, bg='bisque', text="Import from input", command=self.load_file).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, bg='#99ff99', text="Save in input", command=self.save_to_file).grid(row=0,          column=2, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, bg='#ffff99', text="View/Edit input", command=self.open_input_file).grid(row=0,           column=3, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, bg='#ff9999', text="Deselect All", command=self.deselect_all_checkboxes).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
# Create a notebook for sub-tabs
        sub_notebook = ttk.Notebook(frame )
        sub_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=8)        
# sub keyword list        
        self.last_selected = tk.StringVar(value="cube")
        self.SubKyewords_list()
        self.k_list = []
        self.load_input_values
        
# create subtab for each list     
        for keyword, header in zip(self.tabkeywords , self.headerkeywrds):
# set default values                
            self.full_subkeywords = list(getattr(self, f"{keyword}_default_values").keys())
            
            #if keyword in [self.tabkeywords[0], self.tabkeywords[1]]:
                ## include 2 lists in same subtab
                #if keyword == self.tabkeywords[0]:
                    #self.create_tab = ttk.Frame(sub_notebook)
                    #sub_notebook.add(self.create_tab, text=f"{header.capitalize()} ")
                    
                    #self.create_list = []
                    #self.add_create_command(self.create_tab, keyword)
                #elif keyword == self.tabkeywords[1]:
                    #self.create_list = []
                    #self.add_create_command(self.create_tab, keyword)
                    
            #elif keyword in [self.tabkeywords[3], self.tabkeywords[4]]:
                
                #if keyword == self.tabkeywords[3]:
                    #self.create_tab = ttk.Frame(sub_notebook)
                    #sub_notebook.add(self.create_tab, text=f"{header.capitalize()} ")
                    
                    #self.create_list = []
                    #self.add_create_command(self.create_tab, keyword)
                #elif keyword == self.tabkeywords[4]:
                    #self.create_list = []
                    #self.add_create_command(self.create_tab, keyword)
            #elif keyword in [self.tabkeywords[6], self.tabkeywords[7], self.tabkeywords[8]]:
                
                #if keyword == self.tabkeywords[6]:
                    #self.create_tab = ttk.Frame(sub_notebook)
                    #sub_notebook.add(self.create_tab, text=f"{header.capitalize()} ")
                    
                    #self.create_list = []
                    #self.add_create_command(self.create_tab, keyword)
                #elif keyword == self.tabkeywords[7]:
                    #self.create_list = []
                    #self.add_create_command(self.create_tab, keyword)
                #elif keyword == self.tabkeywords[8]:
                    #self.create_list = []
                    #self.add_create_command(self.create_tab, keyword)    
            #else:
                
            self.create_tab = ttk.Frame(sub_notebook)
            sub_notebook.add(self.create_tab, text=f"{header.capitalize()} ")
                
            self.create_list = []
            self.add_create_command(self.create_tab, keyword)

#==========================================            
    def add_create_command(self, tab, keyword):

   
        if keyword == "sim":
            frame = tk.LabelFrame(tab, text=" Simulation attributes & config.:  ", font=("Helvetica", 18, "bold") )
        else:
            frame = tk.LabelFrame(tab, text=f"{keyword.capitalize()} attributes & config: ", font=("Helvetica", 18, "bold") )
        frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True , padx=8, pady=(8, 8))
        
        entries = {}
        row = 0
        col = 0
        max_row = 20    # Set the maximum number of  rows for each list
         
           
        # for subkeys select value
        stringFlag = ["false", "true"]
        crystal = ["sc", "fcc", "bcc", "hcp", "heusler", "kagome", "rocksalt", "spinel"]
        bools = ["enable-bulk-neel-anisotropy","column-headers","voronoi-rounded-grains", "voronoi-row-offset", "crystal-sublattice-materials","select-material-by-height" , "select-material-by-geometry", "fill-core-shell-particles", "material-interfacial-roughness", "interfacial-roughness" ]
        shaps = ["non","full", "cube", "cylinder", "ellipsoid", "sphere", "truncated-octahedron", "particle", "particle-array", "voronoi-film", "particle-centre-offset"]
        algo= ["adaptive", "spin-flip","uniform","angle","hinzke-nowak"]
        prgsim= ["benchmark", "time-series","hysteresis-loop","static-hysteresis-loop","curie-temperature","field-cool","localised-field-cool","laser-pulse", "hamr-simulation","cmc-anisotropy","hybrid-cmc","reverse-hybrid-cmc",
                 "LaGrange-Multiplier", "partial-hysteresis-loop","localised-temperature-pulse","effective-damping","fmr","diagnostic-boltzmann","setting"]
        intgr= ["llg-heun" , "monte-carlollg-midpoint", "constrained-monte-carlo", "hybrid-constrained-monte-carlo" , "monte-carlo"]
        lpulse =["square", "two-temperature", "double-pulse-two-temperature", "double-pulse-square"]
        cool_fun =["exponential","gaussian","double-gaussian","linear","cooling-function" ]
        mpi_mode=["geometric-decomposition","replicated-data" ,"replicated-data-staged"]
       
        Padx = 2
        Wdth = 15    # with of input box 
        if keyword == "material":
            Wdth = 35   
            max_row = 4
        if keyword == "sim":
            Wdth = 15
           
            
        # subkeys here is subkeywords
        for idx, subkeys in enumerate(self.full_subkeywords):
            
            ncol=3*col
            var =  tk.BooleanVar()   
#check boxes ------------
            check = tk.Checkbutton(frame, text=subkeys, variable=var, font=13)
            check.config(command=lambda skw=subkeys, v=var, chk=check: self.update_last_selected(skw, v, shaps, chk))
            check.grid(row=row, column=ncol+1, sticky="w")
             
            loaded_value = getattr(self, f"{keyword}_default_values")[subkeys]
            subkeyword = subkeys.strip().strip("=").strip()
#---create ----------------
            if subkeyword == "crystal-structure":
                entry = ttk.Combobox(frame, values=crystal, state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx  , sticky="e")
                if loaded_value.lower() in crystal:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("sc")
                    entry.insert(0, "sc")
                entries[subkeys] = (var, entry, check)
                
            if subkeyword == "interfacial-roughness-type":
                entry = ttk.Combobox(frame, values=["peaks", "troughs"], state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx  , sticky="e")
                if loaded_value.lower() in ["peaks", "troughs"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("peaks")
                    entry.insert(0, "peaks")
                entries[subkeys] = (var, entry, check)   
                
#--sim-----------------------------
            elif subkeyword == "program":
                entry = ttk.Combobox(frame, values=prgsim, state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in prgsim:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("benchmark")
                    entry.insert(0, "benchmark")
                entries[subkeys] = (var, entry, check)
            elif subkeyword == "integrator":
                entry = ttk.Combobox(frame, values=intgr, state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in intgr:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("llg-heun")
                    entry.insert(0, "llg-heun")
                entries[subkeys] = (var, entry, check)  
            elif subkeyword == "laser-pulse-temporal-profile":
                entry = ttk.Combobox(frame, values=lpulse, state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in lpulse:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("")
                    entry.insert(0, "")
                entries[subkeys] = (var, entry, check) 
            elif subkeyword == "cooling-function":
                entry = ttk.Combobox(frame, values=cool_fun, state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in cool_fun:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("exponential")
                    entry.insert(0, "exponential")
                entries[subkeys] = (var, entry, check) 
             
            elif subkeyword == "save-checkpoint":
                entry = ttk.Combobox(frame, values=["end","continuous"], state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in ["end","continuous"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("")
                    entry.insert(0, "")
                entries[subkeys] = (var, entry, check)    
            elif subkeyword == "load-checkpoint":
                entry = ttk.Combobox(frame, values=["restart","continue"], state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in ["restart","continue"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("")
                    entry.insert(0, "")
                entries[subkeys] = (var, entry, check)    
                
# config ----------------------------------
            elif subkeyword == "atoms" or subkeyword == "macro-cells":
                entry = ttk.Combobox(frame, values=["", "end" , "continuous"] , state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in ["", "end" , "continuous"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("")
                    entry.insert(0, "")
                entries[subkeys] = (var, entry, check)  
                
            elif subkeyword == "output-format":
                entry = ttk.Combobox(frame, values=["text", "binary"] , state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in ["text", "binary"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("text")
                    entry.insert(0, "text")
                entries[subkeys] = (var, entry, check) 
                
            elif subkeyword == "output-mode":
                entry = ttk.Combobox(frame, values=["file-per-node", "legacy","mpi-io", "file-per-process"] , state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in ["file-per-node", "legacy","mpi-io", "file-per-process"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("file-per-node")
                    entry.insert(0, "file-per-node")
                entries[subkeys] = (var, entry, check)    
                
# dipole    
            elif subkeyword == "solver":
                entry = ttk.Combobox(frame, values=["macrocell","tensor","atomistic"] , state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in ["macrocell","tensor","atomistic"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("macrocell")
                    entry.insert(0, "macrocell")
                entries[subkeys] = (var, entry, check) 
#exchange
            elif subkeyword == "function":
                entry = ttk.Combobox(frame, values=["nearest-neighbour","exponential"] , state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in ["nearest-neighbour","exponential"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("")
                    entry.insert(0, "")
                entries[subkeys] = (var, entry, check) 
# montecarlo
            elif subkeyword == "algorithm":
                entry = ttk.Combobox(frame, values=algo , state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in algo:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value)
                else:
                    entry.set("adaptive")
                    entry.insert(0, "adaptive")
                entries[subkeys] = (var, entry, check) 
                
                
#--True\false--------------------------------------            
            elif subkeyword in bools:
                entry = ttk.Combobox(frame, values=["false", "true"], state="readonly", width=Wdth)
                entry.grid(row=row, column=ncol+2, padx=Padx , sticky="w")
                if loaded_value.lower() in ["false", "true"]:
                    entry.set(loaded_value.lower())
                    entry.insert(0, loaded_value.lower())
                else:
                    entry.set("false")
                    entry.insert(0, "false")
                entries[subkeys] = (var, entry, check)
# subkey without value ------------
            elif loaded_value == "none":
                entry = tk.Entry(frame, width=Wdth, state='disabled')
                entry.grid(row=row, column=ncol+2,  padx=Padx , sticky="w")
                entry.insert(0, loaded_value)
                entries[subkeys] = (var, entry, check)
# for the others -----------------------
            else:
                entry = tk.Entry(frame, bg='white', width=Wdth)
                entry.grid(row=row, column=ncol+2,  padx=Padx , sticky="w")
                entry.insert(0, loaded_value)
                entries[subkeys] = (var, entry, check)
# help buttons ----------            
            help_button = tk.Button(frame, text="?", command=lambda skw=subkeys: show_help(skw))
            help_button.grid(row=row, column=ncol+3, sticky="w")

# rows and columns----------
            row += 1
            if (idx + 1) % max_row == 0:
                row = 0
                col += 1
            
        self.k_list.append((keyword, entries))
        self.create_list.append((frame, entries))

#============================================
    def update_last_selected(self, subkeyword, var,shaps, check):
        if var.get():
            self.set_checkbox_color(check, 'blue')
            sub_key=subkeyword.strip().strip("=").strip() 
            if self.last_selected.get():
                if sub_key in shaps:
                    self.set_checkbox_color(check, "green")
                    self.deselect_checkbox(self.last_selected.get(), shaps)
        else:
            self.set_checkbox_color(check, 'black')
        self.last_selected.set(subkeyword) 
        
#=======================================================
    def deselect_checkbox(self, subkeyword, shaps):
        sub_key=subkeyword.strip().strip("=").strip()
        if sub_key in shaps:
            for keyword, entries in self.k_list:
                if subkeyword in entries:
                    entries[subkeyword][0].set(False)
 #======================                
    def set_checkbox_color(self, checkbutton, color):
        checkbutton.config(fg=color) 
 #=======================================================         
    def select_checkbox(self, subkeyword, shaps):
        sub_key=subkeyword.strip().strip("=").strip()
        if sub_key in shaps:
            for keyword, entries in self.k_list:
                if subkeyword in entries:
                    entries[subkeyword][0].set(True)
 #---------------------------------------------
# deselect all chekedbox
    def deselect_all_checkboxes(self):
        for keyword , entries in self.k_list:
            for var, _ , check in entries.values():
                var.set(False)      
                self.set_checkbox_color(check, 'black')
##========================================================
    #def load_default_values(self, keyword, inputfile):
        #try:
            #with open(inputfile, "r") as file:
                #lines = file.readlines()
                #for line in lines:
                    #line.lstrip()
                    #if f"{keyword}:" in line:
                        #key, value = re.split(r'\s|=', line, maxsplit=1)
                        #key = key.strip().split(":")[1]
                        #value = value.strip()
                        #value = value.strip("=")
                        
                        #default_values = getattr(self, f"{keyword}_default_values")
                        #if key in default_values:
                            #getattr(self, f"{keyword}_default_values")[key] = value 
                        #keypls=f"{key}="
                        #if keypls in default_values:
                            #getattr(self, f"{keyword}_default_values")[keypls] = value 
        #except FileNotFoundError:
            #pass         
 ##=============================================================
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
                        Totkey +=1
                        keysubkey, value = re.split(r'\s|=', line, maxsplit=1)
                        key = keysubkey.strip().split(":")[0]
                        sky = keysubkey.strip().split(":")[1]
                        sky =sky.strip().strip("=")
                        value = value.strip().strip("=").strip()
                        #print (value)
      
                        if key in self.tabkeywords:
                            if sky in skywd:
                                numkey +=1
                                subkey = keysubkey.strip().split(":")[1]
                                subkey = subkey.strip().strip("=")
                                value = value.strip().strip("=")
                                if key=="output" and subkey=="applied-field-strength":
                                    subkey="applied-field-strengths"
                                if key=="output" and subkey=="applied-field-unit-vector":
                                    subkey="applied-field-unit-vectors"   
                                if key=="cells" and subkey == "macro-cell-size":
                                    subkey="macro-cell-sizes"
                                if key=="screen" and subkey == "magnetisation-length":
                                    subkey="magnetisation-lengths"
                                if key=="screen" and subkey == "mean-magnetisation-length":
                                    subkey="mean-magnetisation-lengths"
                                if key=="screen" and subkey == "temperature":
                                    subkey="temperatures"
                                if key=="output" and  subkey == "temperature":
                                    subkey="temperature."                        
                                if key=="screen" and subkey == "time-steps":
                                   subkey="time-steps."   
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
    def open_input_file(self):
        InputFileViewer("input_v")
#=============================================                  
    def save_to_file(self):
        filename = "input_v"
        with open(filename, 'w') as file:
            file.write("#------------------------------------------\n")
            file.write("# Sample vampire input file to perform\n")
            file.write("#------------------------------------------\n\n")
            tstkeyword="init"
            for index, (keyword, entries) in enumerate(self.k_list, start=1):
                 
                for subkeyword, (var, entry,_) in entries.items():
                    subk=subkeyword
                    if var.get():
                        if keyword != tstkeyword :
                            if keyword == "sim":
                                file.write("#------------------------------------------\n")
                                file.write(f"#   {keyword.capitalize()}ulation ;; attributes & config \n")
                                file.write("#------------------------------------------\n\n")
                            else:
                                file.write("#------------------------------------------\n")
                                file.write(f"#   {keyword.capitalize()} ;; \n")
                                file.write("#------------------------------------------\n\n")
                        if entry:
                            entry_value = entry.get().strip()
                            if entry_value == "none":
                                if subk == "applied-field-strengths ":
                                    subk="applied-field-strength "
                                if subk == "applied-field-unit-vectors=":
                                    subk="applied-field-unit-vector="
                                if subk == "macro-cell-sizes=":
                                    subk="macro-cell-size="
                                if subk == "magnetisation-lengths ":
                                    subk="magnetisation-length "
                                if subk == "material-magnetisations ":
                                    subk="material-magnetisation " 
                                if subk == "mean-magnetisation-lengths ":
                                    subk="mean-magnetisation-length " 
                                if subk == "temperatures ":
                                    subk="temperature "
                                if  subk == "temperature. ":
                                    subk="temperature "
                                if subk == "time-steps. ":
                                    subk="time-steps "  
                                file.write(f"{keyword}:{subk} \n")
                            else:
                                if subk == "applied-field-strengths ":
                                    subk="applied-field-strength "
                                if subk == "applied-field-unit-vectors=":
                                    subk="applied-field-unit-vector="
                                if subk == "macro-cell-sizes=":
                                    subk="macro-cell-size="
                                if subk == "magnetisation-lengths ":
                                    subk="magnetisation-length "
                                if subk == "material-magnetisations ":
                                    subk="material-magnetisation " 
                                if subk == "mean-magnetisation-lengths ":
                                    subk="mean-magnetisation-length " 
                                if subk == "temperatures ":
                                    subk="temperature "
                                if  subk == "temperature. ":
                                    subk="temperature "
                                if subk == "time-steps. ":
                                    subk="time-steps "  
                                file.write(f"{keyword}:{subk}{entry_value} \n")
                        tstkeyword=keyword
            file.write("\n")
            messagebox.showinfo("Success", f"File '{filename}' saved successfully!")
                
#===================================================================================================================================           
         
    def SubKyewords_list(self):
        self.create_default_values = {
                    "crystal-structure=": "sc",
                    "periodic-boundaries-x ": "none",
                    "periodic-boundaries-y ": "none",
                    "periodic-boundaries-z ": "none",
                    #
                    "full ": "none",
                    "cube ": "none",
                    "cylinder ": "none",
                    "ellipsoid ": "none",
                    "sphere ": "none",
                    "truncated-octahedron ": "none",
                    "tear-drop" : "none" ,
                    "particle ": "none",
                    "particle-array ": "none",
                    "hexagonal-particle-array" : "none",
                    "voronoi-film ": "none",
                    #
                    
                    "particle-centre-offset ": "none",
                    "single-spin ": "none",
                    "select-material-by-height=": "true",
                    "select-material-by-geometry=": "true",
                    "fill-core-shell-particles=": "true",
                    "interfacial-roughness=": "true",
                    "material-interfacial-roughness=": "true",
                    "interfacial-roughness-random-seed=": "2e6",
                    "interfacial-roughness-number-of-seed-points=": "0",
                    "interfacial-roughness-type=": "peaks",
                    "interfacial-roughness-seed-radius=": "0.0 !nm",
                    "interfacial-roughness-seed-radius-variance=": "0.0",
                    "interfacial-roughness-mean-height=": "0.0",
                    "interfacial-roughness-maximum-height=": "0.01 !nm",
                    "interfacial-roughness-height-field-resolution=": "0.01 !nm",
                    #
                    "voronoi-grain-substructure" : "none",
                    "voronoi-size-variance=": "0.01",
                    "voronoi-random-seed=": "10",  
                    "voronoi-rounded-grains-area=": "0.9", 
                    "voronoi-row-offset ": "none",
                    "voronoi-rounded-grains ": "none",
                    "single-spin" : "none",
                    #"crystal-sublattice-materials=": "false3",
                    "alloy-random-seed=": "683614233",
                    "grain-random-seed=": "1527349271",
                    "dilution-random-seed=": "465865253",
                    "intermixing-random-seed=": "100181363",
                    "spin-initialisation-random-seed=": "123456"
                    }
   
        
    
    
        self.dimensions_default_values = {
                    "unit-cell-size=": "3.54  !nm", 
                    "unit-cell-size-x=": "0.01 !nm ",
                    "unit-cell-size-y=": "0.01 !nm",
                    "unit-cell-size-z=": "0.01 !nm",
                    "system-size=": "0.01 !nm",
                    "system-size-x=": "0.01 !nm ",
                    "system-size-y=": "0.01 !nm ",
                    "system-size-z=": "0.01 !nm ",
                    "particle-size=": "0.01 !nm ",
                    "particle-spacing=": "0.01 !nm ",
                    "particle-shape-factor-x=": "1.0",
                    "particle-shape-factor-y=": "1.0",
                    "particle-shape-factor-z=": "1.0",
                    "particle-array-offset-x=": "0.1 !mm", 
                    "particle-array-offset-y=": "0.1 !nm ",
                    "macro-cell-size=": " "
                    }
         
                
        self.material_default_values = {
                    "file=": "sample.mat",
                    "unit-cell-file=": "sample_unit_cell.ucf"
                    }
        self.sim_default_values = {
                    "integrator="  :  "llg-heun", 
                    "program="  :  "", 
                    "enable-dipole-fields=" : " ", 
                    "enable-fmr-field ": "none",
                    "enable-fast-dipole-fields="  :  "false", 
                    "dipole-field-update-rate="  :  "1000", 
                    "time-step=" : "0.01 !ps", 
                    "total-time-steps=":"0", 
                    "loop-time-steps=": "0", 
                    "time-steps-increment=" : "1",
                    "equilibration-time-steps=" : "0", 
                    "simulation-cycles=" : "100",
                    "temperature=" : "0",
                    "minimum-temperature=" : "0", 
                    "maximum-temperature=" : "1000", 
                    "temperature-increment=" : "25",
                    "equilibration-temperature=" : " ",
                    "cooling-time=": "1 !ns ",
                    "laser-pulse-temporal-profile=" : " ",
                    "laser-pulse-time=" : " ",
                    "laser-pulse-power=" : " ",
                    "second-laser-pulse-time=": " ",
                    "second-laser-pulse-power=": " ",
                    "second-laser-pulse-maximum-temperature=": "0",
                    "second-laser-pulse-delay-time=": " ",
                    "two-temperature-heat-sink-coupling=": " ",
                    "two-temperature-electron-heat-capacity=" : " ",
                    "two-temperature-phonon-heat-capacity=" : " ",
                    "two-temperature-electron-phonon-coupling=" : " ",
                    "cooling-function=" : " ",
                    "applied-field-strength=" : " ",
                    "maximum-applied-field-strength=": " ", 
                    "equilibration-applied-field-strength=" : " ",
                    "applied-field-strength-increment=" : " ",
                    "applied-field-angle-theta=": " ",
                    "applied-field-angle-phi=": " ",
                    "applied-field-unit-vector=": " ",
                    "demagnetisation-factor="  :  "000", 
                    "integrator-random-seed="  :  "12345", 
                    "constraint-rotation-update=": "0",
                    "constraint-angle-theta="  :  "0", 
                    "constraint-angle-theta-minimum=": "0", 
                    "constraint-angle-theta-maximum=": " ", 
                    "constraint-angle-theta-increment="  :  "5", 
                    "constraint-angle-phi-minimum=" : " ",
                    "constraint-angle-phi-maximum=" : " ",
                    "constraint-angle-phi-increment=" : " ",
                    "checkpoint=" : "false" ,
                    "save-checkpoint=" : "continuous",
                    "save-checkpoint-rate=" : "1",
                    "load-checkpoint=" : "continue",
                    "load-checkpoint-if-exists " : "none",
                    "preconditioning-steps="  :  "0", 
                    "electrical-pulse-time="  :  "1.0 !ns", 
                    "electrical-pulse-rise-time="  :  "0.0 !ns", 
                    "electrical-pulse-fall-time="  :  "0.0 !ns", 
                    "mpi-mode=" : " ",
                    "mpi-ppn=" : "1",
                        }
        self.montecarlo_default_values = {
                    "algorithm " : "",
                    "constrain-by-grain " : "none"
                        }
        self.exchange_default_values = {
                    "interaction-range="  : "100",
                    "function=" : " " ,
                    "decay-multiplier " : "",
                    "decay-length=" : "1",
                    "decay-shift " : "",
                    "ucc-exchange-parameters[i][j]=" : "",
                    "dmi-cutoff-range=" : "",
                    "ab-initio=" : "",
                    "four-spin-cutoff-1=" : "1.0",
                    "four-spin-cutoff-2=" :  "1.4"
                        }
        self.anisotropy_default_values = {
                    "surface-anisotropy-threshold= " : "0",
                    "surface-anisotropy-nearest-neighbour-range=" : "0.0",
                    "enable-bulk-neel-anisotropy" : "false" ,
                    "neel-anisotropy-exponential-range=" :"2.5" ,
                    "neel-anisotropy-exponential-factor=" : "5.52"
                    }
        self.dipole_default_values = {
                    "solver=" : "   ",
                    "field-update-rate=" : "1000",
                    "cutoff-radius=" : "2" ,
                    "output-atomistic-dipole-field " : "none"
                        }
        self.hamr_default_values = {
                    "laser-FWHM-x="  :  "20.0 !nm",
                    "laser-FWHM-y="  :  "20.0 !nm", 
                    "head-speed="  :  "30.0 !m/s", 
                    "head-field-x="  :  " 20.0 !nm", 
                    "head-field-y="  :  " 20.0 !nm", 
                    "field-rise-time="  :  " 1 !ps", 
                    "field-fall-time="  :  " 1 !ps", 
                    "NPS="  :  " 0.0 !nm", 
                    "bit-size="  :  " 0.0 !nm",
                    "track-size="  :  " 0.0 !nm", 
                    "track-padding="  :  " 0.0 !nm", 
                    "number-of-bits="  :  " 0", 
                    "bit-sequence-type="  :  "  ", 
                    "bit-sequence="  :  " " 
                        }
        self.output_default_values = {
                    "column-headers=" : "true",
                    "time-steps " : "none",
                    "real-time " : "none",
                    "temperature. " : "none",
                    "applied-field-strengths " : "none",
                    "applied-field-unit-vectors " : "none",
                    "applied-field-alignment " : "none",
                    "material-applied-field-alignment " : "none",
                    "magnetisation " : "none",
                    "magnetisation-length ": " ",
                    "mean-magnetisation-length " : "none",
                    "mean-magnetisation " : "none",
                    "material-magnetisation " : "none",
                    "material-mean-magnetisation-length " : "none",
                    "material-mean-magnetisation " : "none",
                    "total-torque " : "none",
                    "mean-total-torque " : "none",
                    "constraint-phi " : "none",
                    "constraint-theta " : "none",
                    "material-mean-torque " : "none",
                    "mean-susceptibility " : "none",
                    "material-mean-susceptibility " : "none",
                    "material-standard-deviation " : "none",
                    "electron-temperature " : "none",
                    "phonon-temperature " : "none",
                    "total-energy " : "none",
                    "mean-total-energy " : "none",
                    "anisotropy-energy " : "none",
                    "mean-anisotropy-energy " : "none",
                    "exchange-energy " : "none",
                    "mean-exchange-energy " : "none",
                    "applied-field-energy " : "none",
                    "mean-applied-field-energy " : "none",
                    "magnetostatic-energy " : "none",
                    "mean-magnetostatic-energy " : "none",
                    "material-total-energy " : "none",
                    "material-mean-total-energy " : "none",
                    "mean-specific-heat " : "none",
                    "material-mean-specific-heat " : "none",
                    "fractional-electric-field-strength " : "none",
                    "mpi-timings " : "none",
                    "gnuplot-array-format " : "none",
                    "output-rate=": "1",
                    "precision=" : "6",
                    "fixed-width " : "none"
                        }       
        self.config_default_values = {
                    "atoms=" : " ",
                    "macro-cells=" : " ",
                    "output-format="  : "text", 
                    "output-mode=" : "file-per-node",
                    "output-nodes=" : "1" ,
                    "atoms-output-rate=" : "1000",
                    "atoms-minimum-x=" : "0.0",
                    "atoms-minimum-y=" : "0.0",
                    "atoms-minimum-z=" : "0.0",
                    "atoms-maximum-x=" : "0.0",
                    "atoms-maximum-y=" : "0.0",
                    "atoms-maximum-z=" : "0.0",
                    "macro-cells-output-rate " : "0",
                    "identify-surface-atoms " : "none",
                    "field-range-descending-minimum": " 0.0 T",
                    "field-range-descending-maximum": " 0.0 T",
                    "field-range-ascending-minimum": " 0.0 T",
                    "field-range-ascending-maximum": " 0.0 T",
                        }
        self.screen_default_values = {
                    "time-steps. " :"none",
                    "temperatures ": "none",
                    "magnetisation-lengths ":"none",
                    "mean-magnetisation-lengths ": "none",
                    "material-magnetisations " : "none"
                        }
        self.cells_default_values = {
                    "macro-cell-sizes=" :"2 !nm",
                        }
#===================================================================================================================================

 
