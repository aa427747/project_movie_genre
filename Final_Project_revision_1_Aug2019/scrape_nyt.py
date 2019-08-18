
# Dependencies
from flask import (request, render_template, jsonify, redirect)
import requests
import json
from config import nyt_key, omdb_key
from bs4 import BeautifulSoup as bs
from splinter import Browser


import matplotlib.pyplot as plt
import pandas as pd

def scrape(movietitle, movieyear):
# Chrome Driver   
   executable_path = {'executable_path': 'chromedriver.exe'}
   browser = Browser('chrome', **executable_path, headless=False)

   # Target Movie & Year

   # target_movie = request.form["movietitle"]
   # #print(target_movie)
   # target_year = movieyear
   # #print(target_year)
   # Build the endpoint URL
   target_url = ('https://api.nytimes.com/svc/movies/v2/reviews/'
               'search.json?query={0}&opening-date={1}-01-01;{1}-12-31&api-key={2}').format(movietitle, movieyear, nyt_key)
   #print(target_url)
   # Run a request to endpoint and convert result to json
   movie_data = requests.get(target_url).json()
   movie_title = movie_data["results"][0]["display_title"]
   review_url = movie_data["results"][0]["link"]["url"]
   try:
      movie_img = movie_data["results"][0]["multimedia"]["src"]
   except TypeError:
      movie_img = "No current image available"

   # #print the movie name and URL
   # print('''
   #    Movie Name: {0}
   #    url: {1}
   #    '''.format(movie_title, review_url))

   # Open NYT Review
   # response = requests.get(review_url)
   browser.visit(review_url)

   # Using old class, pull text of review
   html = browser.html
   soup = bs(html, 'html.parser')
   paragraphs = soup.find_all('p', class_='story-body-text story-content')
   rt1 = ''
   for paragraph in paragraphs:
      review_text1 = paragraph.text
      rt1 = rt1 + ' ' + review_text1

   # Using new class, pull text of review
   html = browser.html
   soup = bs(html, 'html.parser')
   ps = soup.find_all('p', class_='css-exrw3m evys1bk0')
   rt2 = ''
   for p in ps:
      review_text2 = p.text
      rt2 = rt2 + ' ' + review_text2

   # Create if statement to #print all text and create one variable for review text
   review_text = rt2 + rt1
   #print(review_text)

   # Build the endpoint URL for OMDB data

   omdb_url = ('http://www.omdbapi.com/?t={0}&y={1}&apikey={2}').format(movietitle, movieyear, omdb_key)

   # Run a request to endpoint and convert result to json
   omdb_data = requests.get(omdb_url).json()

   # Gather Movie Data from NYT & OMDB
   movie_title = movie_data["results"][0]["display_title"]
   movie_year = omdb_data["Year"]
   imdb_rating = omdb_data["imdbRating"]
   genre = omdb_data["Genre"]
   plot = omdb_data["Plot"]
   poster = omdb_data["Poster"]

      
   # Driver code 
   # if __name__ == "__main__" : 
   
   #    #print("\n1st statement :") 
   
      
   
   # # Create DataFrame for Review Text
   # df = pd.DataFrame(columns =["reviewText"])
   # df.loc[0] = review_text

   # # Split Review Text
   # comment_words = ' '
   # stopwords = set(STOPWORDS)


   # for word in df.reviewText:
   #    word = str(word)
   #    tokens = word.split()
      
   #    for words in tokens:
   #       comment_words = comment_words + words + ' '

  
  

   movie_dict = {
      "movieTitle": movie_title,
      "movieYear": movie_year,
      "movieImg": movie_img,
      "imdbRating": imdb_rating,
      "sentiment": "Positive",
      "genre": genre,
      "plot": plot,
      "review_text": review_text,
      "poster": poster
      }
   #print(movie_dict)
   browser.quit()
   return movie_dict