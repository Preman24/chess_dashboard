# libraries
import json
from datetime import datetime
import os
import logging
import httpx
from retryhttp import retry
from logging_config import setup_logging

# setup logging
setup_logging()
logger = logging.getLogger(__name__)

# set limit for getting data
@retry(max_attempt_number=5, retry_rate_limited=True)
def safe_get(url):
    resp = httpx.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

# retrieve data
def get_data(username, data_dir):
    
    # creata data folder
    os.makedirs(data_dir, exist_ok=True)
    
    # website data
    chess_player_url = f'https://api.chess.com/pub/player/{username}'

    try: 
        # basic information
        data = safe_get(chess_player_url)
        basic_info = data
        with open(f'.//{data_dir}//basic.json', 'w') as basic_file:
            json.dump(basic_info, basic_file, indent=4)
        logger.info("Basic information data has been written to basic.json")
        
        # stats information
        data = safe_get(chess_player_url + '/stats')
        stats_info = data
        with open(f'.//{data_dir}//stats.json','w') as stats_file:
            json.dump(stats_info, stats_file, indent=4)
        logger.info("Stats information data has been written to stats.json")
        
        # games information
        start, last = datetime.fromtimestamp(basic_info['joined']), datetime.fromtimestamp(basic_info['last_online'])
        start_year, start_month, last_year, last_month = int(start.strftime('%Y')), int(start.strftime('%m')), int(last.strftime('%Y')), int(last.strftime('%m'))
        match = []
        while start_year <= last_year and start_month != last_month:
            data = safe_get(chess_player_url + f'/games/{str(start_year)}/{start_month:02}')
            games_info = data
            match.extend(games_info['games'])
            if start_month == 12:
                start_year += 1
                start_month = 1
            else:
                start_month += 1 
        
        with open(f'.//{data_dir}//match.json','w') as match_file:
            json.dump(match, match_file, indent=4)
        logger.info("Match information data has been written to match.json")
    
    # raise error
    except httpx.HTTPStatusError as http_error:
        if data.status_code == 301:
            logger.error(f'301 Moved Permanently: The requested URL has been moved. Please update your request to the new URL.')
        elif data.status_code == 304:
            logger.error(f'304 Not Modified: The data has not changed since your last request.')
        elif data.status_code == 404:
            logger.error(f'404 Not Found: The username "{username}" does not exist or the URL is malformed.')
        elif data.status_code == 410:
            logger.error(f'410 Gone: The data is permanently unavailable at the requested URL. Do not request this URL again.')
        elif data.status_code == 429:
            logger.error(f'429 Too Many Requests: You have exceeded the rate limit. Please try again later.')
        else:
            logger.error(f'HTTP error occurred: {http_error}')
            
    except Exception as err:
        logger.error(f'An unexpected error occurred: {err}')
        
    finally:
        logger.info('Completed Retriving Data...')
        
