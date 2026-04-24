# Cagnotte Project

Project of application to manage a money pool (cagnotte). 
This application can be used via terminal or via a web view commands to manage the pot. 

In this application the current name of a money pool is "cagnotte". 

## Specifications

- Creation and deletion of a money pool.

- Adding and removing expenses, consisting of:
  
  - participant name
  
  - payment amount
  
  - payment date

- Only one expense per participant in a given money pool.

- Calculation of “who owes whom”.

## Technologies

Is a `Python` project under `uv 0.10.11` with :

- Click
- SQLite
- SQLAlchemy
- Flask and Jinja2

Using `dataclasses`, `datetime`, `typing`, `uuid` too.
Dev in `Python 3.14.4`

```bash
cagnotte v1.0
├── click v8.3.3
│   └── colorama v0.4.6
├── flask v3.1.3
│   ├── blinker v1.9.0
│   ├── click v8.3.3 (*)
│   ├── itsdangerous v2.2.0
│   ├── jinja2 v3.1.6
│   │   └── markupsafe v3.0.3
│   ├── markupsafe v3.0.3
│   └── werkzeug v3.1.8
│       └── markupsafe v3.0.3
└── sqlalchemy v2.0.49
    ├── greenlet v3.4.0
    └── typing-extensions v4.15.0
```

## Structure

```bash
.
├── pyproject.toml
├── README.md
└── src
    └── cagnotte
        ├── __init__.py
        ├── data.py
        ├── domain.py
        ├── templates
        │   └── home.html
        └── views.py
```

## Python package and project manager

Run commande line (terminal part):
```bash
$ uv sync           # install project dependencies
$ uv run cagnotte   # run the project
$ uv build          # build the projet

Usage: cagnotte [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add-expense      Add an expense to the cagnotte.
  create-cagnotte  Create a new cagnotte with the name send.
  del-expense      Delete the expense of the person in the cagnotte named.
  delete-cagnotte  Delete the cagnotte named.
  show-cagnottes   Show the list of cagnottes available.
  show-expenses    Show the details of a cagnotte expenses.
  solde            Compute and show the "who have to send to who"
```

Run development server (web part) :
```bash
$ uv sync           # install project dependencies
$ uv run cagnotte   # run the project
$ uv build          # build the projet

uv run flask --app cagnotte.views run
```

## Links

GitHub : [Cagnotte-Project](https://github.com/ZPitor99/Cagnotte)

Course & examples used : [https://kathode.neocities.org/data/archilog](https://kathode.neocities.org/data/archilog)
