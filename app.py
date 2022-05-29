from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from urllib.request import urlopen as uReq


app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        # try:
            #search = request.form['content'].replace(" ","")
            #No_of_pages = request.form['No_of_pages']
        data=request.form.items()
        data=dict(data)
        search=data['content']
        No_of_pages=int(data['No_of_pages'])



        reviews = []

        for i in range(1, No_of_pages+1, 1):
            url = 'https://www.flipkart.com/search?q='
            flipkart_page = requests.get(url + search + "&page" + str(i))
            flipkart_html = bs(flipkart_page.text, 'html.parser')
            products = flipkart_html.findAll('div', {"class": "_4rR01T"})
            Product_description = flipkart_html.findAll('ul', {"class": "_1xgFaf"})
            Product_price = flipkart_html.findAll('div', {"class": "_30jeq3 _1_WHN1"})
            Ratings = flipkart_html.findAll('div', {"class": "_3LWZlK"})[0:25]
            image_url = flipkart_html.findAll('div', {"class": "_2QcLo-"})

            for i in range(1, 24):
                try:
                    product_name = products[i].text

                except:
                    product_name = 'No name'

                try:
                    product_description = Product_description[i].text
                except:
                    product_description = 'No description'

                try:
                    product_price = Product_price[i].text
                except:
                    product_price = 'No price'

                try:
                    product_ratings = Ratings[0:25][i].text
                except:
                    product_ratings = 'No ratings'

                try:
                    product_image = image_url[i].div.div.img['src']
                except:
                    product_image = 'No image'

                mydict = ({"Product_name": product_name, "Product_Description": product_description,
                            'Product_price': product_price, 'Product_ratings': product_ratings,
                            "Image": product_image})
                reviews.append(mydict)
                # print(reviews)
        
        df=pd.DataFrame(reviews)
        columns = ['Product_name', 'Product_Description', 'Product_price', 'Product_ratings', 'Image']
        reviews1=[[df.loc[i, col] for col in df.columns] for i in range(len(df))]
        return render_template('results.html', titles =columns , rows = reviews1)

        # except Exception as e:
        #     print('The Exception message is: ',e)
        #     return 'something is wrong'

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
