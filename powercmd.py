import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os

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

# Store command history and directory state
command_history = []
history_index = -1
current_directory = os.getcwd()  # Start in the script's directory

# Track current theme (dark mode by default)
dark_mode = True  

# Function to execute the command while maintaining directory changes
def execute_command(event=None):
    global current_directory
    command = command_entry.get().strip()
    
    if command:
        try:
            # Handle 'cd' commands separately
            if command.lower() == "cd\\":
                current_directory = "C:\\"
            elif command.lower() == "cd ..":
                current_directory = os.path.abspath(os.path.join(current_directory, ".."))
            elif command.startswith("cd "):
                new_path = command[3:].strip()  
                
                # Handle absolute and relative paths
                if os.path.isabs(new_path):
                    if os.path.isdir(new_path):
                        current_directory = new_path
                    else:
                        messagebox.showerror("Error", f"Directory not found: {new_path}")
                        return
                else:
                    new_path = os.path.abspath(os.path.join(current_directory, new_path))
                    if os.path.isdir(new_path):
                        current_directory = new_path
                    else:
                        messagebox.showerror("Error", f"Directory not found: {new_path}")
                        return
                
                # Show directory change in output
                output_text.config(state=tk.NORMAL)
                output_text.insert(tk.END, f"\n> {command}\nChanged directory to: {current_directory}\n")
                output_text.config(state=tk.DISABLED)
                return  

            # Run other commands in the tracked directory
            result = subprocess.run(command, shell=True, cwd=current_directory, capture_output=True, text=True)

            # Display output
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, f"\n> {command}\n{result.stdout}{result.stderr if 'cannot find' not in result.stderr.lower() else ''}\n")
            output_text.config(state=tk.DISABLED)

            # Store command in history
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
    
    if dark_mode:
        root.config(bg="#1e1e1e")
        command_label.config(bg="#1e1e1e", fg="white")
        command_entry.config(bg="#252526", fg="white", insertbackground="white")
        autocomplete_menu.config(background="#252526", foreground="white")
        output_text.config(bg="#252526", fg="white", insertbackground="white")
        execute_button.config(bg="#333", fg="white", activebackground="#444", activeforeground="white")
        clear_button.config(bg="#333", fg="white", activebackground="#444", activeforeground="white")
        theme_button.config(bg="#333", fg="white", activebackground="#444", activeforeground="white", text="Switch to Light Mode")
    else:
        root.config(bg="white")
        command_label.config(bg="white", fg="black")
        command_entry.config(bg="white", fg="black", insertbackground="black")
        autocomplete_menu.config(background="white", foreground="black")
        output_text.config(bg="white", fg="black", insertbackground="black")
        execute_button.config(bg="lightgray", fg="black", activebackground="darkgray", activeforeground="black")
        clear_button.config(bg="lightgray", fg="black", activebackground="darkgray", activeforeground="black")
        theme_button.config(bg="lightgray", fg="black", activebackground="darkgray", activeforeground="black", text="Switch to Dark Mode")

# Function to update auto-complete dropdown dynamically
def update_suggestions(event):
    typed_text = command_entry.get().strip()
    if typed_text:
        suggestions = [full_cmd for cmd, full_cmd in COMMANDS.items() if cmd.startswith(typed_text)]
        autocomplete_menu['values'] = suggestions
        if suggestions:
            autocomplete_menu.current(0)  
    else:
        autocomplete_menu['values'] = []

# Function to recall previous commands with Up/Down arrow keys
def recall_command(event):
    global history_index
    if event.keysym == "Up":
        if history_index > 0:
            history_index -= 1
    elif event.keysym == "Down":
        if history_index < len(command_history) - 1:
            history_index += 1
    if command_history:
        command_entry.delete(0, tk.END)
        command_entry.insert(0, command_history[history_index])

# GUI Setup
root = tk.Tk()
root.title("CMD-Shell Notes")
root.geometry("700x450")

# Default to dark mode
root.config(bg="#1e1e1e")

# Label for command entry
command_label = tk.Label(root, text="Enter Command:", bg="#1e1e1e", fg="white")
command_label.pack(pady=(10, 0))

# Command Input Field
command_entry = ttk.Entry(root, width=60)
command_entry.pack(pady=5)
command_entry.bind("<KeyRelease>", update_suggestions)  
command_entry.bind("<Up>", recall_command)
command_entry.bind("<Down>", recall_command)
command_entry.bind("<Return>", execute_command)  

# Auto-complete dropdown
autocomplete_menu = ttk.Combobox(root, width=57, state="readonly")
autocomplete_menu.pack(pady=5)

# Buttons Frame
buttons_frame = tk.Frame(root, bg="#1e1e1e")
buttons_frame.pack(pady=5)

# Execute Button
execute_button = tk.Button(buttons_frame, text="Run Command", command=execute_command, bg="#333", fg="white", activebackground="#444", activeforeground="white")
execute_button.pack(side=tk.LEFT, padx=5)

# Clear Output Button
clear_button = tk.Button(buttons_frame, text="Clear Output", command=clear_output, bg="#333", fg="white", activebackground="#444", activeforeground="white")
clear_button.pack(side=tk.LEFT, padx=5)

# Theme Toggle Button
theme_button = tk.Button(buttons_frame, text="Switch to Light Mode", command=toggle_theme, bg="#333", fg="white", activebackground="#444", activeforeground="white")
theme_button.pack(side=tk.LEFT, padx=5)

# Output Text Area (Read-Only)
output_text = tk.Text(root, wrap="word", height=15, state=tk.DISABLED, bg="#252526", fg="white")
output_text.pack(expand=True, fill="both", padx=10, pady=10)

# Run the application
root.mainloop()
