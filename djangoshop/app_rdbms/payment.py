# This file emulates the payment action.
# The result is selected randomly, success is the more probable result.

import random


def local_payment(success=80):
    """
    Emulates payment, 80% probability of success
    :return:
    """
    result = random.randrange(0, 100)

    if result > success:
        return False

    return True

