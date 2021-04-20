from bs4 import BeautifulSoup
import requests
import json
import re

MAIN_URL = 'https://www.imdb.com/search/title/?genres=musical&explore=title_type,genres&ref_=tt_ov_inf'
BASE_URL = 'https://www.imdb.com'
NUMBER_OF_PAGES = 7
movie_id = 0


def get_movie_year(header):
    """
    :param header: header element as BeautifulSoup
    :return: the movie/series year/s
    """
    year = header.find(class_="lister-item-year").text
    year = re.findall(r'\d+', year)
    if len(year) == 2:
        return year[0] + '-' + year[1]
    elif len(year) == 1:
        return year[0]
    else:
        return None


def get_movie_length(movie):
    """
    :param movie: movie card element as BeautifulSoup
    :return: movie length in minutes
    """
    length = movie.find('span', class_="runtime")
    if length:
        length = re.findall(r'\d+', length.text)
    return length


def get_movie_rating(movie):
    """
    :param movie: movie card element as BeautifulSoup
    :return: movie rating (PG-13,R, etc)
    """
    rating = movie.find('span', class_="certificate")
    if rating:
        rating = rating.text
    return rating


def get_movie_genres(movie):
    """
    :param movie: movie card element as BeautifulSoup
    :return: movie genres
    """
    genres = movie.find('span', class_="genre")
    if genres:
        genres = " ".join(genres.text.split())
    return genres


def get_movie_votes_and_gross(movie):
    """
    :param movie: movie card element as BeautifulSoup
    :return: number of votes for the movie and movie's gross
    """
    votes_and_gross = movie.find(class_="sort-num_votes-visible")
    if votes_and_gross:
        votes_and_gross = votes_and_gross.find_all('span', {'name': 'nv'})
        if len(votes_and_gross) == 2:
            votes = votes_and_gross[0].text
            gross = votes_and_gross[1].text
        elif len(votes_and_gross) == 1:
            votes = votes_and_gross[0].text
            gross = None
        else:
            votes = None
            gross = None
    else:
        votes = None
        gross = None
    return votes, gross


def get_movie_imdb_rating(movie):
    """
    :param movie: movie card element as BeautifulSoup
    :return: the movie rating (1-10 stars)
    """
    imdb_rating = movie.find(class_="ratings-imdb-rating")
    if imdb_rating:
        imdb_rating = imdb_rating.find("strong").text
    return imdb_rating


def get_movie_director_and_stars(movie_soup):
    """
    :param movie_soup: the movie page as BeautifulSoup
    :return: the movie director and the stars of the movie
    """
    credits_sum = movie_soup.find_all(class_="credit_summary_item")
    director = None
    stars = None
    if credits_sum:
        for credit in credits_sum:
            if "Director" in credit.find('h4').text:
                director = credit.find('a').text
            elif "Stars" in credit.find('h4').text:
                stars = credit.find_all('a')
                stars = [star.text for star in stars if "See full" not in star.text]
    return director, stars


def get_one_data_from_movie(movie):
    """
    :param movie: movie card element as BeautifulSoup
    :return: dict of the movie data in fields
    """
    global movie_id
    movie_id += 1
    header = movie.find(class_="lister-item-header")
    # handle movie name
    name = header.find('a').text
    url_for_movie = BASE_URL + header.find('a')['href']
    # handle movie year
    year = get_movie_year(header)
    # handle length
    length = get_movie_length(movie)
    # handle movie rating
    rating = get_movie_rating(movie)
    # handle movie genres
    genres = get_movie_genres(movie)
    # handle votes and gross
    votes, gross = get_movie_votes_and_gross(movie)
    # handle imdb rating
    imdb_rating = get_movie_imdb_rating(movie)
    # open request for specific page
    r_movie = requests.get(url_for_movie)
    movie_soup = BeautifulSoup(r_movie.text, 'html.parser')
    # handle director and stars
    director, stars = get_movie_director_and_stars(movie_soup)
    # handle movie full text
    full_text = movie_soup.text
    # return the movie data by field
    return {
        'Name': name,
        'ID': movie_id,
        'Year': year,
        'Length': length,
        'MovieRating': rating,
        'Genres': genres,
        'ImdbRating': imdb_rating,
        'Director': director,
        'Stars': stars,
        'Votes': votes,
        'Gross': gross,
        'URL': url_for_movie,
        'FullText': full_text
    }


def get_data_from_50_pages(main_musical_url):
    """
    :param main_musical_url: url for a list of 50 movies from the genre
    :return: the data of the 50 movies in the page
    """
    r = requests.get(main_musical_url)
    data = {}

    r_soup = BeautifulSoup(r.text, 'html.parser')
    movies = r_soup.find_all(class_="lister-item")

    for movie in movies:
        movie_data = get_one_data_from_movie(movie)
        data[movie_data['Name']] = movie_data

    return data


if __name__ == '__main__':
    current_url = MAIN_URL
    full_data = {}
    # going over 6 pages and 300 movies
    for i in range(NUMBER_OF_PAGES):
        # add data from the main page
        full_data.update(get_data_from_50_pages(current_url))
        # get the url for the next page
        soup = BeautifulSoup(requests.get(current_url).text, 'html.parser')
        current_url = BASE_URL + soup.find('a', class_="lister-page-next")['href']

    # write data to JSON
    with open('data.json', 'w') as outfile:
        json.dump(full_data, outfile, indent=4, sort_keys=False)

    print(len(full_data))
