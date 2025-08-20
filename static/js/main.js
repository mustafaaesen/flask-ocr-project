document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const loader = document.getElementById('loader');
    const output = document.getElementById('output');
    output.textContent = '';
    loader.style.display = 'block';

    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    formData.append('image', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loader.style.display = 'none';
        if (data.text) {
            output.textContent = data.text;
        } else {
            output.textContent = 'Metin algılanamadı.';
        }
    })
    .catch(error => {
        loader.style.display = 'none';
        output.textContent = 'Hata oluştu: ' + error;
    });
});
