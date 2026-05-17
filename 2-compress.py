from PIL import Image
from pathlib import Path

INPUT_DIR = Path("1-scalabled")
OUTPUT_DIR = Path("2-compressed")
OUTPUT_DIR.mkdir(exist_ok=True)

QUALITY = 92  # 90–95 = золотая середина


def compress(input_path, output_path):
    with Image.open(input_path) as img:
        # Для JPG → RGB, для PNG можно оставить RGBA
        if input_path.suffix.lower() in [".jpg", ".jpeg"]:
            img = img.convert("RGB")
            img.save(
                output_path.with_suffix(".jpg"),
                "JPEG",
                quality=QUALITY,
                optimize=True,
                progressive=True
            )
        elif input_path.suffix.lower() == ".png":
            img = img.convert("RGB")  # убираем альфу, иначе JPEG не сохранится
            img.save(
                output_path.with_suffix(".jpg"),
                "JPEG",
                quality=QUALITY,
                optimize=True,
                progressive=True
            )


def main():
    files = list(INPUT_DIR.glob("*.png")) + list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.jpeg"))

    if not files:
        print("No PNG/JPG files found in:", INPUT_DIR)
        return

    for file in files:
        out = OUTPUT_DIR / file.stem
        compress(file, out)
        print(file.name, "->", out.name + ".jpg")

    print("All images processed.")


if __name__ == "__main__":
    main()
