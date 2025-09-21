from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__, static_url_path='', static_folder='static')

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Convert PDF to LaTeX
        latex_filename = filename.replace('.pdf', '.tex')
        try:
            subprocess.run(['python', 'pdf_to_latex.py', filename, latex_filename], check=True)
            return jsonify({'latex_file': os.path.basename(latex_filename)})
        except subprocess.CalledProcessError as e:
            return jsonify({'error': f'Error converting PDF to LaTeX: {e}'}), 500
    else:
        return jsonify({'error': 'Invalid file type, please upload a PDF'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/check', methods=['POST'])
def check_grammar():
    latex_file = request.json.get('latex_file')
    if not latex_file:
        return jsonify({'error': 'No LaTeX file specified'}), 400

    latex_filepath = os.path.join(app.config['UPLOAD_FOLDER'], latex_file)
    if not os.path.exists(latex_filepath):
        return jsonify({'error': 'LaTeX file not found'}), 404

    try:
        result = subprocess.run(['python', 'spell_grammar_check.py', latex_filepath], capture_output=True, text=True, check=True)
        # Process the output to create a structured list of errors
        errors = []
        # This is a placeholder for the actual parsing of the output
        # You will need to adjust this based on the actual output of your spell_grammar_check.py script
        for line in result.stdout.strip().split('\n'):
            parts = line.split(':')
            if len(parts) >= 3:
                errors.append({
                    'line': parts[0],
                    'mistake': parts[1],
                    'suggestion': ':'.join(parts[2:])
                })
        return jsonify({'errors': errors})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Error checking grammar: {e.stderr}'}), 500

if __name__ == '__main__':
    app.run(debug=True)