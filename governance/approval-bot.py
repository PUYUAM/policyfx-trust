#!/usr/bin/env python3
# governance/approval-bot.py — Telegram approval bot for alert rule changes

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
import json
import os
from datetime import datetime

# Load config
TELEGRAM_TOKEN = "8732474762:AAHw142jWzb2fkyf6B-p2R-rcwXMn4uCJ0o"
ADMIN_CHAT_ID = 8545379026  # You

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer("🔐 Governance Approval Bot — ready to review alert rule changes.")

@dp.message(Command("approve"))
async def approve_handler(message: types.Message) -> None:
    # Stub: in prod, this would update custom-rules.json and log
    await message.answer("✅ Rule change approved. Updating...", parse_mode="Markdown")
    
    # Log to audit
    with open('../security/audit/governance.log', 'a') as f:
        f.write(f'{datetime.now().isoformat()}|APPROVE|{message.from_user.id}|{message.text}\n')

@dp.message(Command("deny"))
async def deny_handler(message: types.Message) -> None:
    await message.answer("❌ Rule change denied.", parse_mode="Markdown")
    
    # Log to audit
    with open('../security/audit/governance.log', 'a') as f:
        f.write(f'{datetime.now().isoformat()}|DENY|{message.from_user.id}|{message.text}\n')

async def main() -> None:
    # Send approval request to admin
    await bot.send_message(
        ADMIN_CHAT_ID,
        "📋 *Alert Rule Change Pending Approval*\n\n• Rule ID: `usd_cny_and_shcomp`\n• Change: `fx.rate > 7.30 and shcomp.index < 2900` → `fx.rate > 7.25 and shcomp.index < 2900`\n\nUse /approve or /deny",
        parse_mode="Markdown"
    )
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
