import tkinter as tk
from tkinter import ttk, messagebox
from vampgui.file_io import InputFileViewer 

class ufcFile:
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
        tk.Button(button_frame, bg='cyan', text="Generate UCF File", command=self.generate_ucf_file).grid(row=0, column=0, padx=5, pady=5,sticky="w")
        tk.Button(button_frame, bg='#ffff99', text="View/Edit sample.ucf", command=self.open_sample_file).grid(row=0, column=3,padx=5, pady=5,sticky="w")

       
        #Generate button
        #self.generate_button = tk.Button(frame, text="Generate UCF File", command=self.generate_ucf_file)
        #self.generate_button.grid(row=0, column=0, columnspan=4)
         
        self.mode = tk.LabelFrame(frame, text="Crystal system: ", font=("Helvetica", 14, "bold"))
        self.mode.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(8, 8))
        # Filename
        self.filename_label = tk.Label(self.mode, text="Enter ucf filename [example: template.ucf]")
        self.filename_label.grid(row=0, column=0, sticky='w', pady=5)
        self.filename_entry = tk.Entry(self.mode, width=30,bg='white')
        self.filename_entry.grid(row=0, column=1, columnspan=8, sticky='w', pady=5)

        # Crystal system
        self.crystal_system_label = tk.Label(self.mode, text="Select crystal system")
        self.crystal_system_label.grid(row=1, column=0, sticky='w' , pady=5)
        self.crystal_system_var = tk.StringVar()
        self.crystal_system_options = ["cubic", "tetragonal", "orthorhombic", "hexagonal", "monoclinic", "rhombohedral", "triclinic"]
        self.crystal_system_var.set(self.crystal_system_options[0])
        self.crystal_system_menu = tk.OptionMenu(self.mode, self.crystal_system_var, *self.crystal_system_options, command=self.lock_unlock_lattice_entries)
        self.crystal_system_menu.grid(row=1, column=1, columnspan=8,  sticky='w' , pady=5)

        # Lattice constants
                
        self.lattice_label = tk.Label(self.mode, text="Enter lattice constants:")
        self.lattice_label.grid(row=2, column=1, sticky='w' , pady=5)
        self.lattice_entries = []
        for i, label in enumerate(['a', 'b', 'c']):
            lbl = tk.Label(self.mode ,text=f"{label}:")
            lbl.grid(row=2, column=3*i + 2, sticky='e' , pady=5)
            entry = tk.Entry(self.mode , width=10, bg='white')
            entry.grid(row=2, column=3*i+3, sticky='w' , pady=5)
            self.lattice_entries.append(entry)

        # Vectors
        self.vector_labels = ['x', 'y', 'z']
        self.vector_entries = []
        for vec_num in range(3):
            lbl = tk.Label(self.mode, text=f"Enter vector {vec_num + 1}:")
            lbl.grid(row=3 + vec_num, column=1, sticky='w' , pady=5)
            for i, label in enumerate(self.vector_labels):
                lbl = tk.Label(self.mode ,text=f"{label}:")
                lbl.grid(row=3+ vec_num, column=3*i + 2, sticky='e' , pady=5)
                entry = tk.Entry(self.mode , width=10, bg='white')
                entry.grid(row=3 + vec_num, column=3*i + 3, sticky='w' , pady=5)
                self.vector_entries.append(entry)



        # Number of interactions
        self.number_of_interactions_label = tk.Label(self.mode, text="Enter number of interactions")
        self.number_of_interactions_label.grid(row=7, column=0, sticky='w' , pady=5)
        self.number_of_interactions_entry = tk.Entry(self.mode , width=10, bg='white')
        self.number_of_interactions_entry.grid(row=7, column=1, sticky='w' , pady=5)

        # Exchange type
        self.exchange_type_label = tk.Label(self.mode, text="Enter exchange type")
        self.exchange_type_label.grid(row=8, column=0, sticky='w' , pady=5)
        self.exchange_type_entry = tk.Entry(self.mode , width=10, bg='white')
        self.exchange_type_entry.grid(row=8, column=1, sticky='w' , pady=5)

        # Number of atoms
        self.number_of_atoms_label = tk.Label(self.mode, text="Enter number of atoms")
        self.number_of_atoms_label.grid(row=9, column=0, sticky='w' , pady=5)
        self.number_of_atoms_entry = tk.Entry(self.mode , width=10, bg='white')
        self.number_of_atoms_entry.grid(row=9, column=1, sticky='w' , pady=5)
        
        self.add_atom_parameters_button = tk.Button(self.mode, text="Add Atom Parameters", command=self.add_atom_parameters)
        self.add_atom_parameters_button.grid(row=9, column=2, columnspan=2, sticky='w' , pady=5)
        
        self.mode_p = tk.LabelFrame(frame, text="# Atom parameters: ", font=("Helvetica", 14, "bold"))
        self.mode_p.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(8, 8))
        # Atom parameters
        
        
        
        self.atom_parameters_frame = tk.Frame(self.mode_p)
        self.atom_parameters_frame.grid(row=1, column=0, columnspan=4, sticky='w' , pady=5)
        self.atom_parameters_entries = []
        # Initial lock/unlock of lattice entries
        self.lock_unlock_lattice_entries()

        self.mode_text = tk.LabelFrame(frame, text="## Manually add interaction parameters here: ", font=("Helvetica", 14, "bold"))
        self.mode_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(8, 8))

        self.text_output = tk.Text(self.mode_text, height=40, width=140, wrap='none', bg="white")
        self.text_output.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        ## Ensure the columns expand properly
        #self.mode_text.grid_columnconfigure(0, weight=1)
        #self.mode_text.grid_columnconfigure(1, weight=1)
        #self.mode_text.grid_columnconfigure(2, weight=1)
        #self.mode_text.grid_columnconfigure(3, weight=1)
        #self.mode_text.grid_rowconfigure(4, weight=1)






    def open_sample_file(self):
        InputFileViewer(self.filename_entry.get())

    def lock_unlock_lattice_entries(self, *args):
        crystal_system = self.crystal_system_var.get()

        for entry in self.lattice_entries:
            entry.config(state=tk.NORMAL)

        if crystal_system in ["cubic", "rhombohedral"]:
            self.lattice_entries[1].config(state=tk.DISABLED)
            self.lattice_entries[2].config(state=tk.DISABLED)
        elif crystal_system in ["hexagonal", "tetragonal"]:
            self.lattice_entries[1].config(state=tk.DISABLED)
            self.lattice_entries[2].config(state=tk.NORMAL)
        elif crystal_system in ["orthorhombic", "monoclinic", "triclinic"]:
            for entry in self.lattice_entries:
                entry.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Crystal system does not exist")

    def add_atom_parameters(self):
        for widget in self.atom_parameters_frame.winfo_children():
            widget.destroy()

        num_atoms = int(self.number_of_atoms_entry.get())
        self.atom_parameters_entries = []
        for atom_index in range(num_atoms):
            lbl = tk.Label(self.atom_parameters_frame, text=f"Atom {atom_index + 1}")
            lbl.grid(row=atom_index, column=0, sticky='w' , pady=5)
            row_entries = []
            for param_index, param_label in enumerate(['id', 'cx', 'cy', 'cz', 'mat', 'lc', 'hc']):
                lbl = tk.Label(self.atom_parameters_frame, text=f"{param_label}:")
                lbl.grid(row=atom_index, column=param_index * 2 + 1, sticky='w' , pady=5)
                entry = tk.Entry(self.atom_parameters_frame, width=10, bg='white')
                entry.grid(row=atom_index, column=param_index * 2 + 2, sticky='w' , pady=5)
                row_entries.append(entry)
            self.atom_parameters_entries.append(row_entries)

    def generate_ucf_file(self):
        filename = self.filename_entry.get()
        crystal_system = self.crystal_system_var.get()
        lattice_constant = [entry.get() for entry in self.lattice_entries]

        if crystal_system in ["cubic", "rhombohedral"]:
            a = lattice_constant[0]
            lattice_constant = [a, a, a]
        elif crystal_system in ["hexagonal", "tetragonal"]:
            a, c = lattice_constant[0], lattice_constant[2]
            lattice_constant = [a, a, c]
        elif crystal_system in ["orthorhombic", "monoclinic", "triclinic"]:
            lattice_constant = [entry.get() for entry in self.lattice_entries]
        else:
            messagebox.showerror("Error", "Crystal system does not exist")
            return

        vector1 = [self.vector_entries[i].get() for i in range(3)]
        vector2 = [self.vector_entries[i+3].get() for i in range(3)]
        vector3 = [self.vector_entries[i+6].get() for i in range(3)]

        number_of_atoms = int(self.number_of_atoms_entry.get())
        atom_parameters = [
            [self.atom_parameters_entries[i][j].get() for j in range(7)]
            for i in range(number_of_atoms)
        ]

        number_of_interactions = self.number_of_interactions_entry.get()
        exctype = self.exchange_type_entry.get()

        with open(filename, 'w') as f:
            print("# Unit cell size:", file=f)
            print(lattice_constant[0], "\t", lattice_constant[1], "\t", lattice_constant[2], sep="", file=f)

            print("# Unit cell vectors: ", file=f)
            print(vector1[0], vector1[1], vector1[2], file=f)
            print(vector2[0], vector2[1], vector2[2], file=f)
            print(vector3[0], vector3[1], vector3[2], file=f)

            print("# Atoms num, id cx cy cz mat lc hc", file=f)
            print(number_of_atoms, file=f)
            for i in range(number_of_atoms):
                print("\t".join(atom_parameters[i]), file=f)

            print("#Interactions n exctype, id i j dx dy dz Jij", file=f)
            print(number_of_interactions, exctype, file=f)
            print("#Open ucf to add interaction parameters (id i j dx dy dz Jij). These currently must be added manually.", file=f)
            print("# Manually add interaction parameters here", file=f)
            additional_parameters = self.text_output.get("1.0", tk.END)
            print(additional_parameters, file=f)
        messagebox.showinfo("Success", f"{filename} has been generated.")


    
def main():
    root = tk.Tk()
    root.title("UCF Generator")

    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='Generate UCF File')
    tabControl.pack(expand=1, fill="both")

    ufcFile(tab1)

    root.mainloop()

if __name__ == "__main__":
    main()
 
