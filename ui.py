import customtkinter as ctk
from tkinter import filedialog, messagebox
from logic import extract_students_from_pdf, create_passwords, save_passwords_to_pdf

# Initialize custom tkinter
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Student Password Generator")
        self.geometry("600x500")
        self.passwords = {}

        # PDF File Selection
        self.label_pdf = ctk.CTkLabel(self, text="Select PDF File:")
        self.label_pdf.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_pdf = ctk.CTkEntry(self, width=300)
        self.entry_pdf.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.btn_browse = ctk.CTkButton(self, text="Browse", command=self.browse_file)
        self.btn_browse.grid(row=0, column=2, padx=10, pady=10)

        # Password Length
        self.label_length = ctk.CTkLabel(self, text="Password Length:")
        self.label_length.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_length = ctk.CTkEntry(self, width=50)
        self.entry_length.insert(0, "8")  # Default value
        self.entry_length.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Generate Passwords Button
        self.btn_generate = ctk.CTkButton(self, text="Generate Passwords", command=self.generate_passwords)
        self.btn_generate.grid(row=2, column=0, columnspan=3, pady=10)

        # Result Text
        self.result_text = ctk.CTkTextbox(self, width=550, height=200)
        self.result_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Save to PDF Button
        self.btn_save_pdf = ctk.CTkButton(self, text="Save to PDF", command=self.save_to_pdf)
        self.btn_save_pdf.grid(row=4, column=0, columnspan=3, pady=10)

    def browse_file(self):
        """Open file dialog to select PDF."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        self.entry_pdf.delete(0, "end")
        self.entry_pdf.insert(0, file_path)

    def generate_passwords(self):
        """Generate passwords for students."""
        pdf_path = self.entry_pdf.get()
        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        try:
            student_list = extract_students_from_pdf(pdf_path)
            if not student_list:
                messagebox.showerror("Error", "No student names found in the PDF.")
                return

            try:
                password_length = int(self.entry_length.get())
            except ValueError:
                messagebox.showerror("Error", "Password length must be a number.")
                return

            self.passwords = create_passwords(student_list, password_length)
            self.result_text.delete("1.0", "end")
            for student, password in self.passwords.items():
                self.result_text.insert("end", f"{student}: {password}\n")

            messagebox.showinfo("Success", "Passwords generated successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_to_pdf(self):
        """Save the generated passwords to a PDF."""
        if not self.passwords:
            messagebox.showerror("Error", "No passwords to save. Please generate them first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not save_path:
            return

        try:
            save_passwords_to_pdf(self.passwords, save_path)
            messagebox.showinfo("Success", f"Passwords saved to '{save_path}'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
