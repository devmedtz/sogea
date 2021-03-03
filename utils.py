import uuid
from uuid import uuid4


def get_filename(instance, filename):
    ext = filename.split('.')[1]
    new_filename = f'{uuid4()}.{ext}'
    return new_filename