import os
from PIL import Image, ExifTags

def create_directory(directory):
    os.makedirs(directory, exist_ok=True)

def get_correct_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(orientation)
            if orientation == 3:
                return image.rotate(180, expand=True)
            elif orientation == 6:
                return image.rotate(270, expand=True)
            elif orientation == 8:
                return image.rotate(90, expand=True)
    except Exception as e:
        print(f"Could not get orientation for image: {e}")
    return image

def separate_images(folder_path):
    portrait_folder = os.path.join(folder_path, 'Portrait')
    landscape_folder = os.path.join(folder_path, 'Landscape')

    create_directory(portrait_folder)
    create_directory(landscape_folder)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isdir(file_path):
            continue

        try:
            with Image.open(file_path) as img:
                img = get_correct_orientation(img)
                width, height = img.size
                print(f"Processing {filename}: width={width}, height={height}")

                destination_folder = portrait_folder if width < height else landscape_folder
                new_path = os.path.join(destination_folder, filename)

            os.rename(file_path, new_path)
            print(f'Moved {filename} to {destination_folder}')

        except Exception as e:
            print(f'Could not process {filename}: {e}')

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing the images: ")
    separate_images(folder_path)
