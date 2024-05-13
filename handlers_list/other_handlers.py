from aiogram.types import Message
from lexicon.lexicon import LEXICON
from aiogram import Router


router = Router()


@router.message()
async def send_echo_message(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except:
        await message.answer(text=LEXICON['error_copy'])