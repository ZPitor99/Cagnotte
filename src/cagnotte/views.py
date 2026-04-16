import click

import cagnotte.data as gestion_db
from cagnotte.domain import compute_transactions


@click.group()
def cli():
    gestion_db.init_db()

#Color msg
def echo_err(msg):   click.echo(click.style(msg, fg="red"))
def echo_info(msg):  click.echo(click.style(msg, fg="cyan"))


# -----------------------------------------------------------------------------------------------------------------------

@cli.command()
def show_cagnottes():
    """
    Show the list of cagnottes available.
    """
    data = gestion_db.select_all_cagnottes()
    if not data:
        echo_info("No cagnottes.")
        return
    i = 1
    echo_info(f"The {len(data)} Cagnotte(s)")
    for item in data:
        click.echo(f"{i} - {item[0]}")
        i += 1
    return


@cli.command()
@click.option("-n", "--name", prompt="Name of cagnotte", help="The name of the cagnotte.")
def create_cagnotte(name: str):
    """
    Create a new cagnotte with the name send.
    """
    gestion_db.add_cagnottes(par_name=name)
    echo_info(f"Cagnotte {name} created")
    return


@cli.command()
@click.option("-n", "--name", prompt="Name of cagnotte", help="The name of the cagnotte.")
def delete_cagnotte(name: str):
    """
    Delete the cagnotte named.
    """
    did = gestion_db.del_cagnottes(par_name=name)
    if not did:
        echo_err("The cagnotte does not exist.")
    else:
        echo_info(f"Cagnotte {name} deleted")
    return


@cli.command()
@click.option("-n", "--name", prompt="Name of cagnotte", help="The name of the cagnotte.")
def show_expenses(name: str):
    """
    Show the details of a cagnotte expenses.
    """
    data = gestion_db.select_one_cagnotte(par_name=name)
    if not data:
        echo_info(f"No expenses for {name}.")
        return
    echo_info(f"There is {len(data)} expenses in {name}.")
    for item in data:
        click.echo(item.presentation())
    return


# -----------------------------------------------------------------------------------------------------------------------

def cagnotte_exist(name: str)->bool:
    """
    Say if the cagnotte exists or not.
    Args:
        name (str): The name of the cagnotte.

    Returns:
        bool: True if cagnotte exists else False.

    """
    row = gestion_db.get_cagnotte(name)
    if not row:
        return False
    return True


def est_nombre(s)->bool:
    """
    Say if s can be trans type in a float
    Args:
        s (Any): The value to test.

    Returns:
        bool: True if s can be a float, False otherwise.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


@cli.command()
@click.option("-n", "--name", prompt="Name of cagnotte", help="The name of the cagnotte.")
@click.option("-p", "--person", prompt="The person", help="The name of the person")
@click.option("-a", "--amount", prompt="The amout", help="The amount of expense")
def add_expense(name: str, person: str, amount: float):
    """
    Add an expense to the cagnotte.
    """
    if est_nombre(amount):
        amount = round(float(amount),2)
    else:
        echo_err(f"The amount {amount} need to be a number.")

    if amount <= 0:
        echo_err(f"The amount {amount} cannot be less than zero.")
    elif not cagnotte_exist(name):
        echo_info(f"The cagnotte {name} does not exist.")
    else:
        try:
            gestion_db.add_expense(par_id_cagnotte=name, par_person=person, par_expense=amount)
            echo_info(f"Expense of {amount}€ added for {person} in {name}.")
        except Exception as e:
            echo_err(f"An error occured while adding expense to cagnotte {name}.")
            click.echo(f"Maybe the {person}'s expense for {name} already exists.")
    return


@cli.command()
@click.option("-n", "--name", prompt="Name of cagnotte", help="The name of the cagnotte.")
@click.option("-p", "--person", prompt="The person", help="The name of the person")
def del_expense(name: str, person: str):
    """
    Delete the expense of the person in the cagnotte named.
    """
    if not cagnotte_exist(name):
        echo_info(f"The cagnotte {name} does not exist.")
    else:
        try:
            gestion_db.del_expense(par_id_cagnotte=name, par_person=person)
            echo_info(f"Expense of {person} deleted in {name}.")
        except Exception as e:
            echo_err(f"An error occured while adding expense to cagnotte {name}.")
            click.echo(f"Maybe the {person}'s expense for {name} does not exists.")
    return


@cli.command()
@click.option("-n", "--name", prompt="Name of cagnotte", help="The name of the cagnotte.")
def solde(name: str, ):
    """
    Compute and show the "who have to send to who"
    """
    if not cagnotte_exist(name):
        echo_err(f"The cagnotte {name} does not exist.")
    elif len(gestion_db.select_one_cagnotte(name)) == 0:
        echo_info(f"The cagnotte {name} is empty.")
    else:
        data = gestion_db.select_expenses(name)
        i = 1
        echo_info(f"The {len(data)} Expenses in {name}")
        for item in data:
            click.echo(f"{i} - "
                       f"{item[3].strftime("%Y-%m-%d %H:%M:%S")} | "
                       f"{item[2]}€ - "
                       f"{item[1]}")
            i += 1

        transaction = compute_transactions(name)
        if not transaction or len(transaction) == 0:
            echo_info(f"No transactions for {name}")
        else:
            echo_info(f"\nThe {len(transaction)} transactions")
            for elem in transaction:
                click.echo(f"{elem.presentation()}")
