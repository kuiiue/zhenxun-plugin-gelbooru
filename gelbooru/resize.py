from PIL import Image
import os

def resize_thumb(path, thumb_size: int=720):
    os.chmod(path, 0o777)

    img=Image.open(path)
    width, height=img.size
    img=img.convert('RGB')

    if width>=height and height>thumb_size:
        scale=thumb_size/height
        width=int(width*scale)
        height=thumb_size
    if height>=width and width>thumb_size:
        scale=thumb_size/width
        width=thumb_size
        height=int(height*scale)

    img.thumbnail((width, height))
    img.save(path)
