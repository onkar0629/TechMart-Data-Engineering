"""Payment service extension point.

Payment records are currently generated as part of ``OrderService`` so order
totals, order statuses, and payment statuses stay consistent in one simulation.
This module remains as a documented architectural slot for future payment-only
rules and intentionally contains no business behavior today.
"""

from __future__ import annotations


class PaymentService:
    """Reserved service boundary for future payment workflows."""
