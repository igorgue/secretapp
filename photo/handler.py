from PIL import Image, ImageOps, ImageEnhance
try:
    from cStringIO import StringIO
except:
    import StringIO


class ImageHandler(object):
    def __init__(self, image):
        self.file = Image.open(image)
        self.handle_exif_rotation()
    
    def rotate(self, rotation):
        """ Takes rotation angle in clockwise degrees int """
        self.file = self.file.rotate(rotation)
        return self
    
    def resize(self, max_size):
        """ Takes max_size as a tuple(int, int) of width,height in pixels """
        im = self.file
        self.file = ImageOps.fit(im, max_size, Image.ANTIALIAS, 0, (0.5,0.5))
        return self
    
    def content(self):
        """ Returns the contents of the file """
        sio = StringIO()
        self.file.save(sio, 'jpeg')
        content = sio.getvalue()
        sio.close()
        return content
    
    def content_file(self):
        """ Returns Django specific ContentFile """
        from django.core.files.base import ContentFile
        return ContentFile(self.content())
    
    def handle_exif_rotation(self):
        """
        Handles rotating the exif data to the correct angle
        """
        try:
            orientation_tag = 274
            orientation_angles = { 1: 0, 6: 90, 8: 270, }
            exif = self.file._getexif()
            if exif:
                rotation = orientation_angles[exif[orientation_tag]]
                if rotation:
                    self.rotate(-rotation)
        except:
            pass
