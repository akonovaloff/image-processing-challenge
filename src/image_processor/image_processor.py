from scipy.ndimage import center_of_mass
import numpy as np
import pandas as pd


def calculate_projections(image_array: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Вычисляет проекции изображения по осям X и Y."""
    projection_x = image_array.sum(axis=0)  # по горизонтали (width)
    projection_y = image_array.sum(axis=1)  # по вертикали (height)
    return projection_x, projection_y


def save_projections_to_csv(projection_x: np.ndarray, projection_y: np.ndarray, output_path: str):
    """Сохраняет проекции в CSV файл."""
    max_len = max(len(projection_x), len(projection_y))
    proj_x_padded = np.pad(projection_x, (0, max_len - len(projection_x)), constant_values=0)
    proj_y_padded = np.pad(projection_y, (0, max_len - len(projection_y)), constant_values=0)

    df = pd.DataFrame({
        "projection_x": proj_x_padded,
        "projection_y": proj_y_padded
    })
    df.to_csv(output_path, index=False)
    print(f"Проекции сохранены в {output_path}")


def analyze_spot(image_array: np.ndarray) -> dict:
    """
    Анализирует изображение пятна для определения его положения,
    стандартного отклонения и дисперсии.
    """
    y_indices, x_indices = np.indices(image_array.shape)
    total_intensity = image_array.sum()

    if total_intensity == 0:  # Обработка случая пустого изображения
        # Можно вернуть None, пустой словарь или выбросить исключение
        # в зависимости от желаемого поведения
        h, w = image_array.shape
        return {
            "image_height": h,
            "image_width": w,
            "image_center": [w / 2, h / 2],
            "spot_position_in_pixels": [None, None],
            "results": {
                "position": [None, None],
                "std": [None, None],
                "dispersion": [None, None],
            }
        }

    weights = image_array / total_intensity

    cy_raw, cx_raw = center_of_mass(image_array)  # центр масс пятна в пикселях

    h, w = image_array.shape
    cx0 = w / 2
    cy0 = h / 2  # центр изображения в пикселях

    # Смещение от центра изображения
    # Важно: scipy.ndimage.center_of_mass возвращает (row, col) -> (y, x)
    # cx_raw - это координата по ширине, а cy_raw - по высоте.

    cx_offset = cx_raw - cx0
    cy_offset = cy_raw - cy0  # Порядок (y,x) для center_of_mass, но для результата [cx,cy]

    # Стандартное отклонение
    # x_indices и y_indices должны соответствовать осям cx_raw и cy_raw
    std_x = np.sqrt(np.sum(weights * (x_indices - cx_raw) ** 2))
    std_y = np.sqrt(np.sum(weights * (y_indices - cy_raw) ** 2))

    metrics = {
        "position": [cx_offset, cy_offset],  # [смещение по X, смещение по Y]
        "std": [std_x, std_y],  # [std по X, std по Y]
        "dispersion": [std_x ** 2, std_y ** 2],  # [дисперсия по X, дисперсия по Y]
    }

    # Дополнительная информация для JSON
    full_results = {
        "image_height": h,
        "image_width": w,
        "image_center": [cx0, cy0],  # [центр X, центр Y]
        "spot_position_in_pixels": [cx_raw, cy_raw],  # [абсолютный X, абсолютный Y]
        "results": metrics
    }
    return full_results  # Возвращаем полный набор данных


import json


def save_results_to_json(results_data: dict, output_path: str):
    """Сохраняет результаты обработки в JSON файл."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"computed_metrics": results_data}, f, indent=4)
    print(f"Результаты анализа сохранены в {output_path}")
