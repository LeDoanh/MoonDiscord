#!/usr/bin/env python3.10

"""
Functions cho Moon Discord Bot

File này chứa tất cả các function mà Moon có thể gọi thông qua OpenAI function calling.
"""

import os
import json
import math
import random
import string
import aiohttp
from datetime import datetime
from typing import Dict, Any


def register_all_functions(function_registry):
    """Đăng ký tất cả functions vào registry"""
    
    @function_registry.register(
        name="get_current_time",
        description="Lấy thời gian hiện tại",
        parameters={
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Múi giờ (mặc định là Asia/Ho_Chi_Minh)",
                    "default": "Asia/Ho_Chi_Minh"
                }
            },
            "required": ["timezone"],
            "additionalProperties": False
        }
    )
    async def get_current_time(timezone: str = "Asia/Ho_Chi_Minh") -> str:
        """Trả về thời gian hiện tại"""
        try:
            from datetime import datetime, timedelta
            now = datetime.now()
            # Đảm bảo timezone có giá trị mặc định nếu không được truyền
            if not timezone:
                timezone = "Asia/Ho_Chi_Minh"
                
            if timezone == "Asia/Ho_Chi_Minh":
                return now.strftime("%Y-%m-%d %H:%M:%S UTC+7")
            else:
                return now.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return f"❌ Lỗi khi lấy thời gian: {str(e)}"

    @function_registry.register(
        name="calculate",
        description="Thực hiện phép tính toán học",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Biểu thức toán học để tính (ví dụ: '2+2', '10*5', 'sqrt(16)')"
                }
            },
            "required": ["expression"],
            "additionalProperties": False
        }
    )
    def calculate(expression: str) -> str:
        """Tính toán biểu thức toán học an toàn"""
        # Danh sách các hàm an toàn
        safe_dict = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow,
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "log": math.log, "log10": math.log10, "exp": math.exp,
            "pi": math.pi, "e": math.e
        }
        
        try:
            # Chỉ cho phép các ký tự an toàn
            allowed_chars = set("0123456789+-*/().abcdefghijklmnopqrstuvwxyz_, ")
            if not all(c in allowed_chars for c in expression.lower()):
                return "Biểu thức chứa ký tự không được phép"
            
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return f"Kết quả: {result}"
        except Exception as e:
            return f"Lỗi tính toán: {str(e)}"

    @function_registry.register(
        name="get_weather",
        description="Lấy thông tin thời tiết thực tế từ Open-Meteo API",
        parameters={
            "type": "object", 
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Tên thành phố hoặc địa điểm"
                }
            },
            "required": ["city"],
            "additionalProperties": False
        }
    )
    async def get_weather(city: str) -> str:
        """Lấy thông tin thời tiết thực từ Open-Meteo API"""
        try:
            # Danh sách tọa độ cho các thành phố lớn ở Việt Nam
            city_coordinates = {
                "hà nội": (21.0285, 105.8542),
                "hanoi": (21.0285, 105.8542),
                "hồ chí minh": (10.8231, 106.6297),
                "ho chi minh": (10.8231, 106.6297),
                "saigon": (10.8231, 106.6297),
                "sài gòn": (10.8231, 106.6297),
                "đà nẵng": (16.0544, 108.2022),
                "da nang": (16.0544, 108.2022),
                "cần thơ": (10.0452, 105.7469),
                "can tho": (10.0452, 105.7469),
                "hải phòng": (20.8449, 106.6881),
                "hai phong": (20.8449, 106.6881),
                "huế": (16.4637, 107.5909),
                "hue": (16.4637, 107.5909),
                "nha trang": (12.2388, 109.1967),
                "vũng tàu": (10.4113, 107.1369),
                "vung tau": (10.4113, 107.1369),
                "biên hòa": (10.9446, 106.8197),
                "bien hoa": (10.9446, 106.8197),
                "vinh": (18.6759, 105.6922),
                "pleiku": (13.9833, 108.0),
                "quy nhon": (13.7563, 109.2297),
                "quy nhơn": (13.7563, 109.2297),
                "thái nguyên": (21.5944, 105.8480),
                "thai nguyen": (21.5944, 105.8480),
                "nam định": (20.4339, 106.1739),
                "nam dinh": (20.4339, 106.1739)
            }
            
            city_lower = city.lower().strip()
            
            # Tìm tọa độ của thành phố
            coordinates = None
            for city_key, coords in city_coordinates.items():
                if city_lower in city_key or city_key in city_lower:
                    coordinates = coords
                    break
            
            if not coordinates:
                return f"❌ Không tìm thấy tọa độ cho '{city}'. Hãy thử với các thành phố lớn như: Hà Nội, Hồ Chí Minh, Đà Nẵng, Cần Thơ, Hải Phòng, Huế, Nha Trang, Vũng Tàu..."
            
            latitude, longitude = coordinates
            
            # Gọi Open-Meteo API
            url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "timezone": "Asia/Ho_Chi_Minh"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        return f"❌ Lỗi khi gọi API thời tiết (Status: {response.status})"
                    
                    data = await response.json()
            
            # Xử lý dữ liệu thời tiết
            current = data.get("current", {})
            temp = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            wind_speed = current.get("wind_speed_10m")
            weather_code = current.get("weather_code")
            
            # Chuyển đổi weather code thành mô tả
            weather_descriptions = {
                0: "☀️ Trời quang đãng",
                1: "🌤️ Ít mây", 2: "⛅ Mây rải rác", 3: "☁️ Nhiều mây",
                45: "🌫️ Sương mù", 48: "🌫️ Sương mù đóng băng",
                51: "🌧️ Mưa phùn nhẹ", 53: "🌧️ Mưa phùn vừa", 55: "🌧️ Mưa phùn nặng",
                61: "🌦️ Mưa nhẹ", 63: "🌧️ Mưa vừa", 65: "⛈️ Mưa to",
                71: "❄️ Tuyết nhẹ", 73: "🌨️ Tuyết vừa", 75: "❄️ Tuyết to",
                80: "🌦️ Mưa rào nhẹ", 81: "⛈️ Mưa rào vừa", 82: "⛈️ Mưa rào to",
                95: "⛈️ Dông", 96: "⛈️ Dông có mưa đá nhẹ", 99: "⛈️ Dông có mưa đá to"
            }
            
            weather_desc = weather_descriptions.get(weather_code, "🌡️ Không xác định")
            
            # Format kết quả
            result = f"🌍 **Thời tiết tại {city.title()}:**\n"
            result += f"🌡️ **Nhiệt độ:** {temp}°C\n"
            result += f"💧 **Độ ẩm:** {humidity}%\n"
            result += f"💨 **Tốc độ gió:** {wind_speed} km/h\n"
            result += f"☁️ **Tình trạng:** {weather_desc}\n"
            result += f"⏰ **Cập nhật:** {current.get('time', 'N/A')}"
            
            return result
            
        except aiohttp.ClientError as e:
            return f"❌ Lỗi kết nối mạng: {str(e)}"
        except Exception as e:
            return f"❌ Lỗi khi lấy thông tin thời tiết: {str(e)}"