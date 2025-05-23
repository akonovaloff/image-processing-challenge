import json
import allure
import numpy as np
import pandas as pd
import pytest
import yaml
from PIL import Image


@pytest.fixture(scope="module")
@allure.title("Открыть изображение")
def image_data():
    img = Image.open("data/spot_picture.png").convert("L")

    allure.attach.file(
        "data/spot_picture.png",
        name="Изображение пятна",
        attachment_type=allure.attachment_type.PNG
    )

    return np.array(img)


@pytest.fixture(scope="module")
@allure.title("Загрузить данные из yaml")
def expected_results():
    allure.attach.file(
        "data/expected_results.yaml",
        name="Ожидаемые результаты",
        attachment_type=allure.attachment_type.YAML
    )
    with open("data/expected_results.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module", autouse=True)
@allure.title("Сохранить проекции в *.csv файл")
def save_projection_csv(image_data):
    projection_x = image_data.sum(axis=0)  # по горизонтали (width)
    projection_y = image_data.sum(axis=1)  # по вертикали (height)

    # Приводим к одинаковой длине
    max_len = max(len(projection_x), len(projection_y))
    proj_x = np.pad(projection_x, (0, max_len - len(projection_x)), constant_values=0)
    proj_y = np.pad(projection_y, (0, max_len - len(projection_y)), constant_values=0)

    # Объединяем в таблицу
    df = pd.DataFrame({
        "projection_x": proj_x,
        "projection_y": proj_y
    })

    df.to_csv("results/projection.csv", index=False)

    allure.attach.file(
        "results/projection.csv",
        name="Проекция на оси в csv",
        attachment_type=allure.attachment_type.CSV
    )


@pytest.fixture(scope="module")
@allure.title("Вычислить метрики, сохранить в *.json")
def computed_metrics(image_data):
    from scipy.ndimage import center_of_mass

    y, x = np.indices(image_data.shape)
    total = image_data.sum()
    weights = image_data / total

    cy_raw, cx_raw = center_of_mass(image_data)  # центр масс пятна в пикселях

    h, w = image_data.shape
    cx0 = w / 2
    cy0 = h / 2  # центр изображения в пикселях

    cx = cx_raw - cx0  # смещение от центра изображения
    cy = cy_raw - cy0

    std_x = np.sqrt(np.sum(weights * (x - cx_raw) ** 2))
    std_y = np.sqrt(np.sum(weights * (y - cy_raw) ** 2))

    results = {
        "position": [cx, cy],
        "std": [std_x, std_y],
        "dispersion": [std_x ** 2, std_y ** 2],
    }

    with open("results/results.json", "w") as f:
        json.dump({"computed_metrics":
                       {"image_height": h,
                        "image_width": w,
                        "image_center": [cx0, cy0],
                        "spot_position_in_pixels": [cx_raw, cy_raw],
                        "results": results}}, f, indent=4)

    allure.attach.file(
        "results/results.json",
        name="JSON с результатами",
        attachment_type=allure.attachment_type.JSON
    )

    return results
