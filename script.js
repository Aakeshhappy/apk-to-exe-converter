document.getElementById('uploadForm').addEventListener('submit', async function (event) {
  event.preventDefault();
  const apkFile = document.getElementById('apkFile').files[0];

  if (apkFile) {
    document.getElementById('statusMessage').innerText = 'Uploading and converting your file...';
    document.getElementById('statusMessage').style.color = 'yellow';

    const formData = new FormData();
    formData.append('file', apkFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to convert the file.');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = apkFile.name.replace(/\.(apk|xapk)$/, '.exe');
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);

      document.getElementById('statusMessage').innerText = 'Conversion complete! Downloading your EXE file.';
      document.getElementById('statusMessage').style.color = 'green';
    } catch (error) {
      console.error(error);
      document.getElementById('statusMessage').innerText = 'An error occurred during the conversion.';
      document.getElementById('statusMessage').style.color = 'red';
    }
  }
});
