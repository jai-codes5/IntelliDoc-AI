document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInputNode');
    const fileDisplay = document.getElementById('fileInfoDisplay');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtnNode');
    const loadingBox = document.getElementById('loadingBox');
    const errorBox = document.getElementById('errorBox');
    const errorMessage = document.getElementById('errorMessage');
    const outputArea = document.getElementById('outputArea');

    fileInput.addEventListener('change', (e) => {
        if(e.target.files.length > 0) {
            fileDisplay.textContent = `Target Payload: ${e.target.files[0].name}`;
            fileDisplay.style.display = 'block';
            errorBox.style.display = 'none';
            outputArea.style.display = 'none';
        }
    });

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if(fileInput.files.length === 0) {
            alert("Please select a file first!");
            return;
        }

        submitBtn.disabled = true;
        loadingBox.style.display = 'block';
        errorBox.style.display = 'none';
        outputArea.style.display = 'none';

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Internal Server Pipeline Exception");
            }

            loadingBox.style.display = 'none';
            outputArea.innerHTML = result.analysis_payload;
            outputArea.style.display = 'block';
        } catch (err) {
            loadingBox.style.display = 'none';
            errorMessage.textContent = err.message;
            errorBox.style.display = 'block';
        } finally {
            submitBtn.disabled = false;
        }
    });
});