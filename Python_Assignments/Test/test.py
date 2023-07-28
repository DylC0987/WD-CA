from selenium import webdriver

def test_login():
    # Specify the path to your chromedriver 
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get("https://cs1.ucc.ie/~dmc8/cgi-bin/ca1/run.py/login")

    # Find the elements on the webpage
    username_box = driver.find_element("name", "user_id")
    password_box = driver.find_element("name", "password")
    login_button = driver.find_element("name", "submit")

    # Perform actions on the elements
    username_box.send_keys("Test")
    password_box.send_keys("1234")
    login_button.click()

    # Check the result
    assert "Test" in driver.page_source
    print("Login test passed!")

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    test_login()
