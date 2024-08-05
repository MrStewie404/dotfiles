import settings
import bot_functions
from functions import TimeNow 

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token=settings.BOT_TOKEN)
TimeNow = TimeNow()

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    user_id = message.from_user.id

    if user_id in settings.ADMINS:
        await bot_functions.seller_menu(bot, user_id)
    
    else:
        await bot_functions.start_function(
            bot=bot,
            user_id=message.from_user.id
        )

@dp.message_handler(commands=['help'], state="*")
async def help(message: types.Message):
    print(message.from_user.id)
    await message.answer(
        settings.commands.get(
            message.text.replace('/', '') 
            if len(message.text) == 5
            else message.text.replace('/help', '')
        )
    )


@dp.callback_query_handler(state="*")
async def callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    action = callback_query.data
    user_id = callback_query.from_user.id

    if action == settings.ACTIONS.PRODUCTS:
        await bot_functions.set_product(bot, user_id, action)


    elif settings.ACTIONS.LEFT in action:
        await bot_functions.edit_message(bot, user_id, 
                                        message_id=callback_query.message.message_id,
                                        action=int(action.replace(settings.ACTIONS.LEFT, "")))

    elif settings.ACTIONS.RIGHT in action:
        await bot_functions.edit_message(bot, user_id, 
                                        message_id=callback_query.message.message_id,
                                        action=int(action.replace(settings.ACTIONS.RIGHT, "")))
        
    elif settings.ACTIONS.ADD_TO_CART in action:
        await bot_functions.add_to_cart(bot, user_id, action)


    elif settings.ACTIONS.CART in action:
        await bot_functions.get_cart(bot, user_id)


    elif settings.ACTIONS.CREATE_PRODUCT in action:
        await bot_functions.create_product(bot, user_id, action)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
