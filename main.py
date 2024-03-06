import requests,os,json
from bs4 import BeautifulSoup


# Define the URL of the Wikipedia page to scrape
url="https://en.wikipedia.org/wiki/Hair_loss"

# Send a GET request to the URL and parse the HTML content
r=requests.get(url)

soup=BeautifulSoup(r.text,"html.parser")
data=soup.find_all("div",class_="mw-page-container")

# Function to interact with the GPT-3.5 model for summarization
def ask_chatgpt(prompt, api_key, max_tokens=500, temperature=0.7, engine="davinci"):
  url = "https://api.openai.com/v1/chat/completions"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
  }
  data = {

      "max_tokens": max_tokens,
      "temperature": temperature,

      "model": "gpt-3.5-turbo",
      "messages": [{"role": "system", "content": prompt}]# Use prompt as the content of the message
    }

  response = requests.post(url, json=data, headers=headers)

  if response.status_code == 200:
      return response.json()["choices"][0]["message"]["content"].strip() # Access the generated text
  else:
      print("Error:", response.text)
      return None


# Loop through the scraped data
for content in data:
  # Example usage:
  api_key = os.environ['openaikey'] # Fetch the OpenAI API key from environment variables
  inner_content=content.find_all("div",{"class":"mw-content-ltr mw-parser-output"})
  if inner_content:
    # Prepare the prompt for summarization
    prompt = "summarize in no more than 3 paragraphs: " + inner_content[0].text
    # Call the GPT-3.5 model for summarization
    response = ask_chatgpt(prompt, api_key)
    print(response)