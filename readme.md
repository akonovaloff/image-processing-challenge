### Установка зависимостей:
`pip install -r requirements.txt`

### Запуск тестов:
`pytest`

### Подготовка отчета:
`allure generate results/allure-results/ --clean -o results/allure-report/`

### Задание 

1. Реализовать скрипт для обработки изображения.  
Поиск положения, стандартного отклонения и дисперсии положения пятна [на картинке](data/spot_picture.png).  
Валидные значения читаются из [yaml файла](data/expected_results.yaml):
   - `std: 10` - стандартное отклонение  
   - `dispersion:  10` - дисперсия  
   - `position: [0, 0]` - положение центра пятна, `[0, 0]`  - центр картинки

- [x] Реализовать [3 тестовые функции](tests/test_image_procession.py) для каждого входного значения
- [ ] ~~Функцию отправки метрик в базу данных (например influxDB)~~  
- [x] Результат обработки и результаты тестов собрать в [json файл](results/results.json). 
- [x] В ~~txt~~ cvs собрать [проекцию на оси изображения](results/projection.csv).
- [x] *Собрать [allure-отчет](results/allure-report/index.html) 


2. Написать парсер ASCII символов для прибора работающего по serial интерфейсу.

- [x] Запрос значений: “GET_A” , “GET_B”, “GET_C”
- [x] Ответ: “A_10V”, “B_5V”, “C_15A”
- [x] Предусмотреть смену с serial интерфейса на TCP
