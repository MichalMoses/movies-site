from django.shortcuts import render, redirect
from django.http import HttpResponse
from movies.models import Movie, Cast
from actors.models import Actor

def main(request):
    return redirect('movies:list')

def not_found(request,nonexist):
    return render(request, '404.html')

def about(request):
    return render(request, 'about.html')

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
import string
from bs4 import BeautifulSoup  # need to pip install beautifulsoup4
import os
from actors.models import Actor
from movies.models import Movie, Cast
import httpx
import urllib.request

'''the following function operates the scraper on https://www.themoviedb.org/movie. 
it collects all the data that is presented in this site: movie data and actors data. 
it updates the database only if an entry does not already exist for the Movie or Actor
function access reserved for superusers only'''


@user_passes_test(lambda u: u.is_superuser)
def scraper(request):
    print('---DEBUG scraper starting')
    actors_list = []
    posters_dir = str(os.getcwd()) + ('\media\posters')

    actors_dir = str(os.getcwd()) + (r'\media\actors')

    for k in range(1,6):

        #fake browser headers so the scraper won't get blocked
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

        # ---------------------------------------------------------------------------------------------------------------
        # MOVIES TABLE go over the movie elements one by one and get all the required data
        URL = f"https://www.themoviedb.org/movie?page={k}"
        page =httpx.get(URL, headers=HEADERS,follow_redirects=True)

        soup = BeautifulSoup(page.content, "html.parser")  # soup type: <class 'bs4.BeautifulSoup'>
        # print(f'--DEBUG main soup: {soup}')
        results_main = soup.find("section", id='media_results')  # results type: <class 'bs4.element.Tag'>
        movies_elements = results_main.find_all("div",class_='card style_1')  # movies elements type is <class 'bs4.element.ResultSet'>

        for i, movie_element in enumerate(movies_elements):  # take one movie element
            print(f'---------------------------------------------------------------------------------------------------\nMovie {i} in page {k}')
            movie_title = movie_element.find_all('h2')  # get the movie title which contains name and movie page path
            for data in movie_title:  # extract data from the title
                movie_name = data.find('a').text.strip()
                movie_page_path = data.find('a')['href']
            movie_rating_percent = (movie_element.find('div', class_='outer_ring').find_all('div')[0]['data-percent'])
            movie_rating = float(movie_rating_percent) / 20
            # print(f'--DEBUG movie rating: {movie_rating}')

            poster_name = movie_name.replace(" ","_").replace("/","")

            print(f'--DEBUG movie {movie_name}')

            try:
                movie_exists=Movie.objects.get(name=movie_name)
            except:
                print(f'-- DEBUG movie {movie_exists.name} isnt in DB')
                proceed=1
            else:
                print(f'-- DEBUG movie {movie_exists.name} already exists')
                proceed=0

            if proceed==0:
                print(f'--DEBUG moving on to the next movie')
                continue #go to the next i in loop
            else:
                print(f'--DEBUG continue with the code')



                #download poster
                # '''
                movie_poster_path = movie_element.find('img', class_='poster')['src']  # get the source url of the poster
                print(f'--DEBUG movie poster path: {movie_poster_path}')
                movie_poster_url = "https://www.themoviedb.org/" + movie_poster_path  # go to the poster url to download it

                f = open(f'{posters_dir}\{poster_name}.jpeg', 'wb')
                f.write(urllib.request.urlopen(movie_poster_url).read())
                f.close()
                # '''

                #go to the movie page and get additional data from there
                URL = "https://www.themoviedb.org" + movie_page_path
                # print(f'--DEBUG movie page url {URL}')
                page = httpx.get(URL, headers=HEADERS, follow_redirects=True)
                # print(f'--DEBUG movie page {page}')

                movie_page_soup = BeautifulSoup(page.content, "html.parser")  # sub_soup type: <class 'bs4.BeautifulSoup'>
                # print(f'--DEBUG movie page soup {movie_page_soup}')

                #going through <section class='header poster'> for relevant data
                results_mpage_data = movie_page_soup.find("section", class_='header poster')  # results type: <class 'bs4.element.Tag'>
                # print(f'--DEBUG movie page data {results_mpage_data}')

                try:
                    release = results_mpage_data.find('span', class_="release").text.strip()[:10].replace("-","/")
                except:
                    movie_release = ""
                else:
                    movie_release = f'{release[6:]}-{release[0:2]}-{release[3:5]}'


                movie_genres = ""
                try:
                    movie_genres_soup = results_mpage_data.find('span', class_="genres")
                    # print(f'--DEBUG genre soup {movie_genres_soup}')
                    movie_genres_all = movie_genres_soup.find_all('a')
                except:
                    movie_genres=""
                else:
                # print(f'--DEBUG genre object {movie_genres_all}')
                    for genre in movie_genres_all:
                        movie_genres = movie_genres + genre.text.strip() + ", "
                    print(f'--DEBUG movie genres string: {movie_genres}')

                try:
                    movie_runtime = results_mpage_data.find('span', class_="runtime").text.strip()
                except:
                    movie_runtime=""

                try:
                    movie_overview = results_mpage_data.find('div', class_='overview').text.strip()
                except:
                    movie_overview = ""


                slug = movie_name.lower()
                movie_slug = ''.join([i for i in slug if i in string.ascii_lowercase or i.isnumeric() or i == " "]).replace(" ", "-")

                try:
                    people = results_mpage_data.find_all('li', class_='profile')
                except:
                    movie_director = 'unknown'
                else:
                    for person in people:
                        person_name = person.find('a').text.strip()
                        person_role = person.find('p', class_='character').text.strip()
                        if 'Director' in person_role:
                            movie_director = person_name

                try:
                    movie = Movie.objects.create(poster = f'posters/{poster_name}.jpeg',
                                             name = movie_name,
                                             slug = movie_slug,
                                             overview = movie_overview,
                                             director = movie_director,
                                             release = movie_release,
                                             runtime = movie_runtime,
                                             genre = movie_genres,
                                             rating_avg = movie_rating,
                                             rating_num = 0,
                                             author = request.user
                                             )
                except Exception:
                    continue
                else:
                    movie.save()
                    print(f'----DEBUG movie {movie_name} object created')

                # ---------------------------------------------------------------------------------------------------------------
                # CAST TABLE go over the movie elements one by one and get all the required data

                #going through <div id='cast_scroller'> for actors data
                results_movie_page_actors = movie_page_soup.find("div", id='cast_scroller')  # results type: <class 'bs4.element.Tag'>
                try:
                    actors_elements = results_movie_page_actors.find_all('li', class_='card')
                except:
                    pass
                else:
                    #for each actor get actor name and character for Cast table
                    for j, element in enumerate(actors_elements):
                        actor_name = element.find_all('a')[1].text
                        actor_character = element.find('p', class_='character').text
                        # cast = (actor_name,movie_name,actor_character)

                        try:
                            actors_elements=Actor.objects.get(actor_name=actor_name)
                        except Exception:
                            print(f'--DEBUG actor {actor_name} not in DB')
                            proceed=1
                        else:
                            proceed=0
                            print(f'--DEBUG actor {actor_name} already in DB')

                        if proceed==0:
                            print(f'--DEBUG continue to next actor')
                            continue
                        else:




                            # ---------------------------------------------------------------------------------------------------------------
                            # ACTOR TABLE. only if the actor in Cast doesn't appear in Actors, get their data
                            actor_page_path = element.find_all('a')[0]['href']
                            #go to actor page to fill up the actor details only if the actor doesn't already exists

                            #todo all the actors from the actor table and check in the new actor exists. this is instead of actors_list


                            if actor_name not in actors_list:

                                URL = "https://www.themoviedb.org" + actor_page_path
                                page = httpx.get(URL, headers=HEADERS, follow_redirects=True)
                                actor_page_soup = BeautifulSoup(page.content, "html.parser")  # sub_soup type: <class 'bs4.BeautifulSoup'>

                                results_actor_page = actor_page_soup.find('div', class_='content_wrapper')
                                actor_details = results_actor_page.find('div', class_='column').find_all('p')
                                actor_gender = actor_details[2].text[7:]
                                actor_birthday = actor_details[3].text[9:].strip()[:10]
                                actor_place_of_birth = actor_details[4].text[15:].strip()
                                slug = actor_name.lower()
                                actor_slug = ''.join([i for i in slug if i in string.ascii_lowercase or i.isnumeric() or i == " "]).replace(" ", "-")
                                # print(f'genre: {actor_genre}\nbirthday: {actor_birthday}\nplace: {actor_place_of_birth}')

                                #get the image path, and download
                                # '''
                                portrait_name = actor_name.replace(" ", "_")
                                try:
                                    actor_image_path = results_actor_page.find('div', class_='image_content').find('img')['data-src']
                                except Exception:
                                    continue
                                else:
                                    actor_image_url = "https://www.themoviedb.org/" + actor_image_path  # go to the image url to download it
                                    f = open(f'{actors_dir}/{portrait_name}.jpeg', 'wb')
                                    f.write(urllib.request.urlopen(actor_image_url).read())
                                    f.close()
                                # '''

                                #write actor to Actors and update actors_list
                                try:
                                    actor = Actor.objects.create(actor_name = actor_name,
                                                                 actor_image = f'actors/{portrait_name}.jpeg',
                                                                 actor_gender = actor_gender,
                                                                 actor_birthday = actor_birthday,
                                                                 actor_place_of_birth = actor_place_of_birth,
                                                                 slug = actor_slug
                                                                 )
                                except:
                                    continue
                                else:
                                    actor.save()
                                    print(f'----DEBUG actor {actor_name} object created')
                                    actors_list.append(actor_name)

                            movie = Movie.objects.get(name = movie_name)
                            actor = Actor.objects.get(actor_name = actor_name)

                            cast = Cast.objects.create(actor_name_id = actor.id,
                                                       movie_name_id = movie.id,
                                                       role_in_movie = actor_character)
                            cast.save()
                            print(f'----DEBUG cast for {actor_name} in {movie_name} object created')


    return HttpResponse('<h1>Scraping complete</h1>')

