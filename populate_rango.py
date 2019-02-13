import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango.settings')
django.setup()


from rango.models import Category, Page

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def populate():
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/"},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/"},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/"}]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/"},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/"}]

    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/"},
        {"title": "Flask",
         "url": "http://flask.pocoo.org"}]

    cats = {"Python": {"pages": python_pages},
            "Django": {"pages": django_pages},
            "Other Frameworks": {"pages": other_pages}}

    cats_views_likes = {"Python": {'views': 128, 'likes': 64}, "Django": {
        'views': 64, 'likes': 23}, "Other Frameworks": {'views': 32, 'likes': 16}}

    for cat, cat_data in cats.items():
        c = add_cat(cat, cats_views_likes[cat]
                    ['views'], cats_views_likes[cat]['likes'])
        for p in cat_data["pages"]:
            add_page(c, p['title'], p['url'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("-{0} - {1}".format(str(c), str(p)))


if __name__ == "__main__":
    populate()
