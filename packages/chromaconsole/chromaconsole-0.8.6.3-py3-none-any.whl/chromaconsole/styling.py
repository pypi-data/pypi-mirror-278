class Styling:
    _enabled = True

    @classmethod
    def disable(cls):
        cls._enabled = False
        return ""

    @classmethod
    def enable(cls):
        cls._enabled = True
        return ""

    @classmethod
    def is_enabled(cls):
        return cls._enabled
