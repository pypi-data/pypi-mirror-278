import os
import re
from pyrogram import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from pydantic import BaseModel, ValidationError

# Replace with your own API_ID and API_HASH
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]
TELEGRAM_API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]

# States for conversation
# Define paths
MEDIA_BASE_PATH = os.environ["MEDIA_BASE_PATH"]

# States for conversation
URL, SHOW_CHOICE, NEW_SHOW_NAME = range(3)


class ParsedURL(BaseModel):
    chat_id: int | None = None
    message_id: int
    username: str | None = None


class UserData(BaseModel):
    url: str
    parsed: ParsedURL
    show_name: str | None = None


class TelegramBot:
    def __init__(self, api_id, api_hash, telegram_api_token, media_base_path):
        self.api_id = api_id
        self.api_hash = api_hash
        self.telegram_api_token = telegram_api_token
        self.media_base_path = media_base_path
        self.pyro_client = Client("nodim", api_id=self.api_id, api_hash=self.api_hash)
        self.application = Application.builder().token(telegram_api_token).build()
    
    
    def __del__(self):
        self.pyro_client.stop()

    def parse_telegram_url(self, url):
        patterns = [
            r'https://t.me/c/(?P<chat_id>[\d]+)/(?P<message_id>\d+)',
            r'https://web.telegram.org/a/#-(?P<chat_id>[\d]+)/(?P<message_id>\d+)',
            r'https://t.me/(?P<username>[\w]+)/(?P<message_id>\d+)',
        ]

        for pattern in patterns:
            match = re.match(pattern, url)
            if match:
                result = match.groupdict()
                return ParsedURL(**result)

        return None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Welcome! Please send me the URL of the media you want to download.')
        return URL

    async def receive_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_data = context.user_data
        url = update.message.text

        try:
            parsed = self.parse_telegram_url(url)
            if not parsed:
                raise ValidationError

            user_data['user_data'] = UserData(url=url, parsed=parsed)

            existing_shows = [d for d in os.listdir(self.media_base_path) if os.path.isdir(os.path.join(self.media_base_path, d))]

            if existing_shows:
                show_list = "\n".join([f"{i+1}. {show}" for i, show in enumerate(existing_shows)])
                await update.message.reply_text(f"Please choose an existing show or type 'new' to add a new one:\n{show_list}")
                user_data['existing_shows'] = existing_shows
                return SHOW_CHOICE
            else:
                await update.message.reply_text('No existing shows found. Please send me the name of the new show.')
                return NEW_SHOW_NAME

        except ValidationError:
            await update.message.reply_text('Invalid URL. Please provide a valid Telegram media URL.')
            return URL

    async def receive_show_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_data = context.user_data
        choice = update.message.text

        if choice.lower() == 'new':
            await update.message.reply_text('Please send me the name of the new show.')
            return NEW_SHOW_NAME
        else:
            try:
                choice_index = int(choice) - 1
                show_name = user_data['existing_shows'][choice_index]
                user_data['user_data'].show_name = show_name
                await update.message.reply_text(f"Selected existing show: {show_name}")
                await self.process_media(update, context)
                return ConversationHandler.END
            except (ValueError, IndexError):
                await update.message.reply_text('Invalid choice. Please select a valid option from the list or type \'new\' to add a new show.')
                return SHOW_CHOICE

    async def receive_new_show_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_data = context.user_data
        show_name = update.message.text
        user_data['user_data'].show_name = show_name

        await update.message.reply_text(f"New show name: {show_name}")
        await self.process_media(update, context)
        return ConversationHandler.END

    async def process_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_data = context.user_data['user_data']
        url = user_data.url
        parsed = user_data.parsed
        show_name = user_data.show_name

        await self.pyro_client.start()

        try:
            chat_id = parsed.username if parsed.username else parsed.chat_id
            message_id = parsed.message_id

            message = await self.pyro_client.get_messages(chat_id=chat_id, message_ids=message_id)
            if message:
                show_path = os.path.join(self.media_base_path, show_name)
                os.makedirs(show_path, exist_ok=True)

                if message.video:
                    file_name = message.video.file_name
                else:
                    file_name = 'media_file'

                file_path = os.path.join(show_path, file_name)

                await self.pyro_client.download_media(message, file_name=file_path)
                await update.message.reply_text(f'Media downloaded successfully to {file_path}!')
            else:
                await update.message.reply_text('Failed to find the message.')
        except Exception as e:
            await update.message.reply_text(f'Failed to download media: {str(e)}')


    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Operation cancelled.')
        return ConversationHandler.END

    def run(self) -> None:
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_url)],
                SHOW_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_show_choice)],
                NEW_SHOW_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_new_show_name)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )

        self.application.add_handler(conv_handler)
        self.application.run_polling()

if __name__ == '__main__':
    bot = TelegramBot(API_ID, API_HASH, TELEGRAM_API_TOKEN, MEDIA_BASE_PATH)
    bot.run()