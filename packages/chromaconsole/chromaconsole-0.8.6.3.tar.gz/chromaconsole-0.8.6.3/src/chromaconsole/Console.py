class Console:
    @staticmethod
    def clr_scr_to_end():
        '''Clear from cursor to end of screen'''
        return '\033[0J'
    
    @staticmethod
    def clr_scr_to_begin():
        '''Clear from cursor to beginning of screen'''
        return '\033[1J'
    
    @staticmethod
    def clr_entire_scr():
        '''Clear entire screen'''
        return '\033[2J'

    @staticmethod
    def clr_line_to_end():
        '''Clear from cursor to end of line'''
        return '\033[0K'

    @staticmethod
    def clr_line_to_begin():
        '''Clear from cursor to beginning of line'''
        return '\033[1K'

    @staticmethod
    def clr_entire_line():
        '''Clear entire line'''
        return '\033[2K'
    
    @staticmethod
    def scroll_up(n=1):
        '''
        Scroll the whole page up by n (default 1) lines.
        New lines are added at the bottom.
        '''
        if n > 0:
            return f'\033[{n}S'
        return ''

    @staticmethod
    def scroll_down(n=1):
        '''
        Scroll the whole page down by n (default 1) lines.
        New lines are added at the top.
        '''
        if n > 0:
            return f'\033[{n}T'
        return ''
    
    @staticmethod
    def bell():
        '''
        Sends a BEL (Bell) control character to make an audible noise.
        '''
        print('\x07', end="")
    
    @staticmethod
    def save_cursor():
        '''
        Save the current cursor position.
        Returns: ANSI escape code to save cursor position.
        '''
        return '\033[s'

    @staticmethod
    def restore_cursor():
        '''
        Restore the previously saved cursor position.
        Returns: ANSI escape code to restore cursor position.
        '''
        return '\033[u'
    
    @staticmethod
    def switch_alt_scr():
        '''
        Switch to the alternative screen buffer (CSI ? 1049 h).
        '''
        print('\033[?1049h', end='')

    @staticmethod
    def switch_orig_scr():
        '''
        Switch back to the original screen buffer (CSI ? 1049 l).
        '''
        print('\033[?1049l', end='')

    @staticmethod
    def show_cursor():
        '''
        Show the cursor (CSI ? 25 h).
        '''
        print('\033[?25h', end='')

    @staticmethod
    def hide_cursor():
        '''
        Hide the cursor (CSI ? 25 l).
        '''
        print('\033[?25l', end='')
