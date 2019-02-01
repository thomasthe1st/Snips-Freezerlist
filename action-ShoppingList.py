#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
import io
from shoppinglist import ShoppingList


USERNAME_INTENTS = "domi"


def user_intent(intentname):
    return USERNAME_INTENTS + ":" + intentname


def read_configuration_file(configuration_file):
    try:
        cp = configparser.ConfigParser()
        with io.open(configuration_file, encoding="utf-8") as f:
            cp.read_file(f)
        return {section: {option_name: option for option_name, option in cp.items(section)}
                for section in cp.sections()}
    except (IOError, configparser.Error):
        return dict()


def subscribe_intent_callback(hermes, intent_message):
    # conf = read_configuration_file(CONFIG_INI)
    intentname = intent_message.intent.intent_name
    if intentname == user_intent("addShoppingListItem"):
        result_sentence = shoppinglist.add_item(intent_message)
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    elif intentname == user_intent("removeShoppingListItem"):
        result_sentence = shoppinglist.remove_item(intent_message)
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    elif intentname == user_intent("isItemOnShoppingList"):
        result_sentence = shoppinglist.is_item(intent_message)
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    elif intentname == user_intent("clearShoppingList"):
        result_sentence = shoppinglist.try_clear()
        if result_sentence == "empty":
            result_sentence = "Die Einkaufsliste ist schon leer."
            hermes.publish_end_session(intent_message.session_id, result_sentence)
        else:
            shoppinglist.wanted_intents = [user_intent("confirmShoppingList")]
            hermes.publish_continue_session(intent_message.session_id, result_sentence,
                                            shoppinglist.wanted_intents)
        
    elif intentname == user_intent("confirmShoppingList"):
        if user_intent("confirmShoppingList") in shoppinglist.wanted_intents:
            shoppinglist.wanted_intents = []
            result_sentence = shoppinglist.clear_confirmed(intent_message)
            hermes.publish_end_session(intent_message.session_id, result_sentence)
    
    elif intentname == user_intent("showShoppingList"):
        result_sentence = shoppinglist.show()
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    elif intentname == user_intent("sendShoppingList"):
        result_sentence = shoppinglist.send()
        hermes.publish_end_session(intent_message.session_id, result_sentence)


if __name__ == "__main__":
    config = read_configuration_file("config.ini")
    shoppinglist = ShoppingList(config)
    with Hermes("localhost:1883") as h:
        h.subscribe_intents(subscribe_intent_callback).start()
