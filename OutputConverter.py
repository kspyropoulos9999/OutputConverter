from reportlab.pdfgen import canvas
from dominate import document
from dominate.tags import pre, h1
import sys
from io import StringIO
from fpdf import FPDF

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def run_python_code(code):
    try:
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        exec(code, globals())

        output = sys.stdout.getvalue()
        return output
    except Exception as e:
        return f"Error: {e}"
    finally:
        sys.stdout = original_stdout

def get_user_code():
    print("Enter your Python code (press Ctrl+D on a new line to finish):")
    code_lines = []
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        return '\n'.join(code_lines)

def generate_pdf(code, output_file='output.pdf'):
    output = run_python_code(code)

    # Encode the output as UTF-8
    output_utf8 = output.encode('utf-8')

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Python Code Output', 0, 1, 'C')

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(4)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Python Code Output:')
    pdf.chapter_body(output_utf8.decode('utf-8'))
    pdf.output(output_file)

def generate_html(code, output_file='output.html'):
    output = run_python_code(code)

    doc = document()
    with doc:
        h1("Python Code Output:")
        pre(output)

    with open(output_file, 'w') as f:
        f.write(doc.render())

if __name__ == "__main__":
    user_code = get_user_code()
    generate_pdf(user_code)
    generate_html(user_code)
