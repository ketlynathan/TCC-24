import os

def check_file_encoding(directory):
    print(f"Checking encoding for files in: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                with open(os.path.join(root, file), 'rb') as f:
                    f.read().decode('utf-8')
            except UnicodeDecodeError:
                print(f"Non-UTF-8 encoded file: {os.path.join(root, file)}")

check_file_encoding('c:/Users/gener/OneDrive/Workspace/Treino 2024/TCC')  # Adjust the path if needed
