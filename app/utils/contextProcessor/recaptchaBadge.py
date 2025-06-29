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
        match RECAPTCHA and RECAPTCHA_BADGE:
            case True:
                return True
            case False:
                return False

    return dict(recaptchaBadge=recaptchaBadge())
