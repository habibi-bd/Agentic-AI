import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import json
import re


load_dotenv()

client = genai.Client(api_key="AIzaSyAYJeTPCIkDaRRG6qd9vp3PBTMSMmRt41A")

responce = client.models.generate_content(model="gemini-2.0-flash",
                                       contents= "Hello, world! in java?")

print(responce.text)


# model = genai.GenerativeModel("gemini-1.5-pro")

# response = model.generate_content("Hello, world! in java?")

# print(response.text)
 





class Review(BaseModel):
    key_themes: List[str] = Field(description='Key themes in the review')
    summary: str = Field(description='Summary of the review')
    sentiment: Literal['positive', 'negative', 'neutral'] = Field(description='Sentiment of the review')
    pros: Optional[List[str]] = Field(description='List of pros')
    cons: Optional[List[str]] = Field(description='List of cons')
    name: Optional[str] = Field(default=None, description='Name of the reviewer')

input_text = """I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it's an absolute powerhouse! 
The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I'm gaming, multitasking, or editing photos.
The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.
The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often.
What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light.
Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.
However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung's One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.
Pros:
- Insanely powerful processor (great for gaming and productivity)
- Stunning 200MP camera with incredible zoom capabilities
- Long battery life with fast charging
- S-Pen support is unique and useful
Review by Nitish Singh"""

prompt = f"""Analyze the following review and provide a structured response in JSON format that matches this schema:
{{
    "key_themes": ["list of main themes"],
    "summary": "brief summary",
    "sentiment": "positive/negative/neutral",
    "pros": ["list of pros"],
    "cons": ["list of cons"],
    "name": "reviewer name"
}}

Review text:
{input_text}

Please provide the response in valid JSON format only."""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

try:
    # Clean the response text by removing markdown code block markers if present
    response_text = response.text.strip()
    if response_text.startswith('```json'):
        response_text = response_text[7:]
    if response_text.endswith('```'):
        response_text = response_text[:-3]
    response_text = response_text.strip()
    
    # Parse the response text as JSON
    response_json = json.loads(response_text)
    # Validate the JSON against our Pydantic model
    review = Review.model_validate(response_json)
    print("\nValidated Review:")
    print(json.dumps(review.model_dump(), indent=2))
except json.JSONDecodeError as e:
    print("Error: Response is not valid JSON")
    print("Raw response:", response.text)
except Exception as e:
    print(f"Error: {str(e)}")
