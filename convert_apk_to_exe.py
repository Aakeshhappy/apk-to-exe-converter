import subprocess
import sys
import os
import shutil

def convert_apk_to_exe(apk_file):
    # Create the Python wrapper
    with open("wrapper.py", "w") as f:
        f.write(f"""
import subprocess
def install_apk():
    subprocess.run(['scrcpy', '--install', '{apk_file}'])
install_apk()
""")
    
    # Use PyInstaller to package the wrapper into an EXE
    subprocess.run(["pyinstaller", "--onefile", "--noconsole", "wrapper.py"])

    # Move the EXE to the output folder
    if os.path.exists("dist/wrapper.exe"):
        shutil.move("dist/wrapper.exe", "output.apk-to-exe.exe")
        print("EXE file created successfully: output.apk-to-exe.exe")
    else:
        print("Failed to create EXE.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_apk_to_exe.py <path_to_apk>")
        sys.exit(1)
    
    apk_path = sys.argv[1]
    convert_apk_to_exe(apk_path)
