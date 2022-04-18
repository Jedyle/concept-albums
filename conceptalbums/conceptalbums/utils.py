import string
import random
import jsonschema

from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, field, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, field))
    Klass = instance.__class__
    max_length = Klass._meta.get_field("slug").max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug[: max_length - 5], randstr=random_string_generator(size=4)
        )

        return unique_slug_generator(instance, field, new_slug=new_slug)
    return slug


@deconstructible
class JSONSchemaValidator:

    ERROR_MESSAGE = "Value {} failed jsonschema validation."

    def __init__(self, schema):
        self.schema = schema

    def __eq__(self, other):
        # to make sure this class is serializable for django migrations
        # docs.djangoproject.com/en/4.0/topics/migrations/#migration-serializing
        return self.schema == other.schema

    def __call__(self, value):
        try:
            jsonschema.validate(instance=value, schema=self.schema)
        except jsonschema.exceptions.ValidationError:
            raise ValidationError(self.ERROR_MESSAGE.format(value))
