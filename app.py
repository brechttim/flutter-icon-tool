#!/usr/bin/env python3

import sys
import os
import cv2


def resolution_ok(image_path, min_res):
    img = cv2.imread(image_path)
    if img is None:
        return False
    return img.shape[0] >= min_res and img.shape[1] >= min_res


def generate_ios_icons(input_path, project_path):
    iosloc = os.path.join(
        project_path,
        "ios/Runner/Assets.xcassets/AppIcon.appiconset"
    )

    if not os.path.exists(iosloc):
        print("ios appicon directory not found.")
        return

    img = cv2.imread(input_path)

    sizes = {
        "Icon-App-20x20@1x.png": 20,
        "Icon-App-20x20@2x.png": 40,
        "Icon-App-20x20@3x.png": 60,
        "Icon-App-29x29@1x.png": 29,
        "Icon-App-29x29@2x.png": 58,
        "Icon-App-29x29@3x.png": 87,
        "Icon-App-40x40@1x.png": 40,
        "Icon-App-40x40@2x.png": 80,
        "Icon-App-40x40@3x.png": 120,
        "Icon-App-60x60@2x.png": 120,
        "Icon-App-60x60@3x.png": 180,
        "Icon-App-76x76@1x.png": 76,
        "Icon-App-76x76@2x.png": 152,
        "Icon-App-83.5x83.5@2x.png": 167,
        "Icon-App-1024x1024@1x.png": 1024,
    }

    for filename, size in sizes.items():
        resized = cv2.resize(img, (size, size), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(iosloc, filename), resized)

    print("ios icons generated.")


def generate_android_icons(input_path, project_path):
    android_base = os.path.join(project_path, "android/app/src/main/res")

    if not os.path.exists(android_base):
        print("android res directory not found.")
        return

    img = cv2.imread(input_path)

    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }

    for folder, size in densities.items():
        folder_path = os.path.join(android_base, folder)

        if not os.path.exists(folder_path):
            continue

        resized = cv2.resize(img, (size, size), interpolation=cv2.INTER_CUBIC)

        cv2.imwrite(os.path.join(folder_path, "ic_launcher.png"), resized)

        round_path = os.path.join(folder_path, "ic_launcher_round.png")
        if os.path.exists(round_path):
            cv2.imwrite(round_path, resized)

    print("android icons generated.")


def main():
    if len(sys.argv) != 3:
        print("usage: python app.py <input image> <flutter project directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    project_path = sys.argv[2]

    if not os.path.exists(input_path):
        print("input file does not exist.")
        sys.exit(1)

    if not os.path.exists(project_path):
        print("flutter project directory does not exist.")
        sys.exit(1)

    if not resolution_ok(input_path, 1024):
        print("image resolution must be at least 1024x1024.")
        sys.exit(1)

    generate_ios_icons(input_path, project_path)
    generate_android_icons(input_path, project_path)

    print("all icons successfully generated.")


if __name__ == "__main__":
    main()