import argparse
import cv2
import os
import math
import shutil

description = """Bucket images into subdirectories with one key press.

This will show you each image. Use arrow keys for next/previous, Enter to quit and confirm, Escape to quit and cancel, or Backspace to clear selection for current image. Letter or number keys will tag that image to go to a subdirectory of that name. E.g. hit "a" to put the image under `a/`.
"""

def debug(*args):
    # print(*args)
    pass

def parse_args():
    parser = argparse.ArgumentParser(prog='image_bucket', description=description)
    parser.add_argument('files', nargs='*')
    parser.add_argument( '-d', '--dry', action='store_true')
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
        elif key == 27: # Escape key
            return "Cancel"
        elif key == 13: # Enter key
            return "Save"
        elif key == 2: # Left arrow key
            return "Previous"
        elif key == 0: # Up arrow key
            return "Previous"
        elif key == 3: # Right arrow key
            return "Next"
        elif key == 1: # Down arrow key
            return "Next"
        elif key == 127: # Backspace key
            return "Clear"

        debug("Unknown key", key)
        return False

def bucket(image_files):
    index = 0
    save = False
    # Map image files to subdirectories
    mapped = {}
    if len(image_files) == 0:
        return

    def jump(step):
        nonlocal index
        next = (index + step) % (len(image_files))
        debug("jumping from", index, "to", next)
        index = next

    debug("looping files", image_files)

    # Input loop: go through each image
    while True:
        image_file = image_files[index]
        image = cv2.imread(image_file)

        # Customise overlay text to indicate current selection
        text = mapped.get(image_file, "")
        font_color = (200, 0, 200)
        line_type = cv2.LINE_AA # anti-aliased looks best

        # Determine the image's size
        height, width = image.shape[:2]
        font_scale = width * 0.0025
        font_scale = max(font_scale, 1)
        position = (4, 4 + math.ceil(font_scale * 24))
        thickness = math.ceil(2 * font_scale)

        shadow_color = (0, 200, 0)
        shadow_offset = 2
        for pos in [(position[0] + shadow_offset, position[1] + shadow_offset), (position[0] + shadow_offset, position[1] - shadow_offset), (position[0] - shadow_offset, position[1] + shadow_offset), (position[0] - shadow_offset, position[1] - shadow_offset)]:
            cv2.putText(image, text, pos, cv2.FONT_HERSHEY_DUPLEX, font_scale, shadow_color, thickness + 4, line_type)

        # Overlay the text on the image
        cv2.putText(image, text, position, cv2.FONT_HERSHEY_DUPLEX, font_scale, font_color, thickness, line_type)

        debug("showing", image_file)
        cv2.imshow('image', image)
        debug("mapped", mapped)

        ch = get_chr()
        if ch == "Next":
            jump(1)
        elif ch == "Previous":
            jump(-1)
        elif ch == "Save":
            save = True
            break
        elif ch == "Clear":
            # clear it
            mapped[image_file] = ""
        elif ch == "Cancel": # Escape key
            break
        elif not ch:
            pass
        else:
            # If the key is one of the defined keys, plan to move the image to the corresponding directory
            mapped[image_file] = str(ch)
            jump(1)

    # Close all active window
    cv2.destroyAllWindows()

    if save:
        return mapped

    return None

image_file_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
def classify_inputs(filenames):
    can_show = []
    associated = {}
    ignore = []
    cant_show = []

    for filename in filenames:
        basename, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext in image_file_exts:
            can_show.append(filename)
            associated[basename] = []
        elif ext == '': # probs a dir, don't worry about it
            ignore.append(filename)
        else:
            cant_show.append(filename)

    for filename in cant_show:
        basename, ext = os.path.splitext(filename)
        if basename in associated:
            associated[basename].append(filename)
        else:
            raise ValueError("Don't know what to do with extra file", filename)

    return (can_show, associated)

def move(mapped, associated, dry):
    for mapped_image_file, sub in mapped.items():
        if sub == "":
            continue
        to_move = associated[os.path.splitext(mapped_image_file)[0]]
        to_move.append(mapped_image_file)
        for image_file in to_move:
            target_dir = os.path.join(os.path.dirname(image_file), sub)
            target_file = os.path.join(target_dir, os.path.basename(image_file))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            if dry:
                print(image_file, "\t->\t", target_file)
            else:
                shutil.move(image_file, target_file)

def main():
    args = parse_args()
    (image_files, associated) = classify_inputs(args.files)
    mapped = bucket(image_files)
    if mapped:
        move(mapped, associated, args.dry)

if __name__ == "__main__":
    main()
