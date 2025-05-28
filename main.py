import os
import re
import threading
import time

import discord
from discord.ext import commands
from flask import Flask
from openai import AsyncOpenAI

from config import Config

# Load configuration from config.ini using pydantic
config = Config()
DISCORD_TOKEN = config.discord_token
OPENAI_API_KEY = config.openai_api_key
CHANNEL_IDS = config.channel_ids
STATUS = config.status
OPENAI_BASE_URL = config.openai_base_url
OPENAI_MODEL = config.openai_model
OPENAI_INSTRUCTIONS = config.openai_instructions
CURRENT_CHAT_ID = None  # Lưu ID cuộc trò chuyện hiện tại với OpenAI

# Khởi tạo OpenAI client bất đồng bộ
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

# Khởi tạo bot Discord với quyền đọc nội dung tin nhắn
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Danh sách từ khoá để reset chủ đề trò chuyện
RESET_KEYWORDS = [
    "chủ đề mới",
    "reset",
    "new topic",
]
# Tạo regex pattern để kiểm tra từ khoá reset, không phân biệt hoa/thường
reset_pattern = re.compile(
    r"(" + r"|".join(map(re.escape, RESET_KEYWORDS)) + r")", re.IGNORECASE
)


async def ask_openai(prompt: str) -> str:
    """Gửi prompt tới OpenAI và trả về kết quả trả lời."""
    global CURRENT_CHAT_ID
    # Danh sách từ khóa liên quan đến tóm tắt, tìm kiếm
    SEARCH_KEYWORDS = [
        "tóm tắt",
        "tìm kiếm",
        "tra cứu",
        "hôm nay",
    ]
    # Kiểm tra nếu prompt chứa từ khóa liên quan
    use_web_search = any(kw.lower() in prompt.lower() for kw in SEARCH_KEYWORDS)
    # Cấu hình tool web search nếu cần
    tools = []
    if use_web_search:
        tools.append(
            {
                "type": "web_search_preview",
                "search_context_size": "medium",
                "user_location": {
                    "type": "approximate",
                    "country": "VN",
                },
            }
        )
    try:
        response = await openai_client.responses.create(
            model=OPENAI_MODEL,
            instructions=OPENAI_INSTRUCTIONS,
            previous_response_id=CURRENT_CHAT_ID,
            input=prompt,
            tools=tools if tools else None,
        )
        # Cập nhật ID cuộc trò chuyện nếu có
        if hasattr(response, "id"):
            CURRENT_CHAT_ID = response.id
        return response.output_text.strip()
    except Exception as e:
        return f"OpenAI error: {e}"


@bot.event
async def on_ready():
    """Sự kiện khi bot sẵn sàng hoạt động."""
    print(f"{bot.user} đã sẵn sàng!")
    if STATUS:
        await bot.change_presence(activity=discord.Game(name=STATUS))


@bot.event
async def on_message(message):
    """Xử lý tin nhắn: chỉ trả lời khi được mention và ở kênh hợp lệ."""
    global CURRENT_CHAT_ID
    # Bỏ qua tin nhắn của chính bot
    if message.author == bot.user:
        return
    # Chỉ phản hồi ở các kênh cho phép
    if str(message.channel.id) not in CHANNEL_IDS:
        return
    # Chỉ trả lời khi bot được mention
    if bot.user in message.mentions:
        # Hiển thị trạng thái đang nhập
        async with message.channel.typing():
            # Lấy tên hoặc tag người gửi
            user_mention = f"<@{message.author.id}>"
            # Loại bỏ mention khỏi nội dung để lấy prompt
            prompt = (
                message.content.replace(f"<@{bot.user.id}>", "")
                .replace(f"<@!{bot.user.id}>", "")
                .strip()
            )
            # Nếu phát hiện từ khoá reset, reset ID cuộc trò chuyện
            if reset_pattern.search(prompt):
                CURRENT_CHAT_ID = None
                await message.reply(
                    f"Moon bắt đầu chủ đề mới rồi nè, {user_mention} hỏi gì tiếp đi ạ! ✨"
                )
                return
            # Nếu không có prompt sau mention, nhắc lại
            if not prompt:
                await message.reply(f"{user_mention}, Moon có thể hỗ trợ gì ạ?")
                return
            # Gửi prompt tới OpenAI và trả lời lại, mention người hỏi
            answer = await ask_openai(prompt)
            await message.reply(f"{user_mention} {answer}")
    # Cho phép xử lý các command khác nếu có
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

    # Run app to end build process in render.com
    # This is a workaround for Render.com to keep the build process alive
    def run_flask():
        app = Flask(__name__)

        @app.route("/")
        def hello():
            return "Hello World!"

        port = int(os.environ.get("PORT", 4000))
        app.run(host="0.0.0.0", port=port)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Sleep for 1 minute to keep the process running
    while True:
        time.sleep(60)
