from playwright.sync_api import Playwright, sync_playwright, expect
from pages.GetDescricao import GetClassification
from pages.GetValuePage import GetValuesPage
from pages.GetInfo import GetInfo
from settings import *

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    class_values = GetValuesPage(page)
    class_characteristics = GetInfo(page)
    class_classification = GetClassification(page)

    page.goto(URL, wait_until="load")

    values_page = class_values.scrolling_page()
    if values_page['error']:
        return values_page

    values_pruduct = class_classification.get_rank_pruduct(values_page['data_values'], values_page['data_description'])
    if values_pruduct['error']:
        return values_pruduct
    
    value_information = class_characteristics.characteristics(values_page['data_hrefs'], values_pruduct['data'])
    if value_information['error']:
        return value_information

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)