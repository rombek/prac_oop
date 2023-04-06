import collections
import typing as tp

from src.customer import Customer
from src.utils import logger


class Checkout:
    def __init__(
        self,
        max_capacity: int,
    ):
        self._queue: tp.Deque[Customer] = collections.deque(maxlen=max_capacity)

        self._total_earnings: int = 0
        self._total_served_customers: int = 0
        self._total_waiting_time: int = 0
        self._average_queue_size: float = 0.0
        self._total_ticks = 0

    @property
    def current_customer_progress(self):
        if len(self._queue) == 0:
            return 0
        else:
            total_time = self._queue[-1].service_time
            rem_time = self._queue[-1].remaining_service_time
            return int(rem_time / total_time * 100.0)

    @property
    def current_workload(self):
        return len(self._queue)

    @property
    def total_earnings(self):
        return self._total_earnings

    @property
    def total_served_customers(self):
        return self._total_served_customers

    @property
    def total_waiting_time(self):
        return self._total_waiting_time

    @property
    def average_workload(self):
        return self._average_queue_size

    def receive_customer(self, new_customer: Customer) -> bool:
        """Add customer to the end of checkout"""
        if len(self._queue) == self._queue.maxlen:
            return False
        self._queue.appendleft(new_customer)
        return True

    def _serve_customer(self):
        """Add money to total earnings and increase customers counter and remove customer from queue"""
        cur_customer = self._queue.pop()
        self._total_earnings += cur_customer.purchase_cost
        self._total_served_customers += 1

        logger.debug(f"Serve customer with profit: {cur_customer.purchase_cost}")

    def tick(self, tick_time: int):
        """
        Serve customers and write stats
        """
        remaining_time = tick_time
        self._average_queue_size -= (self._average_queue_size - len(self._queue)) / (self._total_ticks + 1)
        while len(self._queue) != 0 and remaining_time >= self._queue[0].remaining_service_time:
            remaining_time -= self._queue[0].remaining_service_time
            self._serve_customer()
        if len(self._queue) != 0:
            self._queue[0].remaining_service_time -= remaining_time
        else:
            self._total_waiting_time += remaining_time
        self._total_ticks += 1
