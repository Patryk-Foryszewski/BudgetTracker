<a href="https://github.com/vchaptsev/cookiecutter-django-vue">
    <img src="https://img.shields.io/badge/built%20with-Cookiecutter%20Django%20Vue-blue.svg" />
</a>


# BudgetTracker

Simple, very basic application that allows user to create bugdets and track its expenses.
The application allows for creating several users. Each user can create a list of
any number of budgets and share it with any number of users. The budget consists of
income and expenses. They are grouped into categories. It is required to create REST or
GraphQL API and a database. The project should contain authorisation, tests, fixtures,
filtering and pagination

## Table of Contents
* [Technologies Used](#technologies-used)
* [Dependecies](#Requirements)
* [Development](#Development)
<!-- * [Screenshots](#screenshots) -->


## Technologies Used

* Python 3.8.8
* Django 3.2.4


### Dependencies

* You will find all requirements in requirements.txt

<!--  -->
<!-- ## Screenshots -->
<!-- ![Home Page](https://www.remotedir.eu/DjangoPhotoBlogHomePage.png?) -->
<!-- ![Post Details View](https://www.remotedir.eu/DjangoPhotoBlogPostView.png?) -->

## Features

* User can:
    create an account,
    edit account info,
    add profile picture,
    create category for budgetss
    add budget to the category
    edit budget
    add other users to the budget
    track all expenses

## Development

Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/). Start your virtual machines with the following shell command:

`docker-compose up --build`

If all works well, you should be able to create an admin account with:

`docker-compose run backend python manage.py createsuperuser`


## Authors

* Patryk Foryszewski


## License

This project is licensed under the MIT License - see the LICENSE.md file for details
