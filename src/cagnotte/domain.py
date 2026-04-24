from dataclasses import dataclass

from cagnotte.data import select_expenses
import cagnotte.data as gestion_db





@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float

    @classmethod
    def from_data(cls, row):
        return cls(row[0], row[1], row[2])

    def presentation(self) -> str:
        return (
            f"{self.sender} -> {self.receiver}: {self.amount}€"
        )


def compute_transactions(cagnotte_id: str) -> list[Transaction]:
    """
    Indicates who owes how much to whom to balance the expenses.
    Greedy settlement algorithm.
    Args:
        cagnotte_id (): The name of cagnotte to compute

    Returns:
        A list of tuple Transaction
    """
    rows = select_expenses(cagnotte_id)
    if not rows:
        return []

    total = sum(r.expense for r in rows)
    n = len(rows)
    quote_part = total / n

    # solde positif = créditeur, négatif = débiteur
    soldes = {r.person: round(r.expense - quote_part, 2) for r in rows}

    crediteurs = sorted([(v, k) for k, v in soldes.items() if v > 0], reverse=True)
    debiteurs = sorted([(- v, k) for k, v in soldes.items() if v < 0], reverse=True)

    transactions = []
    i, j = 0, 0
    while i < len(crediteurs) and j < len(debiteurs):
        credit, crediteur = crediteurs[i]
        dette, debiteur = debiteurs[j]
        montant = round(min(credit, dette), 2)
        transactions.append(Transaction.from_data((crediteur, debiteur, montant)))
        crediteurs[i] = (round(credit - montant, 2), crediteur)
        debiteurs[j] = (round(dette - montant, 2), debiteur)
        if crediteurs[i][0] == 0:
            i += 1
        if debiteurs[j][0] == 0:
            j += 1

    return transactions

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


def is_number_float(s) -> bool:
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