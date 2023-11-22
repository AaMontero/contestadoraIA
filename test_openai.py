from openai import OpenAI
import openai
import os

class claseOpenAI: 
  def __init__(self,api_key): 
    self.api_key = api_key
    os.environ["OPENAI_API_KEY"] = api_key
    self.client = OpenAI()
  def obtener_respuesta(self, pregunta):
    max_tokens = 100
    completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": pregunta},
        ],
        max_tokens=max_tokens
    )
    return str(completion.choices[0].message.content)

