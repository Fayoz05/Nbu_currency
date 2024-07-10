from telebot import types


def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Курс валюты ЦБ🏦")
    btn2 = types.KeyboardButton("Курсы валют 💸")
    btn3 = types.KeyboardButton("Покупка📈")
    btn4 = types.KeyboardButton("Продажа📉")
    kb.add(btn1, btn2, btn3, btn4)
    return kb


def buy_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    usd = types.InlineKeyboardButton(text="USD🇺🇸", callback_data="USD")
    eur = types.InlineKeyboardButton(text="EUR🇪🇺", callback_data="EUR")
    rub = types.InlineKeyboardButton(text="RUB🇷🇺", callback_data="RUB")
    kzt = types.InlineKeyboardButton(text="KZT🇰🇿", callback_data="KZT")
    jpy = types.InlineKeyboardButton(text="JPY🇯🇵", callback_data="JPY")
    gbp = types.InlineKeyboardButton(text="GBP🇬🇧", callback_data="GBP")
    chf = types.InlineKeyboardButton(text="CHF🇨🇭", callback_data="CHF")
    kb.add(usd, eur, rub, kzt, jpy, gbp, chf)
    return kb


def cell_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    usd = types.InlineKeyboardButton(text="USD🇺🇸", callback_data="Доллар США")
    eur = types.InlineKeyboardButton(text="EUR🇪🇺", callback_data="Евро")
    rub = types.InlineKeyboardButton(text="RUB🇷🇺", callback_data="Российский рубль")
    kzt = types.InlineKeyboardButton(text="KZT🇰🇿", callback_data="Казахстанский тенге")
    jpy = types.InlineKeyboardButton(text="JPY🇯🇵", callback_data="Японская иена")
    gbp = types.InlineKeyboardButton(text="GBP🇬🇧", callback_data="Английский фунт стерлингов")
    chf = types.InlineKeyboardButton(text="CHF🇨🇭", callback_data="Швейцарский франк")
    kb.add(usd, eur, rub, kzt, jpy, gbp, chf)
    return kb


def currency_kb():
    currency_buttons = [
        "USD - Доллар США 🇺🇸",
        "EUR - Евро 🇪🇺",
        "JPY - Японская иена 🇯🇵",
        "KZT - Казахстанский тенге 🇰🇿",
        "KRW - Южнокорейский вон 🇰🇷",
        "PLN - Польский злотый 🇵🇱",
        "RUB - Российский рубль 🇷🇺",
        "TRY - Новая Турецкая лира 🇹🇷",
        "AED - Дирхам ОАЭ 🇦🇪",
        "UAH - Украинская гривна 🇺🇦",
        "CNY - Китайский юань 🇨🇳",
        "CAD - Канадский доллар 🇨🇦",
        "AUD - Австралийский доллар 🇦🇺",
        "CHF - Швейцарский франк 🇨🇭",
        "DKK - Датская крона 🇩🇰",
        "EGP - Египетский фунт 🇪🇬",
        "GBP - Английский фунт стерлингов 🇬🇧",
        "ISK - Исландская крона 🇮🇸",
        "KWD - Кувейтский динар 🇰🇼",
        "LBP - Ливанский фунт 🇱🇧",
        "MYR - Малайзийский ринггит 🇲🇾",
        "NOK - Норвежская крона 🇳🇴",
        "SEK - Шведская крона 🇸🇪",
        "SGD - Сингапурский доллар 🇸🇬",
    ]

    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    for button_text in currency_buttons:
        button = types.KeyboardButton(text=button_text)
        kb.add(button)
    return kb


def back_or_convert():
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    back = types.KeyboardButton("Назад🔙")
    convert = types.KeyboardButton("Конвертер💱")
    kb.add(back, convert)
    return kb


def select_value():
    kb = types.InlineKeyboardMarkup(row_width=1)
    from_uzs = types.InlineKeyboardButton("Из UZS", callback_data="from_uzs")
    to_uzs = types.InlineKeyboardButton("В UZS", callback_data="to_uzs")
    kb.add(from_uzs, to_uzs)
    return kb
