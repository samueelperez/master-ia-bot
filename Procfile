web: cd src/backend && python main_secure.py
ai-module: uvicorn src.ai-module.main:app --host 0.0.0.0 --port 8001
data-service: cd src/data-service && uvicorn main:app --host 0.0.0.0 --port 8002
telegram-bot: python -m src.telegram-bot.core.telegram_bot_secure 