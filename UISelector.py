tailwindUI = False


match tailwindUI:
    case True:
        templateFolder = "templates/tailwindUI"
        staticFolder = "static/tailwindUI"
    case False:
        templateFolder = "templates/standardUI"
        staticFolder = "static/standardUI"
