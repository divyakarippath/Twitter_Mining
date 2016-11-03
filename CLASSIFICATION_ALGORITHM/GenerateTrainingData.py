from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


file = open("Diabetes-Personal.txt",'a')

#Selenium web driver
driver = webdriver.Firefox()
driver.get("https://twitter.com/search?q=Diabetes%20-%23Free%20-%23Deal%20lang%3Aen%20since%3A2016-05-01%20until%3A2016-05-31&src=typd")
time.sleep(1)

# fetch tweets from Twitter web search page
body = driver.find_element_by_tag_name('body')
count =0
for _ in range(500):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
tweets = driver.find_elements_by_class_name('tweet-text')

#write the tweet messages into file
for tweet in tweets:
    count+=1
    file.write(tweet.text+'\n')

