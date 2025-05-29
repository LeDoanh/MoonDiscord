import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands
from fastapi import FastAPI
from openai import AsyncOpenAI

from config import Config

# --- Load configuration ---
config = Config()
DISCORD_TOKEN = config.discord_token
OPENAI_API_KEY = config.openai_api_key
STATUS = config.status
OPENAI_BASE_URL = config.openai_base_url
OPENAI_MODEL = config.openai_model
OPENAI_INSTRUCTIONS = config.openai_instructions

# --- Initialize channel chat IDs dictionary ---
CHANNEL_CHAT_IDS = {}  # key: channel_id (str), value: chat_id (str or None)

# --- Initialize OpenAI client ---
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "Moon Discord bot is running!"}


# --- Custom Bot with setup_hook for slash commands ---
class MoonBot(commands.Bot):
    async def setup_hook(self):
        await self.add_cog(ChatCommand(self))
        await self.tree.sync()
        self.tree_synced = True


# --- Initialize bot with intents ---
intents = discord.Intents.default()
intents.message_content = True
bot = MoonBot(command_prefix="!", intents=intents)


# --- Slash command for chat ---
class ChatCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="chat", description="💬 Gửi câu hỏi tới Moon")
    @app_commands.describe(
        question="Câu hỏi hoặc nội dung muốn hỏi",
        tool="Công cụ hỗ trợ: None, Web search",
    )
    @app_commands.choices(
        tool=[
            app_commands.Choice(name="None", value="none"),
            app_commands.Choice(name="Web search", value="web_search"),
        ]
    )
    async def chat(
        self,
        interaction: discord.Interaction,
        question: str,
        tool: app_commands.Choice[str] = None,
    ):
        channel_id = str(interaction.channel_id)
        chat_id = CHANNEL_CHAT_IDS.get(channel_id)
        await interaction.response.defer(thinking=True)
        user_mention = interaction.user.mention
        tool_value = tool.value if tool else "none"
        answer, new_chat_id = await ask_openai(
            question, tool=tool_value, chat_id=chat_id
        )
        CHANNEL_CHAT_IDS[channel_id] = new_chat_id
        await interaction.followup.send(f"{user_mention} {answer}")

    @app_commands.command(name="new_chat", description="🆕 Bắt đầu chủ đề mới với Moon")
    async def new_chat(self, interaction: discord.Interaction):
        channel_id = str(interaction.channel_id)
        CHANNEL_CHAT_IDS[channel_id] = None
        await interaction.response.send_message(
            f"Moon bắt đầu chủ đề mới rồi nè, {interaction.user.mention} hỏi gì tiếp đi ạ! ✨"
        )

    @app_commands.command(name="help", description="❓ Hướng dẫn sử dụng Moon")
    async def help(self, interaction: discord.Interaction):
        help_text = (
            "**Moon Discord Bot Hướng dẫn sử dụng:**\n"
            "- `/chat <câu hỏi> [tool]`: Gửi câu hỏi tới Moon, có thể chọn công cụ hỗ trợ như Web search.\n"
            "- `/new_chat`: Bắt đầu chủ đề trò chuyện mới với Moon.\n"
            "- Đề cập @MoonBot trong kênh để hỏi nhanh bằng tin nhắn thường.\n"
            "\n"
            "**Ví dụ:**\n"
            "- `/chat Tôi cần tin tức mới nhất về AI`\n"
            "- `/chat Hãy tìm giúp tôi các công cụ học tiếng Anh hay nhất tool:Web search`\n"
            "\n"
            "**Lưu ý:**\n"
            "- Moon sẽ trả lời trong vòng vài giây, nếu không thấy phản hồi có thể do lỗi mạng hoặc quá tải.\n"
            "- Nếu bạn cần bắt đầu lại cuộc trò chuyện, hãy sử dụng lệnh `/new_chat`.\n"
            "- Moon có thể sử dụng công cụ tìm kiếm web để cung cấp thông tin chính xác hơn.\n"
            "- Hãy thường xuyên sử dụng /new_chat để bắt đầu chủ đề mới, tránh làm lộn xộn cuộc trò chuyện.\n"
            "\n"
            "Nếu cần hỗ trợ thêm, hãy liên hệ admin server!"
        )
        await interaction.response.send_message(help_text, ephemeral=True)


# --- Function to send prompt to OpenAI and return the response ---
async def ask_openai(
    prompt: str, tool: str = "none", chat_id: str = None
) -> tuple[str, str]:
    tools = []
    if tool == "web_search":
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
            previous_response_id=chat_id,
            input=prompt,
            tools=tools if tools else None,
        )
        new_chat_id = getattr(response, "id", chat_id)
        return response.output_text.strip(), new_chat_id
    except Exception as e:
        return f"OpenAI error: {e}", chat_id


# --- Discord bot events ---
@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready to chat!")
    if STATUS:
        await bot.change_presence(activity=discord.Game(STATUS))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        channel_id = str(message.channel.id)
        chat_id = CHANNEL_CHAT_IDS.get(channel_id)
        async with message.channel.typing():
            user_mention = f"<@{message.author.id}>"
            prompt = (
                message.content.replace(f"<@{bot.user.id}>", "")
                .replace(f"<@!{bot.user.id}>", "")
                .strip()
            )
            if not prompt:
                await message.reply(f"{user_mention}, Moon có thể hỗ trợ gì ạ?")
                return
            answer, new_chat_id = await ask_openai(prompt, chat_id=chat_id)
            CHANNEL_CHAT_IDS[channel_id] = new_chat_id
            await message.reply(f"{user_mention} {answer}")
    await bot.process_commands(message)


async def log_current_time():
    import asyncio
    import datetime
    import logging

    while True:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Current time: {current_time}")
        # call request to FastAPI to keep it alive
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.get("https://moondiscord.onrender.com/")
                if response.status_code == 200:
                    logging.info("FastAPI is alive!")
                else:
                    logging.warning(
                        f"FastAPI returned status code: {response.status_code}"
                    )
        except Exception as e:
            logging.error(f"Error pinging FastAPI: {e}")

        # Sleep for 10 minutes
        await asyncio.sleep(600)


async def start_web():
    import os

    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    # Start web server and logging in background
    web_task = asyncio.create_task(start_web())
    log_task = asyncio.create_task(log_current_time())
    # Start Discord bot (blocks until exit)
    try:
        await bot.start(DISCORD_TOKEN)
    except discord.errors.HTTPException as e:
        print(e)
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        web_task.cancel()
        log_task.cancel()
        os.system("python restarter.py")
        os.system("kill 1")

    # Optionally, cancel background tasks if bot exits
    web_task.cancel()
    log_task.cancel()


if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(main())
