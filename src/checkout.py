from dataclasses import dataclass
import typing as tp


@dataclass
class CustomerInfo:
    serve_time: int
    purchase_price: int


class Checkout:
    def __init__(
        self,
        max_capacity: int,
        service_time_range: tp.Tuple[int, int],
        purchase_price_range: tp.Tuple[int, int],
    ):
        self._current_capacity: int = 0
        self._max_capacity: int = max_capacity

        self._service_time_range: tp.Tuple[int, int] = service_time_range
        self._purchase_price_range: tp.Tuple[int, int] = purchase_price_range

        self._total_earnings: int = 0
        self._served_customers: int = 0

        self._last_customer: CustomerInfo = CustomerInfo(serve_time=0, purchase_price=0)

    @property
    def current_capacity(self):
        return self._current_capacity

    @property
    def total_earnings(self):
        return self._total_earnings

    @property
    def served_customers(self):
        return self._served_customers

    def recieve_customer(self):
        """Add customer to the end of checkout"""
        self._current_capacity += 1

    def _serve_customer(self):
        """Add money to total earnings and increase customers counter"""
        pass

    def tick(self, tick_time: int):
        """In one tick first of all we serve all possible customers, and after we accept new customers"""
        remaining_time = tick_time
        while remaining_time >= self._last_customer.serve_time:
            self._serve_customer()
            remaining_time -= self._last_customer.serve_time
