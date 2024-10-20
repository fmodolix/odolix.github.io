AUTHOR = 'Odolix'
SITENAME = "Odolix.fr"
SITESUBTITLE = "Conseil et maitrise d'oeuvre en digitalisation" 
SITEURL = ""

PATH = "content"

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = 'feeds/all-{lang}.atom.xml'
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
THEME = "theme/tuxlite_tbs"

# Blogroll
LINKS = (
    ("Django", "https://www.djangoproject.com/"),
    ("Physical units", "https://github.com/fmeurou/djangophysics")
)

# Social widget
SOCIAL = (
)

DEFAULT_PAGINATION = 30

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}
