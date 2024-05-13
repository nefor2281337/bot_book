from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.services import book
from lexicon.lexicon import LEXICON

    

def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    
    kb_builder = InlineKeyboardBuilder()
    
    for arg in sorted(args):
        
        kb_builder.row(
            InlineKeyboardButton(
            text=f'{arg} - {book[arg][:100]}',
            callback_data=str(arg))
            )
        
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_bookmarks_button'],
            callback_data='edit_bookmarks_button'
            ),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
            ), 
            width=2
        )
    
    return kb_builder.as_markup()

def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    
    
    kb_builder = InlineKeyboardBuilder()
    
    for arg in sorted(args):
        
        kb_builder.row(
            InlineKeyboardButton(
            text=f'{LEXICON['del']} {arg} - {book[arg][:100]}',
            callback_data=f'{arg}del')
            )
        
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
            )
        )
    
    return kb_builder.as_markup()
    
    