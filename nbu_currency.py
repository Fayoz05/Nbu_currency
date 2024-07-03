import telebot
import requests

bot=telebot.TeleBot('6793497603:AAEC2ZQ3uaiHafyd6lnyJIbUDvM9WRo7SWU')

@bot.message_handler(commands=['start'])
def start(message):
    user_id=message.from_user.id
    username=message.from_user.first_name
    bot.send_message(user_id,f"""Привет {username}! Это конвертер валют по курсу NBU.
Выберите валюту в которую хотите конвертировать сумму:
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
"CNY" - "Китайский юань" 🇨🇳
"DKK" - "Датская крона" 🇩🇰
"EGP" - "Египетский фунт" 🇪🇬
"GBP" - "Английский фунт стерлингов" 🇬🇧
"ISK" - "Исландская крона" 🇮🇸
"KWD" - "Кувейтский динар" 🇰🇼
"LBP" - "Ливанский фунт" 🇱🇧
"MYR" - "Малайзийский ринггит" 🇲🇾
"NOK" - "Норвежская крона" 🇳🇴
"SEK" - "Шведская крона" 🇸🇪
"SGD" - "Сингапурский доллар" 🇸🇬 """)
    bot.register_next_step_handler(message, get_currency)


def get_currency(message):
    user_id = message.from_user.id
    currency_name = message.text.upper()
    response = requests.get("https://nbu.uz/exchange-rates/json/")
    currencies = response.json()
    check_currency = [currency["code"] for currency in currencies]
    for currency in currencies:
        if currency["code"] == currency_name:
            name=currency["title"]
            value=currency["cb_price"]
            bot.send_message(user_id,f"""Мы получили курс. 1 {currency_name}={value} UZS.
Напишите сумму в UZS: """)
            bot.register_next_step_handler(message,money_convert,value,currency_name)
        if not check_currency:
            bot.send_message(user_id,"К сожалению не нашел такой этой валюты на сайте :(")

def money_convert(message,value,currency_name):
    user_id = message.from_user.id
    sum_str = message.text
    sum_float = float(sum_str)
    value_float=float(value)
    if sum_str.isdigit():
        converted_value = sum_float / value_float
        converted_value_round=round(converted_value,2)
        bot.send_message(user_id, f"Сумма в {sum_float} UZS = {converted_value_round} в {currency_name}")
    else:
        bot.send_message(user_id, "Пожалуйста, введите сумму в числах.")
        return money_convert()

bot.polling(non_stop=True)