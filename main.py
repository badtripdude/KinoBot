"""Bot's code below"""
import threading
import time

from aiogram import Bot, Dispatcher, executor, types
import logging

from lordfilm import LordFilm
from settings import TOKEN, DRIVER

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

LD = LordFilm(DRIVER).init()
mov_cache = {}


def update():
    while 1:
        time.sleep(3600)
        LD.init()


@dp.message_handler(commands=['start', 'help'])
async def start(msg: types.Message):
    await msg.answer('This bot can help you find movies...')


@dp.message_handler(regexp='dl_', )
async def fetch_full_movie(msg: types.Message):
    msg.text = msg.text.replace('/dl_', '')
    try:
        movie = mov_cache[int(msg.text)]
    except KeyError:
        return await msg.answer('Unknown command!')
    movie.fetch_full_info()
    await msg.answer_photo(movie.img_link,
                           f'''<a href='https:{movie.player_link}'><b>{movie.title.upper()}</b></a>\n
year: {movie.year}
KP rate: {movie.kp_rate}
IMBD rate: {movie.imdb_rate}
 ''',
                           # parse_mode='MarkdownV2'
                           parse_mode='html'
                           )
    # await msg.answer('<b>Hulk</b>'
    #                  '<a href=https></a>', parse_mode='html')


def generate_comm(msg, movie):
    _id = hash(movie)
    mov_cache.update({_id: movie})

    dp.register_message_handler(fetch_full_movie,
                                commands=[str(_id)])
    # if hash(movie) not in mov_cache:
    return _id


@dp.message_handler(regexp='')
async def _(msg: types.Message):
    movies = LD.search(msg.text)
    s = ''
    dp.register_message_handler(fetch_full_movie)
    if len(movies) >= 1:
        for i_m in range(len(movies)):
            generate_comm(msg, movies[i_m])
            s += f'{i_m + 1}: {movies[i_m].title}\n' \
                 f'download:/dl_{generate_comm(msg, movies[i_m])}\n\n'
            # f'download: {movies[i_m].player_link}\n\n'

        await msg.answer(s, )
    else:
        await msg.answer('nothing match!')


if __name__ == '__main__':
    threading.Thread(target=update, daemon=True).start()
    executor.start_polling(dp, )
