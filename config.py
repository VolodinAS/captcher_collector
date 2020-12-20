# !/usr/bin/python3
# -*- coding: utf-8 -*-


# BOT-token
telegrambot_data = {
    'token': '1354748675:AAHJo0_-b6-rRzyfmsw3kTxQCDgeXfhK-P4'
}

foiz_data = {
    'login': 'nomercyman',
    'password': '1qw23er4',
    'site': 'https://foiz.ru',
    'page_auth': 'https://foiz.ru/aut.php',
    'page_wow': 'https://foiz.ru/gm',
    'page_elka': 'https://foiz.ru/elka',
    'page_wow_effects': 'https://foiz.ru/gm/effekt.php',
    'page_wow_effects_go': 'https://foiz.ru/gm/effekt.php?',
    'page_wow_battles': 'https://foiz.ru/gm/srajen.php',

    'page_wow_patrul': 'https://foiz.ru/gm/patrul.php',
    'page_wow_patrul_go': 'https://foiz.ru/gm/patrul.php?yes=yes',
    'page_wow_pole': 'https://foiz.ru/gm/pole.php',
    'page_wow_pole_go': 'https://foiz.ru/gm/pole.php?yes=yes',

    'page_wow_shakta': 'https://foiz.ru/gm/shakta.php',
    'page_wow_shakta_go': 'https://foiz.ru/gm/shakta.php?yes=yes',
    'page_wow_shakta_repeat': 'https://foiz.ru/gm/shakta.php?yes=yes2',
    'page_wow_shakta_comon': 'https://foiz.ru/gm/shakta.php?yes=raskopka',
    'page_wow_shakta_quit': 'https://foiz.ru/gm/shakta.php?yes=raskopka',

    'page_wow_bag_potion_use': 'https://foiz.ru/gm/sumka.php?go=mp_6',

    'market_potion_energy_price': 25875,
    'market_potion_energy_post_url': 'https://foiz.ru/gm/magazin.php?mod=elik&go=pokupka_elik&id=6',
    'market_potion_energy_post_url_get': 'https://foiz.ru/gm/magazin.php?mod=elik&go=pokupka_elik_ok&id=6&kol=1',
}

app_data = {
    'timeout': 65,
    'cookie': foiz_data['login'] + '.txt',
    'cookie_auth': foiz_data['login'] + '_auth.txt',
    'captcha_path': 'images/captcha',
    'collection_path': 'images/collection',
    'captcha_ext': 'jpg',
    'old_numbers_file': 'old_numbers.txt',
    'old_numbers_name': 'old_numbers',
    'status_time': 'status.txt',
    'chat_id': 353445676
}

app_flags = {
    'stop_program': False,
    'reauth': False,
    'captcha_need': False,
    'use_potion': True
}

auth_data = {
    'nick': foiz_data['login'],
    'pass': foiz_data['password']
}

auth_headers_data = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36 '
}

Elka_Links_Name = {
    'Моя волшебная пудра': {
        'require_item': None,
        'require_amount': None,
        'require_time': int(5 * 60),
        'require_link': None,
        'isCounting': True,
        'require_remain': None
    },
    'Моя вода': {
        'require_item': None,
        'require_amount': None,
        'require_time': int(5 * 60),
        'require_link': None,
        'isCounting': True,
        'require_remain': None
    },
    'Рост': {
        'require_item': 'Моя вода',
        'require_amount': 6,
        'require_time': int(60 * 60),
        'require_link': None,
        'isCounting': False,
        'require_remain': None
    },
    'Нарядность': {
        'require_item': 'Моя волшебная пудра',
        'require_amount': 15,
        'require_time': int(5 * 60),
        'require_link': 'https://foiz.ru/elka/?5',
        'isCounting': False,
        'require_remain': 'Уровень'
    },
    'Уровень': {
        'require_item': 'Моя волшебная пудра',
        'require_amount': 20,
        'require_time': int(60 * 60),
        'require_link': None,
        'isCounting': False,
        'require_remain': None
    },
    'Найденые эльфы': {
        'require_item': None,
        'require_amount': None,
        'require_time': int(4 * 60),
        'require_link': None,
        'isCounting': True,
        'require_remain': None
    },
    'Созданных предметов': {
        'require_item': 'Найденые эльфы',
        'require_amount': 3,
        'require_time': None,
        'require_link': None,
        'isCounting': False,
        'require_remain': None
    }
}

BattleWarriors = {
    'srajen1': {
        'HP': 300,
        'ENERGY': 138,
        'ENERGY_EFFECT': 69,
        'REQUIRE': None,
        'CURRENT_KEYS': None,
        'COOLDOWN': False,
    },
    'srajen2': {
        'HP': 1000,
        'ENERGY': 138,
        'ENERGY_EFFECT': 69,
        'REQUIRE': {
            'ITEM': 'srajen1',
            'AMOUNT': 10
        },
        'CURRENT_KEYS': -1,
        'COOLDOWN': False,
    },
    'srajen3': {
        'HP': 1000,
        'ENERGY': 138,
        'ENERGY_EFFECT': 69,
        'REQUIRE': {
            'ITEM': 'srajen2',
            'AMOUNT': 5
        },
        'CURRENT_KEYS': -1,
        'COOLDOWN': False,
    }
}

RequireEffects = {
    """
    'post_3': {
        'name': 'Благословение здоровья',
        'desc': 'Увеличивает здоровье на 30%',
        'price': 50,
        'array_element': 3
    },
    """
    'post_4': {
        'name': 'Благословение бодрячка',
        'desc': 'Увеличивает бодрячок на 30%',
        'price': 50,
        'array_element': 4,
    },
    'post_7': {
        'name': 'Сила воли',
        'desc': 'Снижает расход бодрячка в сражениях и логове дракона на 50%',
        'price': 50,
        'array_element': 6,
    }
}