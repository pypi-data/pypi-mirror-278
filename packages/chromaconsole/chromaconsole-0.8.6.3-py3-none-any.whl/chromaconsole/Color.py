from .styling import Styling
from .ColorBackground import Background as background
from .ColorText import Text as text

def parse_color(*args):
    if len(args) == 1:
        if type(args[0]) == tuple:
            r, g, b = args[0]           #*  (rrr,ggg,bbb)
            return (r,g,b)
        else:
            color = args[0].lstrip("#")
            if "," in color:            #*  "rrr,ggg,bbb"
                color = color.replace(" ", "").replace("(", "").replace(")", "")
                color = color.split(",")
                r, g, b = map(int, color)
                return (r,g,b)
            if len(color) == 3:         #*  "#rgb"
                r, g, b = (int(c * 2, 16) for c in color)
                return (r,g,b)
            elif len(color) == 6:       #*  "#rrggbb"
                r, g, b = (int(color[i:i+2], 16) for i in range(0, 6, 2))
                return (r,g,b)
            else:
                raise ValueError(f"Invalid color format\n{args}")
    elif len(args) == 3:
        r, g, b = args
    else:
        raise ValueError(f"Invalid color format\n{args}")
    
def interpolate_color(start_color, end_color, factor):
    return tuple(int(start + (end - start) * factor) for start, end in zip(start_color, end_color))

class Color:
    class Text:
        '''
        Set foreground [color](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)
        '''
        black = staticmethod(text.black)
        red = staticmethod(text.red)
        green = staticmethod(text.green)
        yellow = staticmethod(text.yellow)
        blue = staticmethod(text.blue)
        magenta = staticmethod(text.magenta)
        cyan = staticmethod(text.cyan)
        white = staticmethod(text.white)
        br_black = staticmethod(text.br_black)
        br_red = staticmethod(text.br_red)
        br_green = staticmethod(text.br_green)
        br_yellow = staticmethod(text.br_yellow)
        br_blue = staticmethod(text.br_blue)
        br_magenta = staticmethod(text.br_magenta)
        br_cyan = staticmethod(text.br_cyan)
        br_white = staticmethod(text.br_white)
    class Background:
        '''
        Set background [color](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)
        '''
        black = staticmethod(background.black)
        red = staticmethod(background.red)
        green = staticmethod(background.green)
        yellow = staticmethod(background.yellow)
        blue = staticmethod(background.blue)
        magenta = staticmethod(background.magenta)
        cyan = staticmethod(background.cyan)
        white = staticmethod(background.white)
        br_black = staticmethod(background.br_black)
        br_red = staticmethod(background.br_red)
        br_green = staticmethod(background.br_green)
        br_yellow = staticmethod(background.br_yellow)
        br_blue = staticmethod(background.br_blue)
        br_magenta = staticmethod(background.br_magenta)
        br_cyan = staticmethod(background.br_cyan)
        br_white = staticmethod(background.br_white)

    @staticmethod
    def text(*args): #38;2;r;g;bm
        '''
        changes the color of the text\n
        Color.text(r, g, b)\n
        Color.text("#rrggbb")
        '''
        if args[0] == "":
            return ""
        if Styling.is_enabled():
            return f"\033[38;2;{parse_color(*args)[0]};{parse_color(*args)[1]};{parse_color(*args)[2]}m"
        else:
            return ""
        
    @staticmethod
    def text_gradient(text, start_color, end_color):
        '''
        this can be used to make text gradient\n
        text_gradient(str, (r,g,b) or "#rrggbb" , (r,g,b) or "#rrggbb")
        '''
        gradient_text = ""

        start_color = parse_color(start_color)
        end_color = parse_color(end_color)

        # Compute interpolation steps
        interpolation_step = 1 / (len(text) - 1)
        for i, char in enumerate(text):
            factor = i * interpolation_step
            interpolated_color = interpolate_color(start_color, end_color, factor)
            gradient_text += str(Color.text(interpolated_color)) + char

        return gradient_text + Color.default_text()
        
    @staticmethod
    def default_text(): #39m
        '''
        Default foreground color\n
        Implementation defined (according to standard)
        '''
        return "\033[39m" if Styling.is_enabled() else ""
    
    @staticmethod
    def background(*args): #48;2;r;g;bm
        '''
        changes the color of the text background\n
        Color.background(r, g, b)\n
        Color.background("#rrggbb")
        '''
        if args[0] == "":
            return ""
        if Styling.is_enabled():
            return f"\033[48;2;{parse_color(*args)[0]};{parse_color(*args)[1]};{parse_color(*args)[2]}m"
        else:
            return ""
        
    @staticmethod
    def background_gradient(text, start_color, end_color):
        '''
        this can be used to make background gradient\n
        background_gradient(str, (r,g,b) or "#rrggbb" , (r,g,b) or "#rrggbb")
        '''
        gradient_text = ""

        start_color = parse_color(start_color)
        end_color = parse_color(end_color)

        # Compute interpolation steps
        interpolation_step = 1 / (len(text) - 1)
        for i, char in enumerate(text):
            factor = i * interpolation_step
            interpolated_color = interpolate_color(start_color, end_color, factor)
            gradient_text += Color.background(interpolated_color) + char

        return gradient_text + Color.default_background()
    
    @staticmethod
    def default_background(): #49m
        '''
        Default background color\n
        Implementation defined (according to standard)
        '''
        return "\033[49m" if Styling.is_enabled() else ""