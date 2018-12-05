import mechanicalsoup as ms
import re
from selenium import webdriver
import sys

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


def main():
    userid_str, password_str = (sys.argv[1], sys.argv[2])
    driver = webdriver.Firefox()
    url = "https://www.goodreads.com"
    driver.get(url)
    username = driver.find_element_by_name("user[email]")
    password = driver.find_element_by_name("user[password]")
    username.clear()
    password.clear()
    username.send_keys(userid_str)
    password.send_keys(password_str)
    password.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_contains("Recent Updates"))
    driver.implicitly_wait(5)
    driver.get("https://www.goodreads.com/book/show/36642458-skyward")

    els = driver.find_elements_by_class_name("friendReviews")
    for el in els:
        try:
            stars = el.find_element_by_class_name("staticStars")
            print("numstars", len(stars.find_elements_by_class_name("staticStar")))
        except NoSuchElementException:
            continue

        texts = el.find_elements_by_css_selector("span[id^='freeTextContainer'")
        text = texts[0]
        print(text.text)

    print(len(els))


# get_reviews("https://www.goodreads.com/book/show/2767052-the-hunger-games", browser)


def get_reviews(book_url, browser):
    browser.open(book_url)
    soup = browser.get_current_page()
    print(soup)
    reviews_divs = soup.find_all("div", class_="friendReviews")
    print(reviews_divs)
    for rev in reviews_divs:
        rev_text = rev.find(id=re.compile("freeTextContainer.*")).contents
        print(rev_text)


if __name__ == "__main__":
    main()
