import os
import tempfile
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from app.models import Resume
from app.api import extract_skills
from .utils import extract_text_from_pdf, extract_text_from_docx

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Пришли мне своё резюме в PDF или DOCX, или используй команду /search для вакансий."
    )

@router.message(Command("resume"))
async def cmd_resume(message: types.Message):
    await message.answer("Отправьте PDF или DOCX файл вашего резюме.")

@router.message(lambda message: message.document is not None)
async def handle_document(message: types.Message, bot):
    file_name = message.document.file_name
    file = await bot.get_file(message.document.file_id)

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as tmp:
        temp_path = tmp.name
        await bot.download_file(file.file_path, destination=temp_path)

    try:
        if file_name.endswith(".pdf"):
            text = extract_text_from_pdf(temp_path)
        elif file_name.endswith(".docx"):
            text = extract_text_from_docx(temp_path)
        else:
            await message.answer("Формат не поддерживается. Используйте PDF или DOCX.")
            return

        # resume = Resume(text=text)
        skills = extract_skills(text)
        skills_str = ", ".join(skills) if skills else "Навыки не найдены"

        await message.answer(
            f"Извлечён текст из резюме:\n\n{text[:700]}...\n\n🔍 Навыки: {skills_str}"
        )

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.message(Command("search"))
async def cmd_search(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вакансия 1", url="https://example.com/1")],
            [InlineKeyboardButton(text="Вакансия 2", url="https://example.com/2")],
            [InlineKeyboardButton(text="Вакансия 3", url="https://example.com/3")]
        ]
    )
    await message.answer("Вот 3 заглушки вакансий:", reply_markup=keyboard)
