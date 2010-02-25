from PIL import Image, ImageOps, ImageEnhance
try:
    from cStringIO import StringIO
except:
    import StringIO


class ImageHandler(object):
    def __init__(self, image):
        try:
            self.file = Image.open(image)
        except AttributeError:
            self.file = image
        self.handle_exif_rotation()
    
    def rotate(self, rotation):
        """ Takes rotation angle in clockwise degrees int """
        self.file = self.file.rotate(rotation)
        return self
    
    
    def __aspects(self, source, target, minimum=True):
        """
        1. Using absolute function
        2. Using resize_aspects with minimum=True
        3. Using resize_aspects with minimum=False
    
        Resize
            ``` im.resize(given) ```
            R1. distorts image to exact given measurements
            R2. treats given as minimum but retains aspect ratio - one exact side, one larger side
            R3. treats given as maximum but retains aspect ratio - one exact side, one smaller side
        Fit
            ``` ImageOps.fit(im, given) ```
            F1. same as R2. with the extras cropped
            F2. same as R2.
            F3. same as R3.
    
        """
        source_w, source_h = source
        target_w, target_h = target
        # setup defaults
        resize_w, resize_h = target_w, target_h
    
        source_a = float(source_w) / float(source_h)
        target_a = float(target_w) / float(target_h)
    
        if minimum:
            # work out the aspects needed to see if need to resize by width or height
            if (target_a <  source_a):
                resize_w = target_h * source_a
            elif (target_a > source_a):
                resize_h = target_w / source_a
            else:
                pass
    
        else:
            # if target is bigger than source
            if target_w > source_w and target_h > source_h:
                target_w = source_w
                target_h = source_h
    
            # resize by which ratio
            ratio_w = float(source_w) / float(target_w)
            ratio_h = float(source_h) / float(target_h)
    
            ratio = ratio_w if ratio_w > ratio_h else ratio_h
    
            resize_w = float(source_w) / ratio
            resize_h = float(source_h) / ratio
    
        return int(resize_w), int(resize_h)
    
    def resize(self, max_size):
        """
            Makes sure that the returned image fits the given area NO CROPPING with WHITESPACE.
            Takes max_size as tuple(int, int)
            Returns a new instance of ImageHandler.
        """
        re_size = self.__aspects(self.file.size, max_size, False)
        return ImageHandler(self.file.resize(re_size, Image.ANTIALIAS))
    
    def fit(self, max_size):
        """
            Makes sure that the returned image fits the given area IS CROPPED with NO WHITESPACE.
            Takes max_size as tuple(int, int)
            Returns a new instance of ImageHandler.
        """
        im = self.file
        return ImageHandler(ImageOps.fit(im, max_size, Image.ANTIALIAS, 0, (0.5,0.5)))
    
    def content(self):
        """ Returns the contents of the file """
        sio = StringIO()
        self.file.save(sio, 'jpeg', quality=85)
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
