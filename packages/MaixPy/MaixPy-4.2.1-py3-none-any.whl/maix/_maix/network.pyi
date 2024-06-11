"""
maix.network module
"""
from __future__ import annotations
__all__ = ['have_network']
def have_network() -> bool:
    """
    Return if device have network(WiFi/Eth etc.)
    
    Returns: True if have network, else False.
    """
