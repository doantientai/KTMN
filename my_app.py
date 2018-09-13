#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)
ACCESS_TOKEN = 'EAAHMlABZAqXQBAF6bSsas3LZAKj7mRSIyZB7vi00pVmfddPWgTmwNquZB2xqUtkYjDbM3YHrkXucje6mLm0zMZCrv9ZA6AjCI0eD2qnvt4TE7Q16PtzlL0bEKuBxqw85hs8fu8sJatKcun8A8ZBZCuYTz08rZCtPHBzBi3TiN9yq1hXkT5LualFKd'
VERIFY_TOKEN = 'PyMessenger_0'
list_emotion_vi = ["vui", "buồn"]
list_emotion_en = ["sad", "happy"]


class Bot_new(Bot):

    # def send_welcome_message(self, recipient_id):
    #     return self.send_raw( recipient_id, {
    #         "setting_type":"call_to_actions",
    #         "thread_state":"new_thread",
    #         "call_to_actions":[
    #             {
    #             "message":{"text":"Welcome!"
    #                 }}]})

    def send_quick_replies (self, recipient_id, question):
        """Send an attachment to the specified recipient using URL.
        Input:
            recipient_id: recipient id to send to
            attachment_type: type of attachment (image, video, audio, file)
            attachment_url: URL of attachment
        Output:
            Response from API as <dict>
        """
        return self.send_message(recipient_id, {
            "text": question,
            "quick_replies":[
              {
                "content_type":"text",
                "title":"vui",
                "payload":"<POSTBACK_PAYLOAD>",
                # "image_url":"http://example.com/img/red.png"
              },
              {
                "content_type":"text",
                "title":"buồn",
                "payload":"<POSTBACK_PAYLOAD>",
                # "image_url":"http://example.com/img/red.png"
              }
            ]
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
                # message = messaging[-1]
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        # send_button_message(recipient_id, "Bấm vào đây", "vui")
                        # handle_response(recipient_id=recipient_id, response=message['message'].get('text'))
                        send_message(recipient_id, "Chọn cảm xúc phù hợp với bạn:")


                        # send_message(recipient_id, get_verse_list("joy"))
                        # get_verse_list("joy")
                        # response_sent_text = get_message()
                        # send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    # if message['message'].get('attachments'):
                    #     response_sent_nontext = get_message()
                    #     send_message(recipient_id, response_sent_nontext)
                # messaging_postbacks = event['messaging_postbacks']
                return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    print("response: ", response)
    bot.send_text_message(recipient_id, response)
    return "success"


def send_quick_replies(recipient_id, question):
    #sends user the text message provided via input response parameter
    # print("response: ", response)
    bot.send_quick_replies(recipient_id, question)
    return "success"

def handle_response(recipient_id, response):
    print("handling response...")
    # if response in list_emotion_vi:
    #     print("found response ", response, " in list_emotion_vi")
    #     send_message(recipient_id, "Mình nghĩ câu Kinh Thánh dưới đây sẽ phù hợp với cảm xúc \"" + response + "\" của bạn")
    #     emotion_en = list_emotion_en[list_emotion_vi.index(response)]
    #     send_message(recipient_id, get_verse.get_verse_by_feeling(emotion_en))
    # else:
    #     print("response NOT found in list_emotion_vi")
    #     send_message(recipient_id, "Hãy để mình tìm giúp bạn một câu Kinh Thánh phù hợp với cảm xúc của bạn nhé!")
    #     send_quick_replies(recipient_id, "Bạn đang cảm thấy:")
    return "success"



if __name__ == "__main__":
    app.run()
