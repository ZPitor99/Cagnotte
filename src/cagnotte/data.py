from dataclasses import dataclass
from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    String, Float, DateTime, ForeignKey,
    select, delete, Row, PrimaryKeyConstraint
)


@dataclass
class Expense:
    name: str
    person: str
    amount: float
    datetime: datetime

    @classmethod
    def from_db(cls, row):
        return cls(row[0], row[1], row[2], row[3].strftime("%Y-%m-%d %H:%M:%S"))

    def presentation(self) -> str:
        return (
            f"{self.name} | "
            f"{self.person} | "
            f"{self.amount:.2f}€ | "
            f"{self.datetime}"
        )


engine = create_engine("sqlite:///src/cagnotte.db", echo=False)
metadata = MetaData()

cagnottes = Table(
    "cagnottes", metadata,
    Column("name", String(80), primary_key=True, nullable=False),
)
expenses = Table(
    "expenses", metadata,
    Column("id_cagnotte", String(80), ForeignKey("cagnottes.name", ondelete="CASCADE"), nullable=False),
    Column("person", String(40), nullable=False),
    Column("expense", Float, nullable=False),
    Column("expense_date", DateTime(timezone=False), nullable=False, default=datetime.now(tz=None)),
    PrimaryKeyConstraint("id_cagnotte", "person"),
)


def init_db():
    """
    Set up the database with tables.
    Returns:
        None
    """
    metadata.create_all(engine)


# Cagnotte

def add_cagnottes(par_name: str):
    """
    Add a new cagnotte to the table.
    Args:
        par_name (str): The name of the new cagnotte.

    Returns:
        None
    """
    stmt = cagnottes.insert().values(
        name=par_name
    )
    with engine.begin() as conn:
        result = conn.execute(stmt)
    return


def del_cagnottes(par_name: str) -> bool:
    """
    Delete cagnottes from the table.
    Args:
        par_name (str): The name of the cagnotte to delete.

    Returns:
        True if a record has been deleted, False otherwise.
    """
    stmt_verif = select(cagnottes).where(cagnottes.c.name == par_name)
    stmt = delete(cagnottes).where(cagnottes.c.name == par_name)

    with engine.begin() as conn:
        result_verif = conn.execute(stmt_verif).fetchall()
        if not result_verif:
            return False
        else:
            result = conn.execute(stmt)
            return True


def select_all_cagnottes() -> Sequence[Row[Any]]:
    """
    Get all cagnottes.
    Returns:
        All cagnottes in the database.
    """
    stmt = select(cagnottes).order_by(cagnottes.c.name)
    with engine.begin() as conn:
        result = conn.execute(stmt)
        return result.fetchall()


def select_one_cagnotte(par_name: str) -> list[Expense]:
    """
    Select all data about a cagnotte.
    Args:
        par_name (str): The name of the cagnotte to selec.

    Returns:
        The data of the cagnotte.

    """
    stmt = (select(
        cagnottes.c.name,
        expenses.c.person,
        expenses.c.expense,
        expenses.c.expense_date,
    )
            .join(expenses, cagnottes.c.name == expenses.c.id_cagnotte)
            .where(cagnottes.c.name == par_name, expenses.c.id_cagnotte == par_name))
    with engine.begin() as conn:
        result = conn.execute(stmt).fetchall()
        return [Expense.from_db(r) for r in result]


def get_cagnotte(nom: str):
    with engine.connect() as conn:
        return conn.execute(select(cagnottes).where(cagnottes.c.name == nom)).fetchone()


# Expenses

def add_expense(par_id_cagnotte: str, par_person: str, par_expense: float):
    """
    Add new expense to the table expenses.
    Args:
        par_id_cagnotte (str): The name of the cagnotte of the expense.
        par_person (str): the name of the person that did the expense.
        par_expense (float): The expense.

    Returns:
        None

    """
    stmt = expenses.insert().values(
        id_cagnotte=par_id_cagnotte,
        person=par_person,
        expense=par_expense
    )
    with engine.begin() as conn:
        result = conn.execute(stmt)

    return


def del_expense(par_id_cagnotte: str, par_person: str) -> bool:
    """
    Delete expense from the table expenses.
    Args:
        par_id_cagnotte (str): the name of the cagnotte of the expense.
        par_person (str): the name of the person that did the expense.

    Returns:
        True if a record has been deleted, False otherwise.

    """
    stmt_verif = (select(expenses)
                  .join(expenses, cagnottes.c.name == expenses.c.id_cagnotte)
                  .where(cagnottes.c.name == par_id_cagnotte, expenses.c.person == par_person))
    stmt = expenses.delete().where(expenses.c.id_cagnotte == par_id_cagnotte, expenses.c.person == par_person)
    with engine.begin() as conn:
        result_verif = conn.execute(stmt_verif).fetchall()
        if not result_verif:
            return False
        else:
            result = conn.execute(stmt)
            return True


def select_expenses(par_id_cagnotte: str) -> Sequence[Row[Any]]:
    stmt = select(expenses).where(expenses.c.id_cagnotte == par_id_cagnotte).order_by(expenses.c.expense_date)
    with engine.begin() as conn:
        result = conn.execute(stmt)
        return result.fetchall()
