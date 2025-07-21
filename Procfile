backend: uvicorn src.backend.main_secure:app --host 0.0.0.0 --port 8000
ai-module: uvicorn src.ai-module.main:app --host 0.0.0.0 --port 8001
data-service: uvicorn src.data-service.main:app --host 0.0.0.0 --port 8002
telegram-bot: python -m src.telegram-bot.core.telegram_bot_secure 