from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "D:\DevBase\DeveloperTools\Drivers\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get(url="https://en.wikipedia.org/wiki/Main_Page")

article_count = driver.find_element(by=By.CSS_SELECTOR, value="#articlecount a")
print(article_count.text)

# click links
content_portals = driver.find_element(by=By.LINK_TEXT, value="Content portals")
content_portals.click()

# Search
search = driver.find_element(by=By.ID, value="searchInput")
search.send_keys("James Webb Space Telescope")
search.send_keys(Keys.ENTER)
