import platform

if platform.system().lower() == 'windows':
    from .windows import BGram
else:
    from .termux import BGram

__all__ = [
    'BGram'
]