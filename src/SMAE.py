import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

def format_number(value):
    return '{:.2f}'.format(value) if value is not None else ""

def insert_row():
    nme = entry_nme.get()
    rat = entry_rat.get()
    mca = entry_mca.get()
    grs = entry_grs.get()
    nrg = entry_nrg.get()
    ptn = entry_ptn.get()
    lip = entry_lip.get()
    crb = entry_crb.get()
    r_grs = entry_r_grs.get()
    r_mca = entry_r_mca.get()

    if not r_grs and not r_mca:
        messagebox.showerror("Error", "Enter the required quantity for this recipe")
        return

    if not r_mca and r_grs:
        r_mca = (float(r_grs) / float(grs)) * float(mca)
    elif not r_grs and r_mca:
        r_grs = (float(r_mca) / float(mca)) * float(grs)

    tree.insert("", "end", values=(nme, rat, mca, grs, nrg, ptn, lip, crb, r_grs, r_mca))
    clear_inputs()

def update_values():
    for item in tree.get_children():
        row = tree.item(item, 'values')
        if row[8] and row[2]:
            row = list(row)
            prp = (float(row[9]) / float(row[2]))
            row[1] = prp * float(row[1])
            row[2] = prp * float(row[2])
            row[3] = prp * float(row[3])
            row[4] = prp * float(row[4])
            row[5] = prp * float(row[5])
            row[6] = prp * float(row[6])
            row[7] = prp * float(row[7])
            tree.item(item, values=tuple(row))

def adjust_to_protein_target():
    ptn_target = simpledialog.askfloat("Adjust to Protein Target", "Enter the protein target:")
    if ptn_target:
        ptn_source = sum(float(tree.item(item, 'values')[columns.index("Protein (g)")] or 0) for item in tree.get_children())

        ptn_ratio = ptn_target / ptn_source
        for item in tree.get_children():
            row = tree.item(item, 'values')
            if row[8] and row[2]:
                row = list(row)
                for i in range(1, 10):  # Columns 1 to 9
                    row[i] = format_number(ptn_ratio * float(row[i]))
                tree.item(item, values=tuple(row))

def adjust_to_energetic_target():
    nrg_target = simpledialog.askfloat("Adjust to Energetic Target", "Enter the energetic target:")
    if nrg_target:
        nrg_source = sum(float(tree.item(item, 'values')[columns.index("Energy (kCal)")] or 0) for item in tree.get_children())

        nrg_ratio = nrg_target / nrg_source
        for item in tree.get_children():
            row = tree.item(item, 'values')
            if row[8] and row[2]:
                row = list(row)
                for i in range(1, 10):  # Columns 1 to 9
                    row[i] = format_number(nrg_ratio * float(row[i]))
                tree.item(item, values=tuple(row))

def adjust_to_carb_target():
    nrg_target = simpledialog.askfloat("Adjust to Carb Target", "Enter the carb target:")
    if nrg_target:
        nrg_source = sum(float(tree.item(item, 'values')[columns.index("Carbohydrates (g)")] or 0) for item in tree.get_children())

        nrg_ratio = nrg_target / nrg_source
        for item in tree.get_children():
            row = tree.item(item, 'values')
            if row[8] and row[2]:
                row = list(row)
                for i in range(1, 10):  # Columns 1 to 9
                    row[i] = format_number(nrg_ratio * float(row[i]))
                tree.item(item, values=tuple(row))

def adjust_to_lipid_target():
    nrg_target = simpledialog.askfloat("Adjust to Lipid Target", "Enter the lipid target:")
    if nrg_target:
        nrg_source = sum(float(tree.item(item, 'values')[columns.index("Lipids (g)")] or 0) for item in tree.get_children())

        nrg_ratio = nrg_target / nrg_source
        for item in tree.get_children():
            row = tree.item(item, 'values')
            if row[8] and row[2]:
                row = list(row)
                for i in range(1, 10):  # Columns 1 to 9
                    row[i] = format_number(nrg_ratio * float(row[i]))
                tree.item(item, values=tuple(row))

def clear_inputs():
    entry_nme.delete(0, tk.END)
    entry_rat.delete(0, tk.END)
    entry_mca.delete(0, tk.END)
    entry_grs.delete(0, tk.END)
    entry_nrg.delete(0, tk.END)
    entry_ptn.delete(0, tk.END)
    entry_lip.delete(0, tk.END)
    entry_crb.delete(0, tk.END)
    entry_r_grs.delete(0, tk.END)
    entry_r_mca.delete(0, tk.END)

def edit_row():
    item = tree.selection()
    if item:
        selected_values = tree.item(item, 'values')
        edit_window = tk.Toplevel()
        edit_window.title("Edit Row")

        edit_entries = []
        for value in selected_values:
            entry = tk.Entry(edit_window)
            entry.insert(0, value)
            edit_entries.append(entry)

        for i, col in enumerate(columns):
            label = tk.Label(edit_window, text=col)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = edit_entries[i]
            entry.grid(row=i, column=1, padx=5, pady=5)

        save_button = tk.Button(edit_window, text="Save Changes", command=lambda: save_changes(item, edit_entries, edit_window))
        save_button.grid(row=len(columns), column=0, columnspan=2)

def save_changes(item, edit_entries, edit_window):
    values = [entry.get() for entry in edit_entries]
    if not values[8] and not values[9]:
        messagebox.showerror("Error", "Enter the required quantity for this ingredient")
        return

    if not values[9] and values[8]:
        values[9] = (float(values[8]) / float(values[3])) * float(values[2])
    elif not values[8] and values[9]:
        values[8] = (float(values[9]) / float(values[2])) * float(values[3])

    tree.item(item, values=tuple(values))
    edit_window.destroy()

def move_up():
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item)
        if index > 0:
            tree.move(selected_item, '', index - 1)

def move_down():
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item)
        if index < len(tree.get_children()) - 1:
            tree.move(selected_item, '', index + 1)

def delete_row():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

def duplicate_row():
    selected_item = tree.selection()
    if selected_item:
        selected_values = tree.item(selected_item, 'values')
        tree.insert("", "end", values=selected_values)

def export_to_clipboard():
    clipboard_text = ""
    for item in tree.get_children():
        row_values = tree.item(item, 'values')
        clipboard_text += '\t'.join([str(value) for value in row_values]) + '\n'

    root.clipboard_clear()
    root.clipboard_append(clipboard_text)
    root.update()

def import_from_clipboard():
    clipboard_data = root.clipboard_get()
    lines = clipboard_data.strip().split('\n')
    for line in lines:
        values = line.strip().split('\t')
        tree.insert("", "end", values=values)

root = tk.Tk()
root.title("Recipe Table")

columns = ("Ingredient", "Portion", "Homemade Measure", "Weight (g)", "Energy (kCal)", "Protein (g)", "Lipids (g)", "Carbohydrates (g)", "Required Quantity (g)", "Required Quantity (Homemade Measure)")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack()

entry_frame1 = tk.Frame(root)
entry_frame1.pack()

label_nme = tk.Label(entry_frame1, text="Ingredient")
label_nme.grid(row=0, column=0, padx=5, pady=5)
entry_nme = tk.Entry(entry_frame1)
entry_nme.grid(row=0, column=1, padx=5, pady=5)

label_rat = tk.Label(entry_frame1, text="Portion")
label_rat.grid(row=0, column=2, padx=5, pady=5)
entry_rat = tk.Entry(entry_frame1)
entry_rat.grid(row=0, column=3, padx=5, pady=5)

label_mca = tk.Label(entry_frame1, text="Homemade Measure")
label_mca.grid(row=0, column=4, padx=5, pady=5)
entry_mca = tk.Entry(entry_frame1)
entry_mca.grid(row=0, column=5, padx=5, pady=5)

label_grs = tk.Label(entry_frame1, text="Weight (g)")
label_grs.grid(row=0, column=6, padx=5, pady=5)
entry_grs = tk.Entry(entry_frame1)
entry_grs.grid(row=0, column=7, padx=5, pady=5)

label_nrg = tk.Label(entry_frame1, text="Energy (kCal)")
label_nrg.grid(row=0, column=8, padx=5, pady=5)
entry_nrg = tk.Entry(entry_frame1)
entry_nrg.grid(row=0, column=9, padx=5, pady=5)

entry_frame2 = tk.Frame(root)
entry_frame2.pack()

label_ptn = tk.Label(entry_frame2, text="Protein (g)")
label_ptn.grid(row=0, column=0, padx=5, pady=5)
entry_ptn = tk.Entry(entry_frame2)
entry_ptn.grid(row=0, column=1, padx=5, pady=5)

label_lip = tk.Label(entry_frame2, text="Lipids (g)")
label_lip.grid(row=0, column=2, padx=5, pady=5)
entry_lip = tk.Entry(entry_frame2)
entry_lip.grid(row=0, column=3, padx=5, pady=5)

label_crb = tk.Label(entry_frame2, text="Carbohydrates (g)")
label_crb.grid(row=0, column=4, padx=5, pady=5)
entry_crb = tk.Entry(entry_frame2)
entry_crb.grid(row=0, column=5, padx=5, pady=5)

label_r_grs = tk.Label(entry_frame2, text="Required Quantity (g)")
label_r_grs.grid(row=0, column=6, padx=5, pady=5)
entry_r_grs = tk.Entry(entry_frame2)
entry_r_grs.grid(row=0, column=7, padx=5, pady=5)

label_r_mca = tk.Label(entry_frame2, text="Required Quantity (Homemade Measure)")
label_r_mca.grid(row=0, column=8, padx=5, pady=5)
entry_r_mca = tk.Entry(entry_frame2)
entry_r_mca.grid(row=0, column=9, padx=5, pady=5)

sum_nrg = tk.Entry(root, state="readonly")
sum_ptn = tk.Entry(root, state="readonly")
sum_lip = tk.Entry(root, state="readonly")
sum_crb = tk.Entry(root, state="readonly")

sum_nrg.insert(0, "0.00")
sum_ptn.insert(0, "0.00")
sum_lip.insert(0, "0.00")
sum_crb.insert(0, "0.00")

def update_sums():
    total_nrg = 0.0
    total_ptn = 0.0
    total_lip = 0.0
    total_crb = 0.0

    for item in tree.get_children():
        row = tree.item(item, 'values')
        nrg = float(row[columns.index("Energy (kCal)")] or 0)
        ptn = float(row[columns.index("Protein (g)")] or 0)
        lip = float(row[columns.index("Lipids (g)")] or 0)
        crb = float(row[columns.index("Carbohydrates (g)")] or 0)

        total_nrg += nrg
        total_ptn += ptn
        total_lip += lip
        total_crb += crb

    sum_nrg.config(state="normal")
    sum_ptn.config(state="normal")
    sum_lip.config(state="normal")
    sum_crb.config(state="normal")

    sum_nrg.delete(0, tk.END)
    sum_ptn.delete(0, tk.END)
    sum_lip.delete(0, tk.END)
    sum_crb.delete(0, tk.END)

    sum_nrg.insert(0, str(format_number(total_nrg))+" kCal")
    sum_ptn.insert(0, str(format_number(total_ptn))+" g P")
    sum_lip.insert(0, str(format_number(total_lip))+" g L")
    sum_crb.insert(0, str(format_number(total_crb))+" g C")

    sum_nrg.config(state="readonly")
    sum_ptn.config(state="readonly")
    sum_lip.config(state="readonly")
    sum_crb.config(state="readonly")

sum_nrg.pack()
sum_ptn.pack()
sum_lip.pack()
sum_crb.pack()

button_frame1 = tk.Frame(root)
button_frame1.pack()

insert_button = tk.Button(button_frame1, text="Insert", command=insert_row)
edit_button = tk.Button(button_frame1, text="Edit", command=edit_row)
update_button = tk.Button(button_frame1, text="Calculate Proportions", command=update_values)
update_sums_button = tk.Button(button_frame1, text="Update Sums", command=update_sums)

insert_button.grid(row=0, column=0, padx=5, pady=5)
edit_button.grid(row=0, column=1, padx=5, pady=5)
update_button.grid(row=0, column=2, padx=5, pady=5)
update_sums_button.grid(row=0, column=3, padx=5, pady=5)

button_frame2 = tk.Frame(root)
button_frame2.pack()

energetic_button = tk.Button(button_frame2, text="Energetic Target", command=adjust_to_energetic_target)
protein_button = tk.Button(button_frame2, text="Protein Target", command=adjust_to_protein_target)
lipid_button = tk.Button(button_frame2, text="Lipid Target", command=adjust_to_lipid_target)
carb_button = tk.Button(button_frame2, text="Carb Target", command=adjust_to_carb_target)

energetic_button.grid(row=0, column=0, padx=5, pady=5)
protein_button.grid(row=0, column=1, padx=5, pady=5)
lipid_button.grid(row=0, column=2, padx=5, pady=5)
carb_button.grid(row=0, column=3, padx=5, pady=5)

button_frame3 = tk.Frame(root)
button_frame3.pack()

move_up_button = tk.Button(button_frame3, text="Move Up", command=move_up)
move_down_button = tk.Button(button_frame3, text="Move Down", command=move_down)
import_button = tk.Button(button_frame3, text="Import from Clipboard", command=import_from_clipboard)
export_button = tk.Button(button_frame3, text="Export", command=export_to_clipboard)

move_up_button.grid(row=0, column=0, padx=5, pady=5)
move_down_button.grid(row=0, column=1, padx=5, pady=5)
import_button.grid(row=0, column=2, padx=5, pady=5)
export_button.grid(row=0, column=3, padx=5, pady=5)

button_frame4 = tk.Frame(root)
button_frame4.pack()

duplicate_button = tk.Button(button_frame4, text="Duplicate", command=duplicate_row)
delete_button = tk.Button(button_frame4, text="Delete", command=delete_row)

duplicate_button.grid(row=0, column=0, padx=5, pady=5)
delete_button.grid(row=0, column=1, padx=5, pady=5)



root.mainloop()
