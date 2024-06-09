import tkinter as tk
from samoosa.logic import logic_samoosa


def main_function():
    def on_button_click():
        global entry_text
        entry_text = entry.get()
        if entry_text:
            entry.delete(0, tk.END)
            result_text.insert(tk.END, "Wait for the response...")

            root.update()
            result_text.delete("1.0", tk.END)
            summarised_text = logic_samoosa(entry_text)
            result_text.insert(tk.END, summarised_text)


    # Create the main window
    root = tk.Tk()
    root.geometry("900x900")  # Set window size
    root.title("Samoosa | Summarise Youtube Video!")  # Set window title
    root.configure(bg="#151515")
    # Create a StringVar to associate with the label
    text_var = tk.StringVar()
    text_var.set("Enter the Youtube Video URL:")

    # Create the label widget with all options
    label = tk.Label(root,
                     textvariable=text_var,
                     anchor=tk.CENTER,
                     bg="#EEEEEE",
                     height=1,
                     width=25,
                     bd=3,
                     font=("Arial", 16, "bold"),
                     cursor="hand2",
                     fg="#322C2B",
                     padx=15,
                     pady=15,
                     justify=tk.CENTER,
                     relief=tk.RAISED,
                     underline=0,
                     wraplength=250
                    )
    entry = tk.Entry(root,
                     width=40,
                     font=("Arial", 12)
                    )
    # Create the button widget
    button = tk.Button(root, text="Summarise", command=on_button_click)
    # Create the text widget
    result_text = tk.Text(root,
                          height=20,
                          width=50,
                          font=("Arial", 12)
                         )

    # Pack the label into the window
    label.pack(pady=20)  # Add some padding to the top
    entry.pack(pady=10)
    button.pack(pady=10)
    result_text.pack(pady=10)
    # Run the main event loop
    root.mainloop()
