# Added in V2 -
# scrapes bitinfo ETC for block reward

from selenium import webdriver

# Set browser and options

# browser = webdriver.safari.webdriver.WebDriver(quiet=False)

# Get the web page

# browser.get("https://bitinfocharts.com/comparison/ethereum%20classic-hashrate.html")

def etc_network_hashrate(browser):

    # Get the web page
    browser.get("https://bitinfocharts.com/comparison/ethereum%20classic-hashrate.html")

    # Copy some text from website
    network_hashrate = browser.find_element_by_xpath("/html/body/div[3]/h2/abbr")

    network_content = network_hashrate.get_attribute("innerHTML") # Get HTML of an element

    # Isolate numbers in string and convert them to floats

    network_content = network_content.replace("T", "") # remove letter T from string

    network_content = float(network_content) # Convert string of numbers to float

    return network_content

def etc_block_reward(browser):

    browser.get("https://bitinfocharts.com/ethereum%20classic/")

    block_reward_text = browser.find_element_by_xpath("//*[@id='tdid13']/span[1]/abbr[1]")

    block_reward_html = block_reward_text.get_attribute("innerHTML")

    return float(block_reward_html)

def etc_block_time(browser):

    browser.get("https://bitinfocharts.com/ethereum%20classic/")

    block_time_text = browser.find_element_by_xpath("//*[@id='tdid9']")

    block_time_html = block_time_text.get_attribute("innerHTML")

    block_time_html = block_time_html.replace("s","")

    return float(block_time_html)
