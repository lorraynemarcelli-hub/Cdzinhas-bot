import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

GRUPO_ID = int(os.getenv("GROUP_ID"))
TOPICO_APRESENTACAO = int(os.getenv("TOPIC_ID"))

class Cadastro(StatesGroup):
    nome = State()
    idade = State()
    estado_civil = State()
    municipio = State()
    uf = State()
    foto = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("🌸 Olá linda! Vamos fazer sua apresentação.\n\nQual seu nome feminino?")
    await Cadastro.nome.set()

@dp.message_handler(state=Cadastro.nome)
async def nome(message: types.Message, state: FSMContext):
    await state.update_data(nome=message.text)
    await message.answer("🎂 Qual sua idade?")
    await Cadastro.next()

@dp.message_handler(state=Cadastro.idade)
async def idade(message: types.Message, state: FSMContext):
    await state.update_data(idade=message.text)
    await message.answer("💍 Estado civil?")
    await Cadastro.next()

@dp.message_handler(state=Cadastro.estado_civil)
async def estado_civil(message: types.Message, state: FSMContext):
    await state.update_data(estado_civil=message.text)
    await message.answer("📍 Município?")
    await Cadastro.next()

@dp.message_handler(state=Cadastro.municipio)
async def municipio(message: types.Message, state: FSMContext):
    await state.update_data(municipio=message.text)
    await message.answer("🗺 UF?")
    await Cadastro.next()

@dp.message_handler(state=Cadastro.uf)
async def uf(message: types.Message, state: FSMContext):
    await state.update_data(uf=message.text)
    await message.answer("📸 Envie sua foto montada atual.")
    await Cadastro.next()

@dp.message_handler(content_types=['photo'], state=Cadastro.foto)
async def foto(message: types.Message, state: FSMContext):
    data = await state.get_data()

    caption = f"""
🌸✨ Nova Amiga Chegando ✨🌸

👑 Nome: {data['nome']}
🎂 Idade: {data['idade']}
💍 Estado civil: {data['estado_civil']}
📍 Cidade: {data['municipio']} - {data['uf']}
"""

    await bot.send_photo(
        chat_id=GRUPO_ID,
        photo=message.photo[-1].file_id,
        caption=caption,
        message_thread_id=TOPICO_APRESENTACAO
    )

    await message.answer("💖 Cadastro enviado! Aguarde aprovação.")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)