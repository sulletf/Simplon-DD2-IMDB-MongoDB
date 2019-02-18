from bs4 import BeautifulSoup

import requests
import re

class FilmList:

  def __init__(self, year):
    self.year = year

  def download_html(self):
    for month in range(1,13):
      url = 'https://www.imdb.com/movies-coming-soon/{:04d}-{:02d}'.format(self.year,month)
      r = requests.get(url)

      if r.status_code != 200:
        continue

      soup = BeautifulSoup(r.content, 'html.parser')

      f = open('data/film_lists/{:04d}-{:02d}'.format(self.year,month), 'w')
      f.write(str(soup))
      f.close()

  def get_films_urls(self):
    films = []

    for month in range(1,13):
      f = open('data/film_lists/{:04d}-{:02d}'.format(self.year,month), 'r')
      soup = BeautifulSoup(f, 'html.parser')

      for elem in soup.find_all('td',attrs={"class" :"overview-top"}):
        films.append(elem.h4.a.get('href'))
      
      f.close()

    return films

class Film:

  def __init__(self, url):
    self.url = 'https://www.imdb.com/' + url
    
    l = url.split('/')
    self.id = l[2]

  def download_html(self):
    r = requests.get(self.url)

    if r.status_code != 200: return

    soup = BeautifulSoup(r.content, 'html.parser')

    title = None

    for elem in soup.find_all('div',attrs={"class" :"title_wrapper"}):
      title = elem.h1.text
      break

    f = open('data/films/{}'.format(self.id), 'w')
    f.write(str(soup))
    f.close()
    
  def scrap(self):
    f = open('data/films/{}'.format(self.id), 'r')
    soup = BeautifulSoup(f, 'html.parser')

    self.title = soup.find('h1').text

    self.grossUSA = self.get_amount(soup, 'Gross USA')
    self.grossWW = self.get_amount(soup, 'Cumulative Worldwide Gross')

  def get_amount(self, soup, amount_type):
    amount = None
    for div in soup.find_all('div',attrs={"class" :"txt-block"}):
      h4 = div.find('h4',attrs={"class" :"inline"})
      if h4 is not None and h4.text == amount_type + ':':
        amount = div.text.split('\n')[1]
        # amount is like 'Gross USA: $36,343,858, 15 March 2018'
        # we clean it
        pattern = '^' + amount_type + ': \$((\d+,?)+)(,.+?)?$'
        x = re.match(pattern, amount)
        amount = x.group(1)

    return amount
     
#    self.actors = self.scrap_actors(soup)
