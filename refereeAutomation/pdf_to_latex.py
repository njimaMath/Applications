import os
import shutil
import subprocess
import sys
import tempfile

def pdf_to_latex(pdf_path, latex_path):
    """
    Extracts text from a PDF and saves it as a LaTeX file.

    Args:
        pdf_path (str): The path to the input PDF file.
        latex_path (str): The path to the output LaTeX file.
    """
    try:
        text = extract_text(pdf_path)

        # Basic LaTeX escaping
        text = text.replace('\\', '\\textbackslash{}')
        text = text.replace('{', '\\{')
        text = text.replace('}', '\\}')
        text = text.replace('#', '\\#')
        text = text.replace('$', '\\$')
        text = text.replace('%', '\\%')
        text = text.replace('&', '\\&')
        text = text.replace('_', '\\_')
        text = text.replace('^', '\\textasciicircum{}')
        text = text.replace('~', '\\textasciitilde{}')

        latex_content = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}

\begin{document}

""" + text + r"""

\end{document}
"""

        with open(latex_path, 'w', encoding='utf-8') as latex_file:
            latex_file.write(latex_content)

        print(f"Successfully converted {pdf_path} to {latex_path}")

    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.", file=sys.stderr)
        raise
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        raise


def extract_text(pdf_path):
    """Extract textual content from the PDF using the mutool CLI."""
    if shutil.which('mutool') is None:
        raise RuntimeError("'mutool' is required to extract text. Install MuPDF tools and retry.")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(pdf_path)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_pattern = os.path.join(tmpdir, 'page-%d.txt')
        try:
            subprocess.run(
                ['mutool', 'draw', '-F', 'txt', '-o', output_pattern, pdf_path],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as err:
            raise RuntimeError(f"Failed to extract text using mutool: {err.stderr}") from err

        text_chunks = []
        page_num = 1
        while True:
            page_file = os.path.join(tmpdir, f'page-{page_num}.txt')
            if not os.path.exists(page_file):
                break
            with open(page_file, 'r', encoding='utf-8', errors='ignore') as pf:
                page_text = pf.read().strip()
                if page_text:
                    text_chunks.append(page_text)
            page_num += 1

        return '\n\n'.join(text_chunks)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_latex.py <path_to_pdf_file> <path_to_latex_file>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    latex_file_path = sys.argv[2]
    pdf_to_latex(pdf_file_path, latex_file_path)
