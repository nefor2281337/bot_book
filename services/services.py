BOOK_PATH = 'book.txt'
PAGE_SIZE = 1050


book = {}

def _get_part_text(text: str, start: int, page: int) -> tuple[str, int]:
    fin = (',', '.', '!', ':', ';', '?')
    if start + page > len(text):
        return text[start:], len(text) - start
    else:
        if text[start:start+page+1][-1] in fin:
            page -= 3
        while text[start:start+page][-1] not in fin:
            page -= 1
        return text[start:start+page], page

def prepare_book(path: str) -> None:
    start = 0
    number = 1
    
    with open(path, 'r', encoding='utf-8') as file:
        book_read = file.read()
    
    tr_txt = _get_part_text(book_read, start, PAGE_SIZE)
    while start + tr_txt[1] < len(book_read):
        book[number] = tr_txt[0].strip()
        start += tr_txt[1] + 1
        number += 1
        tr_txt = _get_part_text(book_read, start, PAGE_SIZE)
    book[number] = tr_txt[0].strip()  

prepare_book(BOOK_PATH)

