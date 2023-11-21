from openai import OpenAI
import openai
import os
# Set your OpenAI API key
api_key = "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"  # Replace with your actual API key
os.environ["OPENAI_API_KEY"] = api_key
client = OpenAI( )
max_tokens = 100
"""#Modelo con ADA (No funciona)
response = openai.Completion.create(engine = 'text-ada-01',promp = "Dime los 5 alimentos mas consumidos en LATAM",max_tokens = 50,n =1,temperature=1 )
print(response.choices[0])"""

#"""
completion = client.chat.completions.create(
  model="gpt-3.5-turbo", 
 # model = "text-embedding-ada-002",
  messages=[
    {"role": "assistant", "content": "Quiero saber los ingredientes del seco de pollo"},
  ], 
  max_tokens= max_tokens
)


print(completion.choices[0].message)
#"""

