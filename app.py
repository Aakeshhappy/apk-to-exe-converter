from flask import Flask, request, send_file
import os
import subprocess
import uuid
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return "No selected file", 400

    if not (uploaded_file.filename.endswith('.apk') or uploaded_file.filename.endswith('.xapk')):
        return "Unsupported file type", 400

    file_id = str(uuid.uuid4())
    input_file_path = os.path.join(UPLOAD_FOLDER, file_id + os.path.splitext(uploaded_file.filename)[-1])
    output_file_path = os.path.join(CONVERTED_FOLDER, file_id + ".exe")

    uploaded_file.save(input_file_path)

    try:
        # Generate a Python wrapper for the APK/XAPK
        wrapper_script = f"""
import subprocess
def install_apk():
    subprocess.run(['scrcpy', '--install', '{input_file_path}'])
install_apk()
"""
        wrapper_path = f"{file_id}.py"
        with open(wrapper_path, "w") as f:
            f.write(wrapper_script)

        # Use PyInstaller to package the Python wrapper into an EXE
        subprocess.run(["pyinstaller", "--onefile", "--noconsole", wrapper_path], check=True)

        # Move the generated EXE to the output folder
        shutil.move(f"dist/{file_id}.exe", output_file_path)

        # Clean up temporary files
        shutil.rmtree("dist")
        os.remove(wrapper_path)
        shutil.rmtree("build")
        os.remove(f"{file_id}.spec")

        return send_file(output_file_path, as_attachment=True, download_name=os.path.basename(output_file_path))

    except Exception as e:
        return str(e), 500
    finally:
        # Clean up uploaded file
        if os.path.exists(input_file_path):
            os.remove(input_file_path)

if __name__ == "__main__":
    app.run(debug=True)
