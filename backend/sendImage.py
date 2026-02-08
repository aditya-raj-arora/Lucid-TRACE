import os
import json
import requests
from dotenv import load_dotenv

load_dotenv() 

db_config = {
    'api_user': os.getenv('API_USER'),
    'api_secret': os.getenv('API_SECRET'),
}

api_user = os.getenv('API_USER')
api_secret = os.getenv('API_SECRET')

def send_image(image_path):
    params = {
        'models': 'genai',
        'api_user': api_user,
        'api_secret': api_secret
    }
    files = {'media': open(image_path, 'rb')}
    response = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
    output = json.loads(response.text)
    return output['type']["ai_generated"]

if __name__ == "__main__":
    image_path = 'test5.jpeg'
    result = send_image(image_path)
    print(f"Is the image AI-generated? {result*100} %")