
import os
from PIL import Image

def check_image_color(image):
    """Returns string containing 'ligh' or 'dark' that tells 
    if image is for day or night"""

    if not os.path.isfile(image):
        return "Image not found"

    img = Image.open(image)
    width, height = img.size
    imgl = img.load()
    rgb_im = img.convert('RGB')
    R = G = B = 0

    if image.endswith(".jpg"):
        for w in range(0, width):
            for h in range(0, height):
                r, g, b = imgl[w,h]
                R += r
                G += g
                B += b

    elif image.endswith(".png"):
        for w in range(0, width):
            for h in range(0, height):
                r, g, b = rgb_im.getpixel((w, h))
                R += r
                G += g
                B += b

    # converting to gray to detect if it's really dark or light
    Y = (0.299*R+0.587*G+0.114*B)/(width*height)
    ################only for DEBUGING ############################
    if False:
        i = R/(width*height)
        j = G/(width*height)
        k = B/(width*height)
        image = Image.new("RGB", (200, 200), (int(Y),int(Y),int(Y)))
        image.show()
        image = Image.new("RGB", (200, 200), (int(i),int(j),int(k)))
        image.show()
    ##############################################################
    if Y < 100:
        return('dark')
    else:
        return('light')


if __name__ == "__main__":
    print(check_image_color("sample.png"))
