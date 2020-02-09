from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill

class Thumbnail(ImageSpec):
    processors = [ResizeToFill(60, 80)]


# print('OKOKOKOKOKOKOK')
register.generator('user_profile:thumbnail', Thumbnail)