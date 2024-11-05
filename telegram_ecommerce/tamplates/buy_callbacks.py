from telegram import LabeledPrice
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    filters,
    PreCheckoutQueryHandler,
    MessageHandler)
import requests
from telegram_ecommerce.language import get_text
from telegram_ecommerce.utils.consts import provider_token, currency
from telegram_ecommerce.tamplates.rating import ask_if_user_want_avaluate_the_product
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo

from telegram_ecommerce.database.manipulation import (
    add_orders,
    product_has_purchased)


products_data_key = "list_of_products"
base_url = "https://api.ashewa.com"

def add_pre_checkout_query_to_user_data(context, query):
    context.user_data["last_order"] = query


async def send_a_shipping_message(update, context, product , pattern_identifier):
    title = product.get("name")
    description = product.get("description")
    product_id = product.get("id")
    prices = [LabeledPrice("Price", int( 100 * product.get("selling_price",1050)))]
    telebirr = InlineKeyboardButton("Telebirr", callback_data='telebirr')
    ethswitch = InlineKeyboardButton("Ethswitch", callback_data='ethswitch')
    inline_keyboard = InlineKeyboardMarkup([[telebirr, ethswitch]])
    user_id = update.effective_user.id
    context.transcation = {
        "product_id":product_id,
        "user_id":user_id,
        "price":324132

    }
    
    body =    { "user_id":user_id,
                "product_id": product_id,
                "quantity": 2
    }
    
    try:
        data = requests.post(f"{base_url}/bot/create-order/",body)
        print("data id= ",data.json().get("id"))
        # context.user_data['order_id'] = data.
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Please choose payment method",
            reply_markup=inline_keyboard,
            disable_notification=True
        )
    except requests.ConnectionError as e:
        print("error = ",e)
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{e}",
       
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Please choose payment method",
        reply_markup=inline_keyboard,
        disable_notification=True
    )
   

def process_order(query, product, context):
    PROCESS_OK, PROCESS_FAIL = (True, False)
    if query.invoice_payload != str(product.id):
        return (PROCESS_FAIL, get_text("information_dont_match", context))
    try:
        add_orders(
            query.id,
            (query.total_amount / 100),
            query.from_user.id,
            product.id)
        product_has_purchased(product.id)
        return (PROCESS_OK, None) 
    except:
        return (PROCESS_FAIL, get_text("error_in_orders", context))


async def pre_checkout_callback(update, context):
    query = update.pre_checkout_query
    add_pre_checkout_query_to_user_data(context, query)
    product = context.user_data[products_data_key]["products"].actual()
    (status, error_message) = process_order(query, product, context)
    if status:
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message=error_message)


async def successful_payment_callback(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    await update.message.reply_text(get_text("successful_payment", context))
    await ask_if_user_want_avaluate_the_product(update, context, product)


pre_checkout_handler = PreCheckoutQueryHandler(pre_checkout_callback)


successful_payment_handler = MessageHandler(
    filters.SUCCESSFUL_PAYMENT, successful_payment_callback)





async def payment_handler(update, context) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the button click

    # Handle the selected payment method
    if query.data == 'telebirr':
        await query.edit_message_text(text="You selected Telebirr. Proceeding with payment...")
        # Add further processing logic for Telebirr payment here
    elif query.data == 'ethswitch':
        await query.edit_message_text(text="You selected Ethswitch. Proceeding with payment...")
        # Add further processing logic for Ethswitch payment here

async def handle_payment_method_callback(update, context):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    # Get the payment method from the callback data
    payment_method = query.data

    if payment_method == 'telebirr':
            await query.message.reply_text(
                "Open Telebirr",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(
                            text="Telebirr!",
                            web_app=WebAppInfo(url="https://www.ethiotelecom.et/telebirr/")
                        )]
                    ],
                    resize_keyboard=True,  # Makes the keyboard smaller
                    one_time_keyboard=True  # Hides the keyboard after use
                )
            )
    
        # await context.bot.send_message(
        #     chat_id=query.message.chat.id,
        #     text="You chose Telebirr. Please follow the instructions to complete your payment."
        # )
        # Add more logic for handling Telebirr payment here

    elif payment_method == 'ethswitch':
        
            data = requests.post(f"{base_url}/bot/npg/",{
                "orderId":333,
                "price":322
            })
            print("ethswitch data = ",data.json())
            if data != None:
                data = data.json()
            formUrl = data["data"].get("formUrl",None)
           
          
            await query.message.reply_text(
                "Open Ethiswithch",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(
                            text="Ethswithch!",
                            web_app=WebAppInfo(url=f"{formUrl}")
                        )]
                    ],
                    resize_keyboard=True, 
                    one_time_keyboard=True 
                )
            )
        # Add more logic for handling Ethswitch payment here

    else:
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text="Unknown payment method selected."
        )