'''Contains a number of functions that do not directly involve the ArtSpider, the PermanentDatabase,
nor model_training. Tend to deal with files and folders.
'''

from PIL import Image
from numpy import asarray
import os
import shutil
import csv
import datetime

from permanent_database import PermanentDatabase
import model_training as mt
from artwork import Artwork

def convert(location):
    '''Converts an artwork at a given location to a 7500x1 array.
    '''
    this_image = Image.open(location)

    # Squish the image to 50x50 (may distort shape, instead of cropping)
    # and convert to RGB (may be RGBA otherwise)
    this_image = this_image.resize((50,50)).convert('RGB')
    
    # Transform the 50x50 image into an unrolled vector/list of intensity values
    this_image = list(asarray(this_image).ravel())
    
    return this_image

def save_initial_images(liked_images_dir, disliked_images_dir, database, database_txt,
                        all_liked_artworks_dir):
    '''Saves an initial set of liked and disliked images to database and exports the database.
    Also renames and copies all liked artworks to all_liked_artworks.
    '''
    print('Adding initial artworks to database...')
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
            
            # If it's a liked artwork, rename it to its ID and copy it to the permanent
            # folder for liked artworks
            if new_work.like==1:
                shutil.copy(liked_images_dir+new_work.original_name, all_liked_artworks_dir+str(new_work.ID))
    
    print('Added initial artworks to database')
    
    # Export the full database
    database.export_full(database_txt)

def store_images(scraped_artworks, liked_artworks, database, delete_leftovers):
    '''For a set of .jpgs in the scraped_artworks folder, if an artwork is liked, rename it
    to its ID and move it to the liked_artworks folder; if an artwork is disliked, delete
    it. If the boolean delete_leftovers is true, delete all other remaining files in scraped_artworks.
    '''
    for image in os.listdir(scraped_artworks):
        image_in_database = False
        
        # Get the artwork's like from the database using its original_name
        for artwork in database.artworks:
            if artwork.original_name == image:
                
                # If the artwork is disliked, delete it
                if artwork.like == 0:
                    os.remove(scraped_artworks+image)
                    image_in_database = True
                
                # If the artwork is liked, rename it and move it
                elif artwork.like == 1:
                    shutil.move(scraped_artworks+image, liked_artworks+str(artwork.ID))
                    image_in_database = True
        
        # If it's not in the database and delete_leftovers is true, then delete the file
        if image_in_database == False and delete_leftovers == True:
            os.remove(scraped_artworks+image)

def get_number_of_files(directory):
    '''Returns the number of files in a folder.'''
    return len(os.listdir(directory))

def predict_and_move(scraped_art_dir, scraped_info_txt, models_txt, database, database_txt, predicted_disliked_txt):
    '''For each freshly scraped artwork, predicts if the viewer will like it. If it will be liked,
    the image becomes an Artwork and is added to the Database. If it will be disliked, the .jpg/.png
    is deleted and some of the artwork's info is stored in predicted_disliked.txt.
    '''
    print('Predicting which artworks will be liked...')
    
    name_and_liked = {}
    
    # Get the predicted liked-values for each artwork and store them with their file names
    for artwork in os.listdir(scraped_art_dir):
        # Predict if the artwork will be liked given the latest model in models.txt
        value = mt.predict_if_liked(scraped_art_dir+artwork, mt.get_theta(models_txt))
        
        # Add the name of the artwork and its predicted liked value to the dictionary
        name_and_liked[artwork] = value
        
    # Go through the info for each freshly scraped artwork in scraped_info.txt
    new_artworks = []
    scraped_txt = open(scraped_info_txt, 'r')
    reader = csv.reader(scraped_txt, delimiter=',')
    for work in reader:
        if work[0] != 'artist' and work[0] != '':
            # Get the original name of the .jpg, stored in scraped_info.txt
            original_name = work[4]
            i1 = original_name.find('full/')
            i2 = original_name.find("', 'checksum'")
            original_name = original_name[i1+5:i2]
                        
            # Only convert the work into an Artwork if the viewer is expected to like it
            if name_and_liked.get(original_name) == 1:
                this_work = Artwork()
                this_work.ID = database.number_of_artworks + 1
                
                # Set the like for this work to 2, indicating that the viewer has not yet
                # rated it 
                this_work.like = 2
                
                this_work.artist = work[0]
                this_work.info = work[1]
                this_work.nga_id = int(work[2])
                this_work.nga_page = int(work[5])
                this_work.title = work[6]
                this_work.nga_link = work[7]
                this_work.added = str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                this_work.original_name = original_name
                this_work.vector = convert(scraped_art_dir+original_name)
                
                new_artworks.append(this_work)
                
                # Add the work to the Database 
                database.add_artwork(this_work)
            
            # If the viewer is expected to dislike the artwork, save some info about it to
            # predicted_disliked.txt and delete the .jpg/.png. 
            elif name_and_liked.get(original_name) == 0:
                # Save the artist, info, title, viewing link, and time added
                disliked = work[0]+'~'+work[1]+'~'+work[6]+'~'+work[7]+'~'+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                
                file = open(predicted_disliked_txt, 'a')
                file.write(disliked)
                file.write('\n')
                file.close()
                
                # Delete the .jpg/.png file
                os.remove(scraped_art_dir+original_name)
    
    # Export the new (predicted liked) Artworks to the database
    database.export_new(database_txt, new_artworks)
    
    print('Predicted that %s out of %s artworks will be liked' % (len(new_artworks), len(name_and_liked)))
    
