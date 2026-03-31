import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestSimpleLogin:

    @pytest.fixture
    def driver(self):
        """Настройка браузера"""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        driver.maximize_window()
        yield driver
        driver.quit()

    def test_full_login_logout_flow(self, driver):
        """Полный сценарий: вход с ошибкой -> вход с успехом -> выход"""

        # 1. Переход на сайт
        driver.get("https://www.saucedemo.com/")
        time.sleep(2)
        assert "Swag Labs" in driver.title
        print("1. ✅ Главная страница загружена")

        # 2. Попытка входа с неверными данными
        driver.find_element(By.ID, "user-name").send_keys("test")
        driver.find_element(By.ID, "password").send_keys("test")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(1)

        # Проверка сообщения об ошибке
        error = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "do not match" in error.text
        print("2. ✅ Неверные данные - ошибка отобразилась")

        # 3. Вход с правильными данными
        # Очищаем поля
        username_field = driver.find_element(By.ID, "user-name")
        username_field.clear()
        username_field.send_keys("standard_user")

        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys("secret_sauce")

        # Нажимаем кнопку входа
        driver.find_element(By.ID, "login-button").click()

        # Проверка успешного входа
        WebDriverWait(driver, 5).until(
            EC.url_to_be("https://www.saucedemo.com/inventory.html")
        )
        print("3. ✅ Успешный вход выполнен")

        # 4. Выход из системы (ИСПРАВЛЕННАЯ ЧАСТЬ)
        # Открываем меню (ищем кнопку с другим селектором)
        time.sleep(1)  # Даем время на загрузку страницы

        # Пробуем разные способы найти кнопку меню
        try:
            # Способ 1: По ID
            menu_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
            )
            menu_button.click()
            print("   Меню открыто (способ 1)")
        except:
            try:
                # Способ 2: По CSS классу
                menu_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "bm-burger-button"))
                )
                menu_button.click()
                print("   Меню открыто (способ 2)")
            except:
                # Способ 3: Через JavaScript
                driver.execute_script("document.querySelector('.bm-burger-button button').click()")
                print("   Меню открыто (способ 3 - JavaScript)")

        time.sleep(1)  # Ждем анимации меню

        # Нажимаем Logout (разными способами)
        try:
            # Способ 1: По ID
            logout_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
            )
            logout_btn.click()
            print("   Кнопка Logout нажата (способ 1)")
        except:
            try:
                # Способ 2: По тексту ссылки
                logout_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
                )
                logout_btn.click()
                print("   Кнопка Logout нажата (способ 2)")
            except:
                try:
                    # Способ 3: По CSS селектору
                    logout_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='logout-sidebar-link']"))
                    )
                    logout_btn.click()
                    print("   Кнопка Logout нажата (способ 3)")
                except:
                    # Способ 4: Через JavaScript
                    driver.execute_script("document.getElementById('logout_sidebar_link').click()")
                    print("   Кнопка Logout нажата (способ 4 - JavaScript)")

        time.sleep(1)

        # Проверка выхода (должны вернуться на страницу логина)
        WebDriverWait(driver, 5).until(
            EC.url_to_be("https://www.saucedemo.com/")
        )
        assert driver.current_url == "https://www.saucedemo.com/"
        print("4. ✅ Выход из системы выполнен")

        print("\n" + "=" * 50)
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 50)