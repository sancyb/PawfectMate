import requests

url = "http://localhost:5000/ask"
data={
      "question": "I have 2+2 family with children in age 10-15. We are very active and want to have middle-size dog, easy to train. Write me 5 breeds."}

response = requests.post(json=data,
              url=url)

print("Status:", response.status_code)
print("Text:", response.text)
# print(response.json())