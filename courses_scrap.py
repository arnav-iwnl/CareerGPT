from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrapit(url):
    links = []
    try:
        # Initialize Chrome WebDriver using raw string literal for the path
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options = options)
        # Load the page
        driver.get(url)
        # Find links using appropriate XPath 
        course_elements = driver.find_elements(By.XPATH, "//a[contains(text(), 'View Course')]")
        links = [element.get_attribute("href") for element in course_elements]

        for element in course_elements[:3]:
            link = element.get_attribute("href")
            if link is not None:
                links.append(link)

    except Exception as e:
        print(f"Error scraping course links: {e}")

    finally:
        if 'driver' in locals():
            # Close the WebDriver if it's defined
            driver.quit()

    return links[:3]


# Example usage
# course_url = "https://www.coursebuffet.com/search?q=web"
# course_links = scrapit(course_url)
# print("Course Links:", course_links)