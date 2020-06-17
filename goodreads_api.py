import os
from dotenv import load_dotenv
import requests

load_dotenv('./project1.env')
key = os.environ.get('key')

def get_rating(isbn):
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                    params={"key": key, "isbns": isbn})
        json = res.json()
        num_rating, avg_rating = json['books'][0]['ratings_count'], json['books'][0]['average_rating']
        return num_rating, avg_rating
    except:
        return 0
