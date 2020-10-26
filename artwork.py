'''The Artwork class is to be used to store information about any artwork that will be shown to the
viewer (because the model predicts the viewer will like it, rather than dislike it), and stored
in the permanent database. 
'''

class Artwork:
    def __init__(self, ID=0, like=0, artist='', info='', title='',
                 nga_link='', nga_id=0, nga_page=0, added='', original_name='', vector=[]):
        self.ID = ID
        self.like = like
        self.artist = artist
        self.info = info
        self.title = title
        self.nga_link = nga_link
        self.nga_id = nga_id
        self.nga_page = nga_page
        self.added = added
        self.original_name = original_name
        self.vector = vector
    
    def print_info(self):
        print('ID:', self.ID, 'Like:', self.like)
        print('   Artist:', self.artist, 'Title:', self.title, 'Info:', self.info,
              'Like:', self.like, 'Added:', self.added)
        
    def get_string(self):
        '''Returns the string of all info for artwork, delimited by ~.
        '''
        info = str(self.ID)+'~'+str(self.like)+'~'+self.artist+'~'+self.info+'~' \
                +self.title+'~'+self.nga_link+'~'+str(self.nga_id)+'~'+str(self.nga_page)+'~' \
                +self.added+'~'+self.original_name+'~'+str(self.vector)
        return info
