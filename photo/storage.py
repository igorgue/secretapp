
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files import File
try:
    from cStringIO import StringIO
except:
    import StringIO

class BotoS3Storage(Storage):
    """
    Storage system to save files to S3
        http://docs.djangoproject.com/en/1.1/ref/files/storage/#ref-files-storage
    
    Uses pythonic wrapper Boto
        http://boto.s3.amazonaws.com/ref/s3.html
    """
    def __init__(self, bucket=None, base=None, MEDIA_URL=None, public=True,\
                        AWS_ACCESS_KEY_ID=None, AWS_SECRET_ACCESS_KEY=None):
        # bucket on s3 where files are stored
        if bucket is None:
            bucket = settings.MEDIA_ROOT
        # folder in bucket where files are stored
        if base is None: # eqv to upload_to
            base = ""
        elif len(base) > 1 and not base[-1] == '/':
            # base must end in a slash
            base = "".join([base, '/'])
        # public access base for files - can override if using cloudfront
        if MEDIA_URL is None:
            MEDIA_URL = "http://%s.s3.amazonaws.com/" % bucket
        # AWS access keys
        if AWS_ACCESS_KEY_ID is None:
            AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
        if AWS_SECRET_ACCESS_KEY is None:
            AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
        
        # assign
        self.bucket_name = bucket
        self.base = base
        self.MEDIA_URL = MEDIA_URL
        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
        self.public = public
    
    def _connect(self):    	
        """ returns a connection to s3 """
        import boto
        if hasattr(self, 'connection'):
            return self.connection
        self.connection = boto.connect_s3(self.AWS_ACCESS_KEY_ID, self.AWS_SECRET_ACCESS_KEY)
        return self.connection
    
    def _bucket(self):
        """ returns the bucket where the file is stored """
        if hasattr(self, 'bucket_connection'):
            return self.bucket_connection
        self.bucket_connection = self._connect().get_bucket(self.bucket_name)
        return self.bucket_connection
    
    def _keyname(self, name):
        """ returns the keyname used when interacting with file on s3 """
        return '%s%s' % (self.base, name)
    
    def _key(self, name):
        """ returns the key assigned to the file given by name """
        return self._bucket().get_key(self._keyname(name))
    
    def _open(self, name):
        """ called by Storage.open() returns File object """
        return File(StringIO(self._key(name).get_contents_as_string()))
    
    def _save(self, name, content, public=False):
        """ called by Storage.save() returns name for storage """
        from boto.s3.key import Key
        bucket = self._bucket()
        i = Key(bucket, self._keyname(name))
        i.set_contents_from_file(content, headers={'Content-Type':'image/png'})
        if self.public or public:
            i.set_acl('public-read')
        i.close()
        return name
    
    def get_valid_name(self, name):
        """ gets the name """
        return name
    
    def get_available_name(self, name):
        return name
    
    def url(self, name):
        """ returns the public url where the file can be accessed """
        return "".join([self.MEDIA_URL, self.base, name])
    
    def exists(self, name):
        """ returns True if exists on filesystem """
        return True if self._key(name) else False
    
    def delete(self, name):
        """ deletes file referenced by name """
        k = self._key(name)
        if k: k.delete()
        return
    
    def size(self, name):
        """ returns the size of the file """
        return self._bucket().get_key(self._keyname(name)).size

    def listdir(self, path):
        return [key.name for key in self._bucket().list()]



