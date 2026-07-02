document.addEventListener('DOMContentLoaded', () => {
<<<<<<< HEAD
    const filePayloadInput = document.getElementById('documentPayloadInput');
    const fileStatusDisplay = document.getElementById('fileStatusDisplay');
    const asyncUploadForm = document.getElementById('asyncUploadForm');
    const runtimeResponseSection = document.getElementById('runtimeResponseSection');
    const runtimeStateIcon = document.getElementById('runtimeStateIcon');
    const runtimeStatusText = document.getElementById('runtimeStatusText');
    const analyticalResultViewport = document.getElementById('analyticalResultViewport');

    // Smooth Interactive Input Visual Name Updater Node Loop
    if (filePayloadInput && fileStatusDisplay) {
        filePayloadInput.addEventListener('change', (event) => {
            if (event.target.files.length > 0) {
                fileStatusDisplay.innerHTML = `Target Package Initialized: <span class="text-sky-400 font-bold">${event.target.files[0].name}</span>`;
            } else {
                fileStatusDisplay.textContent = 'Drag & drop your PDF package here, or click to browse workspace';
            }
        });
    }

    // Dynamic Server Transmission Request Handler
    if (asyncUploadForm) {
        asyncUploadForm.addEventListener('submit', async (formEvent) => {
            formEvent.preventDefault();

            if (!filePayloadInput || filePayloadInput.files.length === 0) return;

            const dynamicFormData = new FormData();
            dynamicFormData.append('file', filePayloadInput.files[0]);

            // Activate Loader Terminal Interface Blocks Viewports Properties
            if (runtimeResponseSection) runtimeResponseSection.classList.remove('hidden-element');
            if (runtimeStateIcon) runtimeStateIcon.textContent = '⚙';
            if (runtimeStatusText) {
                runtimeStatusText.textContent = 'Parsing binary data matrices... Cloud processing active.';
                runtimeStatusText.style.color = '#eab308';
            }
            if (analyticalResultViewport) {
                analyticalResultViewport.innerHTML = '<div class="py-10 text-center text-slate-400 animate-pulse">Running advanced document visual block text structure transformation mapping layers on Gemini 1.5 Node Pipeline Engine... Please hold on...</div>';
            }

            try {
                const rawNetworkResponse = await fetch('/upload', {
                    method: 'POST',
                    body: dynamicFormData
                });

                const parsedJsonPayload = await rawNetworkResponse.json();

                if (rawNetworkResponse.ok) {
                    if (runtimeStateIcon) {
                        runtimeStateIcon.textContent = '✔';
                    }
                    if (runtimeStatusText) {
                        runtimeStatusText.textContent = 'Cognitive Execution Pipeline Successfully Completed!';
                        runtimeStatusText.style.color = '#10b981';
                    }
                    
                    // SAFE HTML INJECTION INSTEAD OF TEXT INTERPOLATION CLASH VALUE BREAKS
                    if (analyticalResultViewport) {
                        analyticalResultViewport.innerHTML = parsedJsonPayload.analysis_payload;
                    }
                } else {
                    throw new Error(parsedJsonPayload.error || 'The core server module pipeline execution script faulted.');
                }

            } catch (pipelineException) {
                if (runtimeStateIcon) {
                    runtimeStateIcon.textContent = '❌';
                }
                if (runtimeStatusText) {
                    runtimeStatusText.textContent = 'Pipeline Intercept Network Level Failure Fault.';
                    runtimeStatusText.style.color = '#ef4444';
                }
                if (analyticalResultViewport) {
                    analyticalResultViewport.innerHTML = `<div class="p-4 bg-red-950/40 border border-red-800 rounded-xl text-red-400 font-mono text-sm"><span class="font-bold underline">Error Core Signature:</span> ${pipelineException.message}</div>`;
                }
            }
        });
    }
=======
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
>>>>>>> 9dc707d0c301ea8eac622df7df43edb609886e00
});