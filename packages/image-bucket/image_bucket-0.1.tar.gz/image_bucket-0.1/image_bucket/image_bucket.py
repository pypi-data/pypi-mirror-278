import argparse
import cv2
import os
import shutil

description = """Bucket images into subdirectories with one key press.

This will show you each image. Use j/k for next/previous, q to quit and confirm. Any other letter or number will tag that image to go to a subdirectory of that name. E.g. hit "a" to put the image under `a/`.
"""

def parse_args():
    parser = argparse.ArgumentParser(prog='image_bucket', description=description)
    parser.add_argument('files', nargs='*')
    parsed = parser.parse_args()
    return parsed

def get_chr():
    while True:
        # Wait for a key press
        key = cv2.waitKey(1)
        if key == -1:
            continue

        if chr(key) in "abcdefghijklmnopqrstuvwxyz0123456789":
            return chr(key)

        return False

def bucket(image_files):
    index = 0
    save = False
    mapped = {}
    if len(image_files) == 0:
        return

    # Go through each image
    while True:
        image_file = image_files[index]
        image = cv2.imread(image_file)
        cv2.imshow('image', image)
        ch = get_chr()
        if ch == 'j':
            index += 1
        elif ch == 'k':
            index -= 1
        elif ch == 'q':
            save = True
            break
        elif not ch:
            break
        else:
            # If the key is one of the defined keys, move the image to the corresponding directory
            mapped[image_file] = ch
            index += 1

    # Close all active window
    cv2.destroyAllWindows()

    if save:
        for image_file, ch in mapped.items():
            target_dir = os.path.join(os.path.dirname(image_file), ch)
            target_file = os.path.join(target_dir, os.path.basename(image_file))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            shutil.move(image_file, target_file)

def main():
    args = parse_args()
    image_files = args.files
    bucket(image_files)

if __name__ == "__main__":
    main()
