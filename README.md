# Cagnotte Project

Project of application to manage a money pool (cagnotte).

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
- 

Using `dataclasses`, `datetime`, `typing` too.

```bash
cagnotte v0.1
├── click v8.3.1
│   └── colorama v0.4.6
└── sqlalchemy v2.0.48
    ├── greenlet v3.3.2
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
        │   └── files.html #For Flask (next version)
        └── views.py
```

## Python package and project manager

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

## Links

GitHub : [Cagnotte-Project](https://github.com/ZPitor99/Cagnotte)

Course & examples used : [https://kathode.neocities.org/data/archilog](https://kathode.neocities.org/data/archilog)
