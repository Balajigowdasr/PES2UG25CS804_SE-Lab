def mask_card_number(number):
    """
    Hides all but the last four digits of a card number.
    Handles unexpected or invalid input safely.
    """
    if number is None:
        return "*" * 12

    if not isinstance(number, str):
        number = str(number)

    digits = number.replace(" ", "").replace("-", "")

    if not digits:
        return "*" * 12

    return "*" * 12 + digits[-4:]


def parse_transaction(line):
    """
    Parses 'date,category,amount' into a (category, amount) tuple.
    Handles malformed input without crashing.
    """
    if line is None:
        return "", 0

    if not isinstance(line, str):
        line = str(line)

    parts = line.split(",")

    if len(parts) < 3:
        return "", 0

    category = parts[1].strip().lower()

    try:
        amount = int(parts[2].strip())
    except (ValueError, TypeError):
        amount = 0

    return category, amount


def parse_statement_total(text):
    """
    Reads the amount from a line such as 'Total: 12,500'.
    Handles malformed input without crashing.
    """
    if text is None:
        return 0

    if not isinstance(text, str):
        text = str(text)

    parts = text.split(":", 1)

    if len(parts) < 2:
        return 0

    amount = parts[1].strip().replace(",", "")

    try:
        return int(amount)
    except (ValueError, TypeError):
        return 0


def main():
    print("==== Running mask_card_number ====")
    value = input("Enter a card number (e.g. 4111 1111 1111 1234): ")
    print("Masked card number:", mask_card_number(value))

    print("\n==== Running parse_transaction ====")
    value = input(
        "Enter a transaction as DATE,CATEGORY,AMOUNT "
        "(e.g. 2026-11-05,dining,1550): "
    )
    print("Category and amount:", parse_transaction(value))

    print("\n==== Running parse_statement_total ====")
    value = input(
        "Enter the statement total line "
        "(e.g. Total: 12,500): "
    )
    print("Statement total:", parse_statement_total(value))


if __name__ == "__main__":
    main()