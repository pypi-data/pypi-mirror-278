from bs4 import BeautifulSoup
from lxml import etree
import requests

url = 'https://github.com/awesome-spectral-indices/awesome-spectral-indices?tab=readme-ov-file'
webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup))
indexes = []
planet_elements = dom.xpath("//img[@alt='Planet-Fusion']")
for planet_element in planet_elements:
    indexes.append(planet_element.getparent().getparent().getparent().xpath('.//td')[0].xpath('.//a')[0].text)

print(indexes)
