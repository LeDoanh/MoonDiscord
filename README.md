# MoonDiscord 🌙

**[English](#english-version) | [Tiếng Việt](#vietnamese-version)**

---

## Vietnamese Version

MoonDiscord là bot Discord sử dụng OpenAI GPT để trò chuyện và hỗ trợ người dùng với khả năng đa ngôn ngữ. Bot có thể tùy chỉnh tính cách và phong cách trả lời thông qua INSTRUCTIONS, tạo nên trải nghiệm trò chuyện độc đáo và thân thiện ✨

### Tính năng
- 🌍 **Hỗ trợ đa ngôn ngữ**: Trò chuyện bằng tiếng Việt, Anh, và nhiều ngôn ngữ khác
- 🎭 **Tùy chỉnh tính cách**: Điều chỉnh cách trả lời và tính cách của bot qua INSTRUCTIONS
- 💬 Trả lời tin nhắn và slash command trực tiếp trên Discord
- 🤖 Hỗ trợ nhiều model OpenAI GPT (gpt-4.1, gpt-4o, gpt-4.1-mini, ...)
- 📝 Lưu lịch sử hội thoại theo từng kênh
- 🔍 Hỗ trợ web search (nếu bật qua slash command)
- **🔧 Function calling tự động**: AI tự động sử dụng các function khi cần thiết bằng cách tự Intent Detection
  - ⏰ Xem thời gian (get_current_time)
  - 🌤️ Thời tiết (get_weather)

### Yêu cầu hệ thống
- Python 3.10+
- Các thư viện trong `requirements.txt`

### 💰 Tip: OpenAI Credits miễn phí
Bạn có thể nạp 5$ vào [OpenAI Playground](https://platform.openai.com/playground) và bật "Share data" để nhận:
- **250.000 token GPT-4.1** mỗi ngày
- **2.500.000 token GPT-4.1-mini** mỗi ngày

### Cài đặt
1. Clone repository về máy:
   ```sh
   git clone https://github.com/LeDoanh/MoonDiscord.git
   cd MoonDiscord
   ```
2. Cài đặt thư viện:
   ```sh
   pip install -r requirements.txt
   ```
3. Tạo file `.env` ở thư mục gốc (xem ví dụ bên dưới)

### Cấu hình `.env`
Tạo file `.env` với nội dung mẫu:
```env
DISCORD_TOKEN="<token bot discord>"
DISCORD_STATUS="[]~(￣▽￣)~*"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_API_KEY="<openai_api_key>"
OPENAI_MODEL="gpt-4.1-mini"
OPENAI_INSTRUCTIONS="Moon là một cô bạn vui vẻ, thân thiện và thông minh. Trả lời bằng tiếng Việt với phong cách dễ thương."
```
> **Lưu ý:** 
> - Không chia sẻ file `.env` hoặc token/API key cho người khác.
> - Điều chỉnh `OPENAI_INSTRUCTIONS` để tùy chỉnh tính cách và ngôn ngữ của bot.

### Sử dụng
Chạy bot bằng lệnh:
```sh
python main.py
```
- Bot sẽ tự động kết nối Discord và sẵn sàng nhận lệnh.

### Slash Commands
- `/chat` — Gửi câu hỏi tới Moon, có thể chọn công cụ hỗ trợ (None, Web search)
- `/new_chat` — Bắt đầu chủ đề mới với Moon
- `/functions` — Xem danh sách functions có sẵn
- `/help` — Xem hướng dẫn sử dụng bot

Bạn cũng có thể mention bot trực tiếp trong kênh để trò chuyện nhanh.

### Function Calling Tự Động
Moon sẽ tự động sử dụng các function phù hợp mà không cần chỉ định:
```
/chat Mấy giờ rồi?              # → tự động dùng get_current_time
/chat Thời tiết Hà Nội          # → tự động dùng get_weather
```

### Đóng góp & Báo lỗi
Mọi đóng góp, ý kiến hoặc báo lỗi đều được hoan nghênh qua Issues hoặc Pull Request.

---

## English Version

MoonDiscord is a Discord bot powered by OpenAI GPT that provides multilingual chat support with customizable personality through INSTRUCTIONS, creating a unique and friendly conversation experience ✨

### Features
- 🌍 **Multilingual support**: Chat in Vietnamese, English, and many other languages
- 🎭 **Personality customization**: Adjust bot's response style and personality via INSTRUCTIONS
- 💬 Direct message and slash command responses on Discord
- 🤖 Support for multiple OpenAI GPT models (gpt-4.1, gpt-4o, gpt-4.1-mini, ...)
- 📝 Conversation history saved per channel
- 🔍 Web search support (when enabled via slash command)
- **🔧 Automatic function calling**: AI automatically uses functions when needed through Intent Detection
  - ⏰ Get current time (get_current_time)
  - 🌤️ Weather information (get_weather)

### System Requirements
- Python 3.10+
- Libraries listed in `requirements.txt`

### 💰 Tip: Free OpenAI Credits
You can add $5 to [OpenAI Playground](https://platform.openai.com/playground) and enable "Share data" to receive:
- **250,000 GPT-4.1 tokens** daily
- **2,500,000 GPT-4.1-mini tokens** daily

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/LeDoanh/MoonDiscord.git
   cd MoonDiscord
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create `.env` file in the root directory (see example below)

### Configuration `.env`
Create a `.env` file with the following content:
```env
DISCORD_TOKEN="<your_discord_bot_token>"
DISCORD_STATUS="[]~(￣▽￣)~*"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_API_KEY="<your_openai_api_key>"
OPENAI_MODEL="gpt-4.1-mini"
OPENAI_INSTRUCTIONS="Moon is a cheerful, friendly, and intelligent assistant. Respond in English with a cute style."
```
> **Note:** 
> - Never share your `.env` file or tokens/API keys with others.
> - Adjust `OPENAI_INSTRUCTIONS` to customize the bot's personality and language.

### Usage
Run the bot with:
```sh
python main.py
```
- The bot will automatically connect to Discord and be ready to receive commands.

#### Slash Commands
- `/chat` — Send a question to Moon, with optional tools (None, Web search)
- `/new_chat` — Start a new conversation topic with Moon
- `/functions` — View available functions list
- `/help` — View bot usage instructions

You can also mention the bot directly in channels for quick conversations.

#### Automatic Function Calling
Moon will automatically use appropriate functions without manual specification:
```
/chat What time is it?          # → automatically uses get_current_time
/chat Weather in London         # → automatically uses get_weather
```

### Contributing & Bug Reports
All contributions, feedback, or bug reports are welcome through Issues or Pull Requests.

---
MoonDiscord - Made with ❤️ for Discord!
