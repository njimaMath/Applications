# Interactive Web Tools

This directory contains three interactive web applications intended for educational and productivity use:

1. **Phonics Quiz App**
2. **LaTeX Comment Remover**
3. **Referee Automation**

---

## 1. Phonics Quiz App

**Link**: [https://njima091.github.io/appNakajima/soundEnglish/index.html](https://njima091.github.io/appNakajima/soundEnglish/index.html)

### Description

This is a browser-based phonics quiz tool designed to help learners distinguish between similar English sounds. It covers common pronunciation challenges faced by non-native speakers.

### Features

- Five sound categories:
  - **L vs R**
  - **Th vs S**
  - **V vs B**
  - **N vs NT (Negation practice)**
  - **Vowel pairs**
- Option to take a **Mixed Quiz** combining all categories.
- Audio playback using browser's speech synthesis.
- Responsive layout (mobile-friendly).
- Instant feedback with sound effects for correct/incorrect answers.
- Final score display and feedback message.

### Technical Notes

- Built with **React (via CDN)** and **Tailwind CSS**.
- No server-side processing—fully client-side.
- Audio is generated using `SpeechSynthesisUtterance`; no external audio files are required (except for correct/wrong sounds).

---

## 2. LaTeX Comment Remover

**Link**: [https://njima091.github.io/appNakajima/latexCommentOut/index.html](https://njima091.github.io/appNakajima/latexCommentOut/index.html)

### Description

This tool removes LaTeX comments and `\iffalse...\fi` blocks from pasted LaTeX source text. It is useful for preparing clean LaTeX files, especially before submissions or public sharing.

### Features

- Removes:
  - Comments beginning with `%`
  - Blocks between `\iffalse` and `\fi` (including nested ones)
- Optional preservation of empty lines.
- Three user controls:
  - Remove `%` comments
  - Remove `\iffalse...\fi`
  - Preserve empty lines
- Output can be copied to clipboard.
- Clear button to reset inputs.

### Technical Notes

- Pure HTML, CSS, and JavaScript—no frameworks.
- Inline JavaScript implements all logic client-side.
- Comment parsing includes escape-aware `%` detection and proper nesting for `\iffalse`.

---

## 3. Referee Automation

**Location**: `refereeAutomation/`

### Description

The Referee Automation application is a web-based tool designed to assist academic paper reviewers by automating common tasks in the review process. It provides PDF to LaTeX conversion and grammar/spell checking capabilities.

### Features

- **PDF to LaTeX Conversion**: Upload PDF documents and convert them to LaTeX format using PyPDF2
- **Grammar and Spell Checking**: AI-powered grammar and spell checking for LaTeX documents
- **File Download**: Download converted LaTeX files for further editing
- **Error Reporting**: Detailed error reports with line numbers and suggestions
- **Web Interface**: Clean, responsive web interface for easy file management

### Technical Notes

- Built with **Flask** web framework
- Uses **PyPDF2** for PDF text extraction
- Integrates with **GROQ API** via OpenRouter for grammar checking
- Frontend uses vanilla **HTML, CSS, and JavaScript**
- File uploads handled with proper validation and error handling

### Installation and Usage

1. Navigate to the `refereeAutomation/` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Configure API key in `.env` file (copy from `.env.template`)
4. Run: `python app.py`
5. Open browser to `http://localhost:5000`

---

## License

This repository is released under the MIT License unless otherwise stated.
