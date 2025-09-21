
import PyPDF2
import sys

def pdf_to_latex(pdf_path, latex_path):
    """
    Extracts text from a PDF and saves it as a LaTeX file.

    Args:
        pdf_path (str): The path to the input PDF file.
        latex_path (str): The path to the output LaTeX file.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Basic LaTeX escaping
            text = text.replace('\', '\textbackslash{}')
            text = text.replace('{', '\{')
            text = text.replace('}', '\}')
            text = text.replace('#', '\#')
            text = text.replace('$', '\$')
            text = text.replace('%', '\%')
            text = text.replace('&', '\&')
            text = text.replace('_', '\_')
            text = text.replace('^', '\textasciicircum{}')
            text = text.replace('~', '\textasciitilde{}')


            latex_content = f"""
\documentclass{{article}}
\usepackage[utf8]{{inputenc}}

\begin{{document}}

{text}

\end{{document}}
"""

            with open(latex_path, 'w', encoding='utf-8') as latex_file:
                latex_file.write(latex_content)

            print(f"Successfully converted {pdf_path} to {latex_path}")

    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_latex.py <path_to_pdf_file> <path_to_latex_file>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    latex_file_path = sys.argv[2]
    pdf_to_latex(pdf_file_path, latex_file_path)
