from .styling import Styling

class Text:
    @staticmethod
    def black():
        return "\033[30m" if Styling.is_enabled() else ""
        
    @staticmethod
    def red():
        return "\033[31m" if Styling.is_enabled() else ""
        
    @staticmethod
    def green():
        return "\033[32m" if Styling.is_enabled() else ""
        
    @staticmethod
    def yellow():
        return "\033[33m" if Styling.is_enabled() else ""
        
    @staticmethod
    def blue():
        return "\033[34m" if Styling.is_enabled() else ""
        
    @staticmethod
    def magenta():
        return "\033[35m" if Styling.is_enabled() else ""
        
    @staticmethod
    def cyan():
        return "\033[36m" if Styling.is_enabled() else ""
    
    @staticmethod
    def white():
        return "\033[37m" if Styling.is_enabled() else ""
    
    @staticmethod
    def br_black():
        return "\033[90m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_red():
        return "\033[91m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_green():
        return "\033[92m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_yellow():
        return "\033[93m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_blue():
        return "\033[94m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_magenta():
        return "\033[95m" if Styling.is_enabled() else ""
        
    @staticmethod
    def br_cyan():
        return "\033[96m" if Styling.is_enabled() else ""
    
    @staticmethod
    def br_white():
        return "\033[97m" if Styling.is_enabled() else ""