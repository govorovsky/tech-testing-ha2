# coding=utf-8
import os
import random
import string
import unittest
from selenium.webdriver import DesiredCapabilities, Remote
from pages.Components import AdSettings, CampaignSettings, IncomeSettings, \
    RegionSettings
from pages.Pages import AuthPage, CreatePage, CampaignsPage


def name_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ExampleTest(unittest.TestCase):
    def setUp(self):
        self.USERNAME = 'tech-testing-ha2-38@bk.ru'
        self.PASSWORD = os.environ['TTHA2PASSWORD']
        self.DOMAIN = '@bk.ru'
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.set_domain(self.DOMAIN)
        auth_form.set_login(self.USERNAME)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

    def tearDown(self):
        self.driver.quit()

    def test_create_page_login_ok(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        email = create_page.top_menu.get_email()
        self.assertEqual(self.USERNAME, email)


    def test_create_ad_success(self):
        ad_title = u'hello sddsa'
        ad_text = u'fdsafa fadpf dafd ff 432 32 r'
        ad_img = u'img.jpg'
        ad_url = u'bbbbb.by'
        # create ad and check for preview appear
        create_page = CreatePage(self.driver)
        create_page.open()

        ad_settings = AdSettings(self.driver)
        ad_settings.set_ad_title(ad_title)
        ad_settings.set_ad_text(ad_text)
        ad_settings.set_ad_url(ad_url)
        ad_settings.set_ad_img(ad_img)
        ad_settings.save_add()

        self.assertEqual(ad_settings.get_ad_preview(), (ad_title, ad_text))

    def test_create_ad_empty_field_error(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        ad_settings = AdSettings(self.driver)
        ad_settings.set_ad_img('img.jpg')
        ad_settings.set_ad_text('test ad')
        ad_settings.set_ad_url('test.com')
        ad_settings.save_add()
        ad_settings.wait_for_error_appear()

    def test_select_place_and_target(self):
        # test correct appearing of selection

        create_page = CreatePage(self.driver)
        create_page.open()

        c_settings = CampaignSettings(self.driver)
        c_settings.set_compaign_name("my big company")
        c_settings.set_target_to_adv()
        c_settings.set_place_to_adv()


    def test_income_menu_set(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        income_settings = IncomeSettings(self.driver)
        income_settings.get_drop_menu()
        income_settings.select_income(income_settings.MIDDLE)
        income_settings.select_income(income_settings.LOW)
        self.assertEqual(income_settings.get_menu_text(), u'Выбран')
        self.assertEqual(income_settings.get_selected_incomes(), (True, True, False))

    def test_income_menu_save_after_company_create(self):
        # save company and edit it. check for selected values saved

        create_page = CreatePage(self.driver)
        create_page.open()

        c_settings = CampaignSettings(self.driver)
        c_name = name_generator()
        c_settings.set_compaign_name(c_name)

        ad_settings = AdSettings(self.driver)
        ad_settings.set_ad_title('fdsfs')
        ad_settings.set_ad_text('rerwe  fdfs  fsd')
        ad_settings.set_ad_url('rew.com')
        ad_settings.set_ad_img('img.jpg')
        ad_settings.save_add()

        income_settings = IncomeSettings(self.driver)
        income_settings.get_drop_menu()
        income_settings.select_income(income_settings.MIDDLE)
        income_settings.select_income(income_settings.LOW)

        create_page.save_button.click()  # auto-redirect to camp page!

        camp_page = CampaignsPage(self.driver)
        camp_page.open_last_company_for_edit()

        self.assertEqual(income_settings.get_menu_text(), u'Выбран')
        self.assertEqual(income_settings.get_selected_incomes(), (True, True, False))


    def test_save_selected_after_toogle(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        income_settings = IncomeSettings(self.driver)
        income_settings.get_drop_menu()
        income_settings.select_income(income_settings.HIGH)
        income_settings.select_income(income_settings.LOW)
        self.assertEqual(income_settings.get_selected_incomes(), (True, False, True))
        income_settings.hide_and_get()
        self.assertEqual(income_settings.get_selected_incomes(), (True, False, True))

    def test_region_select(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        r_settings = RegionSettings(self.driver)

        r_settings.click_checkbox(RegionSettings.RUSSIA_CHECKBOX)
        r_settings.click_checkbox(RegionSettings.EUROPE_CHECKBOX)
        self.assertEqual(r_settings.get_europe_selection(), u'Европа', 'should be Europe')
        r_settings.show_europe_drop_menu()
        r_settings.click_checkbox(RegionSettings.BULGARIA_CHECKBOX)
        self.assertEqual(r_settings.get_children_regions_remain(), u'(42 из 43)', 'wrong remain regions count')


    def test_regions_remain_after_campaign_save(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        c_settings = CampaignSettings(self.driver)
        c_name = name_generator()
        c_settings.set_compaign_name(c_name)

        ad_settings = AdSettings(self.driver)
        ad_settings.set_ad_title('ergiosfdf')
        ad_settings.set_ad_text('rerwe fdfds fsd')
        ad_settings.set_ad_url('rew.com')
        ad_settings.set_ad_img('img.jpg')
        ad_settings.save_add()

        r_settings = RegionSettings(self.driver)
        r_settings.click_checkbox(RegionSettings.RUSSIA_CHECKBOX)
        r_settings.click_checkbox(RegionSettings.EUROPE_CHECKBOX)
        r_settings.show_europe_drop_menu()
        r_settings.click_checkbox(RegionSettings.BULGARIA_CHECKBOX)
        r_settings.get_children_regions_remain()  # need to wait for selection

        create_page.save_button.click()

        camp_page = CampaignsPage(self.driver)
        camp_page.open_last_company_for_edit()

        self.assertEqual(r_settings.get_europe_selection(), u'Европа', 'should be Europe')
        self.assertEqual(r_settings.get_children_regions_remain(), u'(42 из 43)', 'wrong remain regions count')


