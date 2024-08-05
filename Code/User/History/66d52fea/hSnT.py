import settings
from aiogram.utils import exceptions
from datetime import datetime as dt
from aiogram.types import InputMediaPhoto
from asyncio import sleep


def EXCEPTION_WRITE(exception):
    print(exception)
    with open(settings.EXCEPTION_LOG, 'a') as file:
        file.write(str(exception) + '\n'*3)
    return


async def delete_keyboard(bot, chat_id):
    message_id = settings.Bot_DB.get_message_id(user_id=chat_id)
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None
        )
    except exceptions.MessageToEditNotFound:
        pass
    except Exception as e:
        EXCEPTION_WRITE(e)
    return


async def edit_text(bot, chat_id, message_id, text, reply_markup = None, parse_mode = "HTML"):
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except exceptions.MessageNotModified:
        pass
    except exceptions.MessageCantBeEdited:
        try:
            await bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
        except exceptions.MessageToDeleteNotFound:
            pass
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        settings.Bot_DB.set_message_id(msg.message_id, chat_id)
    except Exception as e:
        EXCEPTION_WRITE(e)
    return


async def delete_message(bot, chat_id, message_id):
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
    except exceptions.MessageToDeleteNotFound:
        pass
    except Exception as e:
        EXCEPTION_WRITE(e)
    return


async def send_message(bot, chat_id, text, reply_markup = None, parse_mode = "HTML"):
    try:
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        msg_id = msg.message_id
    except Exception as e:
        EXCEPTION_WRITE(e)
        msg_id = 0
    return msg_id

async def edit_message_media(bot, media, chat_id, message_id, reply_markup = None, parse_mode = "HTML"):
    try:
        msg = bot.edit_message_media(media=media,
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=reply_markup,
        parse_mode=parse_mode
        )
        # msg_id = msg.message_id
    except Exception as e:
        EXCEPTION_WRITE(e)
        msg_id = 0
    return msg_id

async def edit_message(bot, caption, photo, chat_id, message_id, reply_markup = None, parse_mode = "HTML"):
    try:

        await bot.edit_message_media(
            chat_id=chat_id, 
            message_id=message_id,
            media=InputMediaPhoto(open(photo, 'rb'))
        )

        await sleep(0.25)

        await bot.edit_message_caption(
            chat_id=chat_id, 
            message_id=message_id, 
            caption=caption,
            parse_mode=parse_mode, 
            reply_markup=reply_markup
        )
        
    except Exception as e:
        EXCEPTION_WRITE(e)
    

async def send_photo(bot, chat_id, photo_path, reply_markup = None, caption = None, parse_mode = "HTML"):
    try:
        msg = await bot.send_photo(
            chat_id=chat_id,
            photo=open(photo_path, 'rb'),
            caption=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
        msg_id = msg.message_id
    except Exception as e:
        EXCEPTION_WRITE(e)
        msg_id = 0
    return msg_id


async def send_location(bot, chat_id, coord, reply_markup = None):
    try:
        msg = await bot.send_location(
            chat_id=chat_id,
            latitude=coord[0],
            longitude=coord[1],
            reply_markup=reply_markup
        )
        msg_id = msg.message_id
    except Exception as e:
        EXCEPTION_WRITE(e)
        msg_id = 0
    return msg_id

async def send_audio(bot, chat_id, audio, reply_markup = None):
    try:
        msg = await bot.send_audio(
            chat_id=chat_id,
            audio=audio,
            reply_markup=reply_markup
        )
        msg_id = msg.message_id
    except Exception as e:
        EXCEPTION_WRITE(e)
        msg_id = 0
    return msg_id




class TimeNow:
    # @staticmethod
    def get_current_time(self):
        """
        Получение текущего времени и даты в виде объекта datetime.
        :return: Объект datetime, представляющий текущее время и дату.
        """
        return self.current_time
    
    def get_today(self):
        """
        Получение текущей даты в формате 'DD.MM.YYYY'.
        :return: Строка с текущей датой.
        """
        return f"{dt.now().day:02d}.{dt.now().month:02d}.{dt.now().year:02d}"

    def get_time(self):
        """
        Получение текущего времени в формате 'HH:MM:SS'.
        :return: Строка с текущим временем.
        """
        return f"{dt.now().hour:02d}:{dt.now().minute:02d}:{dt.now().second:02d}"