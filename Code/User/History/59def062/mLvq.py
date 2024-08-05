from main import NewProduct
from main import storage
import keyboard_fabric
import functions
import keyboards
import settings


async def start_function(bot, user_id):
    # await functions.delete_keyboard(bot=bot, chat_id=user_id)
    
    text = settings.TEXTS.START_MESSAGE
    keyboard = keyboard_fabric.start_keyboard()
    
    await functions.send_message(
        bot=bot,
        chat_id=user_id,
        text=text,
        reply_markup=keyboard
    )
    
    if (settings.Bot_DB.user_exist(user_id=user_id)) is None:
        settings.Bot_DB.add_user(user_id=user_id)
    return


async def seller_menu(bot, user_id):
    keyboard = keyboard_fabric.seller_menu()
    text = "Что хотите сделать?"

    await functions.send_message(
        bot=bot,
        chat_id=user_id,
        text=text,
        reply_markup=keyboard
    )

def get_products(action, product=True):
    product = settings.Bot_DB.get_product(action)
    keyboard_fabric.product_control()

    # if product == True:
    text = (settings.PATTERNS.product
        .replace("NAME", product.name)
        .replace("DESCRIPTION", product.description)
        .replace("RATING", f"{round(product.rating) * '⭐️'} ({product.rating})")
        .replace("PRICE", f"{product.price}₽"))
    
    # else:
    #     text = (settings.PATTERNS.in_cart
    #             .replace("NAME", product.name)
    #             .replace("PRICE", f"{product.price}₽"))

    photo = f'./data/{product.path_folder}/{product.photo_name}'
    
    return text, photo

async def get_cart(bot, user_id):
    cart = settings.Bot_DB.get_cart(user_id)
    text = '<b>Ваша корзина:</b>\n\n'
    if len(cart) != 0:
        for product in cart:
            text += f" — {get_products(product, False)[0]}\n"
    else:
        text += '<b>*Паук плетёт паутину*</b>'

    await functions.send_message(bot=bot, chat_id=user_id, text=text)
    # print(cart, type(cart))

async def set_product(bot, user_id, action):
    # action = 1 if action == 'PRODUCTS' else action
    all_products = (settings.Bot_DB.get_product_all())
    len_products = max([product.id for product in all_products])
    text, photo = get_products(action)

    await functions.send_photo(
        bot=bot,
        chat_id=user_id,
        caption=text,
        photo_path=photo,
        reply_markup=keyboard_fabric.product_control(action, len_products)
    )


async def edit_message(bot, user_id, message_id, action):
    print(action)
    action = 1 if action == 'PRODUCTS' else action
    all_products = (settings.Bot_DB.get_product_all())
    len_products = max([product.id for product in all_products])
    text, photo = get_products(action)

    if not(settings.Bot_DB.user_exist(user_id)):
        reply_markup = keyboard_fabric.product_control(action, len_products)
    else:
        reply_markup = keyboard_fabric.product_control(action, len_products)

    await functions.edit_message(
        bot=bot,
        chat_id=user_id,
        message_id=message_id,
        caption=text,
        photo=photo,
        reply_markup=reply_markup
    )


async def create_order(bot, user_id, action):
    product_id = int( action.replace( settings.ACTIONS.CREATE_ORDER, "" ) )
    settings.Bot_DB.add_order(client_id=user_id, product_id=product_id)
    await functions.send_message(
        bot=bot, 
        chat_id=user_id, 
        text="Заказ оформлен!"
    )

async def add_to_cart(bot, user_id, action):
    product_id = int( action.replace( settings.ACTIONS.ADD_TO_CART, "" ) )
    lastes_products = (settings.Bot_DB.get_cart(user_id=user_id))
    lastes_products.append(product_id)
    settings.Bot_DB.update_cart(client_id=user_id, products=(lastes_products))
    await functions.send_message(
        bot=bot,
        chat_id=user_id,
        text="Товар добавлен в корзину!"
    )

async def create_product(bot, user_id, state, message_id):
    # name='Чехол под наушники'
    # description='Подойдёт для наушников AirPods.\n\nВыполнен из приятной на ощупь кожи. Имеет карабин.'
    # photo_name='headphones.JPG'

    # if settings.Bot_DB.check_product_name_exist(name) == None:
    #     settings.Bot_DB.add_product(
    #         name=name,
    #         description=description,
    #         photo_name=photo_name
    #     )
    #     await functions.send_message(bot=bot, chat_id=user_id, text=f'Товар <b>"{name}"</b> создан')

    # else:
    #     await functions.send_message(bot=bot, chat_id=user_id, 
    #                                 text=f'Товар с именем <b>"{name}"</b> уже существует')

    await storage.set_data(
        chat=user_id, user=user_id,
        data={
            'name':'',
            'description':'',
            'photo_name': ''
        }
    )
    await functions.delete_message(bot=bot, 
        chat_id=user_id,
        message_id=message_id)
    
    await NewProduct.name.set()
    await functions.send_message(
        bot=bot,
        chat_id=user_id,
        text="Вы в панели создания товара"
    )