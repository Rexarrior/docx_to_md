"""
Script to check the contents of a ZIP file.
"""
import zipfile
import sys

def main():
    zip_path = "test_output/example_min.zip"
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            print(f"Contents of {zip_path}:")
            for i, item in enumerate(zip_ref.namelist(), 1):
                print(f"{i}. {item}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 