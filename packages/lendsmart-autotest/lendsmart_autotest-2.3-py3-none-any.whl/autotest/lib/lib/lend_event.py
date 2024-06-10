"""
    hold the lend event
"""

from dataclasses import dataclass


@dataclass
class LendEvent:
    """
        Hold the event data
    """
    event_data: dict
