# !/usr/bin/python3
# -*- coding: utf-8 -*-

from os import path
import json


class CoolSettings(object):
    def __init__(self, filename, default_parameters, debug=False):
        self.filename = filename
        self.json_settings = {}
        self.default_parameters = default_parameters
        self.debug = debug
        self.init_preferences()

    # json_settings = property()

    def init_preferences(self):
        filename = self.filename
        if not path.exists(filename):
            self.json_settings = self.default_settings_generator()
            self.json_settings_save()
        else:
            self.json_settings_load()
            self.check_preferences()

    def default_settings_generator(self):
        arr = {}
        # print(self.default_parameters)
        for DefaultPreset in self.default_parameters.items():
            # print(DefaultPreset)
            # arr[DefaultPreset[0]] = DefaultPreset[1][1]
            arr[DefaultPreset[0]] = DefaultPreset[1][1]
        return arr

    def json_settings_save(self):
        json_string = json.dumps(self.json_settings)
        f = open(self.filename, 'w')
        f.write(json_string)
        f.close()

    def json_settings_load(self):
        with open(self.filename, 'r') as f:
            self.json_settings = json.load(f)

    def check_preferences(self):
        # СРАВНИВАЕМ УДАЛЁННЫЕ НАСТРОЙКИ

        New_JSON_Settings = {}
        for Preset in self.json_settings.items():
            PresetName = Preset[0]
            if PresetName in self.default_parameters:
                if self.debug: print('EXISTS: ', PresetName)
                New_JSON_Settings[PresetName] = Preset[1]
            else:
                if self.debug: print('NOT FOUND, DELETED:', PresetName)

        # СРАВНИВАЕМ НОВЫЕ НАСТРОЙКИ
        Super_JSON_Settings = {}
        for DefaultPreset in self.default_parameters.items():
            DefaultPresetName = DefaultPreset[0]
            if DefaultPresetName in New_JSON_Settings:
                if self.debug: print('OLD: ', DefaultPresetName)
                Super_JSON_Settings[DefaultPresetName] = New_JSON_Settings[DefaultPresetName]
            else:
                if self.debug: print('NEW: ', DefaultPresetName)
                Super_JSON_Settings[DefaultPresetName] = DefaultPreset[1][1]
        self.json_settings = Super_JSON_Settings
        self.json_settings_save()

    @property
    def settings(self):
        return self.json_settings

    def save(self):
        self.json_settings_save()

    @property
    def update(self):
        self.json_settings_load()
        return self.json_settings