#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ontology.dialogue import DialogueConfiguration
import io
from shoppinglist import ShoppingList


USERNAME_INTENTS = "domi"


def add_prefix(intentname):
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


def intent_callback(hermes, intent_message):
    # conf = read_configuration_file(CONFIG_INI)
    intentname = intent_message.intent.intent_name
    if intentname == add_prefix("addShoppingListItem"):
        result_sentence = shoppinglist.add_item(intent_message)
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    elif intentname == add_prefix("removeShoppingListItem"):
        result_sentence = shoppinglist.remove_item(intent_message)
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    elif intentname == add_prefix("isItemOnShoppingList"):
        result_sentence = shoppinglist.is_item(intent_message)
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    elif intentname == add_prefix("clearShoppingList"):
        result_sentence = shoppinglist.try_clear()
        if result_sentence == "empty":
            result_sentence = "Die Einkaufsliste ist schon leer."
            hermes.publish_end_session(intent_message.session_id, result_sentence)
        else:
            shoppinglist.wanted_intents = [add_prefix("confirmShoppingList")]
            dialogue_conf = DialogueConfiguration().enable_intent(add_prefix("confirmShoppingList"))
            hermes.configure_dialogue(dialogue_conf)
            hermes.subscribe_intent_not_recognized(intent_not_recognized_callback)
            hermes.publish_continue_session(intent_message.session_id, result_sentence,
                                            shoppinglist.wanted_intents)
        
    elif intentname == add_prefix("confirmShoppingList"):
        shoppinglist.wanted_intents = []
        result_sentence = shoppinglist.clear_confirmed(intent_message)
        hermes.publish_end_session(intent_message.session_id, result_sentence)
    
    elif intentname == add_prefix("showShoppingList"):
        result_sentence = shoppinglist.show()
        hermes.publish_end_session(intent_message.session_id, result_sentence)

    elif intentname == add_prefix("sendShoppingList"):
        result_sentence = shoppinglist.send()
        hermes.publish_end_session(intent_message.session_id, result_sentence)


def intent_not_recognized_callback(hermes, intent_message):
    configure_message = DialogueConfiguration().disable_intent(add_prefix("confirmShoppingList"))
    hermes.configure_dialogue(configure_message)
    shoppinglist.wanted_intents = []
    hermes.publish_end_session({'sessionId': intent_message.session_id,
                                'text': "Die Einkaufsliste wurde nicht gelöscht."})


if __name__ == "__main__":
    config = read_configuration_file("config.ini")
    shoppinglist = ShoppingList(config)
    with Hermes("localhost:1883") as h:
        h.subscribe_intents(intent_callback)
        h.start()
