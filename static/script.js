document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const imageInput = document.getElementById('imageInput');
    const fileLabel = document.getElementById('fileLabel');
    const preview = document.getElementById('preview');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const results = document.getElementById('results');
    const submitBtn = document.getElementById('submitBtn');

    // Update file label when files are selected
    imageInput.addEventListener('change', function(e) {
        const files = e.target.files;
        if (files.length > 0) {
            fileLabel.textContent = `${files.length} image(s) selected`;
            showPreview(files);
        } else {
            fileLabel.textContent = 'Choose images...';
            preview.innerHTML = '';
        }
    });

    // Show image previews
    function showPreview(files) {
        preview.innerHTML = '';
        Array.from(files).forEach(file => {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const div = document.createElement('div');
                    div.className = 'preview-image';
                    div.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                    preview.appendChild(div);
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const files = imageInput.files;
        if (files.length === 0) {
            showError('Please select at least one image');
            return;
        }

        // Hide previous results and errors
        error.style.display = 'none';
        results.style.display = 'none';

        // Show loading
        loading.style.display = 'block';
        submitBtn.disabled = true;

        try {
            const formData = new FormData();
            Array.from(files).forEach(file => {
                formData.append('images', file);
            });

            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate 3D model');
            }

            showResults(data);
        } catch (err) {
            showError(err.message);
        } finally {
            loading.style.display = 'none';
            submitBtn.disabled = false;
        }
    });

    function showResults(data) {
        results.style.display = 'block';
        
        const html = `
            <div class="result-card">
                <span class="success-badge">✓ Generation Complete</span>
                
                <div class="result-item">
                    <span class="result-label">Images Uploaded:</span>
                    <span class="result-value">${data.num_images}</span>
                </div>
                
                <div class="result-item">
                    <span class="result-label">Views Processed:</span>
                    <span class="result-value">${data.num_views_processed}</span>
                </div>
                
                <div class="result-item">
                    <span class="result-label">Output File:</span>
                    <span class="result-value">${data.output_file}</span>
                </div>
                
                <a href="${data.download_url}" class="download-btn" download>
                    📥 Download 3D Model
                </a>
            </div>
        `;
        
        document.getElementById('resultsContent').innerHTML = html;
        
        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function showError(message) {
        error.textContent = `Error: ${message}`;
        error.style.display = 'block';
        error.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
