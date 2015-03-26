import media
import Image

def grayscale(pic):
    '''Change the image pic so that it is a grayscale version of pic.'''
    
    #Go through all the pixels, and set each colour in the pixel to the pixel's
    #intensity. A pixel's intensity is defined as average value of its red,
    #green, and blue values.
    for x in range(pic.size[0]):
        for y in range(pic.size[1]):
            col = pic.getpixel((x, y))
            intensity = col[0] / 3 + col[1] / 3 + col[2] / 3
            pic.putpixel((x, y), (intensity,) * 3)
            
m  = Image.open('us.jpg')
grayscale(m)
m.save('oinkoink.jpg')