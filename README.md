# MoonDiscord

MoonDiscord là bot Discord sử dụng OpenAI GPT để trò chuyện và hỗ trợ người dùng bằng tiếng Việt, thân thiện và dễ thương ✨

## Tính năng
- Trả lời tin nhắn và slash command trực tiếp trên Discord
- Hỗ trợ nhiều model OpenAI GPT (gpt-4.1, gpt-4o, ...)
- Tùy chỉnh hướng dẫn trả lời (instructions) qua file cấu hình
- Lưu lịch sử hội thoại theo từng kênh
- Hỗ trợ web search (nếu bật qua slash command)

## Yêu cầu hệ thống
- Python 3.10
- Các thư viện trong `requirements.txt`

## Cài đặt
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

## Cấu hình `.env`
Tạo file `.env` với nội dung mẫu:
```env
DISCORD_TOKEN="<token bot discord>"
DISCORD_STATUS="[]~(￣▽￣)~*"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_API_KEY="<openai_api_key>"
OPENAI_MODEL="gpt-4.1-mini"
OPENAI_INSTRUCTIONS="Moon là một cô bạn vui vẻ, thân thiện."
```
> **Lưu ý:** Không chia sẻ file `.env` hoặc token/API key cho người khác.

## Sử dụng
Chạy bot bằng lệnh:
```sh
python main.py
```
- Bot sẽ tự động kết nối Discord và sẵn sàng nhận lệnh.

### Slash Commands
- `/chat` — Gửi câu hỏi tới Moon, có thể chọn công cụ hỗ trợ (None, Web search)
- `/new_chat` — Bắt đầu chủ đề mới với Moon
- `/help` — Xem hướng dẫn sử dụng bot

Bạn cũng có thể mention bot trực tiếp trong kênh để trò chuyện nhanh.

## Đóng góp & Báo lỗi
Mọi đóng góp, ý kiến hoặc báo lỗi đều được hoan nghênh qua Issues hoặc Pull Request.

---
MoonDiscord - Made with ❤️ for Luna!
