from enum import Enum


class ClipDuration(Enum):
    """Duration options for the duration of a clip."""

    UNDER_30 = "UNDER_30"
    BETWEEN_30_AND_60 = "BETWEEN_30_AND_60"
    BETWEEN_60_AND_90 = "BETWEEN_60_AND_90"
    BETWEEN_90_AND_180 = "BETWEEN_90_AND_180"
