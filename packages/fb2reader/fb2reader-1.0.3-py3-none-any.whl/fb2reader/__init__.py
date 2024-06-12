from .fb2reader import fb2book
__all__ = ['get_fb2'],

def _get_file(file):
    file = None    
    if file.lower().endswith(('.fb2')):
        file = fb2book(file)
    return file

def get_fb2(file):
    _get_file(file)

