import telebot
from telebot import types
from config import token

bot = telebot.TeleBot(token)
score = 0
current_question = 0  # Текущий вопрос (0 - начало, 1-5 - вопросы, 6 - завершение)

questions = [
    {
        'text': "Вопрос №1. Что исчезнет быстрее из-за глобального потепления, ледники или кораллы?❄️🔥",
        'options': ["Ледники", "Кораллы"],
        'correct': "Кораллы",
        'explanation': """Кораллы исчезнут быстрее.
Почему?
Ледники тают постепенно (хотя и быстро — например, Гренландия теряет 267 млрд тонн льда в год).
Кораллы гибнут моментально из-за окисления океана и повышения температуры воды. Уже к 2050 году 90% рифов могут погибнуть (WWF).
Нюанс: Таяние ледников поднимет уровень океана, но кораллы — это экосистемы, от которых зависят 25% морских видов."""
    },
    {
        'text': "Вопрос №2. Что сильнее вредит климату за 1 поездку, автомобиль или самолет?🚗✈️",
        'options': ["🚗 Автомобиль", "✈️ Самолет"],
        'correct': "✈️ Самолет",
        'explanation': """Самолёт вреднее на дальних расстояниях.
Цифры:
Автомобиль (бензин): ~0.2 кг CO₂ на км.
Самолёт: ~0.25 кг CO₂ на км пассажира, но рейс Москва–Бангкок (~7 000 км) = 1.75 тонны CO₂ (как год вождения авто).
Нюанс: Если ехать на авто в одиночку, самолёт выгоднее. Но с пассажирами авто экологичнее"""
    },
    {
        'text': 'Вопрос №3. Что "водоёмче" и вреднее для экологии, говядина или авокадо?🥩🌱',
        'options': ["🌱 Авокадо", "🥩 Говядина"],
        'correct': "🥩 Говядина",
        'explanation': """Говядина — абсолютный «чемпион» по вреду.
Данные:
1 кг говядины = 15 000 литров воды + 27 кг CO₂ (как 160 км на авто).
1 кг авокадо = 2 000 литров воды, но из-за спроса вырубают леса (например, в Мексике).
Нюанс: Авокадо — локальная проблема, а мясная индустрия даёт 14.5% всех выбросов."""
    },
    {
        'text': 'Вопрос №4. Что было бы хуже для человечества, глобальное потепление или глобальное похолодание?🌍❄️',
        'options': ["❄️ Глобальное похолодание", "🔥 Глобальное потепление"],
        'correct': "🔥 Глобальное потепление",
        'explanation': """Потепление опаснее для современной цивилизации.
Почему?
Потепление: Экстремальные штормы, засухи, массовые миграции. Уже сейчас ущерб — $210 млрд в год (NASA).
Похолодание: Заморозки, неурожаи, но человечество пережило малый ледниковый период (XIV–XIX века).
Нюанс: Резкое похолодание (например, из-за остановки Гольфстрима) — тоже катастрофа, но менее вероятно."""
    },
    {
        'text': 'Вопрос №5. Кто главный враг климата, заводы или коровы?🏭🌳',
        'options': ["🐄 Коровы", "🏭 Заводы"],
        'correct': "🏭 Заводы",
        'explanation': """Заводы — но коровы близко.
Цифры:
Промышленность и энергетика: 30% выбросов CO₂.
Животноводство: 14% выбросов (метан от коров в 25 раз вреднее CO₂).
Нюанс: Заводы можно decarbonize (зелёная энергия), а коров — только сократить."""
    }
]

@bot.message_handler(commands=['start'])
def start(message):
    global score, current_question
    score = 0
    current_question = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Запустить викторину")
    markup.add(btn1)
    bot.send_message(message.chat.id, 
                   text=f'Привет, {message.from_user.first_name}! Тут ты можешь пройти викторину на тему глобального потепления.',
                   reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global score, current_question
    
    if message.text == "Запустить викторину" and current_question == 0:
        score = 0
        current_question = 1
        ask_question(message)
    
    elif current_question > 0 and current_question <= 5:
        if message.text in questions[current_question-1]['options']:
            check_answer(message)
        elif message.text == "📖 Узнать подробности":
            show_explanation(message)
        elif message.text == "💨 Далее":
            current_question += 1
            if current_question <= 5:
                ask_question(message)
            else:
                show_results(message)

def ask_question(message):
    question = questions[current_question-1]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in question['options']:
        markup.add(types.KeyboardButton(option))
    bot.send_message(message.chat.id, question['text'], reply_markup=markup)

def check_answer(message):
    global score
    question = questions[current_question-1]
    is_correct = message.text == question['correct']
    
    if is_correct:
        score += 1
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💨 Далее"), types.KeyboardButton("📖 Узнать подробности"))
    
    reply_text = "Правильно! ✅" if is_correct else "Неправильно! ❌"
    bot.send_message(message.chat.id, reply_text, reply_markup=markup)

def show_explanation(message):
    question = questions[current_question-1]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💨 Далее"))
    bot.send_message(message.chat.id, question['explanation'], reply_markup=markup)

def show_results(message):
    global current_question
    current_question = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Запустить викторину"))
    bot.send_message(message.chat.id, 
                   f'Молодец! Ты прошел викторину на {score} из 5.\n\nХочешь попробовать еще раз?',
                   reply_markup=markup)

bot.polling(none_stop=True)