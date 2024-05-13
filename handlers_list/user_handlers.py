from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from hand_filters.admin_filter import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards_bots.backmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards_bots.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.services import book

router = Router()

@router.message(CommandStart())
async def send_start_message(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
        
        
@router.message(Command(commands=['help']))
async def send_help_message(message: Message):
    await message.answer(LEXICON[message.text])
    

@router.message(Command(commands=['beginning']))
async def send_beginning_message(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard('backward', f'{users_db[message.from_user.id]['page']}/{len(book)}', 'forward')
        )

    
@router.message(Command(commands=['continue']))
async def send_continue_message(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard('backward', f'{users_db[message.from_user.id]['page']}/{len(book)}', 'forward')
    )
    
    
@router.message(Command(commands=['bookmarks']))
async def send_bookmarls_message(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        tt = users_db[message.from_user.id]['bookmarks']
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(*tt)
        )
    else:
        await message.answer(LEXICON['no_bookmarks'])
        
        
@router.callback_query(F.data == 'forward')
async def edit_forward_text(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard('backward', f'{users_db[callback.from_user.id]['page']}/{len(book)}', 'forward')
        )
    await callback.answer()
    

@router.callback_query(F.data == 'backward')
async def edit_backward_text(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard('backward', f'{users_db[callback.from_user.id]['page']}/{len(book)}', 'forward')
        )
    await callback.answer()
    
    
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit()) 
async def add_bookmarks(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    ) 
    await callback.answer(text=f'Страница {users_db[callback.from_user.id]['page']} успешно добавлена в закладки!')  
    
    
@router.callback_query(IsDigitCallbackData())
async def open_bookmarks(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = int(callback.data)
    text = book[int(callback.data)]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard('backward', f'{users_db[callback.from_user.id]['page']}/{len(book)}', 'forward')
    )
    
    
@router.callback_query(F.data == 'edit_bookmarks_button')
async def edit_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=create_edit_keyboard(*users_db[callback.from_user.id]['bookmarks'])
    ) 
    
    
@router.callback_query(F.data == 'cancel')
async def cancel_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    
    
@router.callback_query(IsDelBookmarkCallbackData())
async def del_bookmarks(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['edit_bookmarks'],
            reply_markup=create_edit_keyboard(*users_db[callback.from_user.id]['bookmarks'])
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['no_bookmarks']
        )