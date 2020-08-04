import random 
import string
from django.utils.text import slugify

#генерирует строку из 10 случайных чисел 
def random_string_generator(size=10, chars=string.ascii_lowercase+ string.digits):
    return ''.join(random.choice(chars) for i in range(size))

#slug для пути к посту 
def slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else: slug = slugify(post_instance.title)

    klass = instance.__class__
    slug_exists = Klass.objects.filter(slug=slug).exists()
    if slug_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug,
                                     randstr=random_string_generator(size=5))
        return slug_generator(instance, new_slug=new_slug)
    return slug 