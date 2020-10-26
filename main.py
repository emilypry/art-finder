from artwork import Artwork
from permanent_database import PermanentDatabase
from spider_speaker import SpiderSpeaker
import model_training as mt
import utilities as ut

from PIL import Image

def main():
    # Create database
    database = PermanentDatabase()

    # Declare relevant directories and files
    database_location = '/home/pi/Documents/Programs/art_finder_env/all_data/permanent_database.txt'
    initial_liked = '/home/pi/Documents/Programs/art_finder_env/all_artworks/initial_liked/'
    initial_disliked = '/home/pi/Documents/Programs/art_finder_env/all_artworks/initial_disliked/'
    all_liked_artworks = '/home/pi/Documents/Programs/art_finder_env/all_artworks/all_liked_artworks/'
    vectors_and_likes = '/home/pi/Documents/Programs/art_finder_env/all_data/vectors_and_likes.txt'
    page_last_scraped = '/home/pi/Documents/Programs/art_finder_env/all_data/page_last_scraped.txt'
    freshly_scraped_artworks = '/home/pi/Documents/Programs/art_finder_env/all_artworks/freshly_scraped/full/'
    freshly_scraped_info = '/home/pi/Documents/Programs/art_finder_env/all_data/freshly_scraped_info.csv'
    stored_models = '/home/pi/Documents/Programs/art_finder_env/all_data/stored_models.txt'
    predicted_disliked = '/home/pi/Documents/Programs/art_finder_env/all_data/predicted_disliked.txt'

    # Convert and store initial liked and disliked images
    # Run this only during initialization; it will delete any existing data in perm_txt!
    ##ut.save_initial_images(initial_liked, initial_disliked, database, database_location, all_liked_artworks)
    
    # If a database is already stored, import it
    #database.import_database(database_location)
    
    # Export the vectors and likes of the artworks in the database to train initial
    # machine learning models
    #database.export_vectors_and_likes(vectors_and_likes)
    
    # Train an initial model
    #model=mt.train_model(database, stored_models, quick=True)

    
    # Run the spider to scrape new artworks
    #spider_speaker = SpiderSpeaker()
    #spider_speaker.scrape_page(page_last_scraped)
    
    # Predict which artworks will be liked/disliked
    #ut.predict_and_move(freshly_scraped_artworks, freshly_scraped_info, stored_models,
    #                 database, database_location, predicted_disliked)
        
    ut.rate_scraped_artworks(freshly_scraped_artworks)


    #database.print_all()
  
    
    
if __name__=="__main__":
    main()

    





