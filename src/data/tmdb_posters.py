import tmdbsimple as tmdb
import os
from dotenv import load_dotenv, find_dotenv
from urllib.error import HTTPError
from urllib.request import urlretrieve
import logging
import click

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

def isValidStr(str_to_test):
    if str_to_test is None: return False
    if str_to_test == "": return False
    if str_to_test == " ": return False

    return True

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
    # Some poster_path has NoneType so check everything and skip issue items
    valid_str_test = [poster_path, title, tmdb_id]
    if sum(list(map(isValidStr, valid_str_test))) != len(valid_str_test):
        return None, None

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
    kwargs = {
        'page': page, 'with_genres': with_genres, 'with_original_language': 'en',
        'release_date_lte': '2017-08-01' # TODO: parameterize release date
    }

    if medium == 'tv':
        discvr.tv(**kwargs)
    else:
        discvr.movie(**kwargs)
    return discvr


@click.command()
@click.argument('search_term', default='sci')
@click.argument('medium', default='movie')
@click.argument('page_limit', default=1)
@click.argument('output_filepath', envvar='TMDB_RAW_DATA_PATH')
def get_posters(search_term, medium, page_limit, output_filepath):

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
    total_pages = total_pages if page_limit == 0 else page_limit

    logger.info('Pulling poster images from: '+str(total_pages)+' page(s) ' +\
        'with '+str(total_results)+' total results')
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

            if (poster_url != None) and (poster_filename != None):
                local_path = output_filepath+poster_filename
                download_image(poster_url, local_path)
            else:
                logger.warning('Item skipped. Poster URL: ' + str(poster_url) +\
                    ' Poster Filename: ' + str(poster_filename))

        logger.info('**********'+' Completed Page '+str(page)+' **********')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    load_dotenv(find_dotenv())
    get_posters()
