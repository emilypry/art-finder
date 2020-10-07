#from matplotlib import image 
#from matplotlib import pyplot 
from PIL import Image
from numpy import asarray
from numpy import savetxt
import numpy as np
import os
import datetime
#import csv
import shutil

from artwork import Artwork
from permanent_database import PermanentDatabase
from spider_speaker import SpiderSpeaker
   
def convert(location):
    '''Converts an artwork at a given location to a 7500x1 array.
    '''
    this_image = Image.open(location)

    # Squish the image to 50x50 (may distort shape, instead of cropping)
    # and convert to RGB (may be RGBA otherwise)
    this_image = this_image.resize((50,50)).convert('RGB')
    
    # Transform the 50x50 image into an unrolled vector/list of intensity values
    this_image = list(asarray(this_image).ravel())
    
    # Print confirmation
    print('Converted artwork')
    
    return this_image

def save_initial_images(liked_images_dir, disliked_images_dir, database, database_dir,
                        all_liked_artworks_dir):
    '''Saves an initial set of liked and disliked images to database and exports the database.
    Also renames and copies all liked artworks to all_liked_artworks.
    '''
    database.clear_all()
    folders = [liked_images_dir, disliked_images_dir]
    for folder in folders:
        for artwork in os.listdir(folder):
            # Create the new artwork
            new_work = Artwork()
            new_work.ID = database.number_of_artworks + 1
            new_work.like = 0
            if folder==liked_images_dir:
                new_work.like = 1
            new_work.artist = artwork
            new_work.added = str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            new_work.original_name = artwork
            new_work.vector = convert(folder+artwork)
            
            # Add the new artwork to the database
            database.add_artwork(new_work)
            
            # Print confirmation
            print('Added artwork #%s to the database' % new_work.ID)
            
            # If it's a liked artwork, rename it to its ID and copy it to the permanent
            # folder for liked artworks
            if new_work.like==1:
                shutil.copy(liked_images_dir+new_work.original_name, all_liked_artworks_dir+str(new_work.ID))
            
    # Export the full database
    database.export_full(database_dir)
    
    # Print confirmation
    print('Exported the full database')

def store_images(artworks, temp_folder, perm_folder):
    '''For a set of artworks, if it is liked, then rename it to its ID and move it from the temporary
    folder to the permanent liked artworks folder. If it is disliked, delete it. Temp_folder will
    be emptied.
    '''
    for artwork in artworks:
        if artwork.like == 1:
            # Rename the artwork from its original name to its ID, and move it from
            # temp_folder to perm_folder
            shutil.move(temp_folder+artwork.original_name, perm_folder+str(artwork.ID))
            
            # Print verification
            print('Renamed and moved liked artwork:', artwork.original_name)
        else:
            # Delete the artwork from temp_folder
            os.remove(temp_folder+artwork.original_name)
            
            # Print verification
            print('Removed disliked artwork:', artwork.original_name)


if __name__=="__main__":
    # Create database
    database = PermanentDatabase()

    # Declare relevant directories
    database_location = '/home/pi/Documents/Programs/art_finder_env/all_data/permanent_database.txt'
    initial_liked = '/home/pi/Documents/Programs/art_finder_env/all_artworks/initial_liked/'
    initial_disliked = '/home/pi/Documents/Programs/art_finder_env/all_artworks/initial_disliked/'
    all_liked_artworks = '/home/pi/Documents/Programs/art_finder_env/all_artworks/all_liked_artworks/'
    data = '/home/pi/Documents/Programs/art_finder_env/all_data/vectors_and_likes.txt'
    page_num = '/home/pi/Documents/Programs/art_finder_env/all_data/page_last_scraped.txt'

    # Convert and store initial liked and disliked images
    # Run this only during initialization; it will delete any existing data in perm_txt!
    ###save_initial_images(initial_liked, initial_disliked, database, database_location, all_liked_artworks)
    
    # If a database is already stored, import it
    database.import_database(database_location)
        
    # Export the vectors and likes of the artworks in the database to train initial
    # machine learning models
    #database.export_vectors_and_likes(data)
    
    # Run the spider to scrape new artworks
    spider_speaker = SpiderSpeaker()
    #spider_speaker.scrape_page(page_num)
    

    #database.print_all()
  
    
    
    

    





