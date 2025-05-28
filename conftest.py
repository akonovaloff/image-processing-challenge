# conftest.py (обновленные фикстуры)
import allure
import numpy as np
import pytest
from PIL import Image
import yaml
# Предполагаем, что image_processor.py находится в том же каталоге или доступен для импорта
from src.image_processor.image_processor import calculate_projections, save_projections_to_csv, analyze_spot, save_results_to_json


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
    # ... (без изменений) ...
    with open("data/expected_results.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module", autouse=True)
@allure.title("Сохранить проекции в *.csv файл")
def processed_projections(image_data):  # Переименовал для ясности, что это результат обработки
    projection_x, projection_y = calculate_projections(image_data)
    output_csv_path = "results/projection.csv"
    save_projections_to_csv(projection_x, projection_y, output_csv_path)

    allure.attach.file(
        output_csv_path,
        name="Проекция на оси в csv",
        attachment_type=allure.attachment_type.CSV
    )
    return {"projection_x": projection_x, "projection_y": projection_y}  # Возвращаем, если нужно в тестах


@pytest.fixture(scope="module")
@allure.title("Вычислить метрики и сохранить в *.json")
def computed_metrics(image_data):  # Переименовал для ясности
    # Вычисляем метрики с помощью новой функции
    analysis_results = analyze_spot(image_data)

    # Сохраняем в JSON
    output_json_path = "results/results.json"
    # Передаем только ту часть, которая была в computed_metrics в json
    save_results_to_json(analysis_results, output_json_path)

    allure.attach.file(
        output_json_path,
        name="JSON с результатами",
        attachment_type=allure.attachment_type.JSON
    )
    # Фикстура должна возвращать именно те метрики, которые используются в тестах
    # В твоем случае это 'position', 'std', 'dispersion' из вложенного 'results'
    return analysis_results["results"]
