# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:33:57 2025

@author: Thommes Eliott
"""

# Library of Messages


# Other Lib
import tkinter as tk
from tkinter import messagebox

# Custom Lib


"""
For non-locking error can go to the control pannel by printing text, showing the time of the error.
"""

def show_error(title, message, non_blocking=True):
    """Show an error message box. Defaults to non-blocking."""
    if non_blocking:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.after(10, lambda: messagebox.showerror(title, message))
        root.after(100, root.destroy)  # Destroy after short delay
    else:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror(title, message)
        root.destroy()

def show_warning(title, message):
    """Show a warning message box."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showwarning(title, message)
    root.destroy()

def show_info(title, message):
    """Show an info message box."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo(title, message)
    root.destroy()

def show_question(title, message):
    """Show a question dialog and return True for Yes or False for No."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    response = messagebox.askyesno(title, message)
    root.destroy()
    return response

def show_retry_cancel(title, message):
    """Show a retry/cancel dialog and return True for Retry or False for Cancel."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    response = messagebox.askretrycancel(title, message)
    root.destroy()
    return response

def show_ok_cancel(title, message):
    """Show an OK/Cancel dialog and return True for OK or False for Cancel."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    response = messagebox.askokcancel(title, message)
    root.destroy()
    return response

def ask_user_input(title, prompt, expected_type=str):
    """Ask for user input through a simple entry dialog and validate its type."""
    def on_submit():
        nonlocal user_input, valid
        user_input = entry.get()
        try:
            if expected_type == int:
                user_input = int(user_input)
            elif expected_type == float:
                user_input = float(user_input)
            elif expected_type == bool:
                user_input = user_input.lower() in ['true', '1', 'yes']
            elif expected_type == str:
                user_input = str(user_input)
            valid = True
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", f"Please enter a valid {expected_type.__name__}.")

    user_input = None
    valid = False

    while not valid:
        dialog = tk.Tk()
        dialog.title(title)

        tk.Label(dialog, text=prompt).pack(pady=10)
        entry = tk.Entry(dialog, width=40)
        entry.pack(pady=5)
        entry.focus()

        tk.Button(dialog, text="Submit", command=on_submit).pack(pady=10)

        dialog.mainloop()

    return user_input

# Example usage
if __name__ == "__main__":
    show_error("Error", "This is a non-blocking error message.")
    show_warning("Warning", "This is a warning message.")
    show_info("Information", "This is an informational message.")
    response = show_question("Question", "Do you want to proceed?")
    print("Question response:", response)
    response = show_retry_cancel("Retry", "Do you want to retry the operation?")
    print("Retry response:", response)
    response = show_ok_cancel("Confirmation", "Do you confirm this action?")
    print("OK/Cancel response:", response)
    user_input = ask_user_input("Input Needed", "Please enter an integer:", expected_type=int)
    print("User input (integer):", user_input)
    user_input = ask_user_input("Input Needed", "Please enter a float:", expected_type=float)
    print("User input (float):", user_input)