from selenium import webdriver

# Test Case Scenario: Testing the login functionality of my "Heard" website

# Test 1
# Test Case Name: Validate Login Functionality 

# Preconditions: The website "https://cs1.ucc.ie/~dmc8/cgi-bin/ca1/run.py/login" is accessible, and there exists a user with username "Test" and password "1234".

# Test Steps:
# Launch the Chrome browser using Selenium WebDriver.
# Open the login page of the "Heard" website.
# Identify the username and password input fields.
# Enter "Test" into the username field.
# Enter "1234" into the password field.
# Identify the "Submit" button and click it.
# Assert that "Test" is found within the page source after logging in.

# Expected Result: The string "Test" should be found in the page source after logging in, indicating a successful login. "Login test passed!" will print to console.

# Actual Result: "Login test passed!" printed on console

# Status: Pass

def test_login_with_valid_credentials():
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


# Test 2
# Test Case Name: Validate Incorrect Password Handling

# Preconditions: The website "https://cs1.ucc.ie/~dmc8/cgi-bin/ca1/run.py/login" is accessible, and there exists a user with username "Test" but the password is not "wrong_password".

# Test Steps:
# Launch the Chrome browser using Selenium WebDriver.
# Open the login page of the "Heard" website.
# Identify the username and password input fields.
# Enter "Test" into the username field.
# Enter "wrong_password" into the password field.
# Identify the "Submit" button and click it.
# Assert that the login was not successful.

# Expected Result: The login should not be successful, and "Incorrect password test passed!" should be printed on the console.

# Actual Result: "Incorrect password test passed!" printed on console

# Status: Pass


def test_login_with_invalid_password():
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
    password_box.send_keys("wrong_password")
    login_button.click()

    # Check the result 
    assert "Incorrect password!" in driver.page_source
    print("Incorrect password test passed!")

    # Close the driver
    driver.quit()


# Test 3
# Test Case Name: Validate Incorrect Username Handling

# Preconditions: The website "https://cs1.ucc.ie/~dmc8/cgi-bin/ca1/run.py/login" is accessible, and there exists a user with username "Test" but the password is not "wrong_password".

# Test Steps:
# Launch the Chrome browser using Selenium WebDriver.
# Open the login page of the "Heard" website.
# Identify the username and password input fields.
# Enter "Test" into the username field.
# Enter "wrong_password" into the password field.
# Identify the "Submit" button and click it.
# Assert that the login was not successful.

# Expected Result: The login should not be successful, and "Incorrect username test passed!" should be printed on the console.

# Actual Result: "Incorrect username test passed!" printed on console.

# Status: Pass    

def test_login_with_invalid_username():
    # Specify the path to your chromedriver 
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get("https://cs1.ucc.ie/~dmc8/cgi-bin/ca1/run.py/login")

    # Find the elements on the webpage
    username_box = driver.find_element("name", "user_id")
    password_box = driver.find_element("name", "password")
    login_button = driver.find_element("name", "submit")

    # Perform actions on the elements
    username_box.send_keys("Invalid_name")
    password_box.send_keys("1234")
    login_button.click()

    # Check the result 
    assert "No such user" in driver.page_source
    print("Incorrect username test passed!")

    # Close the driver
    driver.quit()    

# Test 4
# Test Case Name: Validate Empty Field Handling

# Preconditions: The website "https://cs1.ucc.ie/~dmc8/cgi-bin/ca1/run.py/login" is accessible.

# Test Steps:
# Launch the Chrome browser using Selenium WebDriver.
# Open the login page of the "Heard" website.
# Identify the username and password input fields.
# Leave one or both fields empty.
# Identify the "Submit" button and click it.
# Assert that the login was not successful.

# Expected Result: The login should not be successful, and "Empty field test passed!" should be printed on the console.

# Actual Result: "Empty field test passed!" printed on console.

# Status: Pass

def test_login_with_empty_fields():
    # Specify the path to your chromedriver 
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get("https://cs1.ucc.ie/~dmc8/cgi-bin/ca1/run.py/login")

    # Find the elements on the webpage
    username_box = driver.find_element("name", "user_id")
    password_box = driver.find_element("name", "password")
    login_button = driver.find_element("name", "submit")

    # Perform actions on the elements
    username_box.send_keys("")
    password_box.send_keys("")
    login_button.click()

    # Check the result
    assert "This field is required." in driver.page_source
    print("Empty field test passed!")

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    test_login_with_valid_credentials()
    test_login_with_invalid_password()
    test_login_with_invalid_username()
    test_login_with_empty_fields()
