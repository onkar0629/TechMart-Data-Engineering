"""Review service extension point.

The current review generator derives reviews directly from delivered purchases
and writes CSV output. This module remains as a documented architectural slot
for future review-specific business rules.
"""

from __future__ import annotations


class ReviewService:
    """Reserved service boundary for future review workflows."""
