import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import subprocess
import threading
import sys
import os

# Function to update line numbers
def update_line_numbers():
    line_numbers_text = "\n".join(str(i) for i in range(1, int(code_entry.index('end').split('.')[0])))
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", tk.END)
    line_numbers.insert(tk.END, line_numbers_text)
    line_numbers.config(state="disabled")

# Function to run Python code
def run_code():
    code = code_entry.get("1.0", tk.END).strip()
    if not code:
        console_log.configure(state="normal")  # Enable editing temporarily
        console_log.insert(tk.END, "No code entered.\n")
        console_log.configure(state="disabled")  # Disable editing
        return

    # Save the code to a temporary file
    temp_file = "temp_code.cpp"
    with open(temp_file, "w") as file:
        file.write(code)

# Function to select and run a Python file
def run_file(filepath="pythoncode_tester.py"):
    if not os.path.isfile(filepath):
        console_log.configure(state="normal")
        console_log.insert(tk.END, f"Error: {filepath} not found.\n")
        console_log.configure(state="disabled")
        return

    console_log.configure(state="normal")
    console_log.insert(tk.END, f"Running {filepath} with argument temp_code.cpp...\n")
    console_log.configure(state="disabled")
    
    def execute():
        try:
            process = subprocess.Popen(
                [sys.executable, filepath, "temp_code.cpp"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            def read_output():
                for line in iter(process.stdout.readline, ''):
                    console_log.configure(state="normal")
                    console_log.insert(tk.END, line)
                    console_log.configure(state="disabled")
                    console_log.see(tk.END)
                process.stdout.close()
                process.wait()

            threading.Thread(target=read_output).start()

            def send_input(event=None):
                user_input = input_entry.get()
                input_entry.delete(0, tk.END)
                process.stdin.write(user_input + "\n")
                process.stdin.flush()
                console_log.configure(state="normal")
                console_log.insert(tk.END, f"> {user_input}\n")
                console_log.configure(state="disabled")
                console_log.see(tk.END)

            input_entry.bind("<Return>", send_input)

        except Exception as e:
            console_log.configure(state="normal")
            console_log.insert(tk.END, f"Error: {str(e)}\n")
            console_log.configure(state="disabled")

    threading.Thread(target=execute).start()

# Dictionary of themes
themes = {
    "Light Mode": {"bg": "white", "fg": "black", "btn_bg": "lightgray", "btn_fg": "black", "entry_bg": "white", "entry_fg": "black"},
    "Dark Mode": {"bg": "black", "fg": "white", "btn_bg": "gray20", "btn_fg": "white", "entry_bg": "gray30", "entry_fg": "white"},
    "Blue Mode": {"bg": "#002b36", "fg": "white", "btn_bg": "#073642", "btn_fg": "white", "entry_bg": "#073642", "entry_fg": "white"},
    "Green Mode": {"bg": "#073642", "fg": "#b58900", "btn_bg": "#586e75", "btn_fg": "#b58900", "entry_bg": "#586e75", "entry_fg": "#b58900"},
    "Solarized Mode": {"bg": "#fdf6e3", "fg": "#657b83", "btn_bg": "#eee8d5", "btn_fg": "#657b83", "entry_bg": "#eee8d5", "entry_fg": "#657b83"},
    "Gray Mode": {"bg": "#3c3f41", "fg": "#dcdcdc", "btn_bg": "#4d4d4d", "btn_fg": "#dcdcdc", "entry_bg": "#4d4d4d", "entry_fg": "#dcdcdc"},
    "Purple Mode": {"bg": "#3f0047", "fg": "#f3e5f5", "btn_bg": "#7b1fa2", "btn_fg": "#f3e5f5", "entry_bg": "#7b1fa2", "entry_fg": "#f3e5f5"}
}

# Function to apply the selected theme
def apply_theme(theme_name):
    colors = themes[theme_name]
    root.configure(bg=colors['bg'])
    code_entry.configure(bg=colors['entry_bg'], fg=colors['entry_fg'])
    line_numbers.configure(bg=colors['entry_bg'], fg=colors['fg'])
    console_log.configure(bg=colors['entry_bg'], fg=colors['entry_fg'])
    run_button.configure(bg=colors['btn_bg'], fg=colors['btn_fg'])
    file_button.configure(bg=colors['btn_bg'], fg=colors['btn_fg'])
    clear_console_button.configure(bg=colors['btn_bg'], fg=colors['btn_fg'])
    exit_button.configure(bg=colors['btn_bg'], fg=colors['btn_fg'])  # Apply theme to exit button

    # Apply style to the combobox (theme selector)
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TCombobox", fieldbackground=colors['btn_bg'], background=colors['btn_bg'], foreground=colors['btn_fg'])

# Function to clear console output
def clear_console():
    console_log.configure(state="normal")  # Enable editing temporarily
    console_log.delete("1.0", tk.END)
    console_log.configure(state="disabled")  # Disable editing

# Set up main application window
root = tk.Tk()
root.title("Enhanced Python Code Runner")

# Set full screen, disable resizing, and remove title bar
root.attributes("-fullscreen", True)
root.resizable(False, False)
root.overrideredirect(True)  # Remove window decorations

# Frame for Code Input
code_frame = tk.Frame(root, bg="white")
code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

code_label = tk.Label(code_frame, text="Code Input", font=("Arial", 12, "bold"), bg="white")
code_label.pack(anchor="w", pady=(0, 5))

# Frame for line numbers and code entry
entry_frame = tk.Frame(code_frame, bg="white")
entry_frame.pack(fill=tk.BOTH, expand=True)

# Line numbers
line_numbers = scrolledtext.ScrolledText(entry_frame, width=4, state="disabled", font=("Courier New", 10), wrap="none")
line_numbers.pack(side="left", fill="y")

# Code entry
code_entry = scrolledtext.ScrolledText(entry_frame, height=10, wrap=tk.WORD, font=("Courier New", 10))
code_entry.pack(side="right", fill=tk.BOTH, expand=True)
code_entry.bind("<KeyRelease>", lambda event: update_line_numbers())

# Frame for Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(fill=tk.X, pady=5)

run_button = tk.Button(button_frame, text="Save C++ File", command=run_code, font=("Arial", 10))
run_button.pack(side=tk.LEFT, padx=5)

file_button = tk.Button(button_frame, text="Run Python File", command=run_file, font=("Arial", 10))
file_button.pack(side=tk.LEFT, padx=5)

clear_console_button = tk.Button(button_frame, text="Clear Console", command=clear_console, font=("Arial", 10))
clear_console_button.pack(side=tk.LEFT, padx=5)

# Theme Selector and Exit Button Frame
theme_frame = tk.Frame(root, bg="white")
theme_frame.pack(fill=tk.X, pady=5, anchor="ne", padx=5)

theme_label = tk.Label(theme_frame, text="Select Theme:", font=("Arial", 10), bg="white")
theme_label.pack(side=tk.LEFT)

theme_selector = ttk.Combobox(theme_frame, values=list(themes.keys()), font=("Arial", 10), state="readonly")
theme_selector.current(0)
theme_selector.pack(side=tk.LEFT, padx=5)
theme_selector.bind("<<ComboboxSelected>>", lambda event: apply_theme(theme_selector.get()))

# Exit Button
exit_button = tk.Button(theme_frame, text="Exit", command=root.quit, font=("Arial", 10))
exit_button.pack(side=tk.RIGHT, padx=5)

# Frame for Console Output
console_frame = tk.Frame(root, bg="white")
console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

console_label = tk.Label(console_frame, text="Console Output", font=("Arial", 12, "bold"), bg="white")
console_label.pack(anchor="w", pady=(0, 5))

console_log = scrolledtext.ScrolledText(console_frame, height=15, wrap=tk.WORD, state="disabled", font=("Courier New", 10))
console_log.pack(fill=tk.BOTH, expand=True)

# Entry for user input
input_entry = tk.Entry(root, font=("Arial", 10))
input_entry.pack(fill=tk.X, padx=10, pady=(5, 10))

# Start with the default theme
apply_theme("Light Mode")

# Start the application
root.mainloop()
