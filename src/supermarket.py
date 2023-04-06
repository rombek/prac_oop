import typing as tp

import numpy as np

from src.checkout import Checkout
from src.customer import Customer
from src.utils import logger, MINUTES_PER_DAY


class Supermarket:
    MAX_CHECKOUTS_CAPACITY_DIFF: int = 3

    def __init__(
        self,
        checkouts_num: int,
        max_checkout_capacity: int,
        cashier_salary_per_day: int,
        ads_spend_per_day: int,
        discount_percent: float,
        profit_per_sale_percent: int,
    ):
        self._checkouts: tp.List[Checkout] = [
            Checkout(max_capacity=max_checkout_capacity)
            for _ in range(checkouts_num)
        ]
        self.ads_spend_per_day = ads_spend_per_day
        self.discount_percent = discount_percent
        self.cashier_salary_per_day = cashier_salary_per_day
        self.profit_per_sale_percent = profit_per_sale_percent
        self._total_lost_customers = 0
        self._total_spent_on_ads = 0
        self._total_spent_on_salaries = 0
        self._total_spent_on_discounts = 0
        self._current_day_time = 0

        logger.debug(f'Created Supermarket with {checkouts_num} checkouts(max_capacity={max_checkout_capacity})')

    def _apply_discount_to_customer(self, customer: Customer) -> Customer:
        new_purchase_cost = int(customer.purchase_cost * (100 - self.discount_percent) / 100.0)
        if new_purchase_cost != customer.purchase_cost:
            logger.debug(f"Applied discount to customer: {customer.purchase_cost} -> {new_purchase_cost}")
        self._total_spent_on_discounts += customer.purchase_cost - new_purchase_cost

        return Customer(
            purchase_cost=new_purchase_cost,
            remaining_service_time=customer.remaining_service_time,
            service_time=customer.service_time,
        )

    def recieve_customers(self, customers: tp.List[Customer]):
        """Send customer to some checkout or add to lost clients"""
        for customer in customers:
            updated_customer = self._apply_discount_to_customer(customer)
            logger.debug(f"Recieve customer {customer}, update to {updated_customer}")
            possible_checkout: int = np.argmin(self.current_checkouts_workload)
            is_customer_recieved = self._checkouts[possible_checkout].receive_customer(updated_customer)
            logger.debug(f"Sending customer in checkout № {possible_checkout} with status {is_customer_recieved}")
            if not is_customer_recieved:
                self._total_lost_customers += 1

    def tick(self, tick_time: int):
        logger.debug('Supermarket tick')
        for idx, checkout in enumerate(self._checkouts):
            logger.debug(f"Tick in checkout #{idx}")
            checkout.tick(tick_time)
        self._current_day_time += tick_time
        if self._current_day_time > MINUTES_PER_DAY:
            logger.debug(
                f'Day passed ->'
                f' +{self.ads_spend_per_day} on ads,'
                f' +{self.cashier_salary_per_day * len(self._checkouts)} on salaries'
            )
            self._current_day_time %= MINUTES_PER_DAY
            self._total_spent_on_ads += self.ads_spend_per_day
            self._total_spent_on_salaries += self.cashier_salary_per_day * len(self._checkouts)

    @property
    def current_checkouts_workload(self) -> tp.List[int]:
        return [checkout.current_workload for checkout in self._checkouts]

    @property
    def current_checkouts_customer_progress(self) -> tp.List[int]:
        return [checkout.current_customer_progress for checkout in self._checkouts]

    #  Stats section
    @property
    def average_checkouts_workload(self) -> tp.List[float]:
        return [
            checkout.average_workload
            for checkout in self._checkouts
        ]

    @property
    def total_served_customers(self):
        return sum(
            (checkout.total_served_customers for checkout in self._checkouts),
            start=0
        )

    @property
    def total_earnings(self):
        return sum(
            (checkout.total_earnings for checkout in self._checkouts),
            start=0
        )

    @property
    def total_profit(self):
        return self.total_earnings * self.profit_per_sale_percent / 100.0

    @property
    def total_lost_customers(self):
        return self._total_lost_customers

    @property
    def total_spent_on_ads(self):
        return self._total_spent_on_ads

    @property
    def total_spent_on_salaries(self):
        return self._total_spent_on_salaries

    @property
    def total_spent_on_discounts(self):
        return self._total_spent_on_discounts
