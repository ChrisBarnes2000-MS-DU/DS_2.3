import requests

r = requests.get("https://api.github.com/search/repositories?q=tensorflow")
print(r[:10])
