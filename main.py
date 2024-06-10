def input_data():
    """Gets people and amount data for all users in form of a dictionary"""
    all_names_entered = False
    data = {}
    while not all_names_entered:
        text = input()
        text = text.split("-")
        name = text[0]
        if len(text) == 2:
            paid = float(text[1])
        else:
            paid = 0.0

        if name == "!calc":
            all_names_entered = True
        elif name not in data:
            data.update({name: paid})
        else:
            print(f"Ya hay una persona llamada {name}. Introduce un nombre distinto.")
    return data


def resolve_debts():
    """Resolves the debts and provides a dictionary in which the keys are the people who pay and the values are a
    list of tuples containing (name_to_receive, amount)"""
    results = {}
    for name_payer, amount_payer in people_to_pay.items():
        results.update({name_payer: []})
        paid = False
        for name_receiver, amount_receiver in people_to_receive.items():
            if amount_receiver != 0:
                if amount_payer <= amount_receiver:
                    results[name_payer].append((name_receiver, round(amount_payer, 2)))
                    people_to_receive[name_receiver] -= amount_payer
                    paid = True
                else:
                    results[name_payer].append((name_receiver, round(amount_receiver, 2)))
                    amount_payer -= amount_receiver
                    people_to_receive[name_receiver] -= amount_receiver
            if paid:
                break
    return results


print("Introduce el nombre de las personas y el importe que han pagado en el siguiente formato: nombre-importe")
print("Introduce solo el nombre para quienes no hayan pagado nada.")
print("Cuando hayas terminado de introducir nombres, introduce !calc")

user_data = input_data()

# Modify the user data so that each person has the amount to receive (positive values) or to pay (negative values)
total_amount = sum(user_data.values())
amount_each = total_amount / len(user_data)
user_data = {key:round(value - amount_each, 2) for key, value in user_data.items()}

# Split the people in two lists, people_to_receive and people_to_pay
people_to_receive = {name:amount for name, amount in user_data.items() if amount >= 0}
people_to_pay = {name:abs(amount) for name, amount in user_data.items() if amount < 0}

# Print amounts to receive
print()
for name, amount in people_to_receive.items():
    print(f"{name} recibirá {amount:.2f}€.")

results = resolve_debts()

# Print amounts to pay
print()
for name, to_pay in results.items():
    print(f"{name} paga ", end="")
    times_to_pay = len(to_pay)
    counter = 1
    for name_receiver, amount in to_pay:
        if counter == 1:
            print(f"{amount:.2f}€ a {name_receiver}", end="")
            counter += 1
        elif counter != times_to_pay:
            print(f", {amount:.2f}€ a {name_receiver}", end="")
            counter += 1
        else:
            print(f" y {amount:.2f}€ a {name_receiver}", end="")
    print(".")
