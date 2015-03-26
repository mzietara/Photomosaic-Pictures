from os import listdir, path
from math import sqrt, pow
import media
import Image

class FractalMosaic(object):
    '''Build a fractal photomosaic, which is a single picture represented as a
    grid of smaller component pictures.'''
    
    def __init__(self, pathh):
        '''Initialize the contents of the FractalMosaic object, so that it
        stores all the images in the directory specified by the string path.'''
        
        self.path = pathh
        self.path_images = listdir(pathh)
        self.mpic = None
        
        #create a dictionary with all the images' path names as the keys, and
        #their average colours as the values.
        self.col_avg_d = {}
        for filename in self.path_images:
            pic_name = path.join(self.path, filename)
            self.col_avg_d[pic_name] = color_average(pic_name)
   
    def create_mosaic(self, filename, min_size, threshold):
        '''Create and store a photomosaic version of the single picture
        specified by filename.'''
        
        main_pic = Image.open(filename)
        self.mpic = main_pic
        make_mosaic(self, main_pic, min_size, threshold, x=0, y=0)
    
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

def make_mosaic(mosaic, main_pic, min_size, threshold, x=0, y=0):
    '''make the mosaic.'''
    
    size = main_pic.size
    if size[0] < min_size or size[1] < min_size:
        
        temp = Image.open(closest_pic(main_pic, mosaic.col_avg_d)[0])
        temp = temp.resize(size)
        mosaic.mpic.paste(temp, (x, y))
    
    else:
        #Check if there is a match, and replace the region with the picture
        #if there is one.
        closest = closest_match(mosaic, main_pic)
        if closest[1] < threshold:
            mosaic.mpic.paste(closest[0], (x, y))
            
        #Split the picture into 4 quadrants, and repeat the algorithm.
        else:
            top_left = main_pic.crop((0, 0, size[0] / 2, size[1] / 2))
            top_right = main_pic.crop((size[0] / 2, 0, size[0], size[1] / 2))
            bot_left = main_pic.crop((0, size[1] / 2, size[0] / 2, size[1]))
            bot_right = main_pic.crop((size[0] / 2, size[1] / 2, size[0], \
                                       size[1]))
        
            make_mosaic(mosaic, top_left, min_size, threshold, x, y)
            make_mosaic(mosaic, top_right, min_size, threshold, \
                        x + size[0] / 2, y)
            make_mosaic(mosaic, bot_left, min_size, threshold, x, y + \
                        size[1] / 2)
            make_mosaic(mosaic, bot_right, min_size, threshold, \
                    x + size[0] / 2, y + size[1] / 2)

def closest_match(mosaic, main_pic):
    '''Find the picture in the picture database that is the closest match to
    main_pic picture. Return a tuple, where the first element is the image, and
    the second element is the average distance of each pixel from the image
    to each pixel in main_pic.'''
    
    size = main_pic.size
    closest = (None, 450)
    main_all_pix = main_pic.getdata()
    
    #Go through all of the pictures in the database, and find the one that
    #is the closest match to main_pic by comparing each pixel.
    for picname in mosaic.col_avg_d:
        current_pic = Image.open(picname).resize(size)
        cur_all_pix = current_pic.getdata()
        dist = 0
        
        #Find the distances between each corresponding pixel from main_pic to
        #the current picture that is being looked at in the picture database.
        for i in range(len(main_all_pix)):
            main_pix = media.Color(main_all_pix[i][0], main_all_pix[i][1], \
                                   main_all_pix[i][2])
            cur_pix = media.Color(cur_all_pix[i][0], cur_all_pix[i][1], \
                                  cur_all_pix[i][2])
            dist += main_pix.distance(cur_pix)
        avg_dist = dist / (size[0] * size[1])
            
        if avg_dist < closest[1]:
            closest = (current_pic, avg_dist)
    
    return closest
