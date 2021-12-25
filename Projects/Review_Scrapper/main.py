# Importing libraries
from flask import Flask, render_template,request
import pymongo
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
import requests
import fetch_html ## Custom Libraray to fetch the html page

app = Flask(__name__)  ## Initialising the Flash app with name 'app'

# base URL + /
# https://localhost:8000 + /
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':

         # Form - class in the index HTML and content is field inside it
        searchString = request.form['content'] # Fetching the search string entered by user
        searchString = searchString.replace(" ", "") # Removing all the  blank spaces

        try:
            dbConn = pymongo.MongoClient("mongodb://LOCALHOST:27017/") # Creating a connection with mongoDB db
            ## Creating a DB, if not exist
            db = dbConn['scrapperDB_test'] ## database name - scrapperDB 
            reviews = db[searchString].find({})  # searching the collection with name same as searchString

            if reviews.count() > 0:
                # reviews are available in the scrapperDB
                return render_template('results.html',reviews=reviews)
            else:
                # No reviews are available in the scrapperDB
                # No collection with searchString
                flipkart_url = "https://www.flipkart.com/search?q="
                flipkart_url = flipkart_url + searchString
                flipkart_html = fetch_html.read(flipkart_url)

                allProducts = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
                targetProduct = allProducts[2] # Getting the first product

                # Actual link for target product
                targetProductLink = "https://www.flipkart.com"
                targetProductLink = targetProductLink + targetProduct.div.div.div.a['href']
                product_html = fetch_html.read(targetProductLink)

                reviewBox = product_html.find_all("div", {'class': "_16PBlm"})

                ## Creating the collection in DataBase with same name as searchString
                table = db[searchString]

                reviews = [] # List to store all the reviews under html class _16PBlm
                for review in reviewBox:
                    try:
                        name = review.div.div.find_all('p', {'class': "_2sc7ZR _2V5EHH"})[0].text
                    except:
                        name = 'No Name'

                    try:
                        rating = review.div.div.div.div.text
                    except:
                        rating = 'No Rating'

                    try:
                        commentHead = review.div.div.div.p.text
                    except:
                        commentHead = 'No Comment Heading'

                    try:
                        comtag = review.div.div.find_all('div', {'class': ''})
                        custComment = comtag[0].div.text
                    except:
                        custComment = 'No Customer Comment'

                    mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                              "Comment": custComment}
                    x = table.insert_one(mydict)
                    reviews.append(mydict)

                return render_template('results.html', reviews = reviews)

        except:
            return 'something is wrong'
        finally:
            dbConn.close()

    else: # GET method
        # Append the Data to the url
        return render_template('index.html')  # Initial Web search page # GET - Pass the data



if __name__ == "__main__":
    app.run(port = 8000,debug=True)