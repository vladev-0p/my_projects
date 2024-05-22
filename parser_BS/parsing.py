from bs4 import BeautifulSoup
import lxml
import os.path




BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pars_path = os.path.join(BASE_DIR, "Johnny Depp - Wikipedia.html")
with open(pars_path, encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src,'lxml')
#
title = soup.title
# #
print(title.text)
#page_p = soup.find_all("p") # looks for all paragraph

# for _ in page_p:
#     print(_.text)
x="span class"
page_h = soup.find_all("span", class_="mw-headline") #Looking for headers
k=''
for _ in page_h:
    print(_.text)
