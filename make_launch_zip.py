import zipfile
import os

# Define root and folders to include
root = '/home/puyuam/.openclaw/workspace'
folders = ['GUMROAD', 'SAMPLES', 'LEADS', 'ASSETS', 'EMAILS']

# Create ZIP
zip_path = os.path.join(root, 'ROOTED-NAME-LAUNCH-KIT.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for folder in folders:
        folder_path = os.path.join(root, folder)
        if not os.path.exists(folder_path):
            continue
        for dirpath, _, filenames in os.walk(folder_path):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                arcname = os.path.relpath(file_path, root)
                zipf.write(file_path, arcname)

print(f'✅ ZIP created: {zip_path}')