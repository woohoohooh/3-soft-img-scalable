from PIL import Image
from pathlib import Path

INPUT_DIR = Path("1-scalabled")
OUTPUT_DIR = Path("2-compressed")
OUTPUT_DIR.mkdir(exist_ok=True)

QUALITY = 92  # 90–95 = золотая середина


def compress(input_path, output_path):
    with Image.open(input_path) as img:
        img = img.convert("RGB")  # JPEG не поддерживает alpha

        img.save(
            output_path.with_suffix(".jpg"),
            "JPEG",
            quality=QUALITY,
            optimize=True,
            progressive=True
        )


def main():
    for file in INPUT_DIR.glob("*.png"):
        out = OUTPUT_DIR / file.stem
        compress(file, out)

        print(file.name, "->", out.name)


if __name__ == "__main__":
    main()