from selenium import webdriver
import pandas as pd


def web_scrape():
    # Specify the path to your chromedriver 
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get("https://www.python.org/events/")

    # Find the elements on the webpage
    event_times = driver.find_elements("css selector", ".shrubbery time")
    event_names = driver.find_elements("css selector", ".shrubbery .event-title a")
    event_location = driver.find_elements("css selector", ".shrubbery span.event-location")
    events = {}
    
    #create dictionary of events
    for n in range(len(event_times)):
        events[n] = {
            "name" : event_names[n].text,
            "location" : event_location[n].text,
            "time" : event_times[n].text
        }

    # Convert the dictionary to a pandas DataFrame
    # Because each key in the dictionary is a row number and each value is another dictionary representing an event, orient='index' is used.
    df = pd.DataFrame.from_dict(events, orient='index')

    # Write the DataFrame to a csv file
    df.to_csv('events.csv', index=False)

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    web_scrape()
