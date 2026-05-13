from PIL import Image
from pathlib import Path

# Папка с исходными PNG
INPUT_DIR = Path("input")

# Папка для готовых изображений
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Новый размер
TARGET_SIZE = (3000, 3000)

# Ресемплинг максимального качества
# LANCZOS — лучший алгоритм для увеличения изображений в Pillow
RESAMPLE = Image.LANCZOS


def upscale_image(input_path: Path, output_path: Path):
    with Image.open(input_path) as img:
        # Конвертируем в RGBA, чтобы сохранить прозрачность PNG
        img = img.convert("RGBA")

        # Увеличиваем изображение
        upscaled = img.resize(TARGET_SIZE, RESAMPLE)

        # Сохраняем без потерь
        upscaled.save(
            output_path,
            format="PNG",
            optimize=True,
            compress_level=9  # максимальное сжатие без потери качества
        )


def main():
    png_files = list(INPUT_DIR.glob("*.png"))

    if not png_files:
        print("PNG files not found in:", INPUT_DIR)
        return

    for file in png_files:
        output_path = OUTPUT_DIR / file.name
        upscale_image(file, output_path)
        print(f"Done: {file.name}")

    print("All images processed.")


if __name__ == "__main__":
    main()