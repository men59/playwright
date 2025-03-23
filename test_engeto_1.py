import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()



def test_cookies(page):
    # přejdi na stránku engeto
    page.goto("https://engeto.cz/")

    # klikni na tlačítko odmítnout
    button = page.locator("#cookiescript_reject")
    button.click()

    page.wait_for_timeout(1000)

    # zkontroluj, že celá lišta zmizela
    bar = page.locator("#cookiescript_injected")
    assert bar.is_visible() == False


def test_engeto_termin(page):
    page.goto("https://engeto.cz/")

    # najdu tlačítko na odmítnutí cookies přes jeho id
    btn_refuse = page.locator("#cookiescript_reject")
    btn_refuse.click()

    #with page.expect_popup() as new_popup:

    # najdu tlačítko "Termin"
    page.locator("#main-header > div > div > a").click()
    #new_page = new_popup.value
    print(page.url)
    
    assert page.url == "https://engeto.cz/terminy/"
    


def test_vybor_kurzu_tester(page):
    page.goto("https://engeto.cz/")

    # najdu tlačítko na odmítnutí cookies přes jeho id
    btn_refuse = page.locator("#cookiescript_reject")
    btn_refuse.click()

    
    # najdu tlačítko "Přehled IT kurzů"
    page.locator("body > main > div:nth-child(1) > div > div > a").click()
    assert page.url == "https://engeto.cz/prehled-kurzu/"
   
    
    # najdu tlačítko "Více informací"
    page.locator("body > main > div:nth-child(3) > div.has-text-lg-regular-font-size.fullwidth > div > a:nth-child(3) > span").click()
    print(page.url)

    assert page.url == "https://engeto.cz/tester-s-pythonem/"
   

def test_sign_in_portal(page):
    page.goto("https://portal.engeto.com")

    # click on sign in button:
    page.locator(".cursor-pointer").click()

    # fill in username
    page.locator("#username").fill(" mnazarchuk@seznam.cz")

    # fill in password
    page.locator("#password").fill("   ")

    # click on sign in button
    page.locator("button[type='submit']").click()

    # check the error message appears
    error = page.locator("#error-element-password")

    assert error.is_visible()
