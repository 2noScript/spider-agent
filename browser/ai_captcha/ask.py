import os
import base64
import re
import time
from openai import OpenAI, APIStatusError
from google import genai
from google.genai import types
from browser.settings import AiHelperSettings


gemini_client=genai.Client(api_key=AiHelperSettings.google_api_key)
openai_client=OpenAI(api_key=AiHelperSettings.open_api_key)


