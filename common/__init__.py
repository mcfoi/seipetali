__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from photologue.models import ImageModel
from django.conf import settings
from photologue.models import ImageModel
from django.core.files.base import ContentFile
from io import BytesIO
# Required PIL classes may or may not be available from the root namespace
# depending on the installation method used.
try:
    import Image
    import ImageFile
    import ImageFilter
    import ImageEnhance
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageFile
        from PIL import ImageFilter
        from PIL import ImageEnhance
    except ImportError:
        raise ImportError(
            'Photologue was unable to import the Python Imaging Library. Please confirm it`s installed and available '
            'on your current Python path.')


def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        try:
            im = Image.open(self.image.storage.open(self.image.name))
        except IOError:
            return
        # Save the original format
        im_format = im.format
        # Apply effect if found
        if self.effect is not None:
            im = self.effect.pre_process(im)
        elif photosize.effect is not None:
            im = photosize.effect.pre_process(im)
        # Resize/crop image
        if im.size != photosize.size and photosize.size != (0, 0):
            im = self.resize_image(im, photosize)
        # Apply watermark if found
        if photosize.watermark is not None:
            im = photosize.watermark.post_process(im)
        # Apply effect if found
        if self.effect is not None:
            im = self.effect.post_process(im)
        elif photosize.effect is not None:
            im = photosize.effect.post_process(im)
        # Save file
        im_filename = getattr(self, "get_%s_filename" % photosize.name)()
        try:
            buffer = BytesIO()
            if im_format != 'JPEG' and not getattr(settings,'PHOTOLOGUE_FORCE_JPEG',False):
                im.save(buffer, im_format)
            else:
                im.save(buffer, 'JPEG', quality=int(photosize.quality),
                        optimize=True)
            buffer_contents = ContentFile(buffer.getvalue())
            self.image.storage.save(im_filename, buffer_contents)
        except IOError as e:
            if self.image.storage.exists(im_filename):
                self.image.storage.delete(im_filename)
            raise e

ImageModel.add_to_class('create_size', create_size)
