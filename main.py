import shutil
import sys
from pathlib import Path

preview = input("Preview only? (y/n): ").strip().lower() == "y"
input_folder = input("Enter the path of the folder to organize: ").strip()
if input_folder == "":
    print("Invalid input. Please provide a valid folder path.")
    sys.exit(1)
folder = Path(input_folder)
protected_folders = ["images", "documents", "music"]
if folder.name.lower() in protected_folders:
    print(f"Cannot organize the folder '{folder.name}' as it is a protected folder.")
    sys.exit(1)
if not folder.exists() or not folder.is_dir():
    print("Invalid folder path. Please provide a valid directory.")
    sys.exit(1)
confirmation = (
    input(f"Are you sure you want to organize the folder '{folder}'? (y/n): ")
    .strip()
    .lower()
)
if confirmation != "y":
    print("Operation cancelled.")
    sys.exit(0)

images_folder = folder / "Images"
documents_folder = folder / "Documents"
music_folder = folder / "Music"

if not preview:
    images_folder.mkdir(exist_ok=True)
    documents_folder.mkdir(exist_ok=True)
    music_folder.mkdir(exist_ok=True)


def move_files(file, destination_folder):
    destination = destination_folder / file.name
    print(f"Processing: {file.name}")
    if destination.exists():
        print(f"File {file.name} already exists in {destination_folder}. Renaming...")
        counter = 1
        new_name = f"{file.stem}_copy{counter}{file.suffix}"
        while (destination_folder / new_name).exists():
            counter += 1
            new_name = f"{file.stem}_copy{counter}{file.suffix}"
        shutil.move(file, destination_folder / new_name)
    else:
        shutil.move(file, destination_folder / file.name)


file_types = {
    ".jpg": images_folder,
    ".png": images_folder,
    ".pdf": documents_folder,
    ".txt": documents_folder,
    ".mp3": music_folder,
}

organizer_count = 0
unsupported_count = 0
preview_count = 0

for i in folder.iterdir():
    if not i.is_file():
        continue
    destination_folder = file_types.get(i.suffix.lower())
    if destination_folder is None:
        print(f"File {i.name} has an unsupported file type. Skipping.")
        unsupported_count += 1
    else:
        if preview:
            print(f"Preview: Would move {i.name} to {destination_folder}")
            preview_count += 1
        else:
            move_files(i, destination_folder)
            organizer_count += 1

if preview:
    print("\n---Preview Summary---")
    print(f"Files that would be organized : {preview_count}")
    print("No files were moved.")
else:
    print("\n---Organization Summary---")
    print(f"Files organized: {organizer_count}")

print(f"Unsupported files: {unsupported_count}")
