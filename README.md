# art-finder
Finds art that the user likes via web crawling and machine learning

The user can rate whether they like or dislike a set of artworks scraped from the National Gallery of Art website. A model of the user's preferences is trained 
after the user has rated each set. When the program scrapes another set of artworks, it filters the set through the current model of the user's preferences, 
and only shows the user the artworks that the model predicts they will like. With time, the program should get better at showing the user more and more 
artworks they like.

The user can also view the artworks they've liked (JPEGs of all of them are stored on the user's computer). They can also retrain a model of their preferences
more slowly than is done during the rating sessions, which should improve the model's accuracy. 

All of the user's data is stored in files on their computer. 

NOTE: as of 2/16/21, the National Gallery of Art has updated its website so the art spider, as currently written, does not retrieve new artworks. 
