from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from zomato.elements.base_element import BaseElement

class NavbarElement(BaseElement):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver, "//nav/ul[starts-with(@id, 'navigation_')]")

    def login(self, ph_no: str):
        self.base_element.find_element(by=By.XPATH, value="li[4]/a").click()

        self.driver.switch_to.frame(self.driver.find_element(by=By.ID, value="auth-login-ui"))

        login_section = self.driver.find_element(by=By.XPATH, value="//div[@aria-hidden='false' and @role='dialog']/div[starts-with(@id, 'id-') and @type='default']/section[2]/section")

        login_section.find_element(by=By.XPATH, value="//input[@type='number']").send_keys(ph_no)
        login_section.find_element(by=By.XPATH, value="//button[@role='button']").click()

        loginName = ''
        while (loginName == None or loginName == ''):
            try:
                loginName = self.base_element.find_element(by=By.XPATH, value="li[4]/div/div/div[1]/span").text
            except:
                pass

        self.driver.switch_to.default_content()

        return loginName

    def logout(self):
        logoutElement = self.base_element.find_element(by=By.XPATH, value="li[4]/div/div/div[2]/div[8]")

        if (not logoutElement.is_displayed()):
            self.base_element.find_element(by=By.XPATH, value="li[4]/div/div/div[1]/i").click()

        logoutElement.click()
