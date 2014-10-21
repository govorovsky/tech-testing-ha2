import urlparse
from selenium.webdriver.support.wait import WebDriverWait
from pages.Components import TopMenu, AdSettings, AuthForm


class Page(object):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class CreatePage(Page):
    PATH = '/ads/create'
    SAVE_CAMPAIGN_BUTTON = '.main-button-new'

    @property
    def top_menu(self):
        return TopMenu(self.driver)


    @property
    def ad_settings(self):
        return AdSettings(self.driver)

    @property
    def save_button(self):
        return WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SAVE_CAMPAIGN_BUTTON)
        )


class CampaignsPage(Page):
    PATH = '/ads/campaigns/'
    EDIT_LINK = '.campaign-row .control__link_edit'

    def open_last_company_for_edit(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EDIT_LINK)
        ).click()