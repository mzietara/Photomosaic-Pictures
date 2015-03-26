from mosaic import *
from fractal_mosaic import *
from enhanced_mosaic import *
import media
import time

if __name__ == '__main__':

    #m1 = Mosaic('dali')
    #m2 = FractalMosaic('dali')
    m3 = EnhancedMosaic('dali')
        

    #m1.create_mosaic('karan.jpg', 20)
    #m1.save_as('karan_with_mosaic.jpg')

    #m2.create_mosaic('karan.jpg', 20, 60)
    
    #m2.save_as('karan_with_fractalmosaic.jpg')
    
    m3.create_mosaic('karan.jpg', 20, 60)
    
    m3.save_as('karan_with_enhancements.jpg')