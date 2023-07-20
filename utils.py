import json

from datetime import datetime

def get_data():
    with open('operations.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def get_filtered_data(data):
    # print(f"До фильтрации: { len(data) }")
    # print(f"Без ключа \"state\": {[x for x in data if 'state' not in x] }")

    data = [x for x in data if "state" in x and x["state"] == "EXECUTED"]

    # print(f"После фильтрации: { len(data) }")
    # assert False

    return data


def get_last_values(data, count_last_values):
    # def key_sort(x):
    #     return x["date"]

    # dates = '\n'.join([x['date'] for x in data][:10])
    # print(f"Даты до сортировки:\n{ dates }\n")

    data = sorted(data, key=lambda x: x["date"], reverse=True)
    # data = sorted(data, key=key_sort, reverse=True)

    # dates = '\n'.join([x['date'] for x in data][:10])
    # print(f"Даты после сортировки:\n{ dates }\n")
    # assert False

    data = data[:count_last_values]
    return data


def encode_bill_info(bill_info):
    bill_info = bill_info.split()
    bill, info = bill_info[-1], " ".join(bill_info[:-1])
    if len(bill) == 16:
        # print(f"Счет карты до: { bill }")
        bill = f"{bill[:4]} {bill[4:6]}** **** {bill[-4:]}"
        # print(f"Счет карты после: { bill }")
        # print()
        # assert(False)
    else:
        # print(f"Счет банка до: { bill }")
        bill = f"**{bill[-4:]}"
        # print(f"Счет банка после: { bill }")
        # print()
        # assert(False)

    to = f"{info} {bill}"
    return to


def get_formatted_data(data):
    formatted_data = []
    for row in data:
        # print(f"Дата: { row['date'] }")
        date = datetime.strptime(row["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        # print(f"Дата: { date }")

        description = row["description"]
        # print(f"Описание: { description }")

        if "from" in row:
            # print(f"Отправитель до: { row['from'] }")
            sender = encode_bill_info(row["from"])
            sender = f"{sender} -> "
            # print(f"Отправитель после: { sender }")
            # assert(False)
        else:
            sender = ""

        # print(f"Получатель до: { row['to'] }")
        to = encode_bill_info(row['to'])
        # print(f"Получатель после: { to }")

        operations_amount = f"{row['operationAmount']['amount']} {row['operationAmount']['currency']['name']}"

        formatted_data.append(f"""\
{date} {description}
{sender}{to}
{operations_amount}""")
    return formatted_data
