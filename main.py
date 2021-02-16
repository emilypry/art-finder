from artwork import Artwork
from permanent_database import PermanentDatabase
from spider_speaker import SpiderSpeaker
import model_training as mt
import utilities as ut
import os
import shutil
import sys
import random

from PIL import Image
import subprocess

def main():
    # Create database and spider speaker
    database = PermanentDatabase()
    spider_speaker = SpiderSpeaker()
    
    # Declare relevant directories and files
    # The txt file for the database; create with initials.create_database_txt()
    database_location = '/home/pi/Documents/Programs/art_finder_env/all_data/permanent_database.txt'
    # The folder of initial liked images (if applicable)
    initial_liked = '/home/pi/Documents/Programs/art_finder_env/all_artworks/initial_liked/'
    # The folder of initial disliked images (if applicable)
    initial_disliked = '/home/pi/Documents/Programs/art_finder_env/all_artworks/initial_disliked/'
    # The folder that will hold all liked images
    all_liked_artworks = '/home/pi/Documents/Programs/art_finder_env/all_artworks/all_liked_artworks/'
    # A txt file to export vectors and likes from database (if training model externally)
    vectors_and_likes = '/home/pi/Documents/Programs/art_finder_env/all_data/vectors_and_likes.txt'
    # A txt file to keep track of which pages of NGA website have been scraped;
    # create with initials.create_scraped_page_txt()
    page_last_scraped = '/home/pi/Documents/Programs/art_finder_env/all_data/page_last_scraped.txt'
    # The folder that scraped artworks are added to; will be the directory saved as IMAGES_STORE in
    # art_spider.py, followed by /full/
    freshly_scraped_artworks = '/home/pi/Documents/Programs/art_finder_env/all_artworks/freshly_scraped/full/'
    # A csv file that stores info about the scraped artworks; must be identical to the self.file directory
    # in custom_pipeline.py
    freshly_scraped_info = '/home/pi/Documents/Programs/art_finder_env/all_data/freshly_scraped_info.csv'
    # A txt file that stores info about models of the viewer's art preferences; create with
    # initials.create_models_txt()
    stored_models = '/home/pi/Documents/Programs/art_finder_env/all_data/stored_models.txt'
    # A txt file that stores info about the artworks the model predicts the viewer will dislike;
    # create with initials.create_disliked_txt()
    predicted_disliked = '/home/pi/Documents/Programs/art_finder_env/all_data/predicted_disliked.txt'

    # Convert and store initial liked and disliked images (if you have some to begin with)
    # Run this only during initialization; it will delete any existing data in perm_txt!
    ##ut.save_initial_images(initial_liked, initial_disliked, database, database_location, all_liked_artworks)
    
    # If a database is already stored, import it
    database.import_database(database_location)
    
    # Train an initial model (if using initial liked and disliked images)
    #mt.train_model(database, stored_models, True)
    
    
    # Start the viewer interaction via the command line
    while True:
        task = 0
        
        # Display the main menu on the command line
        print('\n***************************\nWelcome to your art finder! \nWhat would you like to do?')
        
        # Have the viewer pick an initial task from the main menu
        while task==0:
            try:
                task = int(input('1. Rate new artworks \n2. Browse liked artworks' \
                                 '\n3. Improve predictions \n4. Quit art finder \n'))
                assert task==1 or task==2 or task==3 or task==4
                break
            except ValueError:
                print('\nPlease enter a number')
            except:
                print('\nPlease pick between 1-4')
        
        # To rate new artworks
        while task==1:
            # Get the unrated artworks in the database
            new_artworks = database.get_unrated_artworks()
            
            # If there are no unrated artworks in the database, empty the folder of
            # scraped artworks, scrape new artworks, and store only the artworks that
            # the viewer is predicted to like
            if len(new_artworks) == 0:
                print('Retrieving a new set of artworks for rating')
                
                # To be safe, store rated artworks properly and delete leftover files 
                ut.store_images(freshly_scraped_artworks, all_liked_artworks, database, True)
                
                # Scrape new artworks, add to folder
                try:
                    spider_speaker.scrape_page(page_last_scraped)
                except:
                    print('Error scraping artworks')
                    task = 0
                    break
                
                # If no artworks were scraped, break
                if(ut.get_number_of_files(freshly_scraped_artworks)==0):
                    print('Did not retrieve any artworks')
                    task = 0
                    break
                
                # Get rid of the scraped artworks that the viewer is predicted to dislike
                ut.predict_and_move(freshly_scraped_artworks, freshly_scraped_info, stored_models,
                     database, database_location, predicted_disliked)
                
                # Get the new set of unrated artworks (the freshly scraped artworks)
                new_artworks = database.get_unrated_artworks()
            
            # Show the viewer the scraped artworks that they're predicted to like
            newly_rated = []
            i=0
            while i < len(new_artworks):
                artwork = new_artworks[i]
                
                # Display the artwork
                display = subprocess.Popen(['display', freshly_scraped_artworks+artwork.original_name])

                # Keep showing them the artwork until they move to a different one
                while True:   
                    print('\n')
                    # Show the 'like' status of this artwork
                    if artwork.like == 1:
                        print('You have rated this artwork: like')
                    elif artwork.like == 0:
                        print('You have rated this artwork: dislike')
                    else:
                        print('You have not rated this artwork')
                    
                    # Show the viewer their options
                    while True:
                        try:
                            artwork_action = int(input('1. I like this artwork!' \
                                           '\n2. I dislike this artwork!' \
                                           '\n3. Show me information about this artwork' \
                                           '\n4. Show previous artwork' \
                                           '\n5. Show next artwork' \
                                           '\n6. Return to main menu' \
                                           '\n7. Quit art finder \n'))
                            assert artwork_action >= 1 and artwork_action <= 7
                            break
                        except ValueError:
                            print('\nPlease enter a number')
                        except:
                            print('\nPlease pick between 1-7')            
                    
                    # To 'like' the artwork
                    if artwork_action == 1:
                        # Update the artwork's like
                        artwork.like = 1
                        
                        # If the artwork isn't already in newly_rated, then append it
                        if artwork not in newly_rated:
                            newly_rated.append(artwork)
                    
                    # To 'dislike' the artwork
                    elif artwork_action == 2:
                        # Update the artwork's like
                        artwork.like = 0
                        
                        # If the artwork isn't already in newly_rated, then append it
                        if artwork not in newly_rated:
                            newly_rated.append(artwork)
                    
                    # To display info about the artwork
                    elif artwork_action == 3:
                        print('\nInformation about this artwork')
                        artwork.print_art_info()
                    
                    # To go to the previous artwork
                    elif artwork_action == 4:
                        # Update the new_artworks index
                        if i>0:
                            i -= 1
                        
                        # Stop displaying this artwork
                        display.kill()
                        
                        # Break out of the 'show this artwork' loop
                        break
                    
                    # To go to the next artwork
                    elif artwork_action == 5:
                        # Update the new_artworks index
                        if i < len(new_artworks):
                            i += 1
                        
                        # Stop displaying this artwork
                        display.kill()
                        
                        # Break out of the 'show this artwork' loop
                        break
                    
                    # To return to the main menu or quit art finder
                    else:
                        # Stop displaying this artwork
                        display.kill()
                        
                        # Export full database
                        database.export_full(database_location)
                        
                        # Store newly-rated artworks
                        ut.store_images(freshly_scraped_artworks, all_liked_artworks, database, False)
   
                        # To go to the main menu
                        if artwork_action==6:
                            # Set the task to 0 for the main menu
                            task = 0
                            
                            # Get out of the 'show new artworks' loop
                            i = len(new_artworks)
                            
                            # Break out of the 'show this artwork' loop
                            break
                        
                        # To quit art finder
                        elif artwork_action==7:
                            print('Quitting art finder')
                            sys.exit()
                    
                # If worked through the existing set of scraped artworks
                if len(database.get_unrated_artworks()) == 0:
                    print('Finished rating this batch of artworks')
                    
                    # Export the database
                    database.export_full(database_location)
                    
                    # Train a model (quickly, if one already exists)
                    mt.train_model(database, stored_models, quick=True)
                    
                    # Store all of the newly rated artworks
                    ut.store_images(freshly_scraped_artworks, all_liked_artworks, database, False)
                    
        # To browse liked artworks
        while task==2:
            # Get the set of liked artworks from the database
            liked_artworks = database.get_liked_artworks()
            
            # Make sure there are liked artworks to view; if not, return to main menu
            if len(liked_artworks) < 1:
                print('You have not liked any artworks')
                break
            
            while True:
                try:
                    print('\nHow would you liked to browse your liked artworks?')
                    browse = int(input('1. By the order in which I liked them \n2. In random order' \
                                      '\n3. Return to main menu \n'))
                    assert browse==1 or browse==2 or browse == 3
                    break
                except ValueError:
                    print('\nPlease enter a number')
                except:
                    print('\nPlease pick between 1-3')
            
            # To browse liked artworks
            while browse == 1 or browse == 2:
                # To view the artworks in a random order, shuffle them
                if browse == 2:
                    random.shuffle(liked_artworks)
                    
                # Show the viewer each artwork
                i=0
                while i < len(liked_artworks):
                    artwork = liked_artworks[i]
                    
                    # Display the artwork
                    display = subprocess.Popen(['display', all_liked_artworks+str(artwork.ID)])

                    # Keep showing them the artwork until they move to a different one
                    while True:  
                        # Show the viewer their options
                        while True:
                            try:
                                artwork_action = int(input('1. Show me information about this artwork' \
                                               '\n2. Show previous artwork' \
                                               '\n3. Show next artwork' \
                                               '\n4. Return to main menu' \
                                               '\n5. Quit art finder \n'))
                                assert artwork_action >= 1 and artwork_action <= 5
                                break
                            except ValueError:
                                print('\nPlease enter a number')
                            except:
                                print('\nPlease pick between 1-5')
                                
                        # To display info about the artwork
                        if artwork_action == 1:
                            print('\nInformation about this artwork')
                            artwork.print_art_info()
                        
                        # To go to the previous artwork
                        elif artwork_action == 2:
                            # Update the liked_artworks index
                            if i>0:
                                i -= 1
                            
                            # Stop displaying this artwork
                            display.kill()
                            
                            # Break out of the 'show this artwork' loop
                            break
                        
                        # To go to the next artwork
                        elif artwork_action == 3:
                            # Update the liked_artworks index
                            if i < len(liked_artworks):
                                i += 1
                            
                            # Stop displaying this artwork
                            display.kill()
                            
                            # Break out of the 'show this artwork' loop
                            break
                        
                        # To return to the main menu 
                        elif artwork_action == 4:
                            # Stop displaying this artwork
                            display.kill()
                            
                            # Set the task to 0 for the main menu
                            task = 0
                            
                            # Get out of the 'browse liked artworks' loop
                            browse = 3
                                
                            # Get out of the 'view artworks' loop
                            i = len(liked_artworks)
                                
                            # Break out of the 'show this artwork' loop
                            break
                            
                        # To quit art finder
                        else:
                            # Stop displaying this artwork
                            display.kill()
                            
                            print('Quitting art finder')
                            sys.exit()
            
            # To return to the main menu
            if browse == 3:
                task = 0  
        
        # To improve predictions
        if task==3:
            # Train only if there are some artworks in the database.
            if database.number_of_artworks < 1:
                print('You have not rated any artworks yet')      
            else:
                while True:
                    try:
                        print('\nA model of your artwork preferences will be' \
                              '\ntrained extensively, improving its accuracy.' \
                              '\nThis may take several minutes.')
                        train = int(input('1. Train better model \n2. Return to main menu \n'))
                        assert train==1 or train==2
                        break
                    except ValueError:
                        print('\nPlease enter a number')
                    except:
                        print('\nPlease pick between 1-2')
                
                # To train the new model
                if train==1:
                    # Train a model slowly and export it
                    mt.train_model(database, stored_models, quick=False)
                    
                # Return to main menu
                task = 0
        
        # To quit art finder
        if task==4:
            print('Quitting art finder')
            sys.exit()
    
    
if __name__=="__main__":
    main()

    





