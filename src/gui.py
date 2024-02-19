import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.onder_code_interpreter import Interpreter


class OnderApp(tk.Tk):
    """Simple GUI app for ONDERCODEEEEE"""
    def __init__(self):
        super().__init__()
        self.title("OnderCode Interpreter")
        self.create_menu()
        self.text_field = None
        self.button_exec = None
        self.button_close = tk.Button(self, text="Close", command=self._close)
        self.button_steps = None
        self.button_steps_var = tk.StringVar()
        self.before_variables = tk.Variable()
        self.after_variables = tk.Variable()
        self.steps_variable = tk.Variable()
        self.button_steps_var.set("Show Steps")

        self.variables_before_execution = tk.Listbox(self, listvariable=self.before_variables)
        self.scroll_before = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.variables_before_execution.yview)
        self.variables_before_execution["yscrollcommand"] = self.scroll_before.set

        self.variables_after_execution = tk.Listbox(self, listvariable=self.after_variables)
        self.scroll_after = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.variables_after_execution.yview)
        self.variables_after_execution["yscrollcommand"] = self.scroll_after.set

        self.steps_list = tk.Listbox(self, listvariable=self.steps_variable)
        self.scroll_steps = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.steps_list.yview)
        self.steps_list["yscrollcommand"] = self.scroll_steps.set

        self.create_fields()

        self.start_variables = {}

    def create_menu(self):
        """Creates menu, with settings and file options. It exists as a
        separate method to make the code more readable."""
        menu = tk.Menu(self)

        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label="Close", command=self.destroy)
        settings_menu.add_command(label="Add variables", command=self.add_variable)
        settings_menu.add_command(label="Remove variables", command=self.delete_variable)
        # settings_menu.add_command(label="Settings", command=lambda: None)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Load", command=self._load)
        file_menu.add_command(label="Save", command=self._save)
        file_menu.add_separator()
        file_menu.add_command(label="Clear", command=self._clear)

        menu.add_cascade(label="Settings", menu=settings_menu)
        menu.add_cascade(label="File", menu=file_menu)

        self.config(menu=menu)

    def create_fields(self):
        """Creates text fields for the app. It exists as a separate method to make the code more readable."""
        self.text_field = tk.Text(self)
        self.text_field.grid(row=0, column=0, columnspan=3, rowspan=3)

        self.button_exec = tk.Button(self, text="Exec", command=self._exec)
        self.button_steps = tk.Button(self, textvariable=self.button_steps_var, command=self.show_steps)
        self.button_exec.grid(row=3, column=0)
        self.button_steps.grid(row=3, column=2)

    @staticmethod
    def format_variables(variables: dict):
        values = []
        for name, val in variables.items():
            values.append(f"{name} => {val}")
        return values

    def _exec(self):
        with NamedTemporaryFile() as file:
            path = Path(file.name)
            path.write_text(self.text_field.get("1.0", tk.END))
            # dodac obsluge zmiennych
            c = Interpreter(path, **self.start_variables)
            if self.steps_list.winfo_viewable():
                self.steps_list.grid_remove()

            self.variables_before_execution.grid(row=4, column=0)
            self.before_variables.set(self.format_variables(c.variables))
            c()
            self.variables_after_execution.grid(row=4, column=2)
            self.after_variables.set(self.format_variables(c.variables))
            self.button_close.grid(row=3, column=1)
            # jesli blad brakuje zmiennych

    def _close(self):
        """Hides the list of variables and steps"""
        if self.button_close.winfo_viewable():
            self.button_close.grid_remove()

        if self.variables_after_execution.winfo_viewable():
            self.variables_before_execution.grid_remove()
            self.variables_after_execution.grid_remove()

        if self.steps_list.winfo_viewable():
            self.steps_list.grid_remove()

    def show_steps(self):
        """Shows steps of the execution"""
        with NamedTemporaryFile() as file:
            # Yeah i know it's against DRY rule :(
            path = Path(file.name)
            path.write_text(self.text_field.get("1.0", tk.END))
            c = Interpreter(path, **self.start_variables)
            c()
            if self.variables_after_execution.winfo_viewable():
                self.variables_before_execution.grid_remove()
                self.variables_after_execution.grid_remove()
            self.steps_variable.set(c.steps)
            self.steps_list.grid(row=4, column=1)
            self.button_close.grid(row=3, column=1)

    def _clear(self):
        """Clears the text field and hides the list of variables and steps."""
        self.text_field.delete("1.0", tk.END)
        if self.variables_after_execution.winfo_viewable():
            self.variables_after_execution.grid_remove()
            self.variables_before_execution.grid_remove()
        if self.steps_list.winfo_viewable():
            self.steps_list.grid_remove()

    def _load(self):
        """Loads the file and puts it into the text field."""
        filename = filedialog.askopenfilename(filetypes=[("OnderCode", "*.oc")])
        if filename:
            text = Path(filename).read_text()
            self.text_field.delete("1.0", tk.END)
            self.text_field.insert("1.0", text)

    def _save(self):
        """Saves the text from the text field into the file."""
        filename = filedialog.asksaveasfile(defaultextension=".oc", confirmoverwrite=True)
        if filename:
            Path(filename.name).write_text(self.text_field.get("1.0", tk.END))

    def add_variable(self):
        """Adds variable to the list of variables."""
        dialog = tk.Toplevel(self)
        dialog.title("Add Variable")
        lab1 = tk.Label(dialog, text="Variable Name")
        lab1.pack()
        entry1 = tk.Entry(dialog)
        entry1.pack()
        lab2 = tk.Label(dialog, text="Values")
        lab2.pack()
        entry2 = tk.Entry(dialog)
        entry2.pack()
        add_but = tk.Button(dialog, text="Save", command=lambda: self.add_values(entry1.get(), entry2.get(), dialog))
        add_but.pack()

    def delete_variable(self):
        """Deletes variable from the list of variables."""
        dialog = tk.Toplevel(self)
        dialog.title("Delete Variable")
        lab = tk.Label(dialog, text="Select Variables")
        lab.pack()
        items = tk.Listbox(dialog, selectmode=tk.MULTIPLE)
        for key in self.start_variables.keys():
            items.insert(tk.END, key)
        items.pack()
        confirm_but = tk.Button(dialog, text="Delete",
                                command=lambda: self.delete_values(items, items.curselection(), dialog))
        confirm_but.pack()

    def add_values(self, name, values, dialog):
        """Adds values to the dictionary of variables."""
        if len(values.split(",")) > 1:
            values = int(values.split(","))
        self.start_variables[name] = values
        dialog.destroy()

    def delete_values(self, listbox, selected, dialog):
        """Deletes values from the dictionary of variables."""
        if selected:
            for ind in selected:
                del self.start_variables[listbox.get(ind)]
        dialog.destroy()


if __name__ == "__main__":
    app = OnderApp()
    app.mainloop()
