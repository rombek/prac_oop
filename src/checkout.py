import typing as tp

from src.customer import Customer


class Checkout:
    def __init__(
        self,
        max_capacity: int,
    ):
        self._current_capacity: int = 0
        self._max_capacity: int = max_capacity

        self._total_earnings: int = 0
        self._served_customers: int = 0

        self._queue: tp.List[Customer] = []
        self._current_time: int = 0
        self._total_waiting_time: int = 0

    @property
    def current_capacity(self):
        return self._current_capacity

    @property
    def total_earnings(self):
        return self._total_earnings

    @property
    def served_customers(self):
        return self._served_customers

    def receive_customer(self, new_customer: Customer):
        """Add customer to the end of checkout"""
        self._queue.append([new_customer])

    def _serve_customer(self):
        """Add money to total earnings and increase customers counter and remove customer from queue"""
        # TODO: write stats
        self._queue.pop(0)

    def tick(self, tick_time: int) -> int:
        """
        In one tick first of all we serve all possible customers, and after we accept new customers.
        So in supermarket tick use order:
            checkout.tick -> send customers to checkouts -> checkout tick with remaining time.
        """
        remaining_time = tick_time
        while remaining_time >= self._queue[0].service_time:
            remaining_time -= self._queue[0].service_time
            self._serve_customer()

        self._current_time += (tick_time - remaining_time)
        # Return remaining time in tick, because we can serve some customers, that come in this tick
        return remaining_time
