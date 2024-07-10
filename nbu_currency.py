import telebot
import requests
from telebot import types
import buttons as bt
import pandas as pd

bot = telebot.TeleBot('6793497603:AAEC2ZQ3uaiHafyd6lnyJIbUDvM9WRo7SWU')

list1 = ["USD", "EUR", "RUB", "KZT", "JPY", "GBP", "CHF"]
list2 = ["Доллар США", "Евро", "Российский рубль", "Казахстанский тенге", "Японская иена", "Английский фунт стерлингов",
         "Швейцарский франк"]
list3 = ["USD", "EUR", "RUB", "KZT", "JPY"]

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    bot.send_message(user_id, f"""Привет {username}! Это бот привязанный к курсу валют по курсу NBU.
Выберите действие:""", reply_markup=bt.main_kb())


def send_currencies_info(message):
    try:
        info = get_currencies_info()
        bot.send_message(message.chat.id, f"<pre>{info}</pre>", parse_mode='HTML')
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=bt.main_kb())
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=bt.main_kb())


def get_currency(message):
    user_id = message.from_user.id
    currency_name = message.text[:3].upper()
    response = requests.get("https://nbu.uz/exchange-rates/json/")
    currencies = response.json()
    check_currency = [currency["code"] for currency in currencies]

    if currency_name in check_currency:
        for currency in currencies:
            if currency["code"] == currency_name:
                name = currency["title"]
                value = currency["cb_price"]
                user_data[user_id] = {'currency_name': currency_name, 'value': value}
                bot.send_message(user_id, f"Мы получили курс: 1 {currency_name} = {value} UZS.",
                                 reply_markup=bt.back_or_convert())
                bot.register_next_step_handler(message, handle_back_or_convert)
                break
    else:
        bot.send_message(user_id, "К сожалению, не нашел такой валюты на сайте.")

def handle_back_or_convert(message):
    user_id = message.from_user.id
    if message.text == "Конвертер💱":
        bot.send_message(user_id, "Выберите направление конвертации:", reply_markup=bt.select_value())
    elif message.text == "Назад🔙":
        bot.send_message(user_id, "Выберите действие:", reply_markup=bt.main_kb())


def handle_conversion(message, direction):
    user_id = message.from_user.id
    sum_str = message.text
    currency_name = user_data[user_id]['currency_name']
    value = user_data[user_id]['value']

    try:
        sum_float = float(sum_str)
        value_float = float(value)

        if direction == "from_uzs":
            converted_value = sum_float / value_float
        elif direction == "to_uzs":
            converted_value = sum_float * value_float

        converted_value_round = round(converted_value, 2)
        if direction == "from_uzs":
            bot.send_message(user_id, f"Сумма в {sum_float} UZS = {converted_value_round} в {currency_name}")
            bot.send_message(user_id, "Выберите действие:", reply_markup=bt.main_kb())
        elif direction == "to_uzs":
            bot.send_message(user_id, f"Сумма в {sum_float} {currency_name} = {converted_value_round} UZS")
            bot.send_message(user_id, "Выберите действие:", reply_markup=bt.main_kb())

    except ValueError:
        bot.send_message(user_id, "Пожалуйста, введите сумму в числах или в десятичных (Например: 0.1) ")
        bot.register_next_step_handler(message, lambda msg: handle_conversion(msg, direction))


@bot.message_handler(content_types=['text'])
def main_menu(message):
    user_id = message.from_user.id
    if message.text == "Курс валюты ЦБ🏦":
        bot.send_message(user_id, f"""Выберите валюту, чтобы узнать ее курс ЦБ:
"USD" - "Доллар США" 🇺🇸
"EUR" - "Евро" 🇪🇺
"JPY" - "Японская иена" 🇯🇵
"KZT" - "Казахстанский тенге" 🇰🇿
"KRW" - "Южнокорейский вон" 🇰🇷
"PLN" - "Польский злотый" 🇵🇱
"RUB" - "Российский рубль" 🇷🇺
"TRY" - "Новая Турецкая лира" 🇹🇷
"AED" - "Дирхам ОАЭ" 🇦🇪
"UAH" - "Украинская гривна" 🇺🇦
"CNY" - "Китайский юань" 🇨🇳
"CAD" - "Канадский доллар" 🇨🇦
"AUD" - "Австралийский доллар" 🇦🇺
"CHF" - "Швейцарский франк" 🇨🇭
"DKK" - "Датская крона" 🇩🇰
"EGP" - "Египетский фунт" 🇪🇬
"GBP" - "Английский фунт стерлингов" 🇬🇧
"ISK" - "Исландская крона" 🇮🇸
"KWD" - "Кувейтский динар" 🇰🇼
"LBP" - "Ливанский фунт" 🇱🇧
"MYR" - "Малайзийский ринггит" 🇲🇾
"NOK" - "Норвежская крона" 🇳🇴
"SEK" - "Шведская крона" 🇸🇪
"SGD" - "Сингапурский доллар" 🇸🇬 """, reply_markup=bt.currency_kb())
        bot.register_next_step_handler(message, get_currency)
    elif message.text == "Курсы валют 💸":
        send_currencies_info(message)
    elif message.text == "Покупка📈":
        bot.send_message(user_id, "Выберите валюту:", reply_markup=bt.buy_kb())
    elif message.text == "Продажа📉":
        bot.send_message(user_id, "Выберите валюту:", reply_markup=bt.cell_kb())


def get_currencies_info():
    data = []
    date = ""

    response = requests.get("https://nbu.uz/exchange-rates/json/")
    currency_list = response.json()

    for currency in currency_list:
        if currency["code"] in list3:
            title = currency["title"]
            nbu_cell_price = currency["nbu_cell_price"] if currency["nbu_cell_price"] is not None else "N/A"
            nbu_buy_price = currency["nbu_buy_price"] if currency["nbu_buy_price"] is not None else "N/A"
            data.append([title, nbu_cell_price, nbu_buy_price])
            date = currency["date"]

    df = pd.DataFrame(data, columns=["Валюта ", "Покупка", "Продажа"])
    df["Продажа"] = pd.to_numeric(df["Продажа"], errors='coerce')
    df = df.sort_values(by="Продажа", ascending=False)

    result = ""
    result += f"{'Валюта':^20} {'Покупка':^10} {' Продажа':^10}\n"
    result += "-" * 43 + "\n"

    for _, row in df.iterrows():
        title, nbu_cell_price, nbu_buy_price = row
        result += f"{title:^20} {nbu_cell_price:^11} {nbu_buy_price:^10}\n"

    result += "\nДата изменения курса: " + date
    return result



@bot.callback_query_handler(func=lambda call: call.data in list1)
def get_buy_currency(call):
    user_id = call.from_user.id
    response = requests.get("https://nbu.uz/exchange-rates/json/")
    currencies = response.json()
    check_currency = [currency["code"] for currency in currencies]

    if call.data in check_currency:
        for currency in currencies:
            if currency["code"] == call.data:
                bot.delete_message(user_id, call.message.message_id)
                name = currency["title"]
                value = currency["nbu_cell_price"]
                bot.send_message(user_id, f"""Мы получили курс покупки.
1 {name} = {value} UZS.""")
                bot.send_message(user_id, "Выберите действие:", reply_markup=bt.main_kb())
                break
    else:
        bot.send_message(user_id, "К сожалению не нашел такой валюты на сайте :(")


@bot.callback_query_handler(func=lambda call: call.data in list2)
def get_cell_currency(call):
    user_id = call.from_user.id
    response = requests.get("https://nbu.uz/exchange-rates/json/")
    currencies = response.json()
    check_currency = [currency["title"] for currency in currencies]

    if call.data in check_currency:
        for currency in currencies:
            if currency["title"] == call.data:
                bot.delete_message(user_id, call.message.message_id)
                name = currency["title"]
                value = currency["nbu_buy_price"]
                bot.send_message(user_id, f"""Мы получили курс продажи.
1 {name} = {value} UZS.""")
                bot.send_message(user_id, "Выберите действие:", reply_markup=bt.main_kb())
                break
    else:
        bot.send_message(user_id, "К сожалению не нашел такой валюты на сайте :(")


@bot.callback_query_handler(func=lambda call: call.data in ["from_uzs", "to_uzs"])
def handle_conversion_direction(call):
    user_id = call.from_user.id
    direction = call.data
    bot.send_message(user_id, "Пожалуйста, введите сумму:")
    bot.register_next_step_handler(call.message, lambda msg: handle_conversion(msg, direction))
    bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=None)


if __name__ == '__main__':
    bot.polling(non_stop=True)
