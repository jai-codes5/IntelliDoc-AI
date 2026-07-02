document.addEventListener('DOMContentLoaded', () => {
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
});