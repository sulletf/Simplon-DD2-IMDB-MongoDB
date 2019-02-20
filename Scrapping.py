from bs4 import BeautifulSoup

import requests
import re

class FilmList:

  def __init__(self, year):
    self.year = year

  def download_html(self):
    # telechargement des pages HTML 'coming soon' de tous les mois de l'annee

    for month in range(1,13):
      url = 'https://www.imdb.com/movies-coming-soon/{:04d}-{:02d}'.format(self.year,month)
      r = requests.get(url)

      if r.status_code != 200:
        continue

      soup = BeautifulSoup(r.content, 'html.parser')

      f = open('data/film_lists/{:04d}-{:02d}'.format(self.year,month), 'w')
      f.write(str(soup))
      f.close()

  def get_films_ids(self):
    # Recuperation des ids des films de chaque mois

    film_ids = []

    for month in range(1,13):
      f = open('data/film_lists/{:04d}-{:02d}'.format(self.year,month), 'r')
      soup = BeautifulSoup(f, 'html.parser')

      for elem in soup.find_all('td',attrs={"class" :"overview-top"}):
        href = elem.h4.a.get('href')
        id = href.split('/')[2]
        film_ids.append(id)
      
      f.close()

    return film_ids

class Film:

  def __init__(self, id):
    self.url = 'https://www.imdb.com/title/' + id
    self.id = id

  def download_html(self):
    # telechargement de la page HTML du film

    r = requests.get(self.url)

    if r.status_code != 200: return

    soup = BeautifulSoup(r.content, 'html.parser')

    f = open('data/films/{}'.format(self.id), 'w')
    f.write(str(soup))
    f.close()
    
  def download_actors_html(self):
    # telechargement de la page HTML du film

    r = requests.get(self.get_actors_url())

    if r.status_code != 200: return

    soup = BeautifulSoup(r.content, 'html.parser')

    f = open('data/actors/{}'.format(self.id), 'w')
    f.write(str(soup))
    f.close()
    
  def get_actors_url(self):
    # Recuperation de l'URL des acteurs du film

    #f = open('data/films/{}'.format(self.id), 'r')
    #soup = BeautifulSoup(f, 'html.parser')

    #div = soup.find('div',attrs={"id" :"titleCast"})
    #actors_url = div.div.a.get('href')

    #f.close()

    return self.url + '/' + 'fullcredits'

  def scrap(self):
    f = open('data/films/{}'.format(self.id), 'r')
    soup = BeautifulSoup(f, 'html.parser')

    self.title = soup.find('h1').text

    self.grossUSA = self.get_amount(soup, 'Gross USA')
    self.grossWW = self.get_amount(soup, 'Cumulative Worldwide Gross')
    self.actors = self.get_actors()

  def get_actors(self):
    actors = []

    f = open('data/actors/{}'.format(self.id), 'r')
    soup = BeautifulSoup(f, 'html.parser')

    table = soup.find('table', attrs={"class" :"cast_list"})
    if table is None:
      f.close()
      return []

    odd_trs = table.find_all('tr', attrs={"class" :"odd"})
    for tr in odd_trs:
      td = tr.find_all('td')[1]
      actors.append(td.a.text)

    even_trs = table.find_all('tr', attrs={"class" :"even"})
    for tr in even_trs:
      td = tr.find_all('td')[1]
      actors.append(td.a.text)

    f.close()

    return actors

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

  def load(self, db):
    film_dict = {"title": self.title, "url": self.url, "imdb_id": self.id, "grossUSA": self.grossUSA, "grossWW": self.grossWW, "actors": self.actors}

    film_coll = db.films
    film_coll.insert_one(film_dict)
    
  def visu(self):
    # A faire : creation des viz permettant de faire l'analyse des acteurs les 
    pass
    # plus rentables


