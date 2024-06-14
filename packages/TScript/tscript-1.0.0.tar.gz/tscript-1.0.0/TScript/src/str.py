import string as s
import random as r
def random_char(leng):
    o = s.ascii_letters
    return "".join(r.choice(o) for _ in range(leng))
def ascii_digits():
    return s.ascii_letters + s.digits