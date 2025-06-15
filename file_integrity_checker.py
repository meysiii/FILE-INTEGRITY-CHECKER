
import os
import hashlib
import json

# ----------------------------
# FILE INTEGRITY CHECKER TOOL
# ----------------------------

# Function to compute SHA256 hash of a file
def compute_file_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            while chunk := file.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

# Build hash records for all files in a directory
def build_hash_database(folder_path, output_file='file_hashes.json'):
    hash_record = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = compute_file_hash(full_path)
            if file_hash:0
            hash_record[full_path] = file_hash

    with open(output_file, 'w') as f:
        json.dump(hash_record, f, indent=4)
    print(f"Hash database created and saved to {output_file}")

# Compare current file hashes to stored hashes
def check_file_integrity(folder_path, hash_file='file_hashes.json'):
    try:
        with open(hash_file, 'r') as f:
            saved_hashes = json.load(f)
    except FileNotFoundError:
        print("Hash file not found. Please run the hash builder first.")
        return

    for filepath, saved_hash in saved_hashes.items():
        current_hash = compute_file_hash(filepath)
        if current_hash != saved_hash:
            print(f"[MODIFIED] {filepath}")
        else:
            print(f"[UNCHANGED] {filepath}")

# Example execution (uncomment to run)
# build_hash_database('folder_name')
# check_file_integrity('folder_name')
