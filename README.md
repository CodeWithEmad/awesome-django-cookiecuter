# Awesome Django Cookiecutter 🍪

This is a cookiecutter for docker-based development and production environments of a Django application. There are other cookiecutters for Django out there, but they're either too complicated to set up for the first time, or they lack development tools.

## Features

This cookiecutter focuses on Django and Django REST framework with best practices and tools. Celery, Beat, and Flower are set up out of the box. You can simply add your customizations and you're good to go.

Additionally, in the development environment, you have pgAdmin4 to check out your database and a MailHog service to take care of email UI testing, making life easier.

You also have a beautiful documentation using mkdocs.

## Installation

You need `cookiecutter`. If you don't have it, run:

```bash
pip install -U cookiecutter
```

Then, to create the project, run:

```bash
cookiecutter https://github.com/CodeWithEmad/awesome-django-cookiecuter
```

It will prompt you to answer some questions to customize the project.

## Contributing

Any contributions are welcome.

## License

This work is licensed under the terms of the [GNU Affero General Public License (AGPL)](https://github.com/overhangio/tutor/blob/master/LICENSE.txt).
