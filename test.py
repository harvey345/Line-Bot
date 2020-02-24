from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Og8TcoBMDiKfW9wZb25EdQropFnyt12Cu2JjRveX3/3hcqyxZhHj7dcEiF5k27/MgVigk6cB9KFnHg7TcxQFj9RWyg364oSGXF/Cz1nt+Ofg9yYwEEC87Np/0KWZWASGvOKIPpmUpZzj60DYqG3KMgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('376d17a639051188378e5ee8ce84f401')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()