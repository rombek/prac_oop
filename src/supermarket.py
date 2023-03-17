import typing as tp

from src.checkout import Checkout
from src.customer import Customer


class Supermarket:
    MAX_CHECKOUTS_CAPACITY_DIFF: int = 3

    def __init__(
        self,
        checkouts_num: int,
        max_checkout_capacity: int,

    ):
        self._checkouts = [
            Checkout(max_capacity=max_checkout_capacity)
            for _ in range(checkouts_num)
        ]
        self._entering_queue: tp.List[Customer] = []

    def recieve_customer(self, customer: Customer):
        """
        Select possible checkout for customer and send him there.
        1. Select free checkout index
        2. If -1 -> do nothing
        3. If good -> put customer there.
        """
        pass

    def _select_free_checkout(self):
        """Grep all checkouts current capacity and select one depends on conditions(CHECKOUTS_CAP_DIFF)"""
        pass

    @property
    def total_earnings(self):
        return sum(
            (checkout.total_earnings for checkout in self._checkouts),
            start=0
        )

    @property
    def served_customers(self):
        return sum(
            (checkout.served_customers for checkout in self._checkouts),
            start=0
        )

    def get_checkouts_workload(self) -> tp.List[int]:
        return [checkout.current_capacity for checkout in self._checkouts]

    def tick(self, tick_time: int):
        """
        First of all, serve customers in checkouts,
        then grab some new customers from entering queue and send them to checkouts, one by one,
        if customer cannot be sended to any queue, delete him from entering queue.
        By the end of tick, entering queue must be empty!
        """
        checkouts_remaining_time = [
            checkout.tick(tick_time)
            for checkout in self._checkouts
        ]
        for potential_customer in self._entering_queue:
            self.recieve_customer(potential_customer)

        for checkout, checkout_rem_time in zip(self._checkouts, checkouts_remaining_time):
            checkout.tick(checkout_rem_time)
