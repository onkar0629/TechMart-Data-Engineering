from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..config import ORDER_COUNT
from ..logger import setup_logger
from ..models.payment import Payment
from ..services.order_service import OrderSimulationContext
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class PaymentGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)
        self._context = OrderSimulationContext(input_dir=self.output_dir)

    def generate(self, order_count: int = ORDER_COUNT) -> List[Dict[str, Any]]:
        logger.info("Generating Payments")
        simulation = self._context.get_simulation(target_orders=order_count)
        rows = [self._to_row(payment) for payment in simulation.payments]
        logger.info("CSV Writing")
        write_csv(self.output_dir / "payments.csv", rows)
        logger.info("Payments generated: %s", len(rows))
        return rows

    def _to_row(self, payment: Payment) -> Dict[str, Any]:
        return {
            "payment_id": payment.payment_id,
            "order_id": payment.order_id,
            "payment_method": payment.payment_method,
            "payment_date": payment.payment_date.strftime("%Y-%m-%d %H:%M:%S"),
            "payment_status": payment.payment_status,
            "payment_amount": payment.payment_amount,
            "transaction_reference": payment.transaction_reference,
        }
