# MoonDiscord

MoonDiscord là một bot Discord sử dụng OpenAI GPT để trò chuyện và hỗ trợ người dùng.

## Tính năng
- Kết nối với Discord, trả lời tin nhắn trong các kênh chỉ định
- Sử dụng OpenAI GPT (hỗ trợ model gpt-4.1, gpt-4o, ...)
- Tùy chỉnh hướng dẫn trả lời (instructions) cho bot
- Quản lý cấu hình qua file `.env`

## Cài đặt
1. Clone repository về máy:
   ```sh
   git clone https://github.com/LeDoanh/MoonDiscord.git
   cd MoonDiscord
   ```
2. Cài đặt python `3.10.11`
3. Cài đặt các thư viện cần thiết:
   ```sh
   pip install -r requirements.txt
   ```
4. Tạo file `.env` (xem ví dụ trong repo hoặc hướng dẫn bên dưới)

## Cấu hình `.env`
Ví dụ file `.env`:
```env
DISCORD_TOKEN="<token bot discord>"
DISCORD_CHANNEL_IDS=[channel_id_1,channel_id_2]
DISCORD_STATUS="Hello everyone []~(￣▽￣)~*!"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_API_KEY="<openai_api_key>"
OPENAI_MODEL="gpt-4.1"
OPENAI_INSTRUCTIONS="Bạn là 1 trợ lý vui vẻ"
```

## Sử dụng
Chạy bot bằng lệnh:
```sh
python main.py
```

Bot sẽ tự động kết nối Discord và hoạt động trong các kênh đã cấu hình. Đảm bảo file `.env` đã được thiết lập đúng trước khi chạy bot.

## Đóng góp
Mọi đóng góp, ý kiến hoặc báo lỗi đều được hoan nghênh qua Issues hoặc Pull Request.

---
MoonDiscord - Made with ❤️ for Luna!
