from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

from google import genai
import google.generativeai as genai


load_dotenv()

client = genai.configure(api_key="AIzaSyAYJeTPCIkDaRRG6qd9vp3PBTMSMmRt41A")

model1 = genai.GenerativeModel("gemini-2.0-flash")

parser1=StrOutputParser()

class FeedBack(BaseModel):
    sentiment: Literal['Positive', "negative"]= Field(description="Give me the sentment of feedback")

parser2=PydanticOutputParser(pydantic_object=FeedBack)

prompt1=PromptTemplate(
    template="Classify the sentce of the following feedback text into positive or negative {feedback} \n {format_instruction}",
    input_variables=['feedback'],
    partial_variables={'format_instruction':parser2.get_format_instructions()}
)
classifier_chain=prompt1|model1|parser1