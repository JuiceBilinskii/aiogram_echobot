from aiogram.dispatcher.filters.state import StatesGroup, State


class EchoProcessing(StatesGroup):
    ChangeEcho = State()
