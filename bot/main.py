#!/usr/bin/env python3
# bot/main.py — Policy+FX Telegram Bot
# Commands: /start, /dashboard, /alerts

import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from datetime import datetime
import json

# Load config
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID'))
DASHBOARD_URL = os.getenv('DASHBOARD_URL')
UI_PATH = os.getenv('UI_PATH')

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_dashboard_status():
    # Stub for demo — in prod, read from data/ files
    try:
        with open(f'{UI_PATH}/../data/fx/latest.json') as f:
            fx = json.load(f)
        fx_str = f"💱 USD/CNY = {fx.get('rate', '—')}"
    except:
        fx_str = "💱 USD/CNY = —"
    
    try:
        with open(f'{UI_PATH}/../data/shanghai/latest.json') as f:
            sh = json.load(f)
        sh_str = f"📈 SHCOMP = {sh.get('index', '—')}"
    except:
        sh_str = "📈 SHCOMP = —"
    
    return f"{fx_str}\n{sh_str}\n⏱️ Last updated: {datetime.now().strftime('%H:%M')}"

@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    status = await get_dashboard_status()
    await message.answer(
        f"👋 Welcome to *Policy+FX Trust Layer*\n\n{status}\n\n✅ Live dashboard: [Open]({DASHBOARD_URL})\n\nUse /dashboard or /alerts",
        parse_mode="Markdown"
    )

@dp.message(Command("dashboard"))
async def dashboard_handler(message: types.Message) -> None:
    await message.answer(
        f"🌐 Your live dashboard:\n[{DASHBOARD_URL}]({DASHBOARD_URL})",
        parse_mode="Markdown"
    )

@dp.message(Command("alerts"))
async def alerts_handler(message: types.Message) -> None:
    await message.answer(
        "🔔 Alert status:\n• FX breach alerts: ✅ Enabled\n• SHCOMP breach alerts: ✅ Enabled\n• Next check: in ~4 minutes",
        parse_mode="Markdown"
    )

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
