#!/usr/bin/env python3.10

import asyncio
import json
import logging
import os
import random
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from openai import AsyncOpenAI

from config import Config

# --- Load configuration ---
config = Config()
DISCORD_TOKEN = config.discord_token
STATUS = config.status
INSTRUCTIONS = config.instructions
OPENAI_API_KEY = config.openai_api_key
OPENAI_BASE_URL = config.openai_base_url
OPENAI_MODEL = config.openai_model

# --- Setup logging ---
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s"
)

# --- Initialize channel chat IDs dictionary ---
CHANNEL_CHAT_IDS: dict[str, str | None] = {}

# --- Random messages for new chat ---
NEW_CHAT_MESSAGES = [
    "Moon bắt đầu chủ đề mới rồi nè, {user} hỏi gì tiếp đi ạ! ✨",
    "Okay! Moon đã reset tất cả và sẵn sàng cho cuộc trò chuyện mới với {user}! 🌟",
    "Xong rồi! {user} có thể bắt đầu chủ đề hoàn toàn mới với Moon ngay bây giờ! 🚀",
    "Fresh start! Moon đã làm mới và chờ {user} chia sẻ điều gì đó thú vị! 💫",
    "Done! Giờ {user} có thể nói chuyện với Moon về bất kỳ chủ đề nào! 🎉",
    "Reset hoàn tất! {user} muốn khám phá chủ đề gì với Moon hôm nay? 🌈",
    "Chủ đề mới đã sẵn sàng! {user} có câu hỏi hay ý tưởng gì thú vị không? ⭐",
    "Moon đã chuẩn bị tinh thần cho cuộc trò chuyện mới! {user} bắt đầu thôi! 🎊",
    "New chat activated! {user} có muốn thảo luận về điều gì đặc biệt không? 🌸",
]

# --- Random support messages ---
SUPPORT_MESSAGES = [
    "{user}, Moon có thể hỗ trợ gì ạ? 🌙",
    "{user}, có điều gì Moon có thể giúp đỡ không ạ? ✨",
    "Chào {user}! Moon sẵn sàng hỗ trợ bạn rồi đây! 🌟",
    "{user} cần Moon giúp gì nào? Cứ thoải mái hỏi nhé! 💫",
    "Hi {user}! Moon có thể làm gì cho bạn hôm nay? 🚀",
    "{user}, Moon đang lắng nghe và sẵn sàng hỗ trợ! 🎊",
    "Xin chào {user}! Có gì Moon có thể giúp bạn không? 🌈",
    "{user}, bạn muốn Moon hỗ trợ về vấn đề gì vậy? 🎉",
    "Chào bạn {user}! Moon có thể tư vấn hoặc giúp gì không? ⭐",
    "{user}, có câu hỏi hay chủ đề nào bạn muốn thảo luận không? 🌸",
]

# --- Initialize OpenAI client ---
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


# --- Helper function to mention user ---
def mention_user(user: discord.abc.User) -> str:
    return user.mention if hasattr(user, "mention") else f"<@{user.id}>"


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
    def __init__(self, bot: commands.Bot):
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
        tool_value = tool.value if tool else "none"
        prompt = f"<@{interaction.user.id}>: {question.strip()}"
        answer, new_chat_id = await ask_openai(prompt, tool=tool_value, chat_id=chat_id)
        CHANNEL_CHAT_IDS[channel_id] = new_chat_id
        await interaction.followup.send(f"{answer}") @ app_commands.command(
            name="new_chat", description="🆕 Bắt đầu chủ đề mới với Moon"
        )

    async def new_chat(self, interaction: discord.Interaction):
        channel_id = str(interaction.channel_id)
        CHANNEL_CHAT_IDS[channel_id] = None
        message = random.choice(NEW_CHAT_MESSAGES).format(
            user=mention_user(interaction.user)
        )
        await interaction.response.send_message(message)

    @app_commands.command(name="help", description="❓ Hướng dẫn sử dụng Moon")
    async def help(self, interaction: discord.Interaction):
        help_text = (
            "**🌙 Hướng dẫn sử dụng Moon Discord Bot**\n"
            "\n"
            "Chào mừng bạn đến với Moon! Dưới đây là các lệnh hữu ích để bạn trò chuyện và khai thác sức mạnh AI của Moon:\n"
            "\n"
            "**Lệnh chính:**\n"
            "- `/chat <câu hỏi> [tool]`: Đặt câu hỏi cho Moon, có thể chọn công cụ hỗ trợ như Web search để tìm kiếm thông tin mới nhất.\n"
            "- `/new_chat`: Bắt đầu một chủ đề trò chuyện hoàn toàn mới với Moon.\n"
            "- Đề cập @MoonBot trong kênh để hỏi nhanh bằng tin nhắn thông thường.\n"
            "\n"
            "**Ví dụ sử dụng:**\n"
            "- `/chat Hãy tóm tắt tin tức công nghệ hôm nay`\n"
            "- `/chat Gợi ý các phương pháp học tiếng Anh hiệu quả tool:Web search`\n"
            "\n"
            "**Lưu ý quan trọng:**\n"
            "- Moon sẽ phản hồi trong vài giây. Nếu không thấy trả lời, có thể do mạng hoặc hệ thống đang bận.\n"
            "- Hãy dùng `/new_chat` để làm mới cuộc trò chuyện khi chuyển chủ đề, giúp Moon trả lời chính xác hơn.\n"
            "- Khi cần thông tin cập nhật, hãy chọn tool:Web search để Moon tìm kiếm trên Internet.\n"
            "- Đừng ngại hỏi bất cứ điều gì!\n"
            "\n"
            "Nếu gặp khó khăn hoặc cần hỗ trợ thêm, hãy liên hệ admin server. Chúc bạn trò chuyện vui vẻ cùng Moon! ✨"
        )
        await interaction.response.send_message(help_text, ephemeral=True)


# --- Function to send prompt to OpenAI and return the response ---
async def ask_openai(
    prompt: str,
    tool: str = "none",
    chat_id: str = None,
    images: list[str] = None,
    force_model: str = None,
) -> tuple[str, str]:
    usage = load_token_usage()
    # Determine which model to use
    model = force_model or OPENAI_MODEL
    if model == "gpt-4.1" and usage["gpt-4.1"] >= TOKEN_LIMITS["gpt-4.1"]:
        model = "gpt-4.1-mini"
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
    if images:
        input_blocks = [
            {"role": "user", "content": []},
        ]
        input_blocks[0]["content"].append({"type": "input_text", "text": prompt})
        for img_url in images:
            input_blocks[0]["content"].append(
                {"type": "input_image", "image_url": img_url}
            )
    else:
        input_blocks = prompt
    try:
        response = await openai_client.responses.create(
            model=model,
            instructions=INSTRUCTIONS,
            previous_response_id=chat_id,
            input=input_blocks,
            tools=tools if tools else None,
        )
        resp_usage = getattr(response, "usage", None)
        if resp_usage:
            used = getattr(resp_usage, "total_tokens", None)
            if used:
                usage[model] = usage.get(model, 0) + used
                save_token_usage(usage)
                logging.info(
                    f"Used {used} tokens for model {model}. Total usage: {usage[model]} tokens."
                )
        if model == "gpt-4.1" and usage["gpt-4.1"] > TOKEN_LIMITS["gpt-4.1"]:
            return await ask_openai(
                prompt, tool, chat_id, images, force_model="gpt-4.1-mini"
            )
        new_chat_id = getattr(response, "id", chat_id)
        return response.output_text.strip(), new_chat_id
    except Exception as e:
        return f"OpenAI error: {e}", chat_id


# --- Token usage tracking ---
TOKEN_USAGE_FILE = os.path.join(os.path.dirname(__file__), "token_usage.json")
TOKEN_LIMITS = {
    "gpt-4.1": 240_000,
    "gpt-4.1-mini": 2_490_000,
}


def load_token_usage():
    today = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(TOKEN_USAGE_FILE):
        usage = {"date": today, "gpt-4.1": 0, "gpt-4.1-mini": 0}
        with open(TOKEN_USAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(usage, f)
        return usage
    with open(TOKEN_USAGE_FILE, "r", encoding="utf-8") as f:
        usage = json.load(f)
    if usage.get("date") != today:
        usage = {"date": today, "gpt-4.1": 0, "gpt-4.1-mini": 0}
        with open(TOKEN_USAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(usage, f)
    return usage


def save_token_usage(usage):
    with open(TOKEN_USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(usage, f)


# --- Discord bot events ---
@bot.event
async def on_ready():
    logging.info(f"{bot.user} is online and ready to chat!")
    if STATUS:
        await bot.change_presence(activity=discord.Game(STATUS))


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        channel_id = str(message.channel.id)
        chat_id = CHANNEL_CHAT_IDS.get(channel_id)
        async with message.channel.typing():
            user_mention = mention_user(message.author)
            prompt_content = (
                message.content.replace(f"<@{bot.user.id}>", "")
                .replace(f"<@!{bot.user.id}>", "")
                .strip()
            )  # Collect image URLs if any image attachments
            image_urls = [
                att.url
                for att in message.attachments
                if (att.content_type and att.content_type.startswith("image/"))
                or att.filename.lower().endswith(
                    (".png", ".jpg", ".jpeg", ".webp", ".gif")
                )
            ]
            if not prompt_content and not image_urls:
                support_message = random.choice(SUPPORT_MESSAGES).format(
                    user=user_mention
                )
                await message.reply(support_message)
                return
            prompt = (
                f"<@{message.author.id}>: {prompt_content}"
                if prompt_content
                else f"<@{message.author.id}> gửi ảnh:"
            )
            answer, new_chat_id = await ask_openai(
                prompt, chat_id=chat_id, images=image_urls if image_urls else None
            )
            CHANNEL_CHAT_IDS[channel_id] = new_chat_id
            await message.reply(f"{answer}")
    await bot.process_commands(message)


async def main():
    try:
        await bot.start(DISCORD_TOKEN)
    except discord.errors.HTTPException as e:
        logging.error(e)
        logging.error("\n\n\nBLOCKED BY RATE LIMITS\n\n\n")


if __name__ == "__main__":
    asyncio.run(main())
