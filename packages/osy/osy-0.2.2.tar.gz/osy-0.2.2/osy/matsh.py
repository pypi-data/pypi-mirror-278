import csv
import pkg_resources


def sol(text):
    data_path = pkg_resources.resource_filename('osy', 'data/oneliner.csv')
    with open(data_path, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                task, answer = row
                if text in task:
                    print(task, "\n----\n", answer.replace(".", ".\n"))
    print(task, "\n----\n", "Ответ не найден")


def tor(text):
    data_path = pkg_resources.resource_filename('osy', 'data/onelinert.csv')
    with open(data_path, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                task, answer = row
                if text in task:
                    print(task, "\n----\n", answer.replace(".", ".\n"))
    print(task, "\n----\n", "Ответ не найден")
