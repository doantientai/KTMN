#Python libraries that we need to import for our bot
# import random
from flask import Flask, request
from pymessenger.bot import Bot
# import urllib.request
# from bs4 import BeautifulSoup
from random import randint
from time import gmtime, strftime
from flask_sslify import SSLify

LOG_FILE = "tai/logs/feedback.txt"
DEBUG = False
version = "VIET"
# version = "NIV"
language = "vi"
current_feeling = None
current_verse = None

if version == "VIET":
	from bibles import VIET as bible

if language == "en":
    from languages import en as strings
elif language == "vi":
    from languages import vi as strings

#conversation_states: sleep, welcome, choosing, showing, ending
conversation_state = "sleep"

app = Flask(__name__)
sslify = SSLify(app)
ACCESS_TOKEN = 'EAAHMlABZAqXQBAF6bSsas3LZAKj7mRSIyZB7vi00pVmfddPWgTmwNquZB2xqUtkYjDbM3YHrkXucje6mLm0zMZCrv9ZA6AjCI0eD2qnvt4TE7Q16PtzlL0bEKuBxqw85hs8fu8sJatKcun8A8ZBZCuYTz08rZCtPHBzBi3TiN9yq1hXkT5LualFKd'
VERIFY_TOKEN = 'PyMessenger_0'
# bot = Bot(ACCESS_TOKEN)

# list_emotion_vi = ["vui", "buồn"]
# list_emotion_en = ["joy","trust","motivation","confident","love","tired","anxious","anger","sad","sinful","fear"]

# list_emotion = list_emotion_en
list_emotion = []
for feel in strings.feelings:
    list_emotion.append(strings.feelings[feel])


class Bot_new(Bot):
    def send_quick_replies(self, recipient_id, question, list_replies):
        """Send an attachment to the specified recipient using URL.
        Input:
            recipient_id: recipient id to send to
            attachment_type: type of attachment (image, video, audio, file)
            attachment_url: URL of attachment
        Output:
            Response from API as <dict>
        """

        replies = []
        for reply in list_replies:
            quick_reply = {
            "content_type":"text",
            "title": reply,
            "payload":"<POSTBACK_PAYLOAD>",
            # "image_url":"http://example.com/img/red.png"
            }
            replies.append(quick_reply)

        return self.send_message(recipient_id, {
            "text": question,
            "quick_replies": replies
        })

bot = Bot_new(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    # response_sent_text = get_message()
                    if DEBUG:
                        bot.send_text_message(recipient_id, "DEBUG: " + message['message'].get('text'))
                    handle_conversation_state(recipient_id, message['message'].get('text'))

                #if user sends us a GIF, photo,video, or any other non-text item
                # if message['message'].get('attachments'):
                #     response_sent_nontext = get_message()
                #     send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def handle_input_emo(recipient_id, response):
    global current_feeling
    global current_verse
    global conversation_state
    if response in list_emotion:
        if DEBUG:
            bot.send_text_message(recipient_id, "DEBUG: emotion_found")

        current_feeling = response

        ### get key by value
        for emo in strings.feelings:
            if strings.feelings[emo] == response:
                list_verse_match_emotion = bible.bible[emo]
                break

        # bot.send_text_message(recipient_id, "DEBUG: got list")
        number_rand = randint(0,len(list_verse_match_emotion))
        verse_string = list_verse_match_emotion[number_rand]

        ### get current verse for feedback purpose

        current_verse = verse_string

        ### showing result
        bot.send_text_message(recipient_id, strings.text["results"])
        bot.send_quick_replies(recipient_id, verse_string, [strings.button_label["like"], strings.button_label["dislike"]])

        conversation_state = "showing"

    else:
        if DEBUG:
            bot.send_text_message(recipient_id, "DEBUG: emotion_not_found:")
        # bot.send_text_message(recipient_id, strings.text["complain"])
        # bot.send_quick_replies(recipient_id, strings.text["choose_feeling"], list_emotion)
        # conversation_state = "choosing"
        typed_response(recipient_id)

def get_addr_from_str(verse):
    index_quote_close = verse.rfind("\"")
    addr = verse[index_quote_close+4:]
    return addr

def log_feedback(recipient_id, current_feeling, current_verse, feedback):
    time_str = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    addr = get_addr_from_str(current_verse)
    with open(LOG_FILE, "a") as text_file:
        text_file.write(time_str + "\t" + recipient_id + "\t" + addr + "\t" + current_feeling + "\t" + str(feedback) + "\n")
        # text_file.write("jo" + "\n")
    # if DEBUG:
    #     bot.send_text_message(recipient_id, "DEBUG: done log")

def typed_response(recipient_id):
    global conversation_state
    bot.send_text_message(recipient_id, strings.text["complain"])
    bot.send_quick_replies(recipient_id, strings.text["start_over_below"], [strings.button_label["start"]])
    conversation_state = "welcome"

def handle_conversation_state(recipient_id, response):
    global conversation_state
    if DEBUG:
        bot.send_text_message(recipient_id, "DEBUG: " + conversation_state)

    if conversation_state == "sleep":
        bot.send_text_message(recipient_id, strings.text["welcome"])
        bot.send_text_message(recipient_id, strings.text["intro"])
        bot.send_quick_replies(recipient_id, strings.text["start_below"], [strings.button_label["start"]])
        conversation_state = "welcome"

    elif conversation_state == "welcome":
        if response == strings.button_label["start"]:
            bot.send_quick_replies(recipient_id, strings.text["choose_feeling"], list_emotion)
            conversation_state = "choosing"
        else:
            bot.send_quick_replies(recipient_id, strings.text["start_below"], [strings.button_label["start"]])

    elif conversation_state == "choosing":
        handle_input_emo(recipient_id, response)

    elif conversation_state == "showing":
        if response == strings.button_label["like"]:
            bot.send_text_message(recipient_id, strings.text["liked"])
            bot.send_quick_replies(recipient_id, strings.text["want_another_verse"], [strings.button_label["another_verse"], strings.button_label["no_more_verse"]])
            # global conversation_state
            conversation_state = "more_or_not"
            # if DEBUG:
            #     bot.send_text_message(recipient_id, "DEBUG: it should be more_or_not: " + conversation_state)
            log_feedback(recipient_id, current_feeling, current_verse, "like")

        elif response == strings.button_label["dislike"]:
            bot.send_text_message(recipient_id, strings.text["disliked"])
            bot.send_quick_replies(recipient_id, strings.text["me_try_again"], [strings.button_label["another_verse"], strings.button_label["no_more_verse"]])
            conversation_state = "more_or_not"
            # handle_input_emo(recipient_id, current_feeling)
            log_feedback(recipient_id, current_feeling, current_verse, "dislike")

        else:
            typed_response(recipient_id)
            # bot.send_quick_replies(recipient_id, strings.text["start_below"], [strings.button_label["start"]])
            # bot.send_text_message(recipient_id, strings.text["complain"])
            # bot.send_quick_replies(recipient_id, strings.text["choose_feeling"], list_emotion)
            # conversation_state = "choosing"
            # global conversation_state
            # conversation_state = "welcome"


    elif conversation_state == "more_or_not":
        if response == strings.button_label["another_verse"]:
            bot.send_quick_replies(recipient_id, strings.text["choose_feeling"], list_emotion)
            conversation_state = "choosing"
        elif response == strings.button_label["no_more_verse"]:
            bot.send_quick_replies(recipient_id, strings.text["seya"], [strings.button_label["start"]])
            conversation_state = "welcome"
        else:
            if DEBUG:
                bot.send_text_message(recipient_id, "DEBUG: strange state: " + conversation_state)
            typed_response(recipient_id)
            # bot.send_text_message(recipient_id, strings.text["complain"])
            # bot.send_quick_replies(recipient_id, strings.text["choose_feeling"], list_emotion)
            # conversation_state = "choosing"

    else:
        if DEBUG:
            bot.send_text_message(recipient_id, "DEBUG: strange state: " + conversation_state)
        typed_response(recipient_id)
        # bot.send_text_message(recipient_id, strings.text["complain"])
        # bot.send_quick_replies(recipient_id, strings.text["choose_feeling"], list_emotion)
        # conversation_state = "choosing"

#uses PyMessenger to send response to user
# def send_message(recipient_id, response):
#     #sends user the text message provided via input response parameter
#     bot.send_text_message(recipient_id, response)
#     return "success"

if __name__ == "__main__":
    app.run()