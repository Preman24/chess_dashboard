# libraries
import json
import re
import os
from datetime import datetime
import logging
from logging_config import setup_logging

# directory to the data dictionary
directory = './data'

# setup logging
setup_logging()
logger = logging.getLogger(__name__)

# load json file 
def load_json(filepath):
    try:
        with open(filepath, 'r') as file_data:
            return json.load(file_data)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {filepath}")

# convert the data to json format
def convert_to_json(clean_data_dir, data, filename):
    filepath = os.path.join(clean_data_dir, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)
    logger.info(f'{filename[:-5]} has been saved in {filename}')
    
# extract player profiles    
def extract_player_profile(basic_data, stats_data): 
    # empty list to store the preprocessed player information
    player_profile = []
    
    # 3 types of match we want
    match_types = ['rapid', 'bullet', 'blitz']
    
    # iterate through every match type
    for match in match_types:
        
        # put them in json format
        information = {
        'player_name': basic_data['username'],
        'player_league': basic_data['league'],
        'player_joined': datetime.fromtimestamp(basic_data['joined']).strftime('%Y-%m-%d'),
        'match_type': match,
        'current_rating': stats_data[f'chess_{match}']['last']['rating'],
        'record_win': stats_data[f'chess_{match}']['record']['win'],
        'record_loss': stats_data[f'chess_{match}']['record']['loss'],
        'record_draw': stats_data[f'chess_{match}']['record']['draw'],
        'highest_rating_tactics_played': stats_data['tactics']['highest']['rating'],
        'lowest_rating_tactics_played': stats_data['tactics']['lowest']['rating']
        }
        player_profile.append(information)
    return player_profile

def extract_match_data(username, match_data):
    
    # empty list to store the preprocess game
    match_processed_data = []
    
    # iterate through every game
    for game in match_data:
        try:
            
            # if either black or white not found, raise error
            if 'white' not in game or 'black' not in game:
                raise KeyError("Missing player data")
           
            # get the white and black game info
            white = game['white']
            black = game['black']
            
            # get accuracy        
            acc = game.get('accuracies',{})
    
            # Remove the irrelevant strings
            movetext = re.sub('\n', ' ', game['pgn'])
            movetext = re.sub(r"\{[^}]*\}", "", movetext)

            # Retrieve the date and time of the match
            start_time = re.findall(r'\[StartTime "([^"]+)"\]', movetext)[0]
            end_time = re.findall(r'\[EndTime "([^"]+)"\]', movetext)[0]
            start_date = re.findall(r'\[Date "([^"]+)"\]', movetext)[0].replace('.','/')
            end_date = re.findall(r'\[EndDate "([^"]+)"\]', movetext)[0].replace('.','/')
            
            # duration to finish match
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y/%m/%d %H:%M:%S")
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y/%m/%d %H:%M:%S")
            time_difference = end_datetime - start_datetime
            seconds_duration = time_difference.total_seconds()
            
            # categorize the match based on the time 
            hour = start_datetime.hour
            if 5 <= hour < 12:
                time_categorize =  "Morning"      
            elif 12 <= hour < 18:
                time_categorize = "Afternoon"    
            else:
                time_categorize = "Evening"

            # Retrieve the chess moves
            chess_moves = movetext.strip().split()
            white_moves, black_moves = [], []
            for index, values in enumerate(chess_moves):
                if values == '1.':
                    start_index = index
                    chess_moves = chess_moves[start_index:]
                    filtered = [move for move in chess_moves if not move.endswith(".")]
                    filtered.pop(-1)
                    white_moves = filtered[0::2]
                    black_moves = filtered[1::2]
                    break
            
            # get the targeted user information
            if game['white']['username'] == username and len(white_moves) != 0:
                rating = white.get('rating')
                result = white.get('result')
                accuracy = 'Null' if acc.get('white') is None else acc.get('white')
                moves = white_moves
            elif game['black']['username'] == username and len(black_moves) != 0:
                rating = black.get('rating')
                result = black.get('result')
                accuracy = 'Null' if acc.get('black') is None else acc.get('black')
                moves = black_moves
            
            # change result
            if result != 'win' and result != 'agreed' and result != 'stalemate':
                result = 'loss'
            elif result == 'agreed' or result == 'stalemate':
                result = 'draw'
            else:
                result = 'win'
                                
            # opening moves
            opening_move = game['eco'][31:].replace('-',' ')
            index = 0
            while index < len(opening_move) and (opening_move[index].isalpha() or opening_move[index] == ' '):
                index += 1
            opening_move = opening_move[:index].strip()
            if len(white_moves) >= 2 and len(black_moves) >= 2:
                opening_move += f' 1.{white_moves[0]} {black_moves[0]} 2.{white_moves[1]} {black_moves[1]}'
            elif len(white_moves) == 1 and len(black_moves) >= 1:
                opening_move += f' 1.{white_moves[0]} {black_moves[0]}'
            elif len(white_moves) >= 1 and len(black_moves) == 0:
                opening_move += f' 1.{white_moves[0]}'
            elif len(white_moves) == 0 and len(black_moves) >= 1:
                opening_move += f' 1...{black_moves[0]}'
            elif len(white_moves) == 0 and len(black_moves) == 0:
                opening_move += ' No moves available'  
                         
            # Put them in a JSON format
            processed_game = {
                'player_name':username,
                'match_url': game.get('url'),
                'match_type': game.get('time_class'),
                'start_date': start_date,
                'end_date': end_date,
                'start_time': start_time,
                'end_time': end_time,
                'rating': rating,
                'accuracy': accuracy,
                'result': result,
                'first_move': moves[0] if len(moves) > 0 else 'Null',
                'second_move': moves[1] if len(moves) > 1 else 'Null',
                'third_move': moves[2] if len(moves) > 2 else 'Null',
                'forth_move': moves[3] if len(moves) > 3 else 'Null',
                'fifth_move': moves[4] if len(moves) > 4 else 'Null',
                'last_fifth_move': moves[-5] if len(moves) >= 5 else 'Null',
                'last_forth_move': moves[-4] if len(moves) >= 4 else 'Null',
                'last_third_move': moves[-3] if len(moves) >= 3 else 'Null',
                'last_second_move': moves[-2] if len(moves) >= 2 else 'Null',
                'last_first_move': moves[-1] if len(moves) >= 1 else 'Null',
                'opening_move': opening_move,
                'duration': seconds_duration,
                'time_of_day': time_categorize        
            }

            match_processed_data.append(processed_game)
        
        # error raise    
        except KeyError as e:
            logger.warning(f"Skipping game due to missing data: {e}")
        except Exception as e:
            logger.error(f"Error processing game: {e}")
    return match_processed_data

# the pipeline function to run the codes all at once
def process_data(username, clean_data_dir):
    try:
        os.makedirs(clean_data_dir, exist_ok=True)
        
        basic_data = load_json(os.path.join(directory,'basic.json'))
        stats_data = load_json(os.path.join(directory,'stats.json'))
        match_data = load_json(os.path.join(directory,'match.json'))
        
        player = extract_player_profile(basic_data, stats_data)
        match = extract_match_data(username, match_data)
        
        convert_to_json(clean_data_dir, player, 'player_profile.json')
        convert_to_json(clean_data_dir, match, 'match_history.json')
        
    except Exception as e:
        logger.exception("Error occurred during data processing", extra={"function": "process_data", "error": str(e)})