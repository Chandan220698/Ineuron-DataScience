from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

def read(url):

    '''
    Return HTML file after html.parser operation.
    Function takes two argument to generate the html of webpage.
    1. url - main url.
    '''
    uClient = uReq(url)  # requesting the webpage from the internet
    urlPage = uClient.read() # Reading the webpage (HTML code of webpage)
    uClient.close()
    final_html = bs(urlPage, "html.parser")

    return final_html