# MoonDiscord

MoonDiscord là một bot Discord sử dụng OpenAI GPT để trò chuyện và hỗ trợ người dùng bằng tiếng Việt với phong cách thân thiện, dễ thương.

## Tính năng
- Kết nối với Discord, trả lời tin nhắn trong các kênh chỉ định
- Sử dụng OpenAI GPT (hỗ trợ model gpt-4.1, gpt-4o, ...)
- Tùy chỉnh hướng dẫn trả lời (instructions) cho bot
- Quản lý cấu hình qua file `.env`

## Cài đặt
1. Clone repository về máy:
   ```sh
   git clone <repo-url>
   cd MoonDiscord
   ```
2. Cài đặt các thư viện cần thiết:
   ```sh
   pip install -r requirement.txt
   ```
3. Tạo file `.env` (xem ví dụ trong repo hoặc hướng dẫn bên dưới)

## Cấu hình `.env`
```env
DISCORD_TOKEN="<token bot discord>"
DISCORD_CHANNEL_IDS="[\"channel_id_1\", \"channel_id_2\"]"
DISCORD_STATUS="Hello everyone []~(￣▽￣)~*!"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_API_KEY="<openai_api_key>"
OPENAI_MODEL="gpt-4.1"
OPENAI_INSTRUCTIONS="Moon là một cô bạn vui vẻ, thân thiện..."
```

## Sử dụng
Chạy bot bằng lệnh:
```sh
python main.py
```

## Đóng góp
Mọi đóng góp, ý kiến hoặc báo lỗi đều được hoan nghênh qua Issues hoặc Pull Request.

---
MoonDiscord - Made with ❤️ for Discord community!
