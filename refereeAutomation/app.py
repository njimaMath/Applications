from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import subprocess
import os
import sys

app = Flask(__name__, static_url_path='', static_folder='static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

PYTHON_EXECUTABLE = sys.executable

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        safe_name = secure_filename(file.filename)
        pdf_filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        file.save(pdf_filepath)

        # Convert PDF to LaTeX
        base_name, _ = os.path.splitext(safe_name)
        latex_filename = f"{base_name}.tex"
        latex_filepath = os.path.join(app.config['UPLOAD_FOLDER'], latex_filename)
        try:
            result = subprocess.run(
                [
                    PYTHON_EXECUTABLE,
                    os.path.join(BASE_DIR, 'pdf_to_latex.py'),
                    pdf_filepath,
                    latex_filepath,
                ],
                capture_output=True,
                text=True,
                check=True,
                cwd=BASE_DIR,
            )
            print(f"PDF conversion successful: {result.stdout}")
            return jsonify({'latex_file': os.path.basename(latex_filename)})
        except subprocess.CalledProcessError as e:
            print(f"Error converting PDF to LaTeX: {e}")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
            return jsonify({'error': f'Error converting PDF to LaTeX: {e.stderr}'}), 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type, please upload a PDF'}), 400

@app.route('/uploads/<filename>')
def download_file(filename):
    """Serve files from the uploads directory"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/check', methods=['POST'])
def check_grammar():
    latex_file = request.json.get('latex_file')
    if not latex_file:
        return jsonify({'error': 'No LaTeX file specified'}), 400

    latex_filepath = os.path.join(app.config['UPLOAD_FOLDER'], latex_file)
    if not os.path.exists(latex_filepath):
        return jsonify({'error': 'LaTeX file not found'}), 404

    try:
        result = subprocess.run(
            [
                PYTHON_EXECUTABLE,
                os.path.join(BASE_DIR, 'spell_grammar_check.py'),
                latex_filepath,
            ],
            capture_output=True,
            text=True,
            check=True,
            cwd=BASE_DIR,
        )
        
        # Process the output to create a structured list of errors
        errors = []
        # This is a placeholder for the actual parsing of the output
        # You will need to adjust this based on the actual output of your spell_grammar_check.py script
        output_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        for line in output_lines:
            parts = line.split(':')
            if len(parts) >= 3:
                errors.append({
                    'line': parts[0],
                    'mistake': parts[1],
                    'suggestion': ':'.join(parts[2:])
                })
        return jsonify({'errors': errors})
    except subprocess.CalledProcessError as e:
        print(f"Error checking grammar: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return jsonify({'error': f'Error checking grammar: {e.stderr}'}), 500
    except Exception as e:
        print(f"Unexpected error during grammar check: {e}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
