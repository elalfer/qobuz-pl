import logging
import os
import optparse
import configparser
import getpass

from qobuz_dl.core import QobuzDL
from qobuz_dl.utils import get_url_info

"""
This script downloads a Qobuz playlist and generates an XSPF playlist file.

Usage:
    qobuz_pl.py <action> -e <email> -p <password> -u <playlist_url>

Arguments:
    -e, --email      Qobuz account email
    -p, --password   Qobuz account password
    -u, --url        Qobuz playlist URL
    --id             Playlist ID (optional, not used if URL is provided)

The script authenticates with Qobuz, fetches the playlist metadata and tracks,
and writes them to an XSPF file named after the playlist slug.

Dependencies:
    - qobuz_dl (must be installed and accessible in PYTHONPATH)

Example:
    qobuz_pl.py download -e user@example.com -p mypassword -u https://play.qobuz.com/playlist/123456
"""

logging.basicConfig(level=logging.INFO)

"""
This function downloads a Qobuz playlist and writes it to an XSPF file.
"""
def download_and_write_playlist(logger, all_pl, pl):
    logger.info(f'Playlist downloaded with {pl["tracks_count"]} tracks')
    file_name = f'{pl["slug"]}.xspf'

    logger.info('Writing playlist into ' + file_name)

    with open(file_name, 'w', encoding="UTF-8") as of:
        of.write(f"""<?xml version="1.0" encoding="UTF-8"?>
    <playlist version="1" xmlns="http://xspf.org/ns/0/">
    <title>{pl['name']}</title>
    <trackList>""")

        for pl in all_pl:
            logger.info(f'Writing {len(pl["tracks"]["items"])} tracks')
            for item in pl['tracks']['items']:
                of.write(f"""    <track>
                <location>qobuz%3A{item['id']}</location>
                <title>{item['title']}</title>
                <creator>{item['album']['artist']['name']}</creator>
                <album>{item['album']['title']}</album>
                <duration>{item['duration']}000</duration>
                <trackNum>{item['track_number']}</trackNum>
                <image>{item['album']['image']['large']}</image>
            </track>""".replace('&', '&#038;'))

        of.write('  </trackList>\n</playlist>')

def retrieve_playlist_metadata(play_list_url, qobuz, logger):
    logger.info('Fetching playlist')
    _, item_id = get_url_info(play_list_url)
    all_pl = list(qobuz.client.get_plist_meta(item_id))
    logger.info(f'Downloaded {len(all_pl)} chunks')
    pl = all_pl[0]
    return all_pl,pl

global_config = None

def read_from_cfg(field: str) -> str:
    global global_config
    if not global_config:
        global_config = configparser.ConfigParser()
        global_config.read('config.ini')
    if not field in global_config:
        v = input("Input " + field + ": ")
        global_config['DEFAULT'][field] = v

        with open('config.ini', 'w') as configfile:
            global_config.write(configfile)

    return global_config['DEFAULT'][field]
        
    

if __name__ == "__main__":
    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-e', '--email', help='Qobuz email', type=str, default=None)
    opt_parser.add_option('-p', '--password', help='Qobuz password', type=str, default=None)
    opt_parser.add_option('-u', '--url', help='Playlist URL', type=str)
    opt_parser.add_option('--id', help='Playlist id', type=str)
    opts, vals = opt_parser.parse_args()

    if len(vals) != 1:
        opt_parser.error("Invalid number of arguments. Use 'download' or 'list'")

    if not vals[0] in ['download', 'list']:
        opt_parser.error(f"Invalid command {vals[0]}. Use 'download' or 'list'")

    email = opts.email if opts.email else read_from_cfg('email')
    if opts.password:
        password = opts.password
    else:
        # Securely read password from console
        password = getpass.getpass("Enter Qobuz password: ")

    qobuz = QobuzDL()
    qobuz.get_tokens() # get 'app_id' and 'secrets' attrs
    qobuz.initialize_client(email, password, qobuz.app_id, qobuz.secrets)

    logger = logging.getLogger(__name__)

    if vals[0] == 'download':
        logger.info('Starting playlist download...')
        play_list_url = opts.url
        all_pl, pl = retrieve_playlist_metadata(play_list_url, qobuz, logger)
        download_and_write_playlist(logger, all_pl, pl)

        logger.info('Playlist generation completed successfully.')

    if vals[0] == 'list':
        logger.info('Starting playlist listing...')
        opt_parser.error('Not implemented yet.')
