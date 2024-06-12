from .fb2reader import fb2
__all__ = ['get_fb2'],


def _get_file(file):
    file = None
    
    if file.lower().endswith(('.fb2')):
        file = fb2(file)
    return file


def get_fb2(file):
    fb2 = _get_file(file)
