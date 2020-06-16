import os
from dotenv import load_dotenv
import requests

load_dotenv('../1.env')
key = os.environ.get('key')

res = requests.get("https://www.goodreads.com/book/review_counts.json",
                    params={"key": key, "isbns": "9781632168146"})
print(res.json())
