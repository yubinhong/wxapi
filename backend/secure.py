import hashlib
from wb_wx import settings


def to_secure(time):
    secure_word = settings.WX_SALT + '%s' % time
    s = hashlib.md5()
    s.update(secure_word.encode(encoding='utf-8'))
    return s.hexdigest()

