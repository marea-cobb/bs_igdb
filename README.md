bs_igdb
=======

This django application is an immunogen database (Igdb) using the bootstrap webframe.


- bs_igdb: Django Project
    - settings
    - urls.py: contains all common urls and links to the html templates.
    - wsgi.py: auto created with django.

- bs_igdbview: Application
    - migrations: South application creates this folder to help track the changes to models.py (database structure)
    - static: contains the bootstrap templates
    - admin.py
    - base.py
    - models.py: Contains each table as a python model. Django uses this to create the database.
    - urls.py: Currently empty. Can use for application specific urls if multiple applications are grouped in the same django project.
    - utils.py: Contains utility functions
    - views.py: Main python code that filters or modifies the html views.
- templates: contains all of the html views.
    - admin: Included by django. Nice view for registered admins.
    - bs_igdb: Contains all of the bs_igdb application html views.
- upload scripts: Contains the scripts that parse the data to be imported into the database.
- .gitignore: Contains files that will not be uploaded into github (i.e. biological data)
- manage.py: django script that is required to sync the database, migrate the database, and run the server.
    Look at django how_to documentation for further details.
- todo: List of all items that are still required for the project.