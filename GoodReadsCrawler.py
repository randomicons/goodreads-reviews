import os
import sys

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

num_revs_per_book = 200
num_books = 10
df_revs = pd.DataFrame(columns=["book", "author", "rating", "review"])

"""
Logs in to GoodReads to avoid pop ups
Then goes to book links and gathers reviews
"""
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
    wait.until(ec.title_contains("Recent Updates"))
    if not os.path.isfile("book_links.txt"):
        create_book_links(driver)

    with open("book_links.txt", "r") as file:
        links = file.readlines()[33:33 + num_books]

    rev_i = 0
    for link in links:
        rev_i = get_reviews(link, driver, rev_i)
    df_revs.to_csv("data.csv", mode='a')


"""
Given the book links, it goes through every review and pulls relevant information
If there are more reviews, it clicks on more and keeps reading them in
"""
def get_reviews(book_url, driver, rev_i):
    """

    :param book_url: url of book
    :param driver: web driver
    :param rev_i: number of reviews
    :return: updates review data frames and returns the number of reviews read
    """
    driver.get(book_url)
    driver.implicitly_wait(10)
    bookTitle = driver.find_element_by_id("bookTitle").get_attribute("innerHTML")
    first_author = driver.find_element_by_css_selector("a.authorName span").get_attribute("innerHTML")
    wait = WebDriverWait(driver, 10)
    # Press all more to expand reviews
    # mores = driver.find_elements_by_xpath('//a[contains(text(), "{0}") and @class="inner"]'.format("...more"))
    rev_cnt = 0

    while rev_cnt < num_revs_per_book:
        driver.implicitly_wait(10)
        els = driver.find_elements_by_class_name("friendReviews")
        driver.implicitly_wait(0)
        for el in els:
            # Skip reviews that don't actually have stars
            try:
                stars = el.find_element_by_class_name("staticStars")
                print("numstars", len(stars.find_elements_by_class_name("p10")))
                num_stars = len(stars.find_elements_by_class_name("p10"))
            except NoSuchElementException:
                continue

            # Try to press more if possible
            try:
                more = el.find_element_by_link_text("...more")
                more.click()
                # print("found more")
            except NoSuchElementException:
                pass

            # Wait for clicking more to load rest of the review
            # IndexError occurs on reviews with no text just a rating which are skipped
            try:
                wait.until(lambda _: el.find_elements_by_css_selector("span[id^='freeTextContainer'")[0].get_attribute(
                    "innerHTML").strip() != "")
                texts = el.find_elements_by_css_selector("span[id^='freeTextContainer'")
                text = texts[0].get_attribute("innerHTML")
                # print(text)
                df_revs.loc[rev_i] = (bookTitle.strip(), first_author.strip(), num_stars, text.strip())
            except IndexError:
                continue
            rev_cnt += 1
            rev_i += 1
        driver.find_element_by_class_name("next_page").click()
        wait.until(ec.staleness_of(els[5]))
    print(rev_cnt)
    return rev_i


"""
Goes to link and gets all the books in the list
"""
def create_book_links(driver):
    """

    :param driver: web driver
    :return: creates a book list
    """
    driver.get("https://www.goodreads.com/list/show/50.The_Best_Epic_Fantasy")
    books = driver.find_elements_by_class_name("bookTitle")
    books_href = set()
    for book in books:
        books_href.add(book.get_attribute("href"))
    with open("book_links.txt", "w") as file:
        file.write("\n".join(books_href))


if __name__ == "__main__":
    main()
