__author__ = 'FcoHernan'


import Image
# open an image file (.bmp,.jpg,.png,.gif) you have in the working folder
imageFile = "output.png"
im1 = Image.open(imageFile)

# adjust width and height to your needs
width = 5000
height = 5000    
# use one of these filter options to resize the image
im5 = im1.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter
name="output"
im5.save(name+".jpg")
