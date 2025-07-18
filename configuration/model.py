from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from langchain_ibm import ChatWatsonx
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("WATSONX_APIKEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
url = os.getenv("WATSONX_URL")

parameters = TextChatParameters(
    max_tokens=500,
    temperature=0.5,
    top_p=1,
)


# llama-3-3-70b-instruct
watsonx_llm = ChatWatsonx(
    model_id="meta-llama/llama-3-2-90b-vision-instruct",
    url=url,
    apikey=api_key,
    project_id=project_id,
    params=parameters,
)
