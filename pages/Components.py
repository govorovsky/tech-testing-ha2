# coding=utf-8
import urlparse

from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AdSettings(Component):
    AD_TITLE = 'input[data-name="title"]'
    AD_TEXT = 'textarea.banner-form__input'
    AD_LINK = 'li.banner-form__row:nth-child(4) > span:nth-child(2) > input:nth-child(1)'
    AD_IMG = '.banner-form__img-file'
    AD_SAVE = '.banner-form__save-button'
    UPLOADED_PREVIEW = 'span.banner-preview__img'
    ERROR = '.banner-form__error'

    PREVIEW_BANNER = '.added-banner__banner-preview'
    PREVIEW_TEXT = '.added-banner .banner-preview__text'
    PREVIEW_TITLE = '.added-banner .banner-preview__title'
    PREVIEW_IMAGE = '.added-banner .banner-preview__img'


    def set_ad_title(self, title):
        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.AD_TITLE)
        )
        element.send_keys(title)

    def set_ad_text(self, text):
        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.AD_TEXT)
        )
        element.send_keys(text)

    def set_ad_img(self, path):
        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.AD_IMG)
        )
        element.send_keys(path)

    def set_ad_url(self, url):
        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.AD_LINK)
        )
        element.send_keys(url)

    def save_add(self):
        # first wait for upload of img..
        WebDriverWait(self.driver, 30, 0.1).until(
            self.wait_for_upload
        )

        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.AD_SAVE)
        )
        element.click()

    def get_ad_preview(self):

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PREVIEW_BANNER)
        )

        text = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PREVIEW_TEXT)
        )
        title = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PREVIEW_TITLE)
        )
        return title.text, text.text

    def check_error(self, d):
        errors = d.find_elements_by_css_selector(self.ERROR)
        for e in errors:
            if e.get_attribute("style") == 'display: block;':
                return e


    def wait_for_error_appear(self):
        WebDriverWait(self.driver, 5, 0.1).until(
            self.check_error
        )


    def wait_for_upload(self, d):
        # we  need to wait for right preview of uploaded image appear...
        prev = d.find_element_by_css_selector(self.UPLOADED_PREVIEW)
        if prev.value_of_css_property("display") == 'block':
            return prev


class IncomeSettings(Component):
    # уровень дохода
    DROP_MENU_SELECT = '[data-name="income_group"] > .campaign-setting__value.js-setting-value'
    INCOME_CHECKBOXES = '[data-name="income_group"] .campaign-setting__input'
    LOW = 2
    MIDDLE = 1
    HIGH = 0

    def get_menu_text(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.DROP_MENU_SELECT)
        ).text

    def get_drop_menu(self):
        WebDriverWait(self.driver, 30, 1).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.DROP_MENU_SELECT))
        )
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.DROP_MENU_SELECT)
        ).click()

    def hide_and_get(self):
        # hide current menu and get it again
        menu = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.DROP_MENU_SELECT)
        )
        menu.click()
        menu.click()

    def select_income(self, income):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.INCOME_CHECKBOXES)
        )[income].click()

    def get_selected_incomes(self):
        boxes = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.INCOME_CHECKBOXES)
        )
        return boxes[self.LOW].is_selected(), boxes[self.MIDDLE].is_selected(), boxes[self.HIGH].is_selected()


class CampaignSettings(Component):
    # base settings for campaign - name and place
    ADV = '#product-type-6043'  # mobile sites
    PLACE = '#pad-mobile_site_web_service'
    COMPAIGN_NAME = '.base-setting__campaign-name__input'

    def set_compaign_name(self, name):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.COMPAIGN_NAME)
        ).send_keys(name)

    def set_target_to_adv(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.ADV)
        ).click()

    def set_place_to_adv(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PLACE)
        ).click()


class RegionSettings(Component):
    # where to adv, default selection Russia, testing for Europe selection
    RUSSIA_CHECKBOX = '#regions188 > .tree__node__input'
    EUROPE_CHECKBOX = '#regions100002 > .tree__node__input'
    BULGARIA_CHECKBOX = '#regions237 > .tree__node__input'
    VENG_CHECKBOX = '#regions118 > .tree__node__input'

    SELECTION_STATUS = '[data-name="regions"] .campaign-setting__chosen-box__body'
    SELECTED_EUROPE = ' [data-id="100002"] > .campaign-setting__chosen-box__item__name '
    CHILDREN_REGIONS = '[data-id="100002"] > .campaign-setting__chosen-box__item__children'
    EUROPE_COLLAPSE_ICON = '//*[@id="regions100002"]/span[1]'
    REMAIN_REGIONS = 'campaign-setting__chosen-box__item__children'

    def get_selection_text(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.RUSSIA_CHECKBOX)
        ).text

    def wait_for_selection(self, wat, exp):
        WebDriverWait(self.driver, 5, 0.1).until(
            self.check_selection(self.driver, wat, exp)
        )

    def check_selection(self, d, wat, exp):
        d.find_element_by_css_selector(wat)
        if d.text == exp:
            return d.text


    def get_europe_selection(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SELECTED_EUROPE)
        ).text

    def get_children_regions_remain(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CHILDREN_REGIONS)
        ).text

    def show_europe_drop_menu(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.EUROPE_COLLAPSE_ICON)
        ).click()

    def click_checkbox(self, region):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(region)
        ).click()

    def get_remain_regions(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.REMAIN_REGIONS)
        ).text


class AuthForm(Component):
    LOGIN = '#id_Login'
    PASSWORD = '#id_Password'
    DOMAIN = '#id_Domain'
    SUBMIT = '#gogogo>input'

    def set_login(self, login):
        self.driver.find_element_by_css_selector(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_css_selector(self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = self.driver.find_element_by_css_selector(self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT).click()


class TopMenu(Component):
    EMAIL = '#PH_user-email'

    def get_email(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EMAIL).text
        )
