import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

# Store command history and directory state
command_history = []
history_index = -1
current_directory = os.getcwd()  # Start in the script's directory
dark_mode = True  # Default to dark mode

# Dictionary of commands with expected arguments
COMMANDS = {
    "cd": "cd <directory>",
    "dir": "dir",
    "cls": "cls",
    "ipconfig": "ipconfig",
    "ping": "ping <hostname>",
    "echo": "echo <message>",
    "python": "python --version",
    "pip install": "pip install <package_name>",
    "pip uninstall": "pip uninstall <package_name>",
    "git clone": "git clone <repository_url>",
    "git pull": "git pull <branch>",
    "git push": "git push <branch>",
    "shutdown": "shutdown -s -t 60",
    "whoami": "whoami",
    "netstat": "netstat -an",
    "tasklist": "tasklist",
    "systeminfo": "systeminfo"
}

# Function to execute commands via GUI
def execute_command(event=None):
    command = command_entry.get().strip()
    if command:
        try:
            result = subprocess.run(command, shell=True, cwd=current_directory, capture_output=True, text=True)
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, f"\n> {command}\n{result.stdout}{result.stderr}\n")
            output_text.config(state=tk.DISABLED)
            command_history.append(command)
            command_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute command: {str(e)}")

# Function to clear the output window
def clear_output():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)

# Function to toggle light/dark mode
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    theme_settings = {
        True: {"bg": "#1e1e1e", "fg": "white", "entry_bg": "#252526", "btn_bg": "#333", "btn_text": "Switch to Light Mode"},
        False: {"bg": "white", "fg": "black", "entry_bg": "white", "btn_bg": "lightgray", "btn_text": "Switch to Dark Mode"}
    }
    theme = theme_settings[dark_mode]
    root.config(bg=theme["bg"])
    command_label.config(bg=theme["bg"], fg=theme["fg"])
    command_entry.config(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])
    autocomplete_menu.config(background=theme["entry_bg"], foreground=theme["fg"])
    output_text.config(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])
    execute_button.config(bg=theme["btn_bg"], fg=theme["fg"])
    clear_button.config(bg=theme["btn_bg"], fg=theme["fg"])
    theme_button.config(bg=theme["btn_bg"], fg=theme["fg"], text=theme["btn_text"])
    cmd_button.config(bg=theme["btn_bg"], fg=theme["fg"])
    linux_button.config(bg=theme["btn_bg"], fg=theme["fg"])

# Function to open Windows CMD
def open_cmd_window():
    subprocess.Popen(["cmd.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE)

# Function to open Linux Terminal (WSL)
def open_linux_terminal():
    try:
        subprocess.Popen(["wsl"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    except FileNotFoundError:
        messagebox.showerror("Error", "WSL not found. Ensure WSL is installed.")

# Function to update auto-complete dropdown dynamically
def update_suggestions(event):
    typed_text = command_entry.get().strip().lower()
    if typed_text:
        suggestions = [cmd for cmd in COMMANDS.keys() if cmd.startswith(typed_text)]
        if suggestions:
            autocomplete_menu["values"] = suggestions
            autocomplete_menu.current(0)
            autocomplete_menu.event_generate("<Down>")
        else:
            autocomplete_menu["values"] = []
    else:
        autocomplete_menu["values"] = []

# Function to insert selected auto-complete command into the input field
def fill_selected_suggestion(event):
    selected_command = autocomplete_menu.get()
    if selected_command:
        command_entry.delete(0, tk.END)
        command_entry.insert(0, selected_command)

# GUI Setup
root = tk.Tk()
root.title("PowerCMD")
root.geometry("800x500")

command_label = tk.Label(root, text="Enter Command:", bg="#1e1e1e", fg="white")
command_label.pack(pady=(10, 0))

command_entry = ttk.Entry(root, width=60)
command_entry.pack(pady=5)
command_entry.bind("<Return>", execute_command)
command_entry.bind("<KeyRelease>", update_suggestions)

autocomplete_menu = ttk.Combobox(root, width=57, state="readonly")
autocomplete_menu.pack(pady=5)
autocomplete_menu.bind("<<ComboboxSelected>>", fill_selected_suggestion)

buttons_frame = tk.Frame(root, bg="#1e1e1e")
buttons_frame.pack(pady=5)

execute_button = tk.Button(buttons_frame, text="Run Command", command=execute_command, bg="#333", fg="white")
execute_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(buttons_frame, text="Clear Output", command=clear_output, bg="#333", fg="white")
clear_button.pack(side=tk.LEFT, padx=5)

cmd_button = tk.Button(buttons_frame, text="Open Windows CMD", command=open_cmd_window, bg="#333", fg="white")
cmd_button.pack(side=tk.LEFT, padx=5)

linux_button = tk.Button(buttons_frame, text="Open Linux Terminal", command=open_linux_terminal, bg="#333", fg="white")
linux_button.pack(side=tk.LEFT, padx=5)

theme_button = tk.Button(buttons_frame, text="Switch to Light Mode", command=toggle_theme, bg="#333", fg="white")
theme_button.pack(side=tk.LEFT, padx=5)

output_text = tk.Text(root, wrap="word", height=15, state=tk.DISABLED, bg="black", fg="white")
output_text.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()
