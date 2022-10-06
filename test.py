import requests

# url = "https://s3.amazonaws.com/my89public/quac/val_v0.2.json"
# url = "https://s3.amazonaws.com/my89public/quac/train_v0.2.json"
url = "https://downloads.cs.stanford.edu/nlp/data/coqa/coqa-train-v1.0.json"

response = requests.get(url=url)

data = response.json()["data"]

print(len(data))
print(data[:1])
