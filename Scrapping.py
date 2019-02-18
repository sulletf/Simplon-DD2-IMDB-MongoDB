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

  def get_films_urls(self):
    # Recuperation des URLs des films de chaque mois

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
    # telechargement de la page HTML du film

    r = requests.get(self.url)

    if r.status_code != 200: return

    soup = BeautifulSoup(r.content, 'html.parser')

    f = open('data/films/{}'.format(self.id), 'w')
    f.write(str(soup))
    f.close()
    
  def scrap(self):
    #  A faire : Scrapping de la page HTML

  def load(self):
    # A faire : enregistrement du film dans MongoDB

  def visu(self):
    # A faire : creation des viz permettant de faire l'analyse des acteurs les 
    # plus rentables

