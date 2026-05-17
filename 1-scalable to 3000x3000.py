from PIL import Image
from pathlib import Path

# Папка с исходными изображениями
INPUT_DIR = Path("1-input for scalable")

# Папка для готовых изображений
OUTPUT_DIR = Path("1-scalabled")
OUTPUT_DIR.mkdir(exist_ok=True)

# Новый размер
TARGET_SIZE = (3000, 3000)

# Ресемплинг максимального качества
RESAMPLE = Image.LANCZOS


def upscale_image(input_path: Path, output_path: Path):
    with Image.open(input_path) as img:
        # Определяем формат
        if input_path.suffix.lower() == ".png":
            img = img.convert("RGBA")
            upscaled = img.resize(TARGET_SIZE, RESAMPLE)
            upscaled.save(
                output_path.with_suffix(".png"),
                format="PNG",
                optimize=True,
                compress_level=9
            )
        elif input_path.suffix.lower() in [".jpg", ".jpeg"]:
            img = img.convert("RGB")
            upscaled = img.resize(TARGET_SIZE, RESAMPLE)
            upscaled.save(
                output_path.with_suffix(".jpg"),
                format="JPEG",
                quality=95,  # высокое качество
                optimize=True
            )


def main():
    files = list(INPUT_DIR.glob("*.png")) + list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.jpeg"))

    if not files:
        print("No PNG/JPG files found in:", INPUT_DIR)
        return

    for file in files:
        output_path = OUTPUT_DIR / file.stem
        upscale_image(file, output_path)
        print(f"Done: {file.name}")

    print("All images processed.")


if __name__ == "__main__":
    main()
