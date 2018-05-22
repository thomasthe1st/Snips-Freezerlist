#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from shoppinglist import ShoppingList


def subscribe_intent_callback(hermes, intentMessage):
    # conf = read_configuration_file(CONFIG_INI)
    intentname = intentMessage.intent.intent_name
    if intentname == "domi:addShoppingListItem":
        result_sentence = shoppinglist.add_item(intentMessage)
        hermes.publish_end_session(intentMessage.session_id, result_sentence)

    elif intentname == "domi:removeShoppingListItem":
        result_sentence = shoppinglist.remove_item(intentMessage)
        hermes.publish_end_session(intentMessage.session_id, result_sentence)

    elif intentname == "domi:isItemOnShoppingList":
        result_sentence = shoppinglist.is_item(intentMessage)
        hermes.publish_end_session(intentMessage.session_id, result_sentence)

    elif intentname == "domi:clearShoppingList":
        result_sentence = shoppinglist.try_clear()
        if result_sentence == 1:
            result_sentence = "Die Einkaufsliste ist schon leer."
            hermes.publish_end_session(intentMessage.session_id, result_sentence)
        else:
            shoppinglist.wanted_intents = ['domi:confirmShoppingList']
            hermes.publish_end_session(intentMessage.session_id, result_sentence,
                                       shoppinglist.wanted_intents)
        
    elif intentname == "domi:confirmShoppingList":
        if "domi:confirmShoppingList" in shoppinglist.wanted_intents:
            shoppinglist.wanted_intents = []
            result_sentence = shoppinglist.clear_confirmed(intentMessage)
            hermes.publish_end_session(intentMessage.session_id, result_sentence)
    
    elif intentname == "domi:showShoppingList":
        result_sentence = shoppinglist.show()
        hermes.publish_end_session(intentMessage.session_id, result_sentence)


if __name__ == "__main__":
    shoppinglist = ShoppingList()
    with Hermes("localhost:1883") as h:
        h.subscribe_intents(subscribe_intent_callback).start()
