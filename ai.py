import openai
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

openai.api_key = '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'


def generate_present(context, role, max_budget, num_of_ideas):
    if num_of_ideas > 5:
        print("The number of ideas cannot exceed 5")
        return -1
    if num_of_ideas < 1:
        print("The number of ideas must be more than 1")
        return -1
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "system", "content": "Ты полезный ассистент, идеально подбирает подарки по предпочтения."},
        {"role": "assistant", "content": f"Учти, {role} любит {context}."},
        {"role": "user", "content": f"Учитывая эти предпочтения,"
                                    f" выдай {num_of_ideas} идей подарка в двух-трех словах для {role} стоимостью до {max_budget} рублей,"
                                    f" который можно купить в любом интернет-магазине. Выведи их , пронумеровав по порядку"}
    ])
    recommendation = completion.choices[0].message.content
    return recommendation.split('\n')


def link_to_market(string, min_budg, max_budg):
    request_value = string.split()
    request_value.pop(0)
    link = "https://www.wildberries.ru/catalog/0/search.aspx?search="
    for q in request_value:
        link += "%20" + q
    if link[-1] == '.':
        link = link[:-1]
    link += f"&priceU={min_budg}00%3B{max_budg}00"
    return link


def title_with_link_test(context, role, max_budget, num_of_ideas, min_budg):
    response = generate_present(context, role, max_budget, num_of_ideas)
    for link in response:
        print(link, ": ", link_to_market(link, min_budg, max_budget), "\n")


def title_with_link(context, role, max_budget, num_of_ideas, min_budg):
    response = generate_present(context, role, max_budget, num_of_ideas)
    for link in response:
        return link, link_to_market(link, min_budg, max_budget)



# title_with_link_test("машины, игрушки", "друг", 5000, 3, 1500)
