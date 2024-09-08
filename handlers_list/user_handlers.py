from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import (new_user,
                               set_page_one,
                               page_user,
                               bookmarks_user,
                               change_user_page,
                               add_user_bookmarks)
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
    new_user(message.from_user.id)
        
        
@router.message(Command(commands=['help']))
async def send_help_message(message: Message):
    await message.answer(LEXICON[message.text])
    

@router.message(Command(commands=['beginning']))
async def send_beginning_message(message: Message):
    set_page_one(message.from_user.id)
    text = book[page_user(message.from_user.id)]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard('backward', f'{page_user(message.from_user.id)}/{len(book)}', 'forward')
        )

    
@router.message(Command(commands=['continue']))
async def send_continue_message(message: Message):
    text = book[page_user(message.from_user.id)]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard('backward', f'{page_user(message.from_user.id)}/{len(book)}', 'forward')
    )
    
    
@router.message(Command(commands=['bookmarks']))
async def send_bookmarks_message(message: Message):
    if bookmarks_user(message.from_user.id):
        tt = bookmarks_user(message.from_user.id)
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(*tt)
        )
    else:
        await message.answer(LEXICON['no_bookmarks'])
        
        
@router.callback_query(F.data == 'forward')
async def edit_forward_text(callback: CallbackQuery):
    if page_user(callback.from_user.id) < len(book):
        change_user_page(callback.from_user.id, page_user(callback.from_user.id) + 1)
        text = book[page_user(callback.from_user.id)]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard('backward', f'{page_user(callback.from_user.id)}/{len(book)}', 'forward')
        )
    await callback.answer()
    

@router.callback_query(F.data == 'backward')
async def edit_backward_text(callback: CallbackQuery):
    if page_user(callback.from_user.id) > 1:
        change_user_page(callback.from_user.id, page_user(callback.from_user.id) - 1)
        text = book[page_user(callback.from_user.id)]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard('backward', f'{page_user(callback.from_user.id)}/{len(book)}', 'forward')
        )
    await callback.answer()
    
    
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit()) 
async def add_bookmarks(callback: CallbackQuery):
    add_user_bookmarks(callback.from_user.id, page_user(callback.from_user.id))

    await callback.answer(text=f'Страница {page_user(callback.from_user.id)} успешно добавлена в закладки!')
    
    
@router.callback_query(IsDigitCallbackData())
async def open_bookmarks(callback: CallbackQuery):
    change_user_page(callback.from_user.id, int(callback.data))
    text = book[int(callback.data)]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard('backward', f'{page_user(callback.from_user.id)}/{len(book)}', 'forward')
    )
    
    
@router.callback_query(F.data == 'edit_bookmarks_button')
async def edit_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=create_edit_keyboard(*bookmarks_user(callback.from_user.id))
    ) 
    
    
@router.callback_query(F.data == 'cancel')
async def cancel_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    
    
@router.callback_query(IsDelBookmarkCallbackData())
async def del_bookmarks(callback: CallbackQuery):
    bookmarks_user(callback.from_user.id).remove(
        int(callback.data[:-3])
    )
    if bookmarks_user(callback.from_user.id):
        await callback.message.edit_text(
            text=LEXICON['edit_bookmarks'],
            reply_markup=create_edit_keyboard(*bookmarks_user(callback.from_user.id))
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['no_bookmarks']
        )