# -*- coding: utf-8 -*-
import pickle
import random
import io
from ast import literal_eval
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import socket


class FreezerList:
    def __init__(self, config):
        self.config = config
        self.wanted_intents = []  # For reacting only with wanted intents
        self.freezerlist_path = ".freezerlist"
        io.open(self.freezerlist_path, 'a').close()  # Create file, if not available
        self.freezerlist = self.read_freezerlist()

    def add_item(self, intentmessage):
        item_list = [item.value for item in intentmessage.slots.item.all()]
        dublicate_items = [item for item in item_list if item in self.freezerlist]
        added_items = [item for item in item_list if item not in self.freezerlist]
        for item in added_items:
            self.freezerlist.append(item)

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
                                                   "{} auf die Tiefkühlliste geschrieben".format(word_pl_sg)])
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
        self.save_freezerlist()
        return response

    def remove_item(self, intentmessage):
        item_list = [item.value for item in intentmessage.slots.item.all()]
        notlist_items = [item for item in item_list if item not in self.freezerlist]
        removed_items = [item for item in item_list if item in self.freezerlist]
        self.freezerlist = [item for item in self.freezerlist if item not in removed_items]

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
                                                   "{} von der Tiefkühlliste entfernt".format(word_pl_sg)])
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
                                                    "{} auf der Tiefkühlliste nicht vorhanden.".format(word_pl_sg)])
            response += second_str
        self.save_freezerlist()
        return response

    def is_item(self, intentmessage):
        item = intentmessage.slots.item.first().value
        if item in self.freezerlist:
            response = "Ja, {item} steht auf der Tiefkühlliste.".format(item=str(item))
        else:
            response = "Nein, {item} ist nicht auf der Tiefkühlliste.".format(item=str(item))
        return response

    def try_clear(self):
        if len(self.freezerlist) > 1:
            response = "Die Tiefkühlliste enthält noch {num} Elemente." \
                       " Bist du dir sicher?".format(num=len(self.freezerlist))
        elif len(self.freezerlist) == 1:
            response = "Die Tiefkühlliste enthält noch ein Element. Bist du dir sicher?"
        else:
            response = "empty"  # Error: Shoppinglist is already empty - no dialogue start
        return response

    def clear_confirmed(self, intentmessage):
        if intentmessage.slots.answer.first().value == "yes":
            self.freezerlist = []
            self.save_freezerlist()
            return "Die Tiefkühlliste wurde geleert."
        else:
            return "Die Tiefkühlliste wurde nicht geleert."

    def show(self):
        if len(self.freezerlist) > 1:
            freezerlist_str = ""
            for item in self.freezerlist[:-1]:
                freezerlist_str = freezerlist_str + str(item) + ", "
            response = "Die Tiefkühlliste enthält {items}und {last}.".format(
                items=freezerlist_str, last=self.freezerlist[-1])
        elif len(self.freezerlist) == 1:
            response = "Die Tiefkühlliste enthält nur {item}.".format(item=self.freezerlist[0])
        else:  # If freezerlist is empty
            response = "Die Tiefkühlliste ist leer."
        return response

    def send(self):
        if len(self.freezerlist) == 0:
            return "Die Tiefkühlliste ist leer. Eine Email ist daher überflüssig."

        try:
            email_dict = literal_eval(self.config['secret']['email_data'])
            email_dict = dict((key.lower(), value) for key, value in email_dict.items())
            param_names = ["from", "password", "host", "port", "to"]
            good_params = [key for key in email_dict if key in param_names and email_dict.get(key)]
            bad_params = [name for name in param_names if name not in good_params]
        except (ValueError, KeyError) as e:
            email_dict = {}
            bad_params = []
            print("Error: ", e)
        if not email_dict:
            response = "Der Email-Versand ist nicht eingerichtet: Es konnten keine Parameter gefunden werden. " \
                       "Bitte schaue in der Beschreibung dieser App nach, wie man den Versand einrichtet."
            return response
        elif bad_params:
            response = "Der Email-Versand ist falsch eingerichtet. Es fehlen notwendige Parameter."
            print("Fehler: " + response + "\nFehlende Parameter:\n\t" + str(bad_params))
            return response

        msg = MIMEMultipart()
        msg['From'] = email_dict['from']
        msg['To'] = email_dict['to']
        now = datetime.datetime.now()
        now_date = now.strftime("%d.%m.%Y")
        now_time = now.strftime("%H:%M Uhr")
        msg['Subject'] = "Deine Tiefkühlliste vom {date}".format(date=now_date)

        emailtext = "Du hast eine Email mit deiner <b>Tiefkühlliste</b> bekommen, weil du es "
        emailtext += "am {date} um {time} so wolltest.</br></br>".format(date=now_date, time=now_time)
        emailtext += "Hier ist die Liste:<ul>"
        for item in self.freezerlist:
            emailtext += "<li>{item}</li>".format(item=item)
        emailtext += '</ul></br></br></br>Diese Mail wurde automatisch generiert von der App '
        emailtext += '<a href="https://console.snips.ai/store/de/skill_Va52B5v45GB">Tiefkühlliste</a> '
        emailtext += 'aus dem Snips App Store. Der Quellcode ist frei und kann auf Github '
        emailtext += '<a href="https://github.com/thomasthe1st/Snips-Freezer">hier</a> eingesehen werden. '
        emailtext += 'Die Anmeldedaten, die für den Versand benötigt werden, sind lokal im System, auf dem Snips '
        emailtext += 'läuft, gespeichert.'

        msg.attach(MIMEText(emailtext, 'html', 'utf-8'))

        try:
            server = smtplib.SMTP(email_dict['host'], int(email_dict['port']), timeout=1)
        except socket.gaierror:
            response = "Die Email konnte nicht versendet werden, weil der Host oder Port nicht erreichbar ist."
            return response
        except socket.timeout:
            response = "Die Email konnte nicht versendet werden, weil die Anmeldezeit überschritten wurde. " \
                       "Vermutlich ist der Port nicht richtig eingestellt."
            return response

        try:
            server.starttls()
            server.login(email_dict['from'], email_dict['password'])
            text = msg.as_string()
            server.sendmail(email_dict['from'], email_dict['to'], text)
            response = "Die Tiefkühlliste wurde als Email versendet."
        except smtplib.SMTPAuthenticationError:
            response = "Die Email konnte nicht versendet werden, weil die Anmeldedaten ungültig sind."
        except smtplib.SMTPRecipientsRefused:
            response = "Die Email konnte nicht versendet werden, weil die Empfängeradresse diese nicht angenommen " \
                       "hat. Vermutlich ist sie nicht richtig eingestellt."
        finally:
            server.quit()
        return response

    def read_freezerlist(self):
        try:
            with io.open(self.freezerlist_path, 'rb') as f:
                itemlist = pickle.load(f)
            return itemlist
        except EOFError:  # if no list in file
            return []

    def save_freezerlist(self):
        with io.open(self.freezerlist_path, "wb") as f:
            pickle.dump(self.freezerlist, f)
