    const fileInput = document.getElementById('id_image');
    const placeholder = document.getElementById('upload-placeholder');
    const fileInfo = document.getElementById('file-info');
    const filenameLabel = document.getElementById('filename');
    const resetButton = document.getElementById('reset-upload');

    fileInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            filenameLabel.textContent = this.files[0].name;
            placeholder.classList.add('hidden');
            fileInfo.classList.remove('hidden');
        }
    });

    resetButton.addEventListener('click', function(e) {
        e.preventDefault();
        fileInput.value = '';
        fileInfo.classList.add('hidden');
        placeholder.classList.remove('hidden');
    });