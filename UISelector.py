from constants import TAILWIND_UI


match TAILWIND_UI:
    case True:
        TEMPLATE_FOLDER = "templates/tailwindUI"
        STATIC_FOLDER = "static/tailwindUI"
    case False:
        TEMPLATE_FOLDER = "templates/standardUI"
        STATIC_FOLDER = "static/standardUI"
