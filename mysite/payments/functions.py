import random
import string

def random_coupon_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_coupon_generator():
    new_coupon_code = random_coupon_generator()
    return new_coupon_code