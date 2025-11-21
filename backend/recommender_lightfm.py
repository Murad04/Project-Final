"""
This module was previously a LightFM-based recommender.
LightFM has been removed from this project in favor of RecBole.

If you still need the LightFM implementation, restore it from version control.
"""

def __getattr__(name):
    raise ImportError("LightFM support removed. Use RecBole modules instead.")
