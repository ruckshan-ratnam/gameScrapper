import requests
from bs4 import BeautifulSoup


url = ""

r = requests.get(url)

soup = BeautifulSoup(r.text,'html.parser')

info = soup.find_all("span","view")

game_page_link = soup.find("a","list-item")['href']