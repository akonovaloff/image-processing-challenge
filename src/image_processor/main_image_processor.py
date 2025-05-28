# main_image_processing.py
from PIL import Image
import numpy as np
from src.image_processor.image_processor import calculate_projections, save_projections_to_csv, analyze_spot, save_results_to_json


def main():
    # 1. Загрузка и подготовка изображения
    try:
        img = Image.open("../../data/spot_picture.png").convert("L")
        image_array = np.array(img)
        print("Изображение успешно загружено.")
    except FileNotFoundError:
        print("Ошибка: Файл data/spot_picture.png не найден.")
        return
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return

    # 2. Вычисление и сохранение проекций
    print("Вычисление проекций...")
    projection_x, projection_y = calculate_projections(image_array)
    save_projections_to_csv(projection_x, projection_y, "results/projection.csv")

    # 3. Анализ пятна и сохранение метрик
    print("Анализ пятна...")
    spot_metrics_full = analyze_spot(image_array)
    save_results_to_json(spot_metrics_full, "results/results.json")

    print("\n--- Результаты анализа пятна ---")
    print(f"  Положение (смещение от центра X, Y): {spot_metrics_full['results']['position']}")
    print(f"  Стандартное отклонение (X, Y): {spot_metrics_full['results']['std']}")
    print(f"  Дисперсия (X, Y): {spot_metrics_full['results']['dispersion']}")
    print(f"  Абсолютное положение пятна (пиксели X, Y): {spot_metrics_full['spot_position_in_pixels']}")
    print(
        f"  Размеры изображения (ширина, высота): {spot_metrics_full['image_width']}, {spot_metrics_full['image_height']}")
    print(f"  Центр изображения (пиксели X, Y): {spot_metrics_full['image_center']}")
    print("---------------------------------")
    print("Обработка изображения завершена.")


if __name__ == "__main__":
    # Убедись, что директория results существует
    import os

    if not os.path.exists("results"):
        os.makedirs("results")
    main()
