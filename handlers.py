import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from load_all import dp, db
from states import EchoProcessing
from keyboard_menu import menu


@dp.message_handler(CommandStart())
async def register_user(message: types.Message, state: FSMContext):
    db.update_user(message.chat.id, 1)
    await state.update_data({'number_of_replies': 1})
    await message.answer(f'Echobot yibatb')


@dp.message_handler(commands=['change_echo'], state=None)
async def prepare_changing(message: types.Message):
    await message.reply("Set the number of replies", reply_markup=menu)

    await EchoProcessing.ChangeEcho.set()


@dp.message_handler(state=None)
async def echo(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if data.get('number_of_replies') is None:
        number_of_replies = db.get_number_of_replies(message.chat.id)[0]
        await state.update_data({'number_of_replies': number_of_replies})
        data = await state.get_data()

    for i in range(data.get('number_of_replies')):
        await message.answer(message.text)


@dp.message_handler(aiogram.dispatcher.filters.Text(equals=['1', '2', '3', '4', '5']), state=EchoProcessing.ChangeEcho)
async def change_echo(message: types.Message, state: FSMContext):
    db.update_user(message.chat.id, int(message.text))
    await message.reply(f'Number of replies set to {message.text}', reply_markup=types.ReplyKeyboardRemove())
    await state.update_data({'number_of_replies': int(message.text)})

    await state.reset_state(with_data=False)


@dp.message_handler(state=EchoProcessing.ChangeEcho)
async def change_acho_invalid(message: types.Message):
    await message.reply(f'Set correct number from 1 to 5')