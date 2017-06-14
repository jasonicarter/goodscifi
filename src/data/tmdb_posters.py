
import tmdbsimple as tmdb
import os
from dotenv import load_dotenv, find_dotenv
from urllib.error import HTTPError
from urllib.request import urlretrieve
import logging

def init():
    # Find .env automagically by walking up directories until it's found
    # Load up the entries as environment variables
    load_dotenv(find_dotenv())
    tmdb.API_KEY = os.environ.get("TMDB_API_KEY")

    # Get base URL and image size
    config = tmdb.Configuration()
    r = config.info()

    # Poster size [4] is width of 500
    return config.images['secure_base_url']+config.images['poster_sizes'][4]

def get_genre_id(search_term):
    # Get genre ids for 'science fiction' and 'sci-fi & fantasy'
    genre = tmdb.Genres()

    # Need to select tv/movie list, default is movie
    type_of_shows = ['tv', 'movie']
    genre_ids = {}
    for t in range(len(type_of_shows)):
        genre.URLS['list'] = '/'+type_of_shows[t]+'/list'
        r = genre.list()
        genre_ids[type_of_shows[t]] = \
            [item['id'] for item in genre.genres if search_term in item['name'].lower()]

    return genre_ids

def build_poster_url_and_filename(base_image_url, poster_path, title, date, tmdb_id):
    '''
    Build the full image url and new filename for poster
    Args:
        base_url: tmdb base url from configurations
        poster_path: '/hwih4=283d.jpg' path of poster
        title: name of tv show or movie
        date: yyyy-mm-dd of first air date (tv) or release date (movie)
        tmdb_id: id associated to tv show or movie
    Returns: strings poster_url and poster_filename
    '''
    # Replace spaces in title with '-', convert the rest to strings
    fname = [title, date, tmdb_id]
    poster_filename = ('_').join([str(w).replace(' ','-') for w in fname])+'.jpg'
    poster_url = base_image_url+poster_path

    return poster_url, poster_filename

def download_image(image_url, local_path):
    # https://stackoverflow.com/a/39594029
    try:
        urlretrieve(image_url, local_path)
    except FileNotFoundError as err: # add log warning
        print(err, image_url, local_path)
    except HTTPError as err:
        print(err, image_url)

def get_tv_movie_results(medium, with_genres, discvr=tmdb.Discover(), page=1):
    if medium == 'tv':
        discvr.tv(page=page, with_genres=with_genres)
    else:
        discvr.movie(page=page, with_genres=with_genres)
    return discvr

def get_posters(search_term, medium='movie', page_limit=None, output_filepath='/'):

    logger = logging.getLogger(__name__)
    logger.info('getting configurations')
    # Get configurations
    base_image_url = init()

    logger.info('getting genre ids for: '+medium+' with search term: '+search_term)
    # Get genre ids for search_term
    genre_ids = get_genre_id(search_term)
    # Discover() arg 'with_genres' only accepts strings (sep = ',' or '|')
    with_genres = ",".join(str(s) for s in genre_ids[medium])

    logger.info('Creating Discover object and retrieving initial results')
    # Create Discover objects to pull list of tv/movies
    discover = tmdb.Discover()
    discover = get_tv_movie_results(medium, with_genres, discover)
    # Need to do this to figure out how many pages to loop through
    total_pages = discover.total_pages
    total_results = discover.total_results

    # Set attributes / keys for movie and tv objects
    tv_movie_attr = {'tv':['poster_path', 'name', 'first_air_date', 'id'],
                     'movie':['poster_path','title', 'release_date', 'id']}

    # Used for testing mostly
    total_pages = total_pages if page_limit is None else page_limit

    logger.info('Pulling poster images from: '+str(total_pages)+' page(s)')
    # Loop over each page (get page one again) and then all results on each page
    for page in range(1, total_pages+1):
        discover = get_tv_movie_results(medium, with_genres, discover, page)
        for item in range(len(discover.results)):
            # base_image_url, poster_path, name / title, first_air_date / release_date, id
            poster_url, poster_filename = build_poster_url_and_filename(
                base_image_url,
                discover.results[item][tv_movie_attr[medium][0]],
                discover.results[item][tv_movie_attr[medium][1]],
                discover.results[item][tv_movie_attr[medium][2]],
                discover.results[item][tv_movie_attr[medium][3]]
            )

            local_path = output_filepath+poster_filename
            # return t/f and sum them to assert len(discover.results) == sum???
            download_image(poster_url, local_path)

        logger.info('**********'+' Completed Page '+str(page)+' **********')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    output_filepath = os.environ.get("TMDB_RAW_DATA_PATH")
    get_posters('sci', page_limit=1, output_filepath=output_filepath)
