'''Functions for beginning to use the art_finder project.
'''

import os

def create_database_txt(directory, name):
    '''Creates a database.txt file to store the info about each Artwork that the viewer
    has seen or will see. Returns the absolute path of database.txt as a string.
    '''
    file = open(directory+name+'.txt', 'w')
    file.close()
    
    return directory+name+'.txt'
    
def create_models_txt(directory, name):
    '''Creates the models.txt file, delimited by ~, that will be used to store info about each model.
    Returns the absolute path of models.txt as a string.
    '''
    file = open(directory+name+'.txt', 'w')
    file.write('Training Error~Cross Validation Error~Testing Error~Training Accuracy~')
    file.write('Cross Validation Accuracy~Testing Accuracy~Precision Disliked~Recall Disliked~')
    file.write('F1 Disliked~Precision Liked~Recall Liked~F1 Liked~Training Examples~')
    file.write('Cross Validation Examples~Testing Examples~Solver~C~Added~Trained Quickly~Time to Train~Theta')
    file.close()
    
    return directory+name+'.txt'

def create_scraped_page_txt(directory, name):
    '''Creates the scraped_page.txt file, which stores the page number of the NGA website that
    the spider last scraped. Returns the absolute path of scraped_page.txt.
    '''
    file = open(directory+name+'.txt', 'w')
    file.close()
    
    return directory+name+'.txt'

def create_disliked_txt(directory, name):
    '''Creates the predicted_dislike.txt file, which stores info about the scraped artworks that
    the viewer is predicted to dislike (so they are not shown to the viewer for rating.
    '''
    file = open(directory+name+'.txt', 'w')
    file.write('Artist~Artist Info~Title~Viewing Link~Added\n')
    file.close()
    
    return directory+name+'.txt'

create_database_txt('/home/pi/Documents/Programs/art_finder_env/all_data/', 'permanent_database')  
create_models_txt('/home/pi/Documents/Programs/art_finder_env/all_data/', 'stored_models')
create_scraped_page_txt('/home/pi/Documents/Programs/art_finder_env/all_data/', 'page_last_scraped') 
create_disliked_txt('/home/pi/Documents/Programs/art_finder_env/all_data/', 'predicted_disliked')
