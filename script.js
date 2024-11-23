document.getElementById('uploadForm').addEventListener('submit', function (event) {
  event.preventDefault();
  const apkFile = document.getElementById('apkFile').files[0];

  if (apkFile) {
    document.getElementById('statusMessage').innerText = 'Processing your APK file...';
    document.getElementById('statusMessage').style.color = 'yellow';
    document.getElementById('downloadLink').style.display = 'none';

    // Simulate file upload and trigger GitHub Actions
    // This is a simulation; you will need to actually upload the file to GitHub (perhaps via API)
    setTimeout(() => {
      document.getElementById('statusMessage').innerText = 'APK successfully uploaded and being converted!';
      document.getElementById('statusMessage').style.color = 'green';
      document.getElementById('downloadLink').style.display = 'block';
    }, 2000);
  }
});
