# django-apistar

this app is an **experimental** django-apistar hybrid. a pure proof of concept.

the ideas behind this experiment are:

- API Star supports django's ORM out of the box and already works beautifully and quickly in production;
- django has all the features devs love, like the `shell` and the `admin`, all of which are supposed to be for devs only;
- we have no true reason to not hook up them both into the same django models (besides **being shameless**). we would need to run API Star's service in a different thread from the django's (for that django admin goodness), preserving API Star's speed for the clients and the whole django toolbox for devs.

I know, **it is a bad idea**, but I couldn't **not** try.
and everything works. yeah. there's only one catch. **a really big catch: testing.** there's a section about it at the bottom of the readme.

this code is based on [this one](https://github.com/lucianoratamero/apistar-example), used for a series of talks about API Star I've done in Brazil.

## for those who don't know the projects:

- [API Star](https://github.com/encode/apistar) - current version: 0.3.9
- [django](https://www.djangoproject.com/) - current version: 2.0.3

## installation

create a virtualenv with python3 (no python2 support), then install the requirements.
```
pip install -r requirements.txt
```
with the packages installed, you may create your db:
```
apistar migrate
```
then, run the app:
```
apistar run
```
or run the django server, for access to django's admin interface:
```
python manage.py runserver
```
to run the tests, we won't be able (yet) to use anything but `py.test` (I'm explaining this decision at the bottom of the readme). since we don't want to mess up with our db, remember to `export TEST=True` before running the tests or to set it when running them, using `TEST=True`.
```
TEST=True py.test
```

## the problems I've faced while testing

as I've said, testing has proven to be a problem. to start, both API Star and django have their own sets of tools for testing. as expected, django's is more complete, but more coupled; API Star's is leaner and less coupled, but coupled nonetheless.

the good news is that we can use `py.test` directly **and** use tools from API Star to, for example, create a test client and properly check a particular view, using a particular url.

the bad news is that we need to do *waaay* more things manually, like migrating the database before testing and flushing it after each test. nothing that django doesn't already do behind the scenes, but it is a pain.

there are samples of different methods of testing in the [`core/tests.py`](https://github.com/lucianoratamero/django-apistar/tree/master/core/tests.py) file.

## if you have any suggestions to improve this:

please, open an issue or email me at [luciano@ratamero.com](mailto:luciano@ratamero.com). please.
