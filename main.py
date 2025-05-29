import discord
from discord import app_commands
from discord.ext import commands
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
            f"Moon bắt đầu chủ đề mới rồi nè, {interaction.user.mention} hỏi gì tiếp đi ạ! ✨",
            ephemeral=True,
        )


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


if __name__ == "__main__":
    import os
    import threading

    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def root():
        return {"status": "Moon Discord bot is running!"}

    def run_web():
        port = int(os.environ.get("PORT", 10000))
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")

    threading.Thread(target=run_web, daemon=True).start()
    bot.run(DISCORD_TOKEN)
