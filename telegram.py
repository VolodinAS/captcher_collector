# !/usr/bin/python3
# -*- coding: utf-8 -*-

import config
from default_config import default_config
from CoolSettings import CoolSettings
from cookie import save_cookies, load_cookies, save_cookies2, load_cookies2
import codecs
import threading
import time
import requests
from bs4 import BeautifulSoup
import os
import telebot
from telebot import types
import datetime
# from datetime import datetime
import random
from config import Elka_Links_Name
import json
import re
from functions.jprint import jprint
from python_anticaptcha import AnticaptchaClient, ImageToTextTask

PROGRAM_BEGIN = 0
PROGRAM_END = 0

CS = CoolSettings(filename='default_settings.json', default_parameters=default_config)  # debug в консоль
JSON_Settings = CS.settings

bot = telebot.TeleBot(JSON_Settings['telegrambot_data.token'])
ACC = AnticaptchaClient(JSON_Settings['app_data.system.anticaptcha.api_key'])

foiz = requests.session()
myThread = 0

commands1 = ['/start', '/status']
commands2 = ['/base', '/reset']
commands3 = ['/stop', '/restart']
commands4 = ['/elka', '/arena']

keyboard = types.ReplyKeyboardMarkup(True)
keyboard.row(*commands1)
keyboard.row(*commands2)
keyboard.row(*commands3)
keyboard.row(*commands4)

HTML_FOIZ_ELKA_PAGE = ''
HTML_FOIZ_WOW_PAGE = ''
CAPTCHA_URL = ''

ENERGY = -1
SILVER = -1
GOLD = -1

diff = 0

WOW_ARENA_ATTACK_ME = 0
WOW_ARENA_DEFENCE_ME = 1
WOW_ARENA_ATTACK_ENEMY = 5
WOW_ARENA_DEFENCE_ENEMY = 6

EFFECT_TIME_REMAIN = -1

IMIN_shakta = False
IMIN_patrul = False
IMIN_pole = False


def request_get(url, data=None, sleeper=True):
    global foiz, CS, JSON_Settings
    response = -1
    if data is None:
        data = {}
    try:
        response = foiz.get(url, data=data, cookies=load_cookies2(foiz, JSON_Settings['app_data.system.cookie']),
                            headers=JSON_Settings['app_data.system.headers'])
    except Exception:
        print('Возникла ошибка при GET-запросе на ' + url)
    finally:
        if sleeper:
            tout = random.random() * JSON_Settings['app_data.system.randomperiod']
            time.sleep(tout)
        return response


def request_post(url, data=None, sleeper=True):
    global foiz, CS, JSON_Settings
    response = -1
    if data is None:
        data = {}
    try:
        response = foiz.post(url, data=data, cookies=load_cookies2(foiz, JSON_Settings['app_data.system.cookie']),
                             headers=JSON_Settings['app_data.system.headers'])
    except Exception:
        print('Возникла ошибка при POST-запросе на ' + url)
    finally:
        if sleeper:
            tout = random.random() * JSON_Settings['app_data.system.randomperiod']
            time.sleep(tout)
        return response


def get_digits(txt):
    txt = txt.text
    txt = re.findall(r'\d+', txt)
    num = ''.join([str(elem) for elem in txt])
    return int(num)


def newMessages():
    global HTML_FOIZ_WOW_PAGE, CS, JSON_Settings
    # print(HTML_FOIZ_WOW_PAGE)
    mail = BeautifulSoup(HTML_FOIZ_WOW_PAGE, 'html.parser')
    mail_link = mail.select('a[href*="mess"][class*="top_menu_link"]')
    newMess = False
    if len(mail_link) > 0:
        # print(mail_link)
        mail_link = mail_link[0]
        mail_new = mail_link.select('span[class="newevent"]')
        if len(mail_new) > 0:
            newMess = True
            # print(mail_new)
        else:
            JSON_Settings['app_data.flags.newmessage'] = False
            CS.save()
            JSON_Settings.update

    if newMess:
        if not JSON_Settings['app_data.flags.newmessage']:
            JSON_Settings['app_data.flags.newmessage'] = True
            CS.save()
            JSON_Settings.update
            bot.send_message(JSON_Settings['telegrambot_data.chat_id'], '📧 У Вас новое сообщение! 📧')

    # exit()


def send_solution(url, solution, field, type='WOW'):
    global CAPTCHA_URL, bot, CS, JSON_Settings, HTML_FOIZ_WOW_PAGE
    if solution.isdigit():
        # СНАЧАЛА ПРОВЕРЯЕМ ПАПКУ
        collected_numbers = os.listdir(JSON_Settings['app_data.system.collection_path'])
        inBase = True
        solution_data = {field: solution}

        response_solution = request_post(url, data=solution_data)

        if response_solution.text.find('получен') > -1:
            JSON_Settings['app_data.flags.captcha_need'] = False
            HTML_FOIZ_WOW_PAGE = response_solution.text
            if inBase:
                bot.send_message(JSON_Settings['telegrambot_data.chat_id'],
                                 type + ': Капча '+solution+' решена верно! Число уже было в базе...')
            else:
                bot.send_message(JSON_Settings['telegrambot_data.chat_id'],
                                 type + ': Капча '+solution+' решена верно! Число добавлено в базу!')

    else:
        bot.send_message(JSON_Settings['telegrambot_data.chat_id'], type + 'Вы отправили не число '+solution+'!')


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    global foiz, myThread, keyboard, CS, JSON_Settings
    print('► New message by chat.id = ' + str(message.chat.id))
    if message.text == '/start' or message.text == '/help':
        print('♥ Launch message')
        bot.send_message(message.chat.id,
                         '👨‍👩‍👦 Бот предназначен для коллекционирования каптч в игре Мир Победителей на сайте Foiz.ru 👨‍👩‍👧\n\n'
                         '<b>⌨ Доступные команды:</b>\n\n\n'
                         '❓ /start, /help - начало работы\n\n'
                         '⛔ /stop - остановить сервер\n\n'
                         '🗓 /base - список ранее решенных капч\n\n'
                         '🔄 /reset - сброс капчи (ежечасно)\n\n'
                         '💻 /status - последний перезапуск цикла\n\n'
                         '⚙ /restart - перезапуск цикла (только в случае остановки при проверке /status)\n\n'
                         '💯 .число - отправить решение', reply_markup=keyboard, parse_mode='HTML')
        print('► Ready...')
    elif message.text == '/stop':
        print('• Закрываю программу...')
        bot.send_message(message.chat.id, 'Цикл остановлен, однако бот продолжает принимать команды')
        JSON_Settings['app_data.flags.stop_program'] = True
    elif message.text == '/base':
        print('• Вывод списка бывших капч.')
        collected_numbers = os.listdir(JSON_Settings['app_data.system.collection_path'])
        if len(collected_numbers) > 0:
            arr = sorted(collected_numbers)
            message_text = ''
            n = 1
            for num in arr:
                captches = os.listdir(JSON_Settings['app_data.system.collection_path'] + '/' + num)
                captches_len = len(captches)
                if len(message_text) == 0:
                    message_text = str(n) + '. ' + num + ' - ' + str(captches_len)
                else:
                    message_text += '\n' + str(n) + '. ' + num + ' - ' + str(captches_len)
                n += 1

            bot.send_message(message.chat.id,
                             '🗓 <b>Список чисел (' + str(len(collected_numbers)) + '):</b>\n\n' + message_text,
                             parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Список пуст')
    elif message.text == '/reset':
        print('• Сброс капчи')
        bot.send_message(message.chat.id, 'Капча сброшена')
        JSON_Settings['app_data.flags.captcha_need'] = False
    elif message.text == '/restart':
        print('• Рестарт цикла')
        JSON_Settings['app_data.flags.stop_program'] = False
        bot.send_message(message.chat.id, 'Рестарт цикла...')
    elif message.text == '/elka':
        print('• Ёлочка')
        if JSON_Settings['app_data.flags.goelka']:
            JSON_Settings['app_data.flags.goelka'] = False
        else:
            JSON_Settings['app_data.flags.goelka'] = True
        bot.send_message(message.chat.id, f"Режим ёлочки - {JSON_Settings['app_data.flags.goelka']}")
    elif message.text == '/arena':
        print('• Ёлочка')
        if JSON_Settings['app_data.flags.goarena']:
            JSON_Settings['app_data.flags.goarena'] = False
        else:
            JSON_Settings['app_data.flags.goarena'] = True
        bot.send_message(message.chat.id, f"Режим арены - {JSON_Settings['app_data.flags.goarena']}")
    elif message.text == '/status':
        print('• Статус сервера')
        today = datetime.datetime.today()
        f = open(JSON_Settings['app_data.system.status_time'], 'r')
        lasttime = f.read()
        f.close()
        date_time_obj = datetime.datetime.strptime(lasttime, '%Y-%m-%d-%H.%M.%S')
        difftime = today - date_time_obj
        server_sec = abs(difftime.seconds)
        if server_sec < 120:
            server_stat = '❤Работает❤'
        else:
            server_stat = '🆘<b>Не работает</b>🆘'
        bot.send_message(message.chat.id, '💻 <b>Статус сервера:</b>\n\nТекущее время: ' + today.strftime(
            "%Y.%m.%d %H:%M:%S") + '\n' + 'Последний запуск цикла: ' + lasttime + '\n' + 'Разница сервера: ' + str(
            server_sec) + ' сек.\nСтатус: ' + server_stat, parse_mode='HTML')
    elif message.text.find('.') > -1:
        # решение капчи
        captcha_solution_number = message.text[1:]
        curl = JSON_Settings['foiz_data.urls.wow'] + '/'
        send_solution(url=curl, solution=captcha_solution_number, field='chisloGM')
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда')


def makeWowGreatAgain():
    global HTML_FOIZ_WOW_PAGE, ENERGY, SILVER, GOLD, EFFECT_TIME_REMAIN, IMIN_shakta, IMIN_patrul, IMIN_pole, CS, JSON_Settings
    IMIN_shakta = IMIN_pole = IMIN_patrul = False
    AccessToShakta = False
    ARENA = -1
    soup = BeautifulSoup(HTML_FOIZ_WOW_PAGE, 'html.parser')
    div_body = soup.select('div[class="body"]')
    if len(div_body) > 0:
        div_body = div_body[0]
        div_p_m = div_body.select('div[class="p_m"]')
        if len(div_p_m) > 0:
            stats = div_p_m[0]
            moneybar = div_p_m[2]
            sumka = stats.select('a[href*="sumka"]')
            if len(sumka) > 0:
                sumka = sumka[0]
                sumka_text = sumka.text
                sumka_data = sumka_text.split(' ')
                if len(sumka_data) == 2:
                    ene = sumka_data[1]
                    ene = str(ene).strip()
                    ene = ene.replace(',', '')
                    ENERGY = int(ene)
                    money_text = moneybar.text
                    money_data = money_text.split(' ')
                    if len(money_data) > 0:
                        silv = str(money_data[0]).strip()
                        silv = silv.replace(',', '')
                        gol = str(money_data[1]).strip()
                        gol = gol.replace(',', '')
                        GOLD = int(gol)
                        SILVER = int(silv)
                        print('GOLD:', GOLD)
                        print('SILVER:', SILVER)
                        print('ENERGY:', ENERGY)

                        shakta = moneybar.select('a[href*=shakta]')
                        if len(shakta) > 0:
                            # проверяем шахту
                            print(shakta)
                            IMIN_shakta = True

                        patrul = moneybar.select('a[href*=patrul]')
                        if len(patrul) > 0:
                            # проверяем патруль
                            print(patrul)
                            IMIN_patrul = True

                        pole = moneybar.select('a[href*=pole]')
                        if len(pole) > 0:
                            # проверяем пещеру
                            print(pole)
                            IMIN_pole = True

                        print(':::::::::: <АРЕНА> ::::::::::')
                        arena = stats.select('a[href*="arena"]')
                        if JSON_Settings['app_data.flags.goarena']:
                            if len(arena) > 0 and not IMIN_shakta and ENERGY >= 24:
                                arena_text = arena[0].text
                                arena_data = arena_text.split('/')
                                granted_battles = int(arena_data[0])
                                total_battles = int(arena_data[1])
                                if granted_battles < total_battles:

                                    while granted_battles < total_battles:
                                        go_attack = False
                                        response_arena = request_get(JSON_Settings['foiz_data.urls.wow.arena2lvls'],
                                                                     data=None, sleeper=False)
                                        if response_arena != -1:
                                            soup_arena = BeautifulSoup(response_arena.text, 'html.parser')
                                            div_stats = soup_arena.select('div > div.param_st')
                                            if len(div_stats) == 10:
                                                my_attack = div_stats[WOW_ARENA_ATTACK_ME]
                                                my_attack = get_digits(my_attack)

                                                my_defence = div_stats[WOW_ARENA_DEFENCE_ME]
                                                my_defence = get_digits(my_defence)

                                                enemy_attack = div_stats[WOW_ARENA_ATTACK_ENEMY]
                                                enemy_attack = get_digits(enemy_attack)

                                                enemy_defence = div_stats[WOW_ARENA_DEFENCE_ENEMY]
                                                enemy_defence = get_digits(enemy_defence)

                                                diff_attack = round((my_attack / enemy_attack) * 10000) / 100
                                                diff_defence = round((my_defence / enemy_defence) * 10000) / 100

                                                print(
                                                    f"ТЫ: |{my_attack}|&|{my_defence}| vs. ВРАГ: |{enemy_attack}|&|{enemy_defence}|")
                                                print(f"СООТНОШЕНИЕ АТАКИ: |{diff_attack}%|")
                                                print(f"СООТНОШЕНИЕ ЗАЩИТЫ: |{diff_defence}%|")

                                                if diff_attack >= 100:
                                                    # A >= 100
                                                    if diff_attack <= 120:
                                                        print('- моя атака больше')
                                                        if diff_defence < 95:
                                                            print('- вражеский щит сильнее')
                                                            continue
                                                        else:
                                                            print('- соотношения приемлемые, атака')
                                                            go_attack = True
                                                    else:
                                                        continue
                                                else:
                                                    # A < 100
                                                    print('- моя атака меньше, проверяем щиты')
                                                    if diff_attack >= 90:
                                                        # 100 > A >= 90
                                                        print('- атака меньше 10%')
                                                        if diff_defence > 100:
                                                            # D > 100
                                                            print('- щиты больше вражеского, атака')
                                                            go_attack = True
                                                        else:
                                                            continue

                                                if go_attack:
                                                    form_attack_id = -1
                                                    form_attack_rand = -1
                                                    # input_ok = soup_arena.select('form > input[name="yes"][value="ok"]')
                                                    input_ok = soup_arena.find_all("input",
                                                                                   attrs={'name': 'yes', 'value': 'ok'})
                                                    if len(input_ok) > 0:
                                                        # print('input_ok: ', input_ok)
                                                        input_ok = input_ok[0]
                                                        form_attack = input_ok.parent
                                                        # print('form_attack: ', form_attack)
                                                        input_id = form_attack.find("input", attrs={'name': 'id'})
                                                        input_rand = form_attack.find("input", attrs={'name': 'rand'})
                                                        form_attack_id = input_id['value']
                                                        form_attack_rand = input_rand['value']
                                                        # print('input_id: ', input_id)
                                                        # print('input_rand: ', input_rand)
                                                        attack_data = {
                                                            'mod': 'ataka2',
                                                            'id': form_attack_id,
                                                            'rand': form_attack_rand,
                                                            'yes': 'ok'
                                                        }
                                                        print('attack_data:', attack_data)
                                                        url_attack = f"{JSON_Settings['foiz_data.urls.wow.arena2lvls.go']}mod=ataka2&id={form_attack_id}&rand={form_attack_rand}&yes=ok"
                                                        response_attack = request_get(url_attack, sleeper=False)
                                                        soup_end = BeautifulSoup(response_attack.text, 'html.parser')
                                                        div_body = soup_end.select('div[class="body"]')
                                                        if len(div_body) > 0:
                                                            div_body = div_body[0]
                                                            div_p_m = div_body.select('div[class="p_m"]')
                                                            if len(div_p_m) > 0:
                                                                stats = div_p_m[0]
                                                                arena = stats.select('a[href*="arena"]')
                                                                if len(arena) > 0:
                                                                    arena_text = arena[0].text
                                                                    arena_data = arena_text.split('/')
                                                                    granted_battles = int(arena_data[0])
                                                                    total_battles = int(arena_data[1])
                                                    print(f"Битвы: {granted_battles} / {total_battles}")
                                                    # break
                                                print(' ')

                                                # if diff_attack > 0:
                                                #     # моя атака больше
                                                #     if diff_attack < 3000:
                                                #         # атакуй
                                                #     else:
                                                #         continue
                                                # else:

                                            else:
                                                print('Проблемы с получением статов')

                                        else:
                                            print('Проблема с получением арены')
                                        # break
                        else:
                            print('Арена отключена')
                        print(':::::::::: </АРЕНА> ::::::::::')

                        if ENERGY < 207:
                            if JSON_Settings['app_data.flags.use_potion']:
                                print('Энергии нет, использую зелье')
                                if SILVER >= JSON_Settings['foiz_data.wow.market.potion.energy.price']:
                                    response_potion_buy = request_get(
                                        JSON_Settings['foiz_data.wow.market.potion.energy.get'])
                                    print('Энергии нет, зелье куплено')

                                    response_potion_use = request_get(
                                        JSON_Settings['foiz_data.urls.wow.bag.potion.use'])
                                    print('Энергии нет, зелье использовано')
                                else:
                                    print('Энергии нет, для покупки зелья не хватает серебра')

                            else:
                                print('Энергии нет, использование зелья отключено')



                        youCanGo = False
                        effectActive = False
                        if EFFECT_TIME_REMAIN == -1:
                            # проверка эффектов
                            response_wow_effects = request_get(JSON_Settings['foiz_data.urls.wow.effects'])
                            if response_wow_effects != -1:
                                youCanGo = True

                            if youCanGo:
                                print('Проверяем эффекты...')
                                youCanGo = False
                                soup = BeautifulSoup(response_wow_effects.text, 'html.parser')
                                effects = soup.select('img[src*="efakt"]')
                                if len(effects) > 0:
                                    print('Эффекты активны')
                                    form = soup.select('form[class="iform"]')
                                    if len(form) > 0:
                                        form = form[0]
                                        form = ''.join([str(x) for x in form.contents])
                                        form_arr = form.split('<hr/>')

                                        for index in JSON_Settings['arrays.RequireEffects']:
                                            RequireEffect = JSON_Settings['arrays.RequireEffects'][index]
                                            # print('RequireEffect:', RequireEffect)
                                            HtmlDataEffect = form_arr[RequireEffect['array_element']]
                                            # print('HtmlDataEffect:', HtmlDataEffect)
                                            soup_element = BeautifulSoup(HtmlDataEffect, 'html.parser')
                                            effect_text = soup_element.text
                                            # print('effect_text:', effect_text)
                                            remain_arr = effect_text.split('осталось:')
                                            # print('remain_arr:', remain_arr)
                                            time_text = remain_arr[len(remain_arr) - 1]
                                            time_text = time_text.strip()
                                            time_arr = time_text.split(' ')
                                            if len(time_arr) == 2:
                                                if time_arr[1] == 'час.':
                                                    EFFECT_TIME_REMAIN = int(time_arr[0]) * 3600
                                                    effectActive = True
                                            break
                                        effectActive = True
                                else:
                                    print('Эффекты не активны')
                                    # jprint(JSON_Settings['arrays.RequireEffects'])
                                    effects_data = {}
                                    for index in JSON_Settings['arrays.RequireEffects']:
                                        effects_data[index] = '1'
                                    effects_data['activ'] = 'Активировать'

                                    # print('effects_data:', effects_data)

                                    response_effects_on = request_post(JSON_Settings['foiz_data.urls.wow.effects.go'],
                                                                       data=effects_data)

                            else:
                                print('PROBLEMS')
                        else:
                            effectActive = True

                        if effectActive:
                            # СРАЖЕНИЯ
                            response_wow_battles = request_get(JSON_Settings['foiz_data.urls.wow.battles'])
                            if response_wow_battles != -1:
                                print('Инициализируем войнов')
                                soup = BeautifulSoup(response_wow_battles.text, 'html.parser')
                                warrior = soup.select('td[class="p_t"]')
                                n = 1
                                for warr in warrior:
                                    warr_html = ''.join([str(x) for x in warr.contents])
                                    warr_html_arr = warr_html.split('<br/>')
                                    bw_index = 'srajen' + str(n)

                                    if warr_html.find('Воскреснет') > -1:
                                        # print(bw_index + ' мёртв')
                                        JSON_Settings['arrays.BattleWarriors'][bw_index]['COOLDOWN'] = True
                                    else:
                                        JSON_Settings['arrays.BattleWarriors'][bw_index]['COOLDOWN'] = False
                                        # print(bw_index + ' жив')

                                    for warr_elem in warr_html_arr:

                                        if warr_elem.find('Требования') > -1:
                                            warr_require_arr = warr_elem.split('Требования:')
                                            warr_require_text = str(warr_require_arr[1]).strip()
                                            warr_require_text_arr = warr_require_text.split(' ')
                                            warr_require_data = warr_require_text_arr[0].split('/')
                                            if bw_index in JSON_Settings['arrays.BattleWarriors']:
                                                JSON_Settings['arrays.BattleWarriors'][bw_index]['CURRENT_KEYS'] = int(
                                                    warr_require_data[0])
                                    n += 1
                                youCanGo = True

                            # print('youCanGo:', youCanGo)
                            if youCanGo:

                                # print( json.dumps(config.BattleWarriors, indent=4) )

                                for index in reversed(JSON_Settings['arrays.BattleWarriors']):
                                    comon = False
                                    BattleWarrior = JSON_Settings['arrays.BattleWarriors'][index]
                                    battle_url = 'https://foiz.ru/gm/' + index + '.php?mod=ataka'
                                    if not BattleWarrior['REQUIRE'] is None:
                                        RequireWarriorAmount = int(BattleWarrior['REQUIRE']['AMOUNT'])
                                        RequireWarriorCurrent = int(BattleWarrior['CURRENT_KEYS'])
                                        if RequireWarriorCurrent >= RequireWarriorAmount:
                                            comon = True
                                    else:
                                        comon = True
                                    # print('comon:', index, comon)
                                    if comon:
                                        if ENERGY >= BattleWarrior['ENERGY_EFFECT']:
                                            # print('ENERGY:', index, ENERGY)
                                            if not BattleWarrior['COOLDOWN']:
                                                print('BATTLE:', battle_url)
                                                response_wow_battles_srajen = request_get(battle_url)
                                                JSON_Settings['arrays.BattleWarriors'][index]['COOLDOWN'] = False
                                                if response_wow_battles_srajen.text.find('в шахте') > -1:
                                                    AccessToShakta = True
                                                    print('Не могу сражаться - я в шахте')
                                                    break
                                        else:
                                            AccessToShakta = True
                                    # print(' ')
                                # print(json.dumps(config.BattleWarriors, indent=4))

                                # AccessToShakta = True # ВАЖНО

                                newShakta = False
                                if AccessToShakta:
                                    print('Мало энергии, идём в шахту')
                                    if IMIN_shakta:
                                        shakta_text = str(shakta[0].text)
                                        shakta_data = shakta_text.split(' ')
                                        # print(shakta_data)
                                        shakta_time = int(shakta_data[0])
                                        # print('shakta_time:', shakta_time)
                                        if shakta_time == 0:
                                            print('shakta is done')
                                            newShakta = True
                                        else:
                                            print('shakta is not done yet')
                                    else:
                                        print('need to go shakta')
                                        newShakta = True
                                if newShakta:
                                    print('prepare new shakta')
                                    response_wow_shakta = request_get(JSON_Settings['foiz_data.urls.wow.shakta'])
                                    if response_wow_shakta != -1:
                                        if response_wow_shakta.text.find('yes=yes"') > -1:
                                            print('shakta - еще не копаем, надо копать')
                                            if ENERGY >= 69:
                                                print('Энергия восполнилась, надо сражаться')
                                            else:
                                                response_wow_shakta_go = request_get(
                                                    JSON_Settings['foiz_data.urls.wow.shakta.go'])
                                        else:
                                            if response_wow_shakta.text.find('нашли место') > -1:
                                                print('shakta - поиск завершен, оценка')
                                                soup = BeautifulSoup(response_wow_shakta.text, 'html.parser')
                                                div_foot = soup.select('div.page_foot > b')
                                                if len(div_foot) > 0:
                                                    div_foot = div_foot[0]
                                                    div_foot_text = div_foot.text
                                                    # print('div_foot_text:', div_foot_text)
                                                    num = re.findall(r'\d+', div_foot_text)
                                                    if len(num) > 0:
                                                        num = int(num[0])

                                                        if num > 60:
                                                            print('shakta - ценность ' + str(
                                                                num) + '% - начинаю раскопки')
                                                            response_wow_shakta_comon = request_get(
                                                                JSON_Settings['foiz_data.urls.wow.shakta.comon'])
                                                        else:
                                                            print('shakta - ценность ' + str(num) + '% - новый поиск')
                                                            response_wow_shakta_repeat = request_get(
                                                                JSON_Settings['foiz_data.urls.wow.shakta.repeat'])

                                newPatrul = False
                                if IMIN_patrul:
                                    patrul_text = str(patrul[0].text)
                                    patrul_data = patrul_text.split(' ')
                                    # print(patrul_data)
                                    patrul_time = int(patrul_data[0])
                                    # print('patrul_time:', patrul_time)
                                    if patrul_time == 0:
                                        print('patrul is done')
                                        response_wow_patrul_done = request_get(
                                            JSON_Settings['foiz_data.urls.wow.patrul'])
                                        newPatrul = True
                                    else:
                                        print('patrul is not done yet')
                                else:
                                    print('need to go patrul')
                                    newPatrul = True
                                if newPatrul:
                                    print('prepare new patrul')
                                    response_wow_patrul_go = request_get(JSON_Settings['foiz_data.urls.wow.patrul.go'])
                                    if response_wow_patrul_go != -1:
                                        soup = BeautifulSoup(response_wow_patrul_go.text, 'html.parser')
                                        # print( soup.prettify() )
                                        opened = soup.select('input[value="yes"]')
                                        # print(opened)
                                        if len(opened) > 0:
                                            opened = opened[0]
                                            # print(type(opened))
                                            # print('opened:', opened)
                                            rand = opened.find_next_siblings('input')
                                            if len(rand) > 0:
                                                rand = rand[0]
                                                randId = rand.get('value')

                                                patrul_url = JSON_Settings[
                                                                 'foiz_data.urls.wow.patrul'] + '?' + 'dver=yes&rand=' + randId
                                                response_wow_patrul_comon = request_get(patrul_url)
                                                # soup = BeautifulSoup(response_wow_patrul_comon.text, 'html.parser')
                                                # print(soup.prettify())

                                newPole = False
                                if IMIN_pole:
                                    pole_text = str(pole[0].text)
                                    pole_data = pole_text.split(' ')
                                    # print(pole_data)
                                    pole_time = int(pole_data[0])
                                    # print('pole_time:', pole_time)
                                    if pole_time == 0:
                                        print('pole is done')
                                        response_wow_pole_done = request_get(JSON_Settings['foiz_data.urls.wow.pole'])
                                        newPole = True
                                    else:
                                        print('pole is not done yet')
                                else:
                                    print('need to go pole')
                                    newPole = True
                                if newPole:
                                    print('prepare new pole')
                                    response_wow_pole_go = request_get(JSON_Settings['foiz_data.urls.wow.pole.go'])
                                    if response_wow_pole_go != -1:
                                        soup = BeautifulSoup(response_wow_pole_go.text, 'html.parser')
                                        # print( soup.prettify() )
                                        opened = soup.select('input[value="yes"]')
                                        # print(opened)
                                        if len(opened) > 0:
                                            opened = opened[0]
                                            # print(type(opened))
                                            # print('opened:', opened)
                                            rand = opened.find_next_siblings('input')
                                            if len(rand) > 0:
                                                rand = rand[0]
                                                randId = rand.get('value')

                                                pole_url = JSON_Settings[
                                                               'foiz_data.urls.wow.pole'] + '?' + 'vhod=yes&rand=' + randId
                                                # print('pole_url:', pole_url)
                                                response_wow_pole_sunduk = request_get(pole_url)
                                                soup_sunduk = BeautifulSoup(response_wow_pole_sunduk.text,
                                                                            'html.parser')
                                                sunduk = soup_sunduk.select('input[name="sunduk"][value="2"]')
                                                # print(opened)
                                                if len(sunduk) > 0:
                                                    sunduk = sunduk[0]
                                                    # print(type(opened))
                                                    # print('opened:', opened)
                                                    rand = sunduk.find_next_siblings('input')
                                                    if len(rand) > 0:
                                                        rand = rand[0]
                                                        randId = rand.get('value')

                                                        sunduk_url = JSON_Settings[
                                                                         'foiz_data.urls.wow.pole'] + '?' + 'sunduk=2&rand=' + randId
                                                        response_wow_pole_sunduk = request_get(sunduk_url)
                            else:
                                print('PROBLEMS2')
                        else:
                            print('ЭФФЕКТЫ ПОЧЕМУ-ТО НЕ АКТИВНЫ')


def parseElkaPage():
    global HTML_FOIZ_ELKA_PAGE, CS, JSON_Settings
    # 1 - заходим на сайт, в раздел ёлки, получаем страницу
    requestSuccess = False
    response_elka_main = request_get(JSON_Settings['foiz_data.urls.elka'])
    if response_elka_main != -1:
        requestSuccess = True

    if requestSuccess:
        requestSuccess = False
        # 2 - проверяем, есть ли текстовая капча
        html_string = response_elka_main.text
        if html_string.find('роверка') > -1:
            # 2.1 - нашел капчу, нанахожу ответ
            elka_soup = BeautifulSoup(response_elka_main.text, 'html.parser')
            # form_captcha = elka_soup.select('form[class="iform"]')
            captcha = elka_soup.select('img[src*="captcha"]')
            if len(captcha) > 0:
                captcha_url = JSON_Settings['foiz_data.urls.site'] + captcha[0]['src']
                response_captcha = request_get(captcha_url)
                captcha_file = JSON_Settings['app_data.system.captcha_path'] + '/captcha.' + JSON_Settings[
                    'app_data.system.captcha_ext']
                # print(captcha_file)
                captcha_img = open(captcha_file, 'wb')
                captcha_img.write(response_captcha.content)
                captcha_img.close()
                # print(captcha)
                # exit()
                captcha_fp = open(captcha_file, 'rb')
                task = ImageToTextTask(fp=captcha_fp, numeric=1)
                job = -1
                CAPTCHA_SOLUTION = -1
                try:
                    job = ACC.createTask(task)
                except Exception as err:
                    print('Ошибка создания задания')
                    print(job)
                    print(err)
                    JSON_Settings['app_data.flags.captcha_need'] = False
                else:
                    try:
                        job.join()
                    except Exception as err:
                        print('Ошибка запуска задания')
                        print(job)
                        print(err)
                        JSON_Settings['app_data.flags.captcha_need'] = False
                    else:
                        try:
                            CAPTCHA_SOLUTION = job.get_captcha_text()
                        except Exception as err:
                            print(job)
                            print(err)
                            print(CAPTCHA_SOLUTION)
                            JSON_Settings['app_data.flags.captcha_need'] = False
                        else:
                            curl = JSON_Settings['foiz_data.urls.elka'] + '/?'
                            send_solution(url=curl, solution=CAPTCHA_SOLUTION, field='kod', type='ELKA')

            else:
                print('КАПЧИ НЕТ 2')
        else:
            # 3 - капчу не нашел
            print('КАПЧИ НЕТ')
            HTML_FOIZ_ELKA_PAGE = html_string
            # parseElkaPage()
    else:
        print('ПРОБЛЕМА С response_elka_main')
        bot.send_message(JSON_Settings['telegrambot_data.chat_id'], 'Проблема с получением response_elka_main')

    # global HTML_FOIZ_ELKA_PAGE
    soup = BeautifulSoup(HTML_FOIZ_ELKA_PAGE, 'html.parser')
    link_divs = soup.select('div[style="padding:4px"] > div[class="p_t"]')

    # print(Elka_Links_Name)

    Elka_Dynamic = {}

    for link_div in link_divs:
        text = link_div.getText()
        # print('text: ', text)
        arr1 = text.split(' : ')
        # print('arr1: ', arr1)
        ITEM_NAME = arr1[0].strip()

        if ITEM_NAME in Elka_Links_Name:
            ITEM_TIMEOUT = False
            if text.find('Осталось') > -1:
                ITEM_TIMEOUT = True
            ITEM_OBJECT = Elka_Links_Name[ITEM_NAME]
            Elka_Dynamic[ITEM_NAME] = {}
            # if not timeout:

            ITEM_AMOUNT = 0
            if ITEM_OBJECT['isCounting']:
                arr2 = arr1[1].split(' ')
                # print('arr2: ', arr2)
                ITEM_AMOUNT = int(arr2[0])

            link_div_a = link_div.find('a')
            # print(link_div_a)
            ITEM_LINK = link_div_a.get('href')

            Elka_Dynamic[ITEM_NAME]['ITEM_AMOUNT'] = ITEM_AMOUNT
            Elka_Dynamic[ITEM_NAME]['ITEM_LINK'] = ITEM_LINK
            Elka_Dynamic[ITEM_NAME]['ITEM_TIMEOUT'] = ITEM_TIMEOUT
        # print(' ')
    #
    # print(Elka_Dynamic)
    for Index in Elka_Dynamic:
        Element = Elka_Dynamic[Index]
        # print('Element ['+Index+']: ', Element)
        Requires = Elka_Links_Name[Index]
        # print('Requires ['+Index+']: ', Requires)
        if not Element['ITEM_TIMEOUT']:
            if Requires['require_remain'] is None:
                # print('Element(' + Index + '): ', Element)
                # print('Requires(' + Index + '): ', Requires)
                elka_url = ''
                if Requires['require_item'] is None:
                    if Requires['require_link'] is None:
                        elka_url = JSON_Settings['foiz_data.urls.site'] + Element['ITEM_LINK']

                    else:
                        elka_url = JSON_Settings['foiz_data.urls.site'] + Requires['require_link']
                    # print('elka_url: ', elka_url)
                else:
                    # require_item = Requires['require_item']
                    # print('require_item: ', require_item)
                    # require_element = Elka_Dynamic[ require_item ]
                    # print('require_element: ', require_element)
                    # curre
                    # print('REQUIRE: ', Requires['require_item'])
                    if Requires['require_item'] in Elka_Dynamic:
                        current_amount = int(Elka_Dynamic[Requires['require_item']]['ITEM_AMOUNT'])
                        # print('current_amount: ', current_amount)
                        if current_amount >= Requires['require_amount']:
                            if Requires['require_link'] is None:
                                elka_url = JSON_Settings['foiz_data.urls.site'] + Element['ITEM_LINK']

                            else:
                                elka_url = Requires['require_link']
                            # print('elka_url: ', elka_url)
            else:
                tri = Requires['require_remain']
                # print('timeout require item: ', tri)
                CurrentElementTimeout = Elka_Dynamic[tri]
                # print('CurrentElementTimeout: ', CurrentElementTimeout )
                ElementTimeout = CurrentElementTimeout['ITEM_TIMEOUT']
                # print('ElementTimeout: ',ElementTimeout )
                if ElementTimeout:
                    if Requires['require_link'] is None:
                        elka_url = JSON_Settings['foiz_data.urls.site'] + Element['ITEM_LINK']
                    else:
                        elka_url = Requires['require_link']

            if len(elka_url) > 0:
                response_elka_url = request_get(elka_url)
                if response_elka_url != -1:
                    print('Responded ' + elka_url)


def zalooper():
    global foiz, myThread, keyboard, HTML_FOIZ_ELKA_PAGE, PROGRAM_BEGIN, diff, CS, JSON_Settings, ACC, HTML_FOIZ_WOW_PAGE

    print('♠ Start loop')
    PROGRAM_BEGIN = datetime.datetime.now()

    if not JSON_Settings['app_data.flags.stop_program']:

        print('!stop_program: ', JSON_Settings['app_data.flags.stop_program'])

        requestSuccess = False
        response_index = request_get(JSON_Settings['foiz_data.urls.site'])
        if response_index != -1:
            requestSuccess = True
            save_cookies2(foiz, JSON_Settings['app_data.system.cookie'])

        if requestSuccess:
            requestSuccess = False

            # Запрос на страницу с авторизацией
            response_auth = request_post(JSON_Settings['foiz_data.urls.page_auth'],
                                         data=JSON_Settings['app_data.system.auth_data'])
            if response_auth != -1:
                requestSuccess = True
                save_cookies2(foiz, JSON_Settings['app_data.system.cookie'])

            if requestSuccess:
                requestSuccess = False

                # Запрос на страницу игры
                response_wow = request_get(JSON_Settings['foiz_data.urls.wow'])
                if response_wow != -1:
                    requestSuccess = True

                if requestSuccess:
                    soup = BeautifulSoup(response_wow.text, 'html.parser')
                    captcha = soup.select('img[src*="captcha"]')
                    if len(captcha) == 1:
                        if not JSON_Settings['app_data.flags.captcha_need']:
                            JSON_Settings['app_data.flags.captcha_need'] = True
                            captcha_url = JSON_Settings['foiz_data.urls.site'] + captcha[0]['src']
                            print(captcha_url)
                            global CAPTCHA_URL
                            CAPTCHA_URL = captcha_url
                            response_captcha = request_get(CAPTCHA_URL)
                            captcha_file = JSON_Settings['app_data.system.captcha_path'] + '/captcha.' + JSON_Settings[
                                'app_data.system.captcha_ext']
                            # print(captcha_file)
                            captcha_img = open(captcha_file, 'wb')
                            captcha_img.write(response_captcha.content)
                            captcha_img.close()
                            if JSON_Settings['app_data.system.anticaptcha.use']:
                                print('Использую AntiCaptcha')
                                # BALANCE = ACC.getBalance()
                                # print(f"BALANCE: {BALANCE}, BALANCE-type: { type(BALANCE) }")
                                # bot.send_message(JSON_Settings['telegrambot_data.chat_id'],'ВНИМАНИЕ! Пошла антикапча!')
                                captcha_fp = open(captcha_file, 'rb')
                                task = ImageToTextTask(fp=captcha_fp, numeric=1)
                                job = -1
                                CAPTCHA_SOLUTION = -1
                                try:
                                    job = ACC.createTask(task)
                                except Exception as err:
                                    print('Ошибка создания задания')
                                    print(job)
                                    print(err)
                                    JSON_Settings['app_data.flags.captcha_need'] = False
                                else:
                                    try:
                                        job.join()
                                    except Exception as err:
                                        print('Ошибка запуска задания')
                                        print(job)
                                        print(err)
                                        JSON_Settings['app_data.flags.captcha_need'] = False
                                    else:
                                        try:
                                            CAPTCHA_SOLUTION = job.get_captcha_text()
                                        except Exception as err:
                                            print(job)
                                            print(err)
                                            print(CAPTCHA_SOLUTION)
                                            JSON_Settings['app_data.flags.captcha_need'] = False
                                        else:
                                            # send_solution(CAPTCHA_SOLUTION)
                                            curl = JSON_Settings['foiz_data.urls.wow'] + '/'
                                            send_solution(url=curl, solution=CAPTCHA_SOLUTION, field='chisloGM')
                            else:
                                print('Ручное решение капчи')
                                bot.send_photo(JSON_Settings['telegrambot_data.chat_id'], open(captcha_file, 'rb'),
                                               caption='Отправьте ответ с точкой (.число)')

                    else:
                        print('▲ Каптча не требуется')
                        HTML_FOIZ_WOW_PAGE = response_wow.text

        f = open(JSON_Settings['app_data.system.status_time'], 'w')
        today = datetime.datetime.today()
        f.write(today.strftime("%Y-%m-%d-%H.%M.%S"))
        f.close()

    else:
        print('! Поток остановлен')

    # jprint(JSON_Settings)

    if JSON_Settings['app_data.flags.goelka']:
        print('------------------------------------- <ELKA> -------------------------------------')
        parseElkaPage()
        print('------------------------------------- </ELKA> -------------------------------------')

    print('------------------------------------- <MESSAGES> -------------------------------------')
    newMessages()
    print('------------------------------------- </MESSAGES> -------------------------------------')

    print('{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ <WOW> }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}')
    if not JSON_Settings['app_data.flags.captcha_need']:
        if not JSON_Settings['app_data.flags.stop_program']:
            makeWowGreatAgain()
        else:
            print('WoW не запущен, программа остановлена')
    print('{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{ </WOW> }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}')

    PROGRAM_END = datetime.datetime.now()
    print(PROGRAM_BEGIN)
    print(PROGRAM_END)
    diff = (PROGRAM_END - PROGRAM_BEGIN).seconds
    print('Время работы:', (PROGRAM_END - PROGRAM_BEGIN))
    print('♠ End loop. Timeout ' + str(JSON_Settings['app_data.system.timeout'] - diff) + ' secs')

    myThread = threading.Timer(JSON_Settings['app_data.system.timeout'] - diff, zalooper)
    myThread.start()


if __name__ == '__main__':
    print('► Ready...')

    if not JSON_Settings['app_data.flags.stop_program']:
        zalooper()

    bot.polling(none_stop=True)
    # существует проблема сражений, появилась некая кнопка "Добить"
