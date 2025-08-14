#!/usr/bin/env python3.10

"""
Functions cho Moon Discord Bot

File này chứa tất cả các function mà Moon có thể gọi thông qua OpenAI function calling.
"""

import aiohttp

def register_all_functions(function_registry):
    """Đăng ký tất cả functions vào registry"""
    
    @function_registry.register(
        name="get_current_time",
        description="Lấy thời gian hiện tại",
        parameters={}
    )
    async def get_current_time() -> str:
        """Trả về thời gian hiện tại"""
        try:
            from datetime import datetime
            now = datetime.utcnow()
            return "Giờ UTC: " + now.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return f"❌ Lỗi khi lấy thời gian: {str(e)}"

    # @function_registry.register(
    #     name="get_weather",
    #     description="Lấy thông tin thời tiết thực tế từ Open-Meteo API",
    #     parameters={
    #         "type": "object", 
    #         "properties": {
    #             "city": {
    #                 "type": "string",
    #                 "description": "Tên thành phố hoặc địa điểm"
    #             }
    #         },
    #         "required": ["city"],
    #         "additionalProperties": False
    #     }
    # )
    # async def get_weather(city: str) -> str:
    #     """Lấy thông tin thời tiết thực từ Open-Meteo API"""
    #     try:
    #         # Danh sách tọa độ cho các tỉnh/thành phố Việt Nam (cập nhật 2025)
    #         city_coordinates = {
    #             # Tuyên Quang
    #             "tuyên quang": (21.8167, 105.2167),
    #             "tuyen quang": (21.8167, 105.2167),
                
    #             # Cao Bằng  
    #             "cao bằng": (22.6667, 106.2583),
    #             "cao bang": (22.6667, 106.2583),
                
    #             # Lai Châu
    #             "lai châu": (22.3992, 103.4392),
    #             "lai chau": (22.3992, 103.4392),
                
    #             # Lào Cai
    #             "lào cai": (21.7168, 104.8986),
    #             "lao cai": (21.7168, 104.8986),
                
    #             # Thái Nguyên
    #             "thái nguyên": (21.5928, 105.8311),
    #             "thai nguyen": (21.5928, 105.8311),
                
    #             # Điện Biên
    #             "điện biên": (21.3833, 103.0167),
    #             "dien bien": (21.3833, 103.0167),
                
    #             # Lạng Sơn
    #             "lạng sơn": (21.8478, 106.7578),
    #             "lang son": (21.8478, 106.7578),
                
    #             # Sơn La
    #             "sơn la": (21.3269, 103.9136),
    #             "son la": (21.3269, 103.9136),
                
    #             # Phú Thọ
    #             "phú thọ": (21.3000, 105.4333),
    #             "phu tho": (21.3000, 105.4333),
                
    #             # Bắc Ninh
    #             "bắc ninh": (21.2767, 106.2039),
    #             "bac ninh": (21.2767, 106.2039),
                
    #             # Quảng Ninh
    #             "quảng ninh": (20.9000, 107.2000),
    #             "quang ninh": (20.9000, 107.2000),
                
    #             # TP. Hà Nội
    #             "hà nội": (21.0285, 105.8048),
    #             "hanoi": (21.0285, 105.8048),
    #             "ha noi": (21.0285, 105.8048),
                
    #             # TP. Hải Phòng
    #             "hải phòng": (20.8651, 106.6836),
    #             "hai phong": (20.8651, 106.6836),
                
    #             # Hưng Yên
    #             "hưng yên": (20.8333, 106.0833),
    #             "hung yen": (20.8333, 106.0833),
                
    #             # Ninh Bình
    #             "ninh bình": (20.2539, 105.9750),
    #             "ninh binh": (20.2539, 105.9750),
                
    #             # Thanh Hóa
    #             "thanh hóa": (19.8075, 105.7764),
    #             "thanh hoa": (19.8075, 105.7764),
                
    #             # Nghệ An
    #             "nghệ an": (18.6795, 105.6814),
    #             "nghe an": (18.6795, 105.6814),
    #             "vinh": (18.6795, 105.6814),
                
    #             # Hà Tĩnh
    #             "hà tĩnh": (18.3333, 105.9000),
    #             "ha tinh": (18.3333, 105.9000),
                
    #             # Quảng Trị
    #             "quảng trị": (17.4831, 106.5997),
    #             "quang tri": (17.4831, 106.5997),
                
    #             # TP. Huế
    #             "huế": (16.4667, 107.5792),
    #             "hue": (16.4667, 107.5792),
                
    #             # TP. Đà Nẵng
    #             "đà nẵng": (16.0471, 108.2062),
    #             "da nang": (16.0471, 108.2062),
                
    #             # Quảng Ngãi
    #             "quảng ngãi": (15.1167, 108.8000),
    #             "quang ngai": (15.1167, 108.8000),
                
    #             # Gia Lai
    #             "gia lai": (13.9861, 107.9994),
    #             "pleiku": (13.9861, 107.9994),
                
    #             # Đắk Lắk
    #             "đắk lắk": (12.6842, 108.0508),
    #             "dak lak": (12.6842, 108.0508),
    #             "buôn ma thuột": (12.6842, 108.0508),
    #             "buon ma thuot": (12.6842, 108.0508),
                
    #             # Khánh Hòa
    #             "khánh hòa": (12.2564, 109.1964),
    #             "khanh hoa": (12.2564, 109.1964),
    #             "nha trang": (12.2564, 109.1964),
                
    #             # Lâm Đồng
    #             "lâm đồng": (11.9000, 108.4500),
    #             "lam dong": (11.9000, 108.4500),
    #             "đà lạt": (11.9000, 108.4500),
    #             "da lat": (11.9000, 108.4500),
                
    #             # Đồng Nai
    #             "đồng nai": (10.9641, 106.8564),
    #             "dong nai": (10.9641, 106.8564),
    #             "biên hòa": (10.9641, 106.8564),
    #             "bien hoa": (10.9641, 106.8564),
                
    #             # Tây Ninh
    #             "tây ninh": (10.5392, 106.4136),
    #             "tay ninh": (10.5392, 106.4136),
                
    #             # TP. Hồ Chí Minh
    #             "hồ chí minh": (10.7626, 106.6602),
    #             "ho chi minh": (10.7626, 106.6602),
    #             "saigon": (10.7626, 106.6602),
    #             "sài gòn": (10.7626, 106.6602),
    #             "tp hcm": (10.7626, 106.6602),
    #             "tphcm": (10.7626, 106.6602),
                
    #             # Đồng Tháp
    #             "đồng tháp": (10.3750, 106.2778),
    #             "dong thap": (10.3750, 106.2778),
    #             "cao lãnh": (10.3750, 106.2778),
    #             "cao lanh": (10.3750, 106.2778),
                
    #             # An Giang
    #             "an giang": (10.3759, 105.4185),
    #             "long xuyên": (10.3759, 105.4185),
    #             "long xuyen": (10.3759, 105.4185),
                
    #             # Vĩnh Long
    #             "vĩnh long": (10.2500, 105.9667),
    #             "vinh long": (10.2500, 105.9667),
                
    #             # TP. Cần Thơ
    #             "cần thơ": (10.0452, 105.7469),
    #             "can tho": (10.0452, 105.7469),
                
    #             # Cà Mau
    #             "cà mau": (9.1761, 105.1508),
    #             "ca mau": (9.1761, 105.1508)
    #         }
            
    #         city_lower = city.lower().strip()
            
    #         # Tìm tọa độ của thành phố
    #         coordinates = None
    #         for city_key, coords in city_coordinates.items():
    #             if city_lower in city_key or city_key in city_lower:
    #                 coordinates = coords
    #                 break
            
    #         if not coordinates:
    #             return f"❌ Không tìm thấy tọa độ cho '{city}'. Bot hiện hỗ trợ tất cả 34 tỉnh/thành phố Việt Nam. Hãy thử với tên chính thức hoặc tên thông dụng như: 'Tuyên Quang', 'Cao Bằng', 'Lào Cai', 'Thái Nguyên', 'Hà Nội', 'Hồ Chí Minh', 'Cần Thơ'..."
            
    #         latitude, longitude = coordinates
            
    #         # Gọi Open-Meteo API
    #         url = f"https://api.open-meteo.com/v1/forecast"
    #         params = {
    #             "latitude": latitude,
    #             "longitude": longitude,
    #             "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
    #             "timezone": "Asia/Ho_Chi_Minh"
    #         }
            
    #         async with aiohttp.ClientSession() as session:
    #             async with session.get(url, params=params) as response:
    #                 if response.status != 200:
    #                     return f"❌ Lỗi khi gọi API thời tiết (Status: {response.status})"
                    
    #                 data = await response.json()
            
    #         # Xử lý dữ liệu thời tiết
    #         current = data.get("current", {})
    #         temp = current.get("temperature_2m")
    #         humidity = current.get("relative_humidity_2m")
    #         wind_speed = current.get("wind_speed_10m")
    #         weather_code = current.get("weather_code")
            
    #         # Chuyển đổi weather code thành mô tả
    #         weather_descriptions = {
    #             0: "☀️ Trời quang đãng",
    #             1: "🌤️ Ít mây", 2: "⛅ Mây rải rác", 3: "☁️ Nhiều mây",
    #             45: "🌫️ Sương mù", 48: "🌫️ Sương mù đóng băng",
    #             51: "🌧️ Mưa phùn nhẹ", 53: "🌧️ Mưa phùn vừa", 55: "🌧️ Mưa phùn nặng",
    #             61: "🌦️ Mưa nhẹ", 63: "🌧️ Mưa vừa", 65: "⛈️ Mưa to",
    #             71: "❄️ Tuyết nhẹ", 73: "🌨️ Tuyết vừa", 75: "❄️ Tuyết to",
    #             80: "🌦️ Mưa rào nhẹ", 81: "⛈️ Mưa rào vừa", 82: "⛈️ Mưa rào to",
    #             95: "⛈️ Dông", 96: "⛈️ Dông có mưa đá nhẹ", 99: "⛈️ Dông có mưa đá to"
    #         }
            
    #         weather_desc = weather_descriptions.get(weather_code, "🌡️ Không xác định")
            
    #         # Format kết quả
    #         result = f"🌍 **Thời tiết tại {city.title()}:**\n"
    #         result += f"🌡️ **Nhiệt độ:** {temp}°C\n"
    #         result += f"💧 **Độ ẩm:** {humidity}%\n"
    #         result += f"💨 **Tốc độ gió:** {wind_speed} km/h\n"
    #         result += f"☁️ **Tình trạng:** {weather_desc}\n"
    #         result += f"⏰ **Cập nhật:** {current.get('time', 'N/A')}"
            
    #         return result
            
    #     except aiohttp.ClientError as e:
    #         return f"❌ Lỗi kết nối mạng: {str(e)}"
    #     except Exception as e:
    #         return f"❌ Lỗi khi lấy thông tin thời tiết: {str(e)}"

    @function_registry.register(
        name="get_weather",
        description="Lấy thông tin thời tiết chi tiết từ OpenWeatherMap API. Yêu cầu người dùng cung cấp địa chỉ cụ thể (ví dụ: 'Quận 1, TP. Hồ Chí Minh' hoặc 'Phường Bến Nghé, Quận 1, TP.HCM')",
        parameters={
            "type": "object",
            "properties": {
                "address": {
                    "type": "string", 
                    "description": "Địa chỉ cụ thể của địa điểm cần xem thời tiết (ví dụ: 'Quận 1, TP. Hồ Chí Minh' hoặc 'Phường Bến Nghé, Quận 1, TP.HCM')"
                }
            },
            "required": ["address"],
            "additionalProperties": False
        }
    )
    async def get_weather(address: str) -> str:
        """Lấy thông tin thời tiết chi tiết từ OpenWeatherMap API"""
        try:
            # Import config để lấy API key
            from config import Config
            config = Config()
            api_key = config.openweathermap_api_key
            
            if not api_key:
                return "❌ Chưa cấu hình OpenWeatherMap API key. Vui lòng liên hệ admin."
            
            # Geocoding API để chuyển địa chỉ thành tọa độ
            geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
            geocoding_params = {
                "q": address,
                "limit": 1,
                "appid": api_key
            }
            
            async with aiohttp.ClientSession() as session:
                # Lấy tọa độ từ địa chỉ
                async with session.get(geocoding_url, params=geocoding_params) as response:
                    if response.status != 200:
                        return f"❌ Lỗi khi tìm kiếm địa chỉ (Status: {response.status})"
                    
                    geo_data = await response.json()
                    
                    if not geo_data:
                        return f"❌ Không tìm thấy địa chỉ '{address}'. Vui lòng cung cấp địa chỉ cụ thể hơn (ví dụ: 'Quận 1, TP. Hồ Chí Minh')."
                    
                    location = geo_data[0]
                    lat = location['lat']
                    lon = location['lon']
                    location_name = location.get('local_names', {}).get('vi', location['name'])
                    country = location.get('country', '')
                
                # Lấy thông tin thời tiết từ tọa độ
                weather_url = "https://api.openweathermap.org/data/2.5/weather"
                weather_params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": api_key,
                    "units": "metric",
                    "lang": "vi"
                }
                
                async with session.get(weather_url, params=weather_params) as response:
                    if response.status != 200:
                        return f"❌ Lỗi khi lấy thông tin thời tiết (Status: {response.status})"
                    
                    weather_data = await response.json()
                
                # Lấy thông tin dự báo 5 ngày
                forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
                forecast_params = weather_params.copy()
                forecast_params["cnt"] = 8  # Lấy 8 mốc thời gian (24 giờ tới)
                
                async with session.get(forecast_url, params=forecast_params) as response:
                    if response.status == 200:
                        forecast_data = await response.json()
                    else:
                        forecast_data = None
            
            # Xử lý dữ liệu thời tiết hiện tại
            main = weather_data.get('main', {})
            weather = weather_data.get('weather', [{}])[0]
            wind = weather_data.get('wind', {})
            sys_info = weather_data.get('sys', {})
            
            temp = main.get('temp')
            feels_like = main.get('feels_like')
            temp_min = main.get('temp_min')
            temp_max = main.get('temp_max')
            humidity = main.get('humidity')
            pressure = main.get('pressure')
            
            weather_desc = weather.get('description', 'Không xác định')
            weather_icon = weather.get('icon', '01d')
            
            wind_speed = wind.get('speed', 0) * 3.6  # Chuyển m/s sang km/h
            wind_deg = wind.get('deg', 0)
            
            # Xác định hướng gió
            wind_directions = ["Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"]
            wind_dir_index = int((wind_deg + 22.5) / 45) % 8
            wind_direction = wind_directions[wind_dir_index]
            
            # Icon thời tiết
            weather_icons = {
                '01d': '☀️', '01n': '🌙',
                '02d': '⛅', '02n': '☁️',
                '03d': '☁️', '03n': '☁️',
                '04d': '☁️', '04n': '☁️',
                '09d': '🌧️', '09n': '🌧️',
                '10d': '🌦️', '10n': '🌧️',
                '11d': '⛈️', '11n': '⛈️',
                '13d': '🌨️', '13n': '🌨️',
                '50d': '🌫️', '50n': '🌫️'
            }
            
            icon = weather_icons.get(weather_icon, '🌡️')
            
            # Format kết quả
            result = f"📍 **Thời tiết tại {location_name}, {country}**\n"
            result += f"🗺️ **Địa chỉ:** {address}\n\n"
            
            result += f"**🌡️ Hiện tại:**\n"
            result += f"{icon} **Tình trạng:** {weather_desc.capitalize()}\n"
            result += f"🌡️ **Nhiệt độ:** {temp:.1f}°C (Cảm giác như {feels_like:.1f}°C)\n"
            result += f"📊 **Dao động:** {temp_min:.1f}°C - {temp_max:.1f}°C\n"
            result += f"💧 **Độ ẩm:** {humidity}%\n"
            result += f"🌬️ **Gió:** {wind_speed:.1f} km/h - Hướng {wind_direction}\n"
            result += f"🔵 **Áp suất:** {pressure} hPa\n"
            
            # Thêm dự báo nếu có
            if forecast_data:
                result += f"\n**📅 Dự báo 24 giờ tới:**\n"
                forecast_list = forecast_data.get('list', [])[:8]  # Lấy 8 mốc đầu tiên
                
                seen_dates = set()
                for forecast in forecast_list[:3]:  # Chỉ hiển thị 3 mốc thời gian
                    dt_txt = forecast.get('dt_txt', '')
                    date_time = dt_txt.split(' ')
                    if len(date_time) == 2:
                        time = date_time[1][:5]  # Lấy giờ:phút
                        
                        forecast_main = forecast.get('main', {})
                        forecast_weather = forecast.get('weather', [{}])[0]
                        forecast_temp = forecast_main.get('temp', 0)
                        forecast_desc = forecast_weather.get('description', '')
                        forecast_icon_code = forecast_weather.get('icon', '01d')
                        forecast_icon = weather_icons.get(forecast_icon_code, '🌡️')
                        
                        result += f"  • {time}: {forecast_icon} {forecast_temp:.1f}°C - {forecast_desc}\n"
            
            # Thời gian cập nhật
            from datetime import datetime
            update_time = datetime.now().strftime("%H:%M %d/%m/%Y")
            result += f"\n⏰ **Cập nhật:** {update_time}"
            
            return result
            
        except aiohttp.ClientError as e:
            return f"❌ Lỗi kết nối mạng: {str(e)}"
        except KeyError as e:
            return f"❌ Lỗi khi xử lý dữ liệu thời tiết: {str(e)}"
        except Exception as e:
            return f"❌ Lỗi khi lấy thông tin thời tiết: {str(e)}"