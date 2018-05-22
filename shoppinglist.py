# -*- coding: utf-8 -*-
import pickle
import random
import io


class ShoppingList:
    def __init__(self):
        self.wanted_intents = []  # For reacting only with wanted intents
        self.shoppinglist_path = ".shoppinglist"
        try:
            with io.open(self.shoppinglist_path, 'rb') as f:
                itemlist = pickle.load(f)
            print("opened:", itemlist)
        except EOFError as e:  # if no list in file
            print("eerrroorr:", e)
        io.open(self.shoppinglist_path, 'a').close()  # Create file, if not available
        self.shoppinglist = self.read_shoppinglist()

    def add_item(self, intentMessage):
        item = intentMessage.slots.item.first().value
        if item in self.shoppinglist:
            response = random.choice(["{item} steht schon auf der Liste.".format(item=str(item)),
                                      "{item} ist auf der Liste schon vorhanden.".format(item=str(item))])
        else:
            self.shoppinglist.append(item)
            self.save_shoppinglist()
            response = random.choice(["{item} wurde hinzugefügt.".format(item=str(item)),
                                      "{item} wurde auf die Einkaufsliste geschrieben.".format(item=str(item))])
        return response

    def remove_item(self, intentMessage):
        item = intentMessage.slots.item.first().value
        if item in self.shoppinglist:
            self.shoppinglist.remove(item)
            self.save_shoppinglist()
            response = "{item} wurde von der Einkaufsliste entfernt.".format(item=str(item))
        else:
            response = "{item} ist auf der Einkaufsliste nicht vorhanden.".format(item=str(item))
        return response

    def is_item(self, intentMessage):
        item = intentMessage.slots.item.first().value
        if item in self.shoppinglist:
            response = "Ja, {item} steht auf der Einkaufsliste.".format(item=str(item))
        else:
            response = "Nein, {item} ist nicht auf der Einkaufsliste.".format(item=str(item))
        return response

    def try_clear(self):
        if len(self.shoppinglist) > 1:
            response = "Die Einkaufsliste enthält noch {num} Elemente." \
                       "Bist du dir sicher?".format(num=len(self.shoppinglist))
        elif len(self.shoppinglist) == 1:
            response = "Die Einkaufsliste enthält noch ein Element. Bist du dir sicher?"
        else:
            response = 1  # Error: Shoppinglist is already empty - no dialogue start
        return response

    def clear_confirmed(self, intentMessage):
        if intentMessage.slots.answer.first().value == "yes":
            self.shoppinglist = []
            self.save_shoppinglist()
            return "Die Einkaufsliste wurde geleert."
        else:
            return "Die Einkaufsliste wurde nicht geleert."

    def show(self):
        if len(self.shoppinglist) > 1:
            shoppinglist_str = ""
            for item in self.shoppinglist[:-1]:
                shoppinglist_str = shoppinglist_str + item + ", "
            response = "Die Einkaufsliste enthält {items}und {last}.".format(items=shoppinglist_str,
                                                                             last=self.shoppinglist[-1])
        elif len(self.shoppinglist) == 1:
            response = "Die Einkaufsliste enthält nur {item}.".format(item=self.shoppinglist[0])
        else:  # If shoppinglist is empty
            response = "Die Einkaufsliste ist leer."
        return response

    def read_shoppinglist(self):
        try:
            with io.open(self.shoppinglist_path, 'rb') as f:
                itemlist = pickle.load(f)
            return itemlist
        except EOFError:  # if no list in file
            return []

    def save_shoppinglist(self):
        with io.open(self.shoppinglist_path, "wb") as f:
            pickle.dump(self.shoppinglist, f)

