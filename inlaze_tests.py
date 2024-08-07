import unittest  # Libreria para pruebas unitarias.
from ddt import ddt, data, unpack
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class TestInlaze(unittest.TestCase):

    def sign_up(self, fullname, username, password, password_confirmation):
        # Encuentra los campos de nombre, usuario, contraseña y contraseña de confirmacion
        fullname_field = self.driver.find_element(By.ID, 'full-name')
        username_field = self.driver.find_element(By.ID, 'email')
        password_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="password"][id="password"]') # Debido a la existencia de multiples elementos con id=password, es necesario buscar por CSS
        password_confirmation_field = self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="password"][id="confirm-password"]')

        # Ingresa los datos de registro
        fullname_field.click()
        fullname_field.clear()
        fullname_field.send_keys(fullname)
        username_field.click()
        username_field.clear()
        username_field.send_keys(username)
        password_field.click()
        password_field.clear()
        password_field.send_keys(password)
        password_confirmation_field.click()
        password_confirmation_field.clear()
        password_confirmation_field.send_keys(
            password_confirmation)

    def press_signin_signup_button(self):
        # Encuentra y hace clic en el enlace de 'Sign up'
        signup_field = self.driver.find_element(
            By.XPATH, f"//*[contains(text(), 'Sign up')]")
        signup_field.click()

    def press_submit_button(self):
        signup_button = self.driver.find_element(
            By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
        signup_button.click()

    def login(self, username, password):
        # Encuentra los campos de usuario y contraseña
        username_field = self.driver.find_element(By.ID, 'email')
        password_field = self.driver.find_element(By.ID, 'password')

        # Ingresa las credenciales
        username_field.click()
        username_field.send_keys(username)
        password_field.click()
        password_field.send_keys(password)


@ddt
class TestInlazeSignUp(TestInlaze):

    def setUp(self):
        self.driver = webdriver.Safari()
        self.driver.get('https://test-qa.inlaze.com/auth/sign-up')

    # Test cases 1, 3, 15
    @data(("Angie Jimenez", "angiel.jimenezp@gmail.com", "Contraseña12!", "Contraseña12!"))
    @unpack
    def test_successful_sign_up(self, fullname, username, password, password_confirmation):
        self.sign_up(fullname, username, password, password_confirmation)
        time.sleep(1)
        self.press_submit_button()
        time.sleep(2)
        self.assertEqual(self.driver.current_url,
                         "https://test-qa.inlaze.com/auth/sign-in")

    @data(("Angie", "angiel.jimenezp@gmail.com", "Contraseña12*", "Contraseña12*"),  # TC 2
          ("Angie", "angiel.jimenezp@gmail*com",
           "Contraseña12*", "Contraseña12*"),  # TC 4
          ("Angie Jimenez", "angiel.jimenezp@gmail.com", "Ab1!", "Ab1!"),  # TC 6
          ("Angie Jimenez", "angiel.jimenezp@gmail.com",
           "Contraseña1234*", "Contraseña1234*"),  # TC 6
          ("Angie Jimenez", "angiel.jimenezp@gmail.com",
           "contraseña12*", "contraseña12*"),  # TC 7
          ("Angie Jimenez", "angiel.jimenezp@gmail.com",
           "CONTRASENA12*", "CONTRASENA12*"),  # TC 8
          ("Angie Jimenez", "angiel.jimenezp@gmail.com",
           "Contraseña*", "Contraseña*"),  # TC 9
          ("Angie Jimenez", "angiel.jimenezp@gmail.com",
           "Contraseña12", "Contraseña12"),  # TC 10
          ("", "angiel.jimenezp@gmail.com",
           "Contraseña123", "Contraseña123"),  # TC 11
          ("Angie Jimenez", "", "Contraseña123", "Contraseña123"),  # TC 12
          ("Angie Jimenez", "angiel.jimenezp@gmail.com",
           "", "Contraseña123"),  # TC 13
          ("Angie Jimenez", "angiel.jimenezp@gmail.com", "Contraseña123", "Contrasena123"))  # TC 14
    @unpack
    def test_unsuccessful_sign_up(self, fullname, username, password, password_confirmation):
        signup_button = self.driver.find_element(
            By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
        self.assertFalse(signup_button.is_enabled())
        self.sign_up('Pepito perez', 'Pepito_perez@gmail.com',
                     'Contraseña321', 'Contraseña321')
        self.assertTrue(signup_button.is_enabled())
        time.sleep(1)
        self.sign_up(fullname, username, password, password_confirmation)
        self.assertFalse(signup_button.is_enabled())
        time.sleep(2)

    # Test case 5
    @data(("Angie Jimenez", "angiel.jimenezp@gmail.com", "Contraseña12!", "Contraseña12!"))
    @unpack
    def test_already_created_user(self, fullname, username, password, password_confirmation):
        # primer sign up.
        self.sign_up(fullname, username, password, password_confirmation)
        time.sleep(1)
        self.press_submit_button()
        time.sleep(2)
        self.assertEqual(self.driver.current_url,
                         "https://test-qa.inlaze.com/auth/sign-in")

        # segundo sign up.
        self.driver.get('https://test-qa.inlaze.com/auth/sign-up')
        self.sign_up(fullname, username, password, password_confirmation)
        time.sleep(1)
        self.press_submit_button()
        time.sleep(2)
        self.assertEqual(self.driver.current_url,
                         "https://test-qa.inlaze.com/auth/sign-up")

    def tearDown(self):
        self.driver.quit()


@ddt
class TestInlazeLogin(TestInlaze):

    def setUp(self):
        self.driver = webdriver.Safari()
        self.driver.get('https://test-qa.inlaze.com/auth/sign-in')

    @data(("angiel.jimenezp@gmail.com", "Contraseña123"))
    @unpack
    # Test case 16
    def test_successful_login(self, email, password):
        self.press_signin_signup_button()
        time.sleep(1)
        self.sign_up('Pepito perez', email,
                     password, password)
        self.press_submit_button()
        time.sleep(2)
        self.assertEqual(self.driver.current_url,
                         "https://test-qa.inlaze.com/auth/sign-in")

        self.login(email, password)
        time.sleep(1)
        self.press_submit_button()
        time.sleep(5)
        self.assertEqual(self.driver.current_url,
                         "https://test-qa.inlaze.com/panel")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
