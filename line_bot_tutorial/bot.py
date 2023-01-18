from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, TemplateSendMessage, StickerSendMessage, ButtonsTemplate, ImageSendMessage, CarouselTemplate, CarouselColumn, MessageTemplateAction, PostbackTemplateAction
from urllib.parse import parse_qsl

line_bot_api = LineBotApi('CHANNEL ACCESS TOKEN')
handler = WebhookHandler('CHANNEL SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text = True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@噢':
        try:
            message = TextSendMessage(
                text = 'You sent \"oh\"'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='ERROR'))
    elif mtext == '@嗨':
        try:
            send_button_template(event)                
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='ERROR'))
    elif mtext == '@嘿':
        try:
            sticker_message = StickerSendMessage(
                package_id = 789,
                sticker_id = 10863
            )
            line_bot_api.reply_message(event.reply_token, sticker_message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='ERROR'))
    elif mtext == '@齁':
        try:
            send_carousel(event)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='ERROR'))
    elif mtext == '@欸':
        try:
            message = ImageSendMessage(
                original_content_url = 'https://rimage.gnst.jp/livejapan.com/public/article/detail/a/00/00/a0000370/img/basic/a0000370_main.jpg?20201002142956&q=80&rw=750&rh=536',
                preview_image_url = 'https://rimage.gnst.jp/livejapan.com/public/article/detail/a/00/00/a0000370/img/basic/a0000370_main.jpg?20201002142956&q=80&rw=750&rh=536'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='ERROR'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

@handler.add(PostbackEvent)
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))
    if backdata.get('choice') == 'Chocolate':
        message = StickerSendMessage(
            package_id = 789,
            sticker_id = 10869
        )
        line_bot_api.reply_message(event.reply_token, message)    
    elif backdata.get('choice') == 'Honey':
        message = StickerSendMessage(
            package_id = 8522,
            sticker_id = 16581276
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif backdata.get('choice') == 'Butter':
        message = StickerSendMessage(
            package_id = 11537,
            sticker_id = 52002762
        )
        line_bot_api.reply_message(event.reply_token, message)


def send_button_template(event):
    message = TemplateSendMessage(
        alt_text = "template message not supported",
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://www.allrecipes.com/thmb/3uPX0T-lD38fbTLJtKqOR359qpc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20334-Banana-Pancakes-mfs__2x3-21fe4c9bcb35452dacd21d2f76639e13.jpg',
            title = 'Some pancakes?',
            text = 'Choose flavors:',
            actions = [
                PostbackTemplateAction(
                    label = 'Chocolate',
                    data = 'choice=Chocolate'
                ),
                PostbackTemplateAction(
                    label = 'Honey',
                    data = 'choice=Honey'
                ),
                PostbackTemplateAction(
                    label = 'Butter',
                    data = 'choice=Butter'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def send_carousel(event):
    message = TemplateSendMessage(
        alt_text = 'carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fimg1.cookinglight.timeinc.net%2Fsites%2Fdefault%2Ffiles%2Fstyles%2Fmedium_2x%2Fpublic%2F1542062283%2Fchocolate-and-cream-layer-cake-1812-cover.jpg%3Fitok%3DrEWL7AIN',
                    title='Cake',
                    text='Choose a flavor',
                    actions=[
                        MessageTemplateAction(
                            label = 'Banana',
                            text = 'Banana cake'
                        ),
                        MessageTemplateAction(
                            label = 'Coffee',
                            text = 'Coffee cake'
                        ),
                        MessageTemplateAction(
                            label = 'Pandan',
                            text = 'Pandan cake'
                        ),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://www.foodandwine.com/thmb/Dl7L5u2c7sbVp6vyxnqhcxz9M50=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Super-Scoops-FT-2-MAG0622-00568f6534a44e0c8a422b66b25d6cf6.jpg',
                    title='Ice Cream',
                    text='Choose a flavor',
                    actions=[
                        MessageTemplateAction(
                            label = 'Vanilla',
                            text = 'Vanilla ice cream'
                        ),
                        MessageTemplateAction(
                            label = 'Strawberry',
                            text = 'Strawberry ice cream'
                        ),
                        MessageTemplateAction(
                            label = 'Coconut',
                            text = 'Coconut ice cream'
                        ),
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == '__main__':
    app.run()
