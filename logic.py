import random
import string
import fitz  # PyMuPDF for PDF handling
from fpdf import FPDF

def extract_students_from_pdf(pdf_path):
    """Extract student names from a PDF file."""
    student_list = []
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text = page.get_text()
                student_list.extend(text.splitlines())
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")
    return [name.strip() for name in student_list if name.strip()]

def generate_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def create_passwords(student_list, password_length=8):
    """Create a dictionary of students with their passwords."""
    passwords = {}
    for student in student_list:
        passwords[student] = generate_password(password_length)
    return passwords

def save_passwords_to_pdf(passwords, save_path):
    """Save the passwords to a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add table header
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(90, 10, "Student", border=1, align="C")
    pdf.cell(90, 10, "Password", border=1, align="C")
    pdf.ln()

    # Add rows
    pdf.set_font("Arial", size=12)
    for student, password in passwords.items():
        pdf.cell(90, 10, student, border=1)
        pdf.cell(90, 10, password, border=1)
        pdf.ln()

    pdf.output(save_path)
