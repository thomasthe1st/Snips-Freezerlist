# -*- encoding: utf-8 -*-
import pickle
import random
import io


class ShoppingList:
    def __init__(self):
        self.wanted_intents = []  # For reacting only with wanted intents
        self.shoppinglist_path = ".shoppinglist"
        io.open(self.shoppinglist_path, 'a').close()  # Create file, if not available
        self.shoppinglist = self.read_shoppinglist()

    def add_item(self, intentMessage):
        item_list = [item.value.encode('utf8') for item in intentMessage.slots.item.all()]
        dublicate_items = []
        added_items = []
        for item in item_list:
            if item in self.shoppinglist:
                dublicate_items.append(item)
            else:
                added_items.append(item)
                self.shoppinglist.append(item)
        response = ""
        if added_items:
            items_str = "".join(item + ", " for item in added_items[:-1])
            if len(added_items) >= 2:
                items_str += "und {} ".format(added_items[-1])
                word_pl_sg = "wurden"
            else:
                items_str += "{} ".format(added_items[-1])
                word_pl_sg = "wurde"
            first_str = items_str + random.choice(["{} hinzugefügt".format(word_pl_sg),
                                                   "{} auf die Einkaufsliste geschrieben".format(word_pl_sg)])
            if not dublicate_items:
                first_str += "."
            else:
                first_str += ", aber "
            response += first_str
        if dublicate_items:
            items_str = "".join(item + ", " for item in dublicate_items[:-1])
            if len(dublicate_items) >= 2:
                items_str += "und {} ".format(dublicate_items[-1])
                word_pl_sg = "sind"
            else:
                items_str += "{} ".format(dublicate_items[-1])
                word_pl_sg = "ist"
            second_str = items_str + random.choice(["{} schon auf der Liste.".format(word_pl_sg),
                                                    "{} auf der Liste schon vorhanden.".format(word_pl_sg)])
            response += second_str
        self.save_shoppinglist()
        return response.decode('utf8')

    def remove_item(self, intentMessage):
        item_list = intentMessage.slots.item.all()
        notlist_items = []
        removed_items = []
        for item in item_list:
            if item.value in self.shoppinglist:
                removed_items.append(item.value)
                self.shoppinglist.remove(item.value)
            else:
                notlist_items.append(item.value)
        response = ""
        if removed_items:
            items_str = "".join(item + ", " for item in removed_items[:-1])
            if len(removed_items) >= 2:
                items_str += "und {} ".format(removed_items[-1])
                word_pl_sg = "wurden"
            else:
                items_str += "{} ".format(removed_items[-1])
                word_pl_sg = "wurde"
            first_str = items_str + random.choice(["{} entfernt".format(word_pl_sg),
                                                   "{} von der Einkaufsliste entfernt".format(word_pl_sg)])
            if not notlist_items:
                first_str += "."
            else:
                first_str += ", aber "
            response += first_str
        if notlist_items:
            items_str = "".join(item + ", " for item in notlist_items[:-1])
            if len(notlist_items) >= 2:
                items_str += "und {} ".format(notlist_items[-1])
                word_pl_sg = "sind"
            else:
                items_str += "{} ".format(notlist_items[-1])
                word_pl_sg = "ist"
            second_str = items_str + random.choice(["{} nicht auf der Liste.".format(word_pl_sg),
                                                    "{} auf der Einkaufsliste nicht vorhanden.".format(word_pl_sg)])
            response += second_str
        self.save_shoppinglist()
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
                       " Bist du dir sicher?".format(num=len(self.shoppinglist))
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
                shoppinglist_str = shoppinglist_str + str(item) + ", "
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

