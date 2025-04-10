

# Habit Tracker - Only 21 Days Needed to Form a Habit

#### This is a simple habit tracking app. If you want to create a new habit, you have to do it for at least 21 days straight. This app uses a library called `plotly-calplot` to create calendar heatmaps similar to GitHub's contribution graph.

## Installation

#### Create a virtual environment in the project root directory

```Shell
python3.13 -m venv venv
```

#### Activate the virtual environment

- ##### For Linux / Mac

  ```Shell
  source venv/bin/activate
  ```

- ##### For Windows

  ```PowerShell
  .\venv\Scripts\activate
  ```

#### Install the required packages

```Shell
(venv) $ pip install -r requirements.txt
```

## Running

### Prepare the database

#### You have two options: use SQLite or PostgreSQL.

If you want to use PostgreSQL, you need to install it on your computer and run it. After that, connect to PostgreSQL in the terminal.

```Shell
(venv) $ sudo -u postgres psql
```

Then, create a database, a user, and grant the user privileges to the database:

```SQL
CREATE DATABASE your_database;
CREATE USER your_username WITH LOGIN SUPERUSER CREATEDB CREATEROLE ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_database TO your_username;
```

After creating everything, add this information to your settings file:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "your_database",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Then, run migrations and create a superuser:

```Shell
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
(venv) $ python manage.py createsuperuser
```

If you prefer to use SQLite, comment out the PostgreSQL settings and uncomment the SQLite settings:

```python
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
```

After that, repeat the migrations and superuser creation steps:

```Shell
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
(venv) $ python manage.py createsuperuser
```

Finally, run the development server:

```Shell
(venv) $ python manage.py runserver
```

## Software Dependencies

[Django](https://www.djangoproject.com/) – The web framework for perfectionists with deadlines. 

[Plotly-calplot](https://github.com/brunorosilva/plotly-calplot) – Makes it easier to visualize and customize time-relevant or time-series data with Plotly interaction.

[Bootstrap v5](https://getbootstrap.com/) – A powerful, extensible, and feature-packed frontend toolkit.

[Django-crispy-forms](https://django-crispy-forms.readthedocs.io/) – Makes forms more elegant and user-friendly.

[Cssbuttons](https://cssbuttons.io/) – A frontend toolkit for button design.

For the full list of software dependencies, see [requirements.txt](requirements.txt).

## Latest Releases

**v0.1.0** (2025-04-07)

## API References

[Api-ninjas](https://www.api-ninjas.com/) – Used for motivational quotes.

## [License](LICENSE)

The MIT License (MIT)

Copyright (c) 2025 Owl Coding

