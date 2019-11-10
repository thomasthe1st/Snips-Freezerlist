# Snips-Freezerlist :memo:
With this app for [Snips.ai](https://snips.ai/) you can manage a freezerlist with your voice.

##### Table of Contents  
[Features](#i-features)  
[Installation](#ii-installation)  
[Configuration](#iii-configuration)  
[Usage](#iv-usage)  
[Troubleshooting](#v-troubleshooting)  
[Contribution](#vi-contribution)  


## I. Features

- Ability to send the freezerlist to an email address :postal_horn:

## II. Installation

:exclamation: The following instructions assume that [Snips](https://snips.gitbook.io/documentation/snips-basics) is
already configured and running on your device (e.g. a Raspberry Pi 3 from the 
[Snips Maker Kit](https://www.seeedstudio.com/snips.html) with 
[Raspbian](https://www.raspberrypi.org/downloads/raspbian/) Buster Lite). 
[SAM](https://snips.gitbook.io/getting-started/installation) should
also already be set up and connected to your device and your account.

1. In the German [app store](https://console.snips.ai/) add the
app `TK-liste` (by domi; [this](https://console.snips.ai/store/de/skill_Va52B5v45GB)) to
your *German* assistant.

2. If you already have the same assistant on your platform, update it with:
      ```bash
      sam update-assistant
      ```
      
   Otherwise install the assistant on the platform with the following command to
   choose it (if you have multiple assistants in your Snips console):
      ```bash
      sam install assistant
      ```

3. With using SAM you will be asked to enter something
for the parameter "email_data". Below in the next section you 
can found the explanation of it.
    
## III. Configuration

You can configure the app so that it is able to send an email
containing the freezerlist to an address.

:exclamation: Never enter credentials into a programm or website unless you know exactly what is happening to it.
In this case you can view the source code and see what is done
with it. The problem is that I could also simply insert code into the programm, which let it sent the login credentials
to me. But this should only be a warning, so that you know what is possible.
Be careful with your data!

The value of the parameter "email_data" is a string in form of a python dictionary.
Don't worry if you never heard of something like that.
Two curly brackets containing five items which are key-value pairs:
- "from": email address from which the freezerlist will be sent
- "password": password which belongs to the email address - Since I ported this app to Python 3 you can't have a `%` in
   your password anymore (I'm still trying to fix this).
- "host": SMTP host, ex.: "mail.gmx.net"
- "port": SMTP port, usually 587
- "to": email address to which the shopping list will be sent

The email address used in "FROM" and "TO" can be the same.

*Examples:*

`{"from": "meinemail@gmx.net", "password": "eb457fg9", "host":
"mail.gmx.net", "port": 587, "to": "meinemail@gmx.net"}`

`{"from": "hello@gmx.com", "password": "bo95345b3v", "host":
"mail.gmx.com", "port": 587, "to": "hello@gmx.com"}`

Don't forget all the quotation marks and the curly brackets at the beginning and at the end!

With a Google email configuration you have to enable the option called like "allow external apps to send emails".

The content of the `config.ini` file should look like this:

```
[secret]
email_data={"from": "meinemail@gmx.net", "password": "eb457fg9", "host":
"mail.gmx.com", "port": 587, "to": "hello@gmx.com"}
```

## IV. Usage

### 1. Example sentences

**Add item:**

- *Schreibe `Tomaten` auf meine Tiefkühlliste.*
- *Kannst du bitte `Brot` auf meiner Tiefkühlliste notieren?*

**Ask for item:**

- *Ist `Kuchen` schon auf der Tiefkühlliste?*
- *Stehen `Himbeeren` auf meiner Tiefkühlliste?*

**Get items:**

- *Was steht auf der Tiefkühlliste?*
- *Lese meine Tiefkühlliste vor.*

**Send list:**

- *Schicke meine Tiefkühlliste per Email.*
- *Ich möchte die Tiefkühlliste als Email auf mein Handy haben.*

**Delete item:**

- *Entferne `Himbeeren` von der Tiefkühlliste.*
- *Streiche `Buttergemüse` von der Tiefkühlliste weg.*
- *Ich habe keine `Pommes` mehr.*

**Delete list:**

- *Lösche die Tiefkühlliste.*
- *Entferne die gesamte Tiefkühlliste.*


## V. Troubleshooting

- The time in the emails is wrong.

    Make sure that the time and date are correct on your device.
    
- I cannot see an email in my inbox, but Snips said it has been sent.
    
    Have a look in your spam folder.

## VI. Contribution

Please report errors and bugs (you can see them with `sam service log snips-skill-server` or on the Pi
with `sudo tail -f /var/log/syslog`) by opening
a [new issue](https://github.com/MrJohnZoidberg/Snips-Freezerlist/issues/new).
You can also write other ideas for this app. Thank you for your contribution.

Made with :blue_heart:
