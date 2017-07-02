# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import tmdb_posters

@click.command()
@click.argument('output_filepath', type=click.Path())
def main(output_filepath):
    '''
    Runs data processing scripts to turn raw data from into
    cleaned data ready to be analyzed.
    '''
    logger = logging.getLogger(__name__)
    logger.info('TMDB data retrieval')
    tmdb_posters.get_posters('sci', medium='tv', page_limit=1, output_filepath=output_filepath)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    main()
