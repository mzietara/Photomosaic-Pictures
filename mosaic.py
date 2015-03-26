from os import listdir, path
from math import sqrt, pow
import media
import Image

class Mosaic(object):
    '''Build a basic photomosaic, which is a single picture represented as a
    grid of smaller component pictures.'''
    
    def __init__(self, pathh):
        '''Initialize the contents of the Mosaic object, so that it stores all
        the images in the directory specified by the string path.'''
        
        self.path = pathh
        self.path_images = listdir(pathh)
        self.mpic = None
        
        #create a dictionary with all the images' path names as the keys, and
        #their average colours as the values.
        self.col_avg_d = {}
        for filename in self.path_images:
            pic_name = path.join(self.path, filename)
            self.col_avg_d[pic_name] = color_average(pic_name)

    def create_mosaic(self, filename, min_size):
        '''Create and store a photomosaic version of the single picture
        specified by filename.'''
        
        main_pic = Image.open(filename)
        self.mpic = main_pic
        make_mosaic(self, main_pic, min_size, x=0, y=0)
    
    def save_as(self, filename):
        '''Save the picture that stores the photomosaic resulting from
        create_mosaic in a file called filename. If the photomosaic hasn't
        been created yet, don't save anything.'''
        
        if self.mpic != None:
            self.mpic.save(filename)

def color_average(filename):
    '''Return a media.Color object of the average colour in the picture at the
    path filename. Filename can either accept a path to a picture, or a picture
    object.'''
    
    #If it's a path to a filename, open the picture at that filename.
    if isinstance(filename, str):
        pic = Image.open(filename)
    else:
        pic = filename
        
    total_red, total_green, total_blue = 0, 0, 0
    hist = pic.histogram()
    
    #Using the histogram, add all the values for red from each pixel to
    #total_red, all the green values to total_green, and all the blue values to
    #total_blue.
    for i in range(len(hist)):
        if i <= 255:
            total_red += i * hist[i]
        elif i <= 511:
            total_green += (i % 256) * hist[i]
        else:
            total_blue += (i % 256) * hist[i]
            
    #find the total number of pixels, then divide that by total_red to get the
    #average red, etc.
    total_pix = pic.size[0] * pic.size[1]
    red = total_red / total_pix
    green = total_green / total_pix
    blue = total_blue / total_pix
    
    return media.Color(red, green, blue)
    
def closest_pic(main_pic, col_avg_d):
    '''Main_pic is a media.Picture object, and col_avg_d is a dictionary where
    the keys are the path names to images, and the values are the average
    colours. Return a tuple where the first element is the path of the image
    that has the smallest colour distance to main_pic, and the second element
    is the distance.'''
    
    main_pic_avg = color_average(main_pic)
    
    #Keep track of the closest pic so far.
    closest = ("", 450)
    
    for (key, value) in col_avg_d.items():
        dist = main_pic_avg.distance(value)
        if dist < closest[1]:
            closest = (key, dist)
        
    return closest

def make_mosaic(mosaic, main_pic, min_size, x=0, y=0):
    '''Create the photomosaic.'''
    
    size = main_pic.size
    if size[0] < min_size or size[1] < min_size:
        temp = Image.open(closest_pic(main_pic, mosaic.col_avg_d)[0])
        temp = temp.resize(size)
        mosaic.mpic.paste(temp, (x, y))
        
    #Split the picture into 4 quadrants, and repeat the algorithm.
    else:
        top_left = main_pic.crop((0, 0, size[0] / 2, size[1] / 2))
        top_right = main_pic.crop((size[0] / 2, 0, size[0], size[1] / 2))
        bot_left = main_pic.crop((0, size[1] / 2, size[0] / 2, size[1]))
        bot_right = main_pic.crop((size[0] / 2, size[1] / 2, size[0], size[1]))
        
        make_mosaic(mosaic, top_left, min_size, x, y)
        make_mosaic(mosaic, top_right, min_size, x + size[0] / 2, y)
        make_mosaic(mosaic, bot_left, min_size, x, y + size[1] / 2)
        make_mosaic(mosaic, bot_right, min_size, x + size[0] / 2, y + \
                    size[1] / 2)
