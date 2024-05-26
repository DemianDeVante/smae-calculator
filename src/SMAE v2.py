import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Function to format numbers to 2 decimal places
def format_number(value):
    return '{:.2f}'.format(value) if value is not None else ""

# Function to insert a new row
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

# Function to update values based on required quantities
def update_values():
    for item in tree.get_children():
        row = tree.item(item, 'values')
        if row[8] and row[2]:
            row = list(row)
            prp = (float(row[9]) / float(row[2]))
            for i in range(1, 8):  # Columns 1 to 7
                row[i] = prp * float(row[i])
            tree.item(item, values=tuple(row))

# Function to adjust values to a target (generic for energy, protein, lipids, carbs)
def adjust_to_target(target_name, column_name):
    target_value = simpledialog.askfloat(f"Adjust to {target_name} Target", f"Enter the {target_name.lower()} target:")
    if target_value:
        source_value = sum(float(tree.item(item, 'values')[columns.index(column_name)] or 0) for item in tree.get_children())
        ratio = target_value / source_value
        for item in tree.get_children():
            row = tree.item(item, 'values')
            if row[8] and row[2]:
                row = list(row)
                for i in range(1, 8):  # Columns 1 to 7
                    row[i] = format_number(ratio * float(row[i]))
                tree.item(item, values=tuple(row))

# Function to clear input fields
def clear_inputs():
    for entry in (entry_nme, entry_rat, entry_mca, entry_grs, entry_nrg, entry_ptn, entry_lip, entry_crb, entry_r_grs, entry_r_mca):
        entry.delete(0, tk.END)

# Function to edit a selected row
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

# Function to save changes after editing
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

# Function to move a row up
def move_up():
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item)
        if index > 0:
            tree.move(selected_item, '', index - 1)

# Function to move a row down
def move_down():
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item)
        if index < len(tree.get_children()) - 1:
            tree.move(selected_item, '', index + 1)

# Function to delete a selected row
def delete_row():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

# Function to duplicate a selected row
def duplicate_row():
    selected_item = tree.selection()
    if selected_item:
        selected_values = tree.item(selected_item, 'values')
        tree.insert("", "end", values=selected_values)

# Function to export treeview data to clipboard
def export_to_clipboard():
    clipboard_text = ""
    for item in tree.get_children():
        row_values = tree.item(item, 'values')
        clipboard_text += '\t'.join([str(value) for value in row_values]) + '\n'

    root.clipboard_clear()
    root.clipboard_append(clipboard_text)
    root.update()

# Function to import data from clipboard to treeview
def import_from_clipboard():
    clipboard_data = root.clipboard_get()
    lines = clipboard_data.strip().split('\n')
    for line in lines:
        values = line.strip().split('\t')
        tree.insert("", "end", values=values)

# Function to update sum of energy, protein, lipids, and carbohydrates
def update_sums():
    total_nrg, total_ptn, total_lip, total_crb = 0.0, 0.0, 0.0, 0.0
    for item in tree.get_children():
        row = tree.item(item, 'values')
        total_nrg += float(row[columns.index("Energy (kCal)")] or 0)
        total_ptn += float(row[columns.index("Protein (g)")] or 0)
        total_lip += float(row[columns.index("Lipids (g)")] or 0)
        total_crb += float(row[columns.index("Carbohydrates (g)")] or 0)

    for sum_entry, total in zip((sum_nrg, sum_ptn, sum_lip, sum_crb), (total_nrg, total_ptn, total_lip, total_crb)):
        sum_entry.config(state="normal")
        sum_entry.delete(0, tk.END)
        sum_entry.insert(0, f"{format_number(total)} {'kCal' if 'Energy' in sum_entry.get() else 'g'}")
        sum_entry.config(state="readonly")

# Main window setup
root = tk.Tk()
root.title("Recipe Table")

columns = ("Ingredient", "Portion", "Homemade Measure", "Weight (g)", "Energy (kCal)", "Protein (g)", "Lipids (g)", "Carbohydrates (g)", "Required Quantity (g)", "Required Quantity (Homemade Measure)")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack()

# Input frames
entry_frame1 = tk.Frame(root)
entry_frame1.pack()
entry_nme, entry_rat, entry_mca, entry_grs, entry_nrg = [tk.Entry(entry_frame1) for _ in range(5)]
labels1 = ["Ingredient", "Portion", "Homemade Measure", "Weight (g)", "Energy (kCal)"]
for i, (label_text, entry) in enumerate(zip(labels1, (entry_nme, entry_rat, entry_mca, entry_grs, entry_nrg))):
    tk.Label(entry_frame1, text=label_text).grid(row=0, column=i)
    entry.grid(row=1, column=i)

entry_frame2 = tk.Frame(root)
entry_frame2.pack()
entry_ptn, entry_lip, entry_crb, entry_r_grs, entry_r_mca = [tk.Entry(entry_frame2) for _ in range(5)]
labels2 = ["Protein (g)", "Lipids (g)", "Carbohydrates (g)", "Required Quantity (g)", "Required Quantity (Homemade Measure)"]
for i, (label_text, entry) in enumerate(zip(labels2, (entry_ptn, entry_lip, entry_crb, entry_r_grs, entry_r_mca))):
    tk.Label(entry_frame2, text=label_text).grid(row=0, column=i)
    entry.grid(row=1, column=i)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()
buttons = [
    ("Insert Row", insert_row),
    ("Update Values", update_values),
    ("Adjust to Energy Target", lambda: adjust_to_target("Energy", "Energy (kCal)")),
    ("Adjust to Protein Target", lambda: adjust_to_target("Protein", "Protein (g)")),
    ("Adjust to Lipids Target", lambda: adjust_to_target("Lipids", "Lipids (g)")),
    ("Adjust to Carbohydrates Target", lambda: adjust_to_target("Carbohydrates", "Carbohydrates (g)")),
    ("Edit Row", edit_row),
    ("Move Up", move_up),
    ("Move Down", move_down),
    ("Delete Row", delete_row),
    ("Duplicate Row", duplicate_row),
    ("Export to Clipboard", export_to_clipboard),
    ("Import from Clipboard", import_from_clipboard),
    ("Update Sums", update_sums)
]
for i, (text, command) in enumerate(buttons):
    tk.Button(button_frame, text=text, command=command).grid(row=i // 3, column=i % 3, padx=5, pady=5)

# Sum Entries
sum_frame = tk.Frame(root)
sum_frame.pack()
sum_nrg, sum_ptn, sum_lip, sum_crb = [tk.Entry(sum_frame, state="readonly") for _ in range(4)]
sum_labels = ["Total Energy (kCal)", "Total Protein (g)", "Total Lipids (g)", "Total Carbohydrates (g)"]
for i, (label_text, sum_entry) in enumerate(zip(sum_labels, (sum_nrg, sum_ptn, sum_lip, sum_crb))):
    tk.Label(sum_frame, text=label_text).grid(row=0, column=i)
    sum_entry.grid(row=1, column=i)

root.mainloop()

