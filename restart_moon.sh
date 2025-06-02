#!/bin/bash

# Kích hoạt môi trường ảo
source .venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Dừng tiến trình cũ nếu tồn tại
if [ -f moon_pid.txt ]; then
    kill -9 $(cat moon_pid.txt) 2>/dev/null
    rm moon_pid.txt
fi

# Chạy lại bot và lưu PID
nohup python3 main.py > moon.log 2>&1 &
echo $! > moon_pid.txt