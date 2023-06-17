# Authors Lens
A community where words come to life, providing an opportunity for hidden talented storytellers to showcase their skills. The initiative aims to identify and promote aspiring writers who have the potential to captivate an audience with their narratives. The community encourages storytellers to unleash their inner writing skills and express themselves, as we offer exposure to talented writers who may have previously gone unnoticed. The initiative seeks to provide a platform for emerging voices and to nurture the art of storytelling.


## Table of Contents
* Introduction
* Features
* Installation
* Usage
* Acknowledgements


## Introduction
A server side app integrated with database to authenticate user, store and retrieve blog posts - built with python, django rest framework, pyotp, and mongodb.


## Features
* Python version: 3.9
* Python Decouple: 3.8
* Django version: 4.1
* Django RestFramework: 3.14.0
* Pillow: 9.5.0
* Cloudinary: 1.32
* SQLite database for local development
* MongoDB database for production (djongo: 1.3.6)
* Basic folder structure with common Django apps


## Installation
Before you start, make sure you have the following software installed on your system:
* Python 3.x
* Pip (Python package manager)


## Usage
To get started with this Django project template, follow these steps:
* Clone this repository to your local machine using 
```console
git clone https://github.com/PeterOyelegbin/authors-lens-api.git
```

* Change to the project directory using 
```console
cd authors-lens-api
```

* Create a virtual environment using
```console
python3 -m venv env
```
(on Windows, use python -m venv env).

* Activate the virtual environment:
On macOS/Linux:
```console
source env/bin/activate
```
On Windows: 
```console
env\Scripts\activate
```

* Install the dependencies using
```console
pip install -r requirements.txt
```

* Run migrations to create the SQLite database using
```console
python manage.py migrate
```

* Start the development server using
```console
python manage.py runserver
```

* Open your web browser and go to http://127.0.0.1:8000/ to see the Django welcome page.


## TODO: Features to add
Adding likes and comment features to the blog app.


## Acknowledgements
Acknowledgements and credits to **CodevoWeb** for the insight from Django – Implement (2FA) Two-Factor Authentication at [https://codevoweb.com/django-implement-2fa-two-factor-authentication/], and **Philip Oyelegbin** who contributed by integrating this project to a React app to build a full functional blog app. Thanks to vercel and Atlas database for the free web hosting and database.
