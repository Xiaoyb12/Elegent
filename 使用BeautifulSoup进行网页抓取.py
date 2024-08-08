import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 从网页中提取数据
data = soup.find('div', class_='content')
print(data.text)