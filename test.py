import requests

# The URL of your FastAPI application
url = "http://127.0.0.1:8000/search/"

# The query string you want to search for
query_text = "How to configure SAP build apps"

# The number of top similar documents you want to retrieve
top_n = 5

# The payload to send in the POST request
payload = {
    "query_text": query_text,
    "top_n": top_n
}

# Send the POST request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    results = response.json()
    print(results)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
