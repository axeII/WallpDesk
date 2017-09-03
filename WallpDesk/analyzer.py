
import os
from PIL import Image

def check_image_color(image):
    """Returns string containing 'ligh' or 'dark' that tells 
    if image is for day or night, Y - converting to gray to detect if 
    it's really dark or light"""

    if not os.path.isfile(image):
        return "Image not found"

    im = Image.open(image)
    width, height = im.size
    img = im.load()
    rgb_im = im.convert('RGB')
    R = 0
    G = 0
    B = 0

    try:
        for w in range(0, width):
            for h in range(0, height):
                if image.endswith(".jpg") or image.endswith(".jpeg"):
                        r, g, b = img[w,h]
                elif image.endswith(".png"):
                    r, g, b = rgb_im.getpixel((w, h))
                R += r
                G += g
                B += b
    except:
        return "Unknown format"

    Y = (0.299*R+0.587*G+0.114*B)/(width*height)
    """ only for debuging
    if False:
        i = R/(width*height)
        j = G/(width*height)
        k = B/(width*height)
        image = Image.new("RGB", (200, 200), (int(Y),int(Y),int(Y)))
        image.show()
        image = Image.new("RGB", (200, 200), (int(i),int(j),int(k)))
        image.show()
    """
    return "dark" if Y < 100 else "light"
