from torlog_package.utils.logic import generate_rainbow_colors, hex_to_rgb, parse_color
from torlog_package.utils.errors import error_list
import time
import sys


current_step = 0

def log(message, rainbow: bool = False, interval: int = 1, static: str = "#FFFFFF"):
    global current_step

    if isinstance(interval, float):
        print(error_list[0])
        sys.exit()
    
    if not isinstance(rainbow, bool):
        print(error_list[1])
        sys.exit()
        
    if interval > 63 or interval < 1:
        print(error_list[2])
        sys.exit()
    
    if rainbow and static != "#FFFFFF":
        print(error_list[4])
        sys.exit()

    standard_colors = {
        "red": "#FF0000",
        "green": "#00FF00",
        "blue": "#0000FF",
        "light_red": "#FF9999",
        "dark_red": "#800000",
        "light_green": "#90EE90",
        "dark_green": "#006400",
        "light_blue": "#ADD8E6",
        "dark_blue": "#00008B",
        "yellow": "#FFFF00",
        "light_yellow": "#FFFFE0",
        "dark_yellow": "#808000",
        "orange": "#FFA500",
        "light_orange": "#FFD700",
        "dark_orange": "#FF8C00",
        "purple": "#800080",
        "light_purple": "#BA55D3",
        "dark_purple": "#4B0082",
        "cyan": "#00FFFF",
        "light_cyan": "#E0FFFF",
        "dark_cyan": "#008B8B",
        "magenta": "#FF00FF",
        "light_magenta": "#FFB6C1",
        "dark_magenta": "#8B008B",
        "pink": "#FFC0CB",
        "light_pink": "#FFB6C1",
        "dark_pink": "#FF69B4",
        "brown": "#A52A2A",
        "light_brown": "#D2B48C",
        "dark_brown": "#8B4513",
        "gray": "#808080",
        "light_gray": "#D3D3D3",
        "dark_gray": "#A9A9A9",
        "black": "#000000",
        "white": "#FFFFFF",
        "lighter_red": "#FF6666",
        "darker_red": "#660000",
        "lighter_green": "#66FF66",
        "darker_green": "#006600",
        "lighter_blue": "#6666FF",
        "darker_blue": "#000066",
        "lighter_yellow": "#FFFF66",
        "darker_yellow": "#666600",
        "lighter_orange": "#FF9933",
        "darker_orange": "#994C00",
        "lighter_purple": "#CC66FF",
        "darker_purple": "#660066",
        "lighter_cyan": "#66FFFF",
        "darker_cyan": "#006666",
        "lighter_magenta": "#FF99CC",
        "darker_magenta": "#990066",
        "lighter_pink": "#FF99CC",
        "darker_pink": "#993366",
        "lighter_brown": "#CC9966",
        "darker_brown": "#663300",
        "lighter_gray": "#CCCCCC",
        "darker_gray": "#666666",
    }

    if static.lower() in standard_colors:
        static = standard_colors[static.lower()]
    else:
        static = parse_color(static)
        if static == None:
            print(error_list[3])
            sys.exit()

    rainbow_colors = generate_rainbow_colors()
    
    if not rainbow:
        colored_time = f"\033[38;2;{hex_to_rgb(static)[0]};{hex_to_rgb(static)[1]};{hex_to_rgb(static)[2]}m[{time.strftime('%H:%M:%S')}]\033[0m"
        print(f"{colored_time} | {message}")
        return

    steps = len(rainbow_colors) // interval

    current_time = time.strftime("%H:%M:%S")
    colored_time = ""

    for char in current_time:
        char_color = ""
        for step in range(steps):
            progress = step * interval / len(rainbow_colors)
            rainbow_index = int(progress * len(rainbow_colors))
            rainbow_index = min(rainbow_index, len(rainbow_colors) - 1)
            color = rainbow_colors[rainbow_index]
            char_color = f"\033[38;2;{hex_to_rgb(color)[0]};{hex_to_rgb(color)[1]};{hex_to_rgb(color)[2]}m{char}\033[0m"
            if step == current_step:
                break
        colored_time += char_color

    try:
        print(f"[{colored_time}] | {message}")
    except Exception as e:
        pass

    current_step += 1
    if current_step >= steps:
        current_step = 0
