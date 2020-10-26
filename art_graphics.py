from graphics import *
#from PIL import Image

# Draw the box to hold all graphics
win = GraphWin('Box', 1800, 900)
win.setBackground('#F5F5F5')

# Draw the right panel
panel = Rectangle(Point(1500,0), Point(1800,900))
panel.setFill('#DAA520')
panel.setOutline('#DAA520')
panel.draw(win)

# Draw labels
artist_label = Text(Point(1650, 30), 'Artist')
artist_label.draw(win)
title_label = Text(Point(1650, 170), 'Title')
title_label.draw(win)
info_label = Text(Point(1650, 320), 'Artist Information')
info_label.draw(win)
rating_label = Text(Point(1650, 470), 'Rating')
rating_label.draw(win)

# Draw next and previous buttons
previous = Text(Point(1580, 800), 'Previous')
previous.draw(win)
nextb = Text(Point(1730, 800), 'Next')
nextb.draw(win)

# Draw image
image = Image(Point(750, 450), '/home/pi/Documents/Programs/art_finder_env/all_artworks/freshly_scraped/full/031691267d02c259d3a72ff62fb1840eebaa11a6.jpg')
image.draw(win)

