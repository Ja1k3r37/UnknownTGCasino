import logging
from aiogram import Bot, Dispatcher, executor, types
import config 
from referaldb import DataBase
from telebot import types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
import sqlite3
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import random
from aiogram.types import InputFile

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase('last.sqlite3')
conn = sqlite3.connect('last.sqlite3')
class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()



knopka_one = KeyboardButton('/Mamonts_For_Admin')
knopka_two = KeyboardButton('/Scammers_For_Admin')
knopka_three = KeyboardButton('/Scammers_For_Admin')

keyboard_admin = ReplyKeyboardMarkup()

keyboard_admin.add(knopka_one).add(knopka_two).add(knopka_three) #Админ Клавиатура

buttons_list = ['button_1', 'button_2', 'button_3', 'button_4', 'button_5', 'button_6', 'button_7', 'button_8', 'button_9', 'button_10',
                'button_11', 'button_12', 'button_13', 'button_14', 'button_15']

group_of_mamonts = []
test_list = []

Play = InlineKeyboardButton(text='🎰Играть', callback_data='Play')
Bank = InlineKeyboardButton(text='🏦Личный Кабинет', callback_data='Bank')
Support = InlineKeyboardButton(text='👨‍💻Поддержка', callback_data='Support')
Information = InlineKeyboardButton(text='ℹ️Информация', callback_data='Information')
Popolnenie = InlineKeyboardButton(text='📥Пополнить', callback_data='POPOLNENIE')
Vivod = InlineKeyboardButton(text='📤Вывести', callback_data='VIVOD')


start_keyboard = InlineKeyboardMarkup(row_width=2)
start_keyboard.row(Play, Bank)
start_keyboard.row(Support, Information)
start_keyboard.row(Popolnenie, Vivod)
class user(StatesGroup):
    answer = State()
    mamont_id = State()
    mamont_money = State()
    win_or_lose = State()
    amount_qiwi_money = State()
    summa_stavki = State()
    numbers_percent = State()
    summa_stavki2 = State()
    vivod_card = State()
    summa_vivoda = State()
    summa_popolnenie = State()
class MyStates(StatesGroup):
    state1 = State()

@dp.message_handler(commands=['start', 'меню'])
async def start(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            pass
            start_command = message.text
            referrer_id = str(start_command[7:])
            if str(referrer_id) != "":
                if str(referrer_id) != str(message.from_user.id):
                    db.add_user(message.from_user.id, referrer_id)
                    try:
                        await bot.send_message(referrer_id, f"По вашей ссылке зарегестрировался <b>новый пользователь</b> - {message.from_user.username}", parse_mode='html')
                    except:
                        pass
                else:
                    await bot.send_message(message.from_user.id, f'По собственной ссылке регистрация не оформляется')
            else:
                db.add_user(message.from_user.id)
        db.start_message(message.from_user.id)
        with open('image.jpg', 'rb') as photo:
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🎰 Добро пожаловать в FonBet Casino 🎰\n\n 👨‍💻 Поддержка: @ijustwait\n\n<b>Для управления меню используйте клавиатуру</b>", parse_mode='html', reply_markup=start_keyboard)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, f'Напишите команду /start <b>{message.from_user.username}</b>', parse_mode='html')



@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Профиль в ворк панели':
            try:
                await bot.send_message(message.from_user.id, f"ID: {message.from_user.id}\n https://t.me/{config.BOT_NICKNAME}?start={message.from_user.id}\n Количество рефералов: {db.count_referals(message.from_user.id)}")
            except Exception as e: print(e)
      
        if message.text == 'Федеральная система':
             sqlite_connection = sqlite3.connect('last.sqlite3')
             cursor = sqlite_connection.cursor()
             sqlite_select_query = f"""SELECT user_id, refferer_money FROM users WHERE referrer_id = {message.from_user.id}"""
             cursor.execute(sqlite_select_query)
             records = cursor.fetchall()
             
             
             main_menuuu = ReplyKeyboardMarkup(row_width=3)
             for row in records:
                    
                    knopochka = row[0]
                    try:
                        test_button = KeyboardButton(knopochka)
                        test_list.append(str(knopochka))
                        main_menuuu.add(test_button)
                        group_of_mamonts.append(test_button)
                        
                    except Exception as e: await bot.send_message(message.from_user.id, f'Ошибка - {e}')
             print(test_list)
             await bot.send_message(message.from_user.id, f"Ваши мамонты:", reply_markup=main_menuuu)

        if message.text in test_list:
            sqlite_connection = sqlite3.connect('last.sqlite3')
            cursor = sqlite_connection.cursor()
            sqlite_select_query = f"""SELECT user_id, refferer_money FROM users WHERE referrer_id = {message.from_user.id}"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            number_of_mamont = message.text
            sqlite_select_query = f"""SELECT refferer_money FROM users WHERE referrer_id = {message.from_user.id} AND user_id = {message.text}"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print(records)
            await bot.send_message(message.from_user.id, f"ID Мамонта - `{number_of_mamont}`", parse_mode='MARKDOWN')
            await bot.send_message(message.from_user.id, f"Баланс этого мамонта - {records[0][0]}")
            await message.answer("Будете менять баланс мамонта? ДА\НЕТ")
            await user.answer.set()
            

@dp.message_handler(state=user.answer)
async def get_answer(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    await user.next()
    if data['answer'] == 'ДА':
        await message.answer("Введите id мамонта: ")
        await user.mamont_id.set()
    else:
        try:
            sqlite_connection.close()
        except:
            await state.finish()
            await returnim(message)


@dp.message_handler(state=user.mamont_id)
async def get_id(message: types.Message, state: FSMContext):
        await state.update_data(mamont_id=message.text)
        data = await state.get_data()
        sqlite_connection = sqlite3.connect('last.sqlite3')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = f"""SELECT refferer_money FROM users WHERE referrer_id = {message.from_user.id} AND user_id = {data['mamont_id']}"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        await bot.send_message(message.from_user.id, f"{records}")# ВЫВОДИМ ДВУМЯ МАССИВАМИ
        await bot.send_message(message.from_user.id, f"{records[0][0]}") # ВЫВОД ЧИСТОГО ЧИСЛА
        await message.answer("Введите новый баланс мамонта: ")
        await user.mamont_money.set()

@dp.message_handler(state=user.mamont_money)
async def DA_yaujehz(message: types.Message, state: FSMContext):
    await state.update_data(mamont_money=message.text)
    data = await state.get_data()
    sqlite_connection = sqlite3.connect('last.sqlite3')
    
    db.change_balance(data['mamont_id'], message.from_user.id, data['mamont_money'])
    print(f"{data['mamont_money']}")
    print(f" {message.from_user.id}")
    print(f"{data['mamont_id']}")
    await bot.send_message(message.from_user.id, f"Баланс мамонта с <b>ID {data['mamont_id']}</b> был успешно изменен на <b>{data['mamont_money']}</b>", parse_mode='html')
    await message.answer('Если хотите, что бы мамонт проигрывал - Введите 0 \n Для выигрышей мамонта - Введите 1')
    await user.win_or_lose.set()

@dp.message_handler(state=user.win_or_lose)
async def win_or_lose(message: types.Message, state: FSMContext):
    await state.update_data(win_or_lose=message.text)
    data = await state.get_data()
    print(message.from_user.id, data['mamont_id'], data['win_or_lose'])
    db.change_win_upd(data['win_or_lose'], data['mamont_id'], message.from_user.id)
    db.change_win(message.from_user.id)
    if data['win_or_lose'] == '1':
        await bot.send_message(message.from_user.id, f"Информация о <b>мамонте</b>: \n Баланс: {data['mamont_money']}\nВыигрыш мамонта: <b>True</b>", parse_mode='html')
        await bot.send_message(message.from_user.id, f"Информация о <b>мамонте</b>: \n Баланс: {data['mamont_money']}\nВыигрыш мамонта: {db.change_win(data['mamont_id'], message.from_user.id)[0][0]}", parse_mode='html')
    else:
        await bot.send_message(message.from_user.id, f"Информация о <b>мамонте</b>: \n Баланс: {data['mamont_money']}\nВыигрыш мамонта: <b>False</b>", parse_mode='html')
    await state.finish()
    return 'Hello world'
    


@dp.message_handler(commands=['returnim'])
async def returnim(message: types.Message):
    await bot.send_message(message.from_user.id, 'Возвращаемся в меню!', parse_mode='html')

@dp.callback_query_handler(text='Bank')
async def Bank(message: types.Message):
    back_button = InlineKeyboardButton(text='🔙Назад', callback_data='startingg')
    back_kb = InlineKeyboardMarkup()
    back_kb.add(back_button)
    with open('kabinet.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f"🏦 Личный кабинет\n\n 💼 Пользователь: <b>{message.from_user.username}</b>\n╠ Пользовательский ID: <b>{message.from_user.id}</b>\n\n 💵 Баланс: <b>{db.show_balance(message.from_user.id)[0][0]} RUB</b>", parse_mode='html', reply_markup=back_kb)


@dp.callback_query_handler(text='Support')
async def Support(message: types.Message):
    back_button = InlineKeyboardButton(text='🔙Назад', callback_data='startingg')
    back_kb = InlineKeyboardMarkup()
    back_kb.add(back_button)
    with open('support.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f"👨‍💻 Актуальные и единственные контакты поддержки:\n @ijustwait\n\n📚 Правила общения с тех. поддержкой:\n\n➕ Общайтесь вежливо, по ту сторону сидит такой же живой человек, как и Вы.\n\n➕ Старайтесь формулировать обращение к поддержке емко и лаконично, в одно сообщение.\n\n➕ Обращаться в поддержку только по существу.\n\n\➕ Флуд, спам, оскорбления, клевета крается блокировкой и аннулированием игрового счета.", reply_markup=back_kb)

@dp.callback_query_handler(text='VIVESTI')
async def VIVESTI(message: types.Message):
    button_start = KeyboardButton("/start", callback_data='start')
    VIVESTI_keyboard = ReplyKeyboardMarkup()
    VIVESTI_keyboard.add(button_start)
    await bot.send_message(message.from_user.id, f"💵 На вашем счету: <b>{db.show_balance(message.from_user.id)[0][0]} RUB</b>\n💵 Минимальное для вывода: <b>5000 RUB</b>",parse_mode='html', reply_markup=VIVESTI_keyboard)

@dp.callback_query_handler(text='SETTINGS')
async def SETTINGS(message: types.Message):
    change_language = InlineKeyboardButton("🇷🇺 Выбор языка", callback_data='change_language')
    change_language_k = InlineKeyboardMarkup()
    change_language_k.add(change_language)
    await bot.send_message(message.from_user.id, "🔨Настройки бота", reply_markup=change_language_k)

@dp.callback_query_handler(text='Information')
async def Information(message: types.Message):
    back_button = InlineKeyboardButton(text='🔙Назад', callback_data='startingg')
    back_kb = InlineKeyboardMarkup()
    back_kb.add(back_button)
    with open('information.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f"🌍 *Текущий онлайн*: `{random.randint(2000, 2500)}` пользователей\n\n🔥 *Последний выигрыш*  : `{random.randint(2000, 10000)}` RUB\n\n📤 *Последний вывод*:  `{random.randint(300, 7000)}` RUB\n ╚ *Верификация*: `{random.choice(['Partial', 'Missing', 'Complete'])}`", parse_mode='MARKDOWN', reply_markup=back_kb)

@dp.callback_query_handler(text='change_language')
async def change_language(message: types.Message):
    await bot.send_message(message.from_user.id, "Язык <b>успешно изменен</b> на <b>RU</b>🇷🇺", parse_mode='html')



@dp.callback_query_handler(text='Play')
async def Play(message: types.Message):
    numbers = InlineKeyboardButton(text='🔢 Числа', callback_data='numbers')
    dice = InlineKeyboardButton(text='🎲 Кости', callback_data='dice')
    back_button = InlineKeyboardButton(text='🔙Назад', callback_data='startingg')
    play_kb = InlineKeyboardMarkup()
    play_kb.row(numbers)
    play_kb.row(dice, back_button)
    await bot.send_message(message.from_user.id, "🎰 <b>Выберите интересующую Вас игру:</b>", parse_mode='html', reply_markup=play_kb)

@dp.callback_query_handler(text='startingg')
async def startingg(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите команду /start для *возвращения в меню*", parse_mode='MARKDOWN')


@dp.callback_query_handler(text='numbers')
async def numbers(message: types.Message):
    await bot.send_message(message.from_user.id, f"Введите сумму ставки 🔥\nВаш баланс: *{db.show_balance(message.from_user.id)[0][0]} RUB*\n Для выхода в меню напишите `любой символ`", parse_mode='MARKDOWN')
    await message.answer(f"Введите сумму ставки 🔥\nВаш баланс: {db.show_balance(message.from_user.id)[0][0]} RUB")
    await user.summa_stavki.set()
            

@dp.message_handler(state=user.summa_stavki)
async def get_summa_stavki(message: types.Message, state: FSMContext):
    try:
        await state.update_data(summa_stavki=int(message.text))
        data = await state.get_data()
    except Exception as e:
        await bot.send_message(message.from_user.id, "Вы ввели недопустимый формат")
        await state.finish()
        print(f"{e} И ОШИБКА НА 289 СТРОКЕ")

    back_button = InlineKeyboardButton(text='🔙Назад', callback_data='startingg')
    back_kb = InlineKeyboardMarkup()
    back_kb.add(back_button)
    try:
        mamont_balance = db.show_balance(message.from_user.id)[0][0]
        await bot.send_message(message.from_user.id, f"Ваш баланс: {mamont_balance}")
        data['summa_stavki'] = int(data['summa_stavki'])
        sum = int(data['summa_stavki'])
        if sum <= 0:
            await bot.send_message(message.from_user.id, f"*Некорректное значение* ставки!", reply_markup=back_kb)
            await state.finish()
            return "Hello world :D"
        if sum > int(mamont_balance):
            await bot.send_message(message.from_user.id, f"Ваш *баланс меньше* суммы ставки!", eply_markup=back_kb)
            return "HELLO WORLD :D"
        if int(mamont_balance) > sum:
            bolwe_50 = KeyboardButton(">50")
            menwe_50 = KeyboardButton("<50")
            chislo_50 = KeyboardButton("=50")
            back_button = KeyboardButton('/меню')
            greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(bolwe_50).add(menwe_50).add(chislo_50)
            greet_kb1.add(back_button)

            await bot.send_message(message.from_user.id, f"Сейчас выпадет рандомное число от 1 до 99\n\nВыберите исход события ⭐️\n\n*<50 - x2*\n*=50 - x10*\n* >50 - x2*", reply_markup=greet_kb1, parse_mode='MARKDOWN')
            await message.answer("Выберите число на клавиатуре: ")
            await user.numbers_percent.set()
    except Exception as e:
        print(e, "ошибка на 306 строке")
        await bot.send_message(message.from_user.id, f"Введите команду /start для выхода в меню")
@dp.message_handler(state=user.numbers_percent)
async def get_summa_stavki(message: types.Message, state: FSMContext):
    await state.update_data(numbers_percent=message.text)
    data = await state.get_data()
    try:
        if data['numbers_percent'] != '>50' and data['numbers_percent'] != '<50' and data['numbers_percent'] != '=50': #Когда пользователь ввел невалидное число
            await bot.send_message(message.from_user.id, f"Вы ввели *неверный процент*! Вернитесь в меню командой /start\n\n\n{data['numbers_percent']}", parse_mode='MARKDOWN')
            await state.finish() 
        elif data['numbers_percent'] == '>50' and db.change_win(message.from_user.id)[0][0] == 1:
            await bot.send_message(message.from_user.id, f"Вы победили! 🍀 Выпало число - *{random.randint(51, 100)}*", parse_mode='MARKDOWN')
            db.change_balance_plus(data['summa_stavki']*2, message.from_user.id)
            await bot.send_message(message.from_user.id, f"Текущий баланс: *{db.show_balance(message.from_user.id)[0][0]}RUB*", parse_mode='MARKDOWN')
            await state.finish()
        elif data['numbers_percent'] == '>50' and db.change_win(message.from_user.id)[0][0] == 0:
            await bot.send_message(message.from_user.id, f"Вы проиграли! 🛑 Выпало число - *{random.randint(1, 50)}*", parse_mode='MARKDOWN')
            db.change_balance_minus(data['summa_stavki'], message.from_user.id)
            await bot.send_message(message.from_user.id, f"Текущий баланс: *{db.show_balance(message.from_user.id)[0][0]} RUB*", parse_mode='MARKDOWN')
            await state.finish()
        elif data['numbers_percent'] == '=50' and db.change_win(message.from_user.id)[0][0] == 1:
            await bot.send_message(message.from_user.id, "Вы победили! 🍀 Выпало число - *50*", parse_mode='MARKDOWN')
            db.change_balance_plus(data['summa_stavki']*10, message.from_user.id)
            await bot.send_message(message.from_user.id, f"Текущий баланс: *{db.show_balance(message.from_user.id)[0][0]}RUB*", parse_mode='MARKDOWN')
            await state.finish()
        elif data['numbers_percent'] == '=50' and db.change_win(message.from_user.id)[0][0] == 0:
            await bot.send_message(message.from_user.id, f"Вы проиграли! 🛑 Выпало число - *{random.randint(1, 50)}*", parse_mode='MARKDOWN')
            db.change_balance_minus(data['summa_stavki'], message.from_user.id)
            await bot.send_message(message.from_user.id, f"Текущий баланс: *{db.show_balance(message.from_user.id)[0][0]}RUB*", parse_mode='MARKDOWN')
            await state.finish()
        elif data['numbers_percent'] == '<50' and db.change_win(message.from_user.id)[0][0] == 0:
            await bot.send_message(message.from_user.id, f"Вы проиграли! 🛑 Выпало число - *{random.randint(50, 100)}*", parse_mode='MARKDOWN')
            db.change_balance_minus(data['summa_stavki'], message.from_user.id)
            await bot.send_message(message.from_user.id, f"Текущий баланс: *{db.show_balance(message.from_user.id)[0][0]}RUB*", parse_mode='MARKDOWN')
            await state.finish()
        elif data['numbers_percent'] == '<50' and db.change_win(message.from_user.id)[0][0] == 1:
            await bot.send_message(message.from_user.id, f"Вы победили! 🍀 Выпало число - *{random.randint(0, 50)}*", parse_mode='MARKDOWN')
            db.change_balance_plus(data['summa_stavki']*2, message.from_user.id)
            await bot.send_message(message.from_user.id, f"Текущий баланс: *{db.show_balance(message.from_user.id)[0][0]}RUB*", parse_mode='MARKDOWN')
            await state.finish()
        else:
            print(type(db.change_win(message.from_user.id)[0][0]))
            await bot.send_message(message.from_user.id, f"Так вот сука\n {data['numbers_percent']}\n {db.change_win(message.from_user.id)[0][0]}", parse_mode='MARKDOWN')
            await state.finish()
    except Exception as e:
        print(e)
        
@dp.callback_query_handler(text='dice')
async def dice(message: types.Message):
    await bot.send_message(message.from_user.id, f"Введите сумму ставки 🔥\nВаш баланс: *{db.show_balance(message.from_user.id)[0][0]} RUB*\n Для выхода в меню напишите `любой символ`", parse_mode='MARKDOWN')
    await message.answer(f"Введите сумму ставки 🔥\nВаш баланс: {db.show_balance(message.from_user.id)[0][0]} RUB")
    await user.summa_stavki2.set()

@dp.message_handler(state=user.summa_stavki2)
async def get_summa_stavki2(message: types.Message, state: FSMContext):
    try:
        await state.update_data(summa_stavki2=int(message.text))
        data = await state.get_data()
        await bot.send_message(message.from_user.id, f"Ваш баланс {db.show_balance(message.from_user.id)}")
    except:
        await bot.send_message(message.from_user.id, f"Вернитесь в меню командой /start")
        await state.finish()
        return "Hello world"
    print(db.show_balance(message.from_user.id)[0][0])
    if db.show_balance(message.from_user.id)[0][0] <=0:
        await bot.send_message(message.from_user.id, "Ваш баланс *недостаточен для* игры!\nВернитесь в меню командой /start", parse_mode='MARKDOWN')
        await state.finish()
    if data['summa_stavki2'] > db.show_balance(message.from_user.id)[0][0]:
        await bot.send_message(message.from_user.id, "Ваш баланс *меньше суммы* ставки! \nВернитесь в меню командой /start", parse_mode='MARKDOWN')
        await state.finish()
        return "HELLO WORLD"
    if db.change_win(message.from_user.id)[0][0] == 1:
        a = random.randint(5,6)
        if a == 6:
            await bot.send_animation(chat_id=message.from_user.id, animation=InputFile('dice/6.tgs'))
        elif a == 5:
            await bot.send_animation(chat_id=message.from_user.id, animation=InputFile('dice/5.tgs'))
        await bot.send_animation(chat_id=message.from_user.id, animation=InputFile('dice/1.tgs'))
        await bot.send_message(message.from_user.id, f"💚 Вы победили!\n Ваше число - *{a}*, число бота - *1*", parse_mode='MARKDOWN')
        db.change_balance_plus(data['summa_stavki2']*2, message.from_user.id)
        await bot.send_message(message.from_user.id, f"Текущий баланс: *{db.show_balance(message.from_user.id)[0][0]}RUB*", parse_mode='MARKDOWN')
        await state.finish()
    if db.change_win(message.from_user.id)[0][0] == 0:
        a = random.randint(5,6)
        b = random.randint(1,4)
        if a == 6:
            await bot.send_animation(chat_id=message.from_user.id, animation=InputFile('dice/6.tgs'))
        elif a == 5:
            await bot.send_animation(chat_id=message.from_user.id, animation=InputFile('dice/5.tgs'))
        await bot.send_animation(chat_id=message.from_user.id, animation=InputFile(f'dice/{b}.tgs'))
        await bot.send_message(message.from_user.id, f"🤍 Вы проиграли!\n Ваше число - *{b}*", parse_mode='MARKDOWN')
        db.change_balance_minus(data['summa_stavki2'], message.from_user.id)
        await bot.send_message(message.from_user.id, f"Текущий баланс: *{db.show_balance(message.from_user.id)[0][0]}RUB*", parse_mode='MARKDOWN')
        await state.finish()

@dp.callback_query_handler(text='VIVOD')
async def VIVOD(message: types.Message):
    await bot.send_message(message.from_user.id, f"📤 *Введите реквизиты для вывода:*\n 💳 Вывод возможен только на те реквизиты, с которых пополнялся Ваш баланс!", parse_mode='MARKDOWN')
    await message.answer(f"📤 *Введите реквизиты для вывода:*\n 💳 Вывод возможен только на те реквизиты, с которых пополнялся Ваш баланс!")
    await user.vivod_card.set()

@dp.message_handler(state=user.vivod_card)
async def vivod_card(message: types.Message, state: FSMContext):
    try:
        await state.update_data(vivod_card=int(message.text))
        data = await state.get_data()
    except:
        await bot.send_message(message.from_user.id, f"Вы ввели неверное значение для реквизитов")
        await state.finish()
    if len(str(data['vivod_card'])) != 11:
        await bot.send_message(message.from_user.id, f"*Введите корректный номер.*", reply_markup='MARKDOWN')
        await state.finish()
    if len(str(data['vivod_card'])) == 11 and str(data['vivod_card']) != '79196305107':
        await bot.send_message(message.from_user.id, f"🛠️ Вывод возможен только на те QIWI кошельки или карты, с которых *пополнялся ваш баланс!*\n⚠️ Обратитесь в Тех. Поддержку: @ijustwait", parse_mode='MARKDOWN')
        await state.finish()
    if len(str(data['vivod_card'])) == 11 and str(data['vivod_card']) == '79196305107':
        await message.answer(f"📤 Введите сумму вывода💳:")
        await user.summa_vivoda.set()
@dp.message_handler(state=user.summa_vivoda)
async def summa_vivoda(message: types.Message, state: FSMContext):
    await state.update_data(summa_vivoda=int(message.text))
    data = await state.get_data()
    if db.show_balance(message.from_user.id)[0][0] < int(data['summa_vivoda']):
        await bot.send_message(message.from_user.id, f"На вашем балансе *недостаточно средств* для вывода\n Ваш баланс: `{db.show_balance(message.from_user.id)[0][0]}`*RUB*\n Вы пытаетесь вывести: {data['summa_vivoda']}", parse_mode='MARKDOWN')
        await state.finish()
    else:
        db.withdrawals(data['summa_vivoda'], message.from_user.id)
        await bot.send_message(message.from_user.id, f"Ваши средства были поставлены в очередь вывода!", parse_mode='MARKDOWN')
        await state.finish()

@dp.callback_query_handler(text='POPOLNENIE')
async def POPOLNENIE(message: types.Message):
    await bot.send_message(message.from_user.id, f"📥* Введите сумму пополнения от 3000 до 25000 RUB:*", parse_mode='MARKDOWN')
    await message.answer("Введите сумму пополнения от 3000 до 25000 RUB:")
    await user.summa_popolnenie.set()

@dp.message_handler(state=user.summa_popolnenie)
async def summa_popolnenie(message: types.Message, state: FSMContext):
    await state.update_data(summa_popolnenie=int(message.text))
    data = await state.get_data()
    support_button = InlineKeyboardButton(text='👨‍💻Поддержка', url='https://t.me/ijustwait')
    back_button = InlineKeyboardButton(text='🔙Назад', callback_data='startingg')
    sp_keyboard = InlineKeyboardMarkup()
    sp_keyboard.row(support_button)
    sp_keyboard.row(back_button)
    await bot.send_message(message.from_user.id, f"👨‍💻 Напишите в поддержку (http://t.me/https://t.me/ijustwait) сумму депозита и удобный способ оплаты.\n\n *Не пишите, если НЕ готовы совершать перевод. При запросе реквизитов и НЕ совершении оплаты — Вы будете заблокированы.*", parse_mode='MARKDOWN', reply_markup=sp_keyboard)
    await state.finish()





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
