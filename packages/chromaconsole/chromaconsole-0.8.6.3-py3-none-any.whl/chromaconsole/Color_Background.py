from .styling import Styling

class Background:
    @staticmethod
    def black():
        return "\033[40m" if Styling.is_enabled() else ""
        
    @staticmethod
    def red():
        return "\033[41m" if Styling.is_enabled() else ""
        
    @staticmethod
    def green():
        return "\033[42m" if Styling.is_enabled() else ""
        
    @staticmethod
    def yellow():
        return "\033[43m" if Styling.is_enabled() else ""
        
    @staticmethod
    def blue():
        return "\033[44m" if Styling.is_enabled() else ""
        
    @staticmethod
    def magenta():
        return "\033[45m" if Styling.is_enabled() else ""
        
    @staticmethod
    def cyan():
        return "\033[46m" if Styling.is_enabled() else ""
    
    @staticmethod
    def white():
        return "\033[47m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_black():
        return "\033[100m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_red():
        return "\033[101m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_green():
        return "\033[102m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_yellow():
        return "\033[103m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_blue():
        return "\033[104m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_magenta():
        return "\033[105m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_cyan():
        return "\033[106m" if Styling.is_enabled() else ""
    
    @staticmethod
    def br_white():
        return "\033[107m" if Styling.is_enabled() else ""