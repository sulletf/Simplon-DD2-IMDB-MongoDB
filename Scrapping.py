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
    #  A faire : Scrapping de la page HTML
    pass

  def load(self):
    # A faire : enregistrement du film dans MongoDB
    pass

  def visu(self):
    # A faire : creation des viz permettant de faire l'analyse des acteurs les 
    pass
    # plus rentables


