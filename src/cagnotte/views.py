import click
import uuid

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

import cagnotte.data as gestion_db
from cagnotte.domain import compute_transactions


@click.group()
def cli():
    gestion_db.init_db()


# Color msg
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

def cagnotte_exist(name: str) -> bool:
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


def est_nombre(s) -> bool:
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
        amount = round(float(amount), 2)
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
                       f"{item[3].strftime('%Y-%m-%d %H:%M:%S')} | "
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


app = Flask(__name__)
app.config['SECRET_KEY'] = uuid.uuid4().hex


@app.route("/")
def home():
    """
    Function to render the home page.
    Returns:
        render_template : Show the template with data.
    """
    gestion_db.init_db()
    selected_name = (request.args.get("name") or "").strip()
    action = (request.args.get("action") or "").strip()

    cagnottes = [item[0] for item in gestion_db.select_all_cagnottes()]

    expenses = []
    transactions = []
    raw_expenses = []
    if selected_name and cagnotte_exist(selected_name):
        expenses = gestion_db.select_one_cagnotte(selected_name)
        raw_expenses = gestion_db.select_expenses(selected_name)
        if action == "solde" and raw_expenses:
            transactions = compute_transactions(selected_name)

    return render_template(
        "home.html",
        cagnottes=cagnottes,
        selected_name=selected_name,
        expenses=expenses,
        transactions=transactions,
        raw_expenses=raw_expenses,
    )


@app.post("/action_expenses")
def perform_action_expenses():
    """
    Resolve action about expenses.
    Returns:
        redirect to the home page.
    """
    gestion_db.init_db()
    action = (request.form.get("action") or "").strip()
    name = (request.form.get("name") or "").strip()
    person = (request.form.get("person") or "").strip()
    amount_raw = (request.form.get("amount") or "").strip()

    if action == "add_expense":
        if not name or not person:
            flash("Cagnotte and person are required.", "error")
        elif not est_nombre(amount_raw):
            flash(f"The amount {amount_raw} need to be a number.", "error")
        else:
            amount = round(float(amount_raw), 2)
            if amount <= 0:
                flash(f"The amount {amount} cannot be less than zero.", "error")
            elif not cagnotte_exist(name):
                flash(f"The cagnotte {name} does not exist.", "error")
            else:
                try:
                    gestion_db.add_expense(
                        par_id_cagnotte=name,
                        par_person=person,
                        par_expense=amount,
                    )
                    flash(f"Expense of {amount}€ added for {person} in {name}.", "success")
                except Exception:
                    flash(f"Maybe the {person}'s expense for {name} already exists.", "error")
    elif action == "del_expense":
        if not name or not person:
            flash("Cagnotte and person are required.", "error")
        elif not cagnotte_exist(name):
            flash(f"The cagnotte {name} does not exist.", "error")
        else:
            did = gestion_db.del_expense(par_id_cagnotte=name, par_person=person)
            if did:
                flash(f"Expense of {person} deleted in {name}.", "success")
            else:
                flash(f"Maybe the {person}'s expense for {name} does not exists.", "error")
    else:
        flash("Unknown action.", "error")

    params = {}
    if name:
        params["name"] = name
    return redirect(url_for("home", **params))


@app.post("/action_cagnotte")
def perform_action_cagnotte():
    """
    Resolve action about cagnottes.
    Returns:
        redirect to the home page.
    """
    gestion_db.init_db()
    action = (request.form.get("action") or "").strip()
    name = (request.form.get("name") or "").strip()

    if action == "create_cagnotte":
        if not name:
            flash("Name of cagnotte is required.", "error")
        else:
            try:
                gestion_db.add_cagnottes(par_name=name)
                flash(f"Cagnotte {name} created.", "success")
            except Exception:
                flash(f"An error occured while creating cagnotte {name}.", "error")
    elif action == "delete_cagnotte":
        if not name:
            flash("Name of cagnotte is required.", "error")
        else:
            did = gestion_db.del_cagnottes(par_name=name)
            if did:
                flash(f"Cagnotte {name} deleted.", "success")
            else:
                flash("The cagnotte does not exist.", "error")
    elif action == "show_expenses":
        if not name:
            flash("Name of cagnotte is required.", "error")
        elif not cagnotte_exist(name):
            flash(f"The cagnotte {name} does not exist.", "error")
        elif len(gestion_db.select_one_cagnotte(name)) == 0:
            flash(f"No expenses for {name}.", "info")
        else:
            flash(f"Showing expenses for {name}.", "info")
    elif action == "solde":
        if not name:
            flash("Name of cagnotte is required.", "error")
        elif not cagnotte_exist(name):
            flash(f"The cagnotte {name} does not exist.", "error")
        elif len(gestion_db.select_one_cagnotte(name)) == 0:
            flash(f"The cagnotte {name} is empty.", "info")
        else:
            flash(f"Showing transactions for {name}.", "info")
    else:
        flash("Unknown action.", "error")

    params = {}
    if name:
        params["name"] = name
    if action == "solde":
        params["action"] = "solde"
    return redirect(url_for("home", **params))
