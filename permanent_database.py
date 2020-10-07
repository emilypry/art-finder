'''The PermanentDatabase class stores the information about all of the Artworks that have been,
or soon will be, shown to the viewer. (It does not store information about scraped artworks that
the model predicted the viewer would dislike.) The PermanentDatabase information is accessible
in a .txt file, delimited by ~.
'''

import csv
from artwork import Artwork

class PermanentDatabase:
    def __init__(self, artworks=[], number_of_artworks=0):
        self.artworks = artworks
        self.number_of_artworks = number_of_artworks
        
    def add_artwork(self, artwork):
        self.artworks.append(artwork)
        self.number_of_artworks += 1
        
    def print_all(self):
        for artwork in self.artworks:
            artwork.print_info()
    
    def export_full(self, directory):
        '''Writes (rewrites) the entire database as a .txt file.
        '''
        print('Exporting database...')
        file = open(directory, 'w')
        file.write('ID~Like~Artist~Info~Title~NGA Link~NGA ID~NGA Page~Added~Original File Name~Vector\n')
        for artwork in self.artworks:
            file.write(artwork.get_string())
            file.write('\n')
        file.close()
        print('Exported database')
    
    def export_vectors_and_likes(self, directory):
        '''Writes (rewrites) all vectors (without brackets) and likes in the database as a .txt file.
        '''
        print('Exporting vectors/likes from database...')
        file = open(directory, 'w')
        for artwork in self.artworks:
            file.write(artwork.vector[1:-1])
            file.write(', ')
            file.write(artwork.like)
            file.write('\n')
        file.close()
        print('Exported vectors/likes')
    
    def clear_all(self):
        '''Deletes all artworks from database.
        '''
        self.artworks = []
    
    def import_database(self, database_txt):
        '''Imports a database from a database.txt file.
        '''
        print('Importing database...')
        db = open(database_txt, 'r')
        reader = csv.reader(db, delimiter='~')
        
        # Take the info from each row in the .txt file and turn it into an artwork
        for work in reader:
            # Make sure it's a row with artwork info, rather than the header or an empty row
            if work[0] != 'ID' and work[0] != '':
                this_work = Artwork()
                
                this_work.ID = work[0]
                this_work.like = work[1]
                this_work.artist = work[2]
                this_work.info = work[3]
                this_work.title = work[4]
                this_work.nga_link = work[5]
                this_work.nga_id = work[6]
                this_work.nga_page = work[7]
                this_work.added = work[8]
                this_work.original_name = work[9]
                this_work.vector = work[10]
                
                # Add the artwork to the database
                self.add_artwork(this_work)
                
        # Print verification
        print('Imported database with %s artworks' % self.number_of_artworks)