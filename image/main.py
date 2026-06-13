from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

if not os.getenv("OPENAI_API_KEY") and os.getenv("OPEN_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user",
         "content":[
             {"type": "text", "text": "describe in brife the image"},
             {"type": "image_url", "image_url": { "url": "https://images.pexels.com/photos/879109/pexels-photo-879109.jpeg?_gl=1*wg0wsz*_ga*MTc2OTA3Mzc0NS4xNzgxMzM0MTIx*_ga_8JE65Q40S6*czE3ODEzMzQxMjEkbzEkZzEkdDE3ODEzMzQyMDMkajQxJGwwJGgw"} }    
         ]
         }
    ]
)

print(response.choices[0].message.content)
