# libraries
from argparse import ArgumentParser
import logging
from preprocess import process_data
from retrieve import get_data
from database import send_data
from logging_config import setup_logging

# logging setup
setup_logging()
logger = logging.getLogger(__name__)

def main():
    # get user input
    parser = ArgumentParser(description="Chess.com ETL pipeline")
    parser.add_argument("username", help="Chess.com username to fetch data for")
    args = parser.parse_args()
    
    # get data from the chess.com
    logger.info(f"Starting ETL for user '{args.username}'")
    data_dir = './data'
    get_data(args.username, data_dir)    
    
    # preprocess the data
    clean_data_dir = './cleaned_data'
    process_data(args.username, clean_data_dir)
    
    # send it to mongodb database for storage
    url = "your-mongodb-link"
    send_data(url,clean_data_dir) 
    logger.info("ETL process completed successfully")  
    
    
if __name__ == "__main__":
    main()