def generate_rainbow_colors():
    rainbow_colors = [
        "#FF0000", "#FF2600", "#FF4D00", "#FF7300", "#FF9900", "#FFBF00",
        "#FFE500", "#FFEB1A", "#FFF040", "#FFF666", "#FFFB8C", "#FFFFB2",
        "#FFFFD8", "#FFFFFF", "#E2FFE2", "#C6FFC6", "#A9FFA9", "#8CFF8C",
        "#70FF70", "#54FF54", "#37FF37", "#1BFF1B", "#00FF00", "#00FA28",
        "#00F450", "#00F778", "#00F29F", "#00EDC7", "#00E8EF", "#00D6FF",
        "#00BFFF", "#00AAFF", "#0095FF", "#007FFF", "#006AFF", "#0054FF",
        "#003EFF", "#0029FF", "#0013FF", "#0A00FF", "#2000FF", "#3500FF",
        "#4B00FF", "#6000FF", "#7600FF", "#8C00FF", "#A200FF", "#B700FF",
        "#CD00FF", "#E300FF", "#F900FF", "#FF00FB", "#FF00E5", "#FF00D0",
        "#FF00BA", "#FF00A5", "#FF008F", "#FF007A", "#FF0064", "#FF004F",
        "#FF0039"
    ]
    return rainbow_colors

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def interpolate_color(start_color, end_color, progress):
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    interpolated_rgb = [int(start + (end - start) * progress) for start, end in zip(start_rgb, end_rgb)]
    return "#" + "".join(format(c, "02x") for c in interpolated_rgb)

def parse_color(color_str):
    try:
        if color_str.startswith("#"):
            # Check if the string represents a valid hexadecimal color
            if len(color_str) == 7 and all(c in "0123456789ABCDEFabcdef" for c in color_str[1:]):
                return color_str
            else:
                return None
        else:
            # Add "#" if not present and check if the resulting string is a valid hexadecimal color
            color_with_hash = "#" + color_str
            if len(color_with_hash) == 7 and all(c in "0123456789ABCDEFabcdef" for c in color_with_hash[1:]):
                return color_with_hash
            else:
                return None
    except ValueError as e:
        return None