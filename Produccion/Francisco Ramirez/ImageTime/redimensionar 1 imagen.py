__author__ = 'FcoHernan'


import Image
# open an image file (.bmp,.jpg,.png,.gif) you have in the working folder
imageFile = "132MP.jpg"
im1 = Image.open(imageFile)

# adjust width and height to your needs
width = 30551
height = 22913    
# use one of these filter options to resize the image
im5 = im1.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter
name="700MP"
im5.save(name+".jpeg")
