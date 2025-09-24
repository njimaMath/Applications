
document.addEventListener('DOMContentLoaded', () => {
    const pdfUpload = document.getElementById('pdf-upload');
    const uploadBtn = document.getElementById('upload-btn');
    const downloadSection = document.getElementById('download-section');
    const downloadYes = document.getElementById('download-yes');
    const downloadNo = document.getElementById('download-no');
    const checkBtn = document.getElementById('check-btn');
    const errorList = document.getElementById('error-list');

    let latexFileName = null;

    uploadBtn.addEventListener('click', () => {
        const file = pdfUpload.files[0];
        if (!file) {
            alert('Please select a PDF file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                latexFileName = data.latex_file;
                downloadSection.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            alert('An error occurred while uploading the file.');
        });
    });

    downloadYes.addEventListener('click', () => {
        if (latexFileName) {
            // Create a temporary link element to trigger download
            const link = document.createElement('a');
            link.href = `/uploads/${latexFileName}`;
            link.download = latexFileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        downloadSection.style.display = 'none';
    });

    downloadNo.addEventListener('click', () => {
        downloadSection.style.display = 'none';
    });

    checkBtn.addEventListener('click', () => {
        if (!latexFileName) {
            alert('Please upload a PDF and convert it to LaTeX first.');
            return;
        }

        fetch('/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ latex_file: latexFileName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                errorList.innerHTML = '';
                if (data.errors.length === 0) {
                    errorList.innerHTML = '<p>No errors found.</p>';
                } else {
                    data.errors.forEach(error => {
                        const errorDiv = document.createElement('div');
                        errorDiv.classList.add('error');
                        errorDiv.innerHTML = `
                            <div><span class="line">Line ${error.line}:</span></div>
                            <div><span class="mistake">Mistake:</span> ${error.mistake}</div>
                            <div><span class="suggestion">Suggestion:</span> ${error.suggestion}</div>
                        `;
                        errorList.appendChild(errorDiv);
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error checking for errors:', error);
            alert('An error occurred while checking for errors.');
        });
    });
});
