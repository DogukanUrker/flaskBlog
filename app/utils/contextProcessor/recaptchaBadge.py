from settings import (
    RECAPTCHA,
    RECAPTCHA_BADGE,
)


def recaptchaBadge():
    """
    Returns a dictionary with a constant indicating whether the recaptcha badge should be visible or not.

    Returns:
        dict: A dictionary with a constant indicating whether the recaptcha badge should be visible or not.
    """

    def recaptchaBadge():
        if RECAPTCHA and RECAPTCHA_BADGE:
            return True
        else:
            return False

    return dict(recaptchaBadge=recaptchaBadge())
