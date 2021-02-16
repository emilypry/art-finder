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
    
    def export_full(self, database_txt):
        '''Writes (rewrites) the entire database as a .txt file.
        '''
        print('Exporting database...')
        file = open(database_txt, 'w')
        file.write('ID~Like~Artist~Info~Title~NGA Link~NGA ID~NGA Page~Added~Original File Name~Vector\n')
        for artwork in self.artworks:
            file.write(artwork.get_string())
            file.write('\n')
        file.close()
        print('Exported database')
    
    def export_new(self, database_txt, artworks):
        '''Adds a new set of artworks to the database.txt file.
        '''
        print('Exporting recent artworks...')
        file = open(database_txt, 'a')
        for artwork in artworks:
            file.write(artwork.get_string())
            file.write('\n')
        file.close()
        print('Exported recent artworks')
    
    def get_vectors_and_likes(self):
        '''For all artworks in the database that have been rated already, returns a list of their
        vectors (lists) and their likes (0 or 1).
        '''
        all_vectors = []
        all_likes = []
        for artwork in self.artworks:
            # Skip over any artworks that have not yet been rated by the viewer
            if artwork.like != 0 and artwork.like != 1:
                continue
            all_vectors.append(artwork.vector)
            all_likes.append(artwork.like)
        
        return all_vectors, all_likes
    
    def export_vectors_and_likes(self, directory):
        '''Writes (rewrites) all vectors (without brackets) and likes in the database as a .txt file.
        Likes are in the final column.
        '''
        print('Exporting vectors/likes from database...')
        file = open(directory, 'w')
        for artwork in self.artworks:
            # Skip over any artworks that have not yet been rated by the viewer
            if artwork.like != 0 and artwork.like != 1:
                continue
            file.write(artwork.vector)
            file.write(', ')
            file.write(artwork.like)
            file.write('\n')
        file.close()
        print('Exported vectors/likes')
    
    def clear_all(self):
        '''Deletes all artworks from database.
        '''
        self.artworks = []
        self.number_of_artworks = 0 
    
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
                
                this_work.ID = int(work[0])
                this_work.like = int(work[1])
                this_work.artist = work[2]
                this_work.info = work[3]
                this_work.title = work[4]
                this_work.nga_link = work[5]
                this_work.nga_id = int(work[6])
                this_work.nga_page = int(work[7])
                this_work.added = work[8]
                this_work.original_name = work[9]
                
                # Read the vector as a list of ints, rather than strings
                vector = []
                i=1
                while len(vector) < 7500:
                    this_value = ''
                    while work[10][i] != '[' and work[10][i] != ']' and work[10][i] != ',':
                        this_value += work[10][i]
                        i+=1
                    vector.append(int(this_value))
                    i+=1
                this_work.vector = vector
                
                # Add the artwork to the database
                self.add_artwork(this_work)
                
        # Print verification
        print('Imported database with %s artworks' % self.number_of_artworks)
        
    def get_unrated_artworks(self):
        '''Returns a list of the artworks in the database that have not yet been rated (liked=2).
        '''
        unrated = []
        for artwork in self.artworks:
            if artwork.like == 2:
                unrated.append(artwork)
        return unrated
    
    def get_liked_artworks(self):
        '''Returns a list of the artworks in the database that have been liked (liked=1).
        '''
        liked_artworks = []
        for artwork in self.artworks:
            if artwork.like == 1:
                liked_artworks.append(artwork)
        return liked_artworks
    
    def delete_unrated_artworks(self):
        '''Removes unrated artworks from the database.
        '''
        unrated = self.get_unrated_artworks()
        for artwork in unrated:
            self.artworks.remove(artwork)
            self.number_of_artworks -= 1
        