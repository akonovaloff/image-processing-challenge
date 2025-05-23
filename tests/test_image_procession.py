import pytest
import allure


class TestImageProcession:
    atol = 5  # здесь нужно задать допустимую дельту

    @allure.title("Тест: положение пятна")
    def test_position(self, expected_results, computed_metrics):
        expected = expected_results["position"]
        actual = computed_metrics["position"]

        with allure.step(f"Ожидаемое значение: {expected}, актуальное: {actual}"):
            for exp, act in zip(expected, actual):
                assert abs(exp - act) <= self.atol, f"Ожидаемое значение: {expected}, актуальное: {actual}"

    @allure.title("Тест: стандартное отклонение")
    def test_std(self, expected_results, computed_metrics):
        expected_std = expected_results["std"]
        actual_std = computed_metrics["std"]
        with allure.step(f"Ожидаемое значение: {expected_std}, актуальное: [{actual_std[0]}, {actual_std[1]}]"):
            assert actual_std[0] <= expected_std
            assert actual_std[1] <= expected_std

    @allure.title("Тест: дисперсия")
    def test_dispersion(self, expected_results, computed_metrics):
        expected_disp = expected_results["dispersion"]
        actual_disp = computed_metrics["dispersion"]
        with allure.step(f"Ожидаемое значение: {expected_disp}, актуальное: {actual_disp}"):
            assert actual_disp[0] <= expected_disp
            assert actual_disp[1] <= expected_disp
