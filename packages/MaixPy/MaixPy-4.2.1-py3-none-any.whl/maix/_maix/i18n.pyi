"""
maix.i18n module
"""
from __future__ import annotations
__all__ = ['Trans', 'get_language_name', 'get_locale', 'locales', 'names']
class Trans:
    def __init__(self, locales_dict: dict[str, dict[str, str]]) -> None:
        ...
    def get_locale(self) -> str:
        """
        Get current locale.
        
        Returns: locale name, e.g. "zh", "en", etc. @see maix.i18n.locales
        """
    def set_locale(self, locale: str) -> None:
        """
        Set locale temporarily, will not affect system settings.
        
        Args:
          - locale: locale name, e.g. "zh", "en", etc. @see maix.i18n.locales
        """
    def tr(self, key: str, locale: str = '') -> str:
        """
        Translate string by key.
        
        Args:
          - key: string key, e.g. "Confirm"
          - locale: locale name, if not assign, use default locale set by system settings or set_locale function.
        
        
        Returns: translated string, if find translation, return it, or return key, e.g. "确认", "Confirm", etc.
        """
def get_language_name() -> str:
    """
    Get system config of language name.
    
    Returns: language name, e.g. English, 简体中文, 繁體中文, etc.
    """
def get_locale() -> str:
    """
    Get system config of locale.
    
    Returns: language locale, e.g. en, zh, zh_CN, zh_TW, etc.
    """
locales: list = ['en', 'zh', 'zh-tw', 'ja']
names: list = ['English', '简体中文', '繁體中文', '日本語']
