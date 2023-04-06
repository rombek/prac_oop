import random
import sys
import typing as tp

from src.customer import Customer
from src.supermarket import Supermarket
from src.utils import (
    logger,
    HOURS_PER_DAY,
    MINUTES_PER_DAY,
    MINUTES_PER_HOUR,
    Weekday,
)


class SupermarketModel:
    ADS_FLOW_INCREASE_PERCENT = 10
    ADS_COST_TO_FLOW_INCREASE = 7000

    DISCOUNT_FLOW_INCREASE_PERCENT = 0.5
    DISCOUNT_COST_TO_FLOW_INCREASE = 1

    EVENING_FLOW_INCREASE_PERCENT = 25
    DAYTIME_HOURS_WITH_HIGH_FLOW = [16, 17, 18, 19]
    WEEKENDS_FLOW_INCREASE_PERCENT = 25

    FLOW_DECREASE_PER_PERSON_PERCENT = 5

    def __init__(
        self,
        total_checkouts: int,
        max_checkout_capacity: int,
        time_between_customers_range: tp.Tuple[int, int],
        customer_service_time_range: tp.Tuple[int, int],
        customer_purchase_price_range: tp.Tuple[int, int],
        ads_spend_per_day: int,
        discount_percent: float,
        profit_per_sale_percent: float,
        cashier_salary_per_day: int,
        tick_time: int,
        random_state: int = None
    ):
        self._supermarket = Supermarket(
            checkouts_num=total_checkouts,
            max_checkout_capacity=max_checkout_capacity,
            ads_spend_per_day=ads_spend_per_day,
            discount_percent=discount_percent,
            cashier_salary_per_day=cashier_salary_per_day,
            profit_per_sale_percent=profit_per_sale_percent
        )
        self._time_between_customers_range = time_between_customers_range
        self._customer_service_time_range = customer_service_time_range
        self._customer_purchase_price_range = customer_purchase_price_range
        self._tick_time = tick_time
        self._current_weekday = Weekday.MONDAY
        self._current_daytime_minutes = 0  # in minutes
        self._current_tick = 0
        self._passed_days = 0
        logger.debug(
            f"Model with parameters: tick_time={self._tick_time}, "
            f"time_btw_cust = {self._time_between_customers_range}")
        # if random_state:
        #     random.setstate(random_state)

    def _get_updated_time_between_customers(self):
        current_time_between_customers_range = self._time_between_customers_range
        flow_increase_percent = 0

        #  Day/week time flow increase
        if self._current_weekday in [Weekday.SATURDAY, Weekday.SUNDAY]:
            flow_increase_percent += self.WEEKENDS_FLOW_INCREASE_PERCENT
        if self._current_daytime_minutes // MINUTES_PER_HOUR in self.DAYTIME_HOURS_WITH_HIGH_FLOW:
            flow_increase_percent += self.EVENING_FLOW_INCREASE_PERCENT

        #  Ads flow increase
        ads_spend_per_day = self._supermarket.ads_spend_per_day
        flow_increase_percent += (ads_spend_per_day // self.ADS_COST_TO_FLOW_INCREASE) * self.ADS_FLOW_INCREASE_PERCENT

        #  Discounts flow increase
        discount_percent = self._supermarket.discount_percent
        flow_increase_percent += \
            (discount_percent // self.DISCOUNT_COST_TO_FLOW_INCREASE) * self.DISCOUNT_FLOW_INCREASE_PERCENT

        #  Current workload flow decrease (min queue in checkouts -> -X% per each person
        min_checkout_workload = min(self._supermarket.current_checkouts_workload)
        flow_increase_percent -= min_checkout_workload * self.FLOW_DECREASE_PER_PERSON_PERCENT

        logger.debug(
            f"ADS FLOW increase percent = {(ads_spend_per_day // self.ADS_COST_TO_FLOW_INCREASE) * self.ADS_FLOW_INCREASE_PERCENT}")
        logger.debug(f"FLOW increase percent = {flow_increase_percent}")
        return tuple(
            map(
                int,
                [t * 100 / (100 + flow_increase_percent) for t in self._time_between_customers_range]
            )
        )

    def _generate_customers(self) -> tp.List[Customer]:
        """
        Generate customers with given random parameters.
        """
        remaining_time = self._tick_time
        generated_customers = []
        updated_time_between_customers_range = self._get_updated_time_between_customers()

        while remaining_time > 0:
            customer_service_time = random.randint(*self._customer_service_time_range)
            generated_customers.append(
                Customer(
                    service_time=customer_service_time,
                    remaining_service_time=customer_service_time,
                    purchase_cost=random.randint(*self._customer_purchase_price_range)
                )
            )
            time_between_customers = random.randint(*updated_time_between_customers_range)
            remaining_time -= time_between_customers
        return generated_customers

    def tick(self):
        """
        Grab statistics about checkouts current workload,
        generate new customers based on this, weekday, ads and discounts.
        Then makes supermarket tick.
        """
        generated_customers = self._generate_customers()
        logger.debug(f'TICK# {self._current_tick + 1}: generated_customers = {generated_customers}')
        self._supermarket.recieve_customers(generated_customers)
        self._supermarket.tick(self._tick_time)
        self._current_daytime_minutes += self._tick_time
        if self._current_daytime_minutes >= MINUTES_PER_DAY:
            self._current_daytime_minutes %= MINUTES_PER_DAY
            self._current_weekday += 1
            self._passed_days += 1
            self._current_weekday %= len(Weekday)
        self._current_tick += 1

    # Stats sections

    def average_checkouts_workload(self) -> tp.List[float]:
        return self._supermarket.average_checkouts_workload

    def total_served_customers(self) -> int:
        return self._supermarket.total_served_customers

    def total_lost_customers(self) -> int:
        return self._supermarket.total_lost_customers

    def total_potential_customers(self) -> int:
        return self._supermarket.total_lost_customers + self._supermarket.total_served_customers

    def total_earnings(self) -> int:
        return self._supermarket.total_earnings

    def total_profit(self) -> int:
        return self._supermarket.total_profit

    def total_spent_on_ads(self):
        return self._supermarket.total_spent_on_ads

    def total_spent_on_salaries(self):
        return self._supermarket.total_spent_on_salaries

    def total_spent_on_discounts(self):
        return self._supermarket.total_spent_on_discounts

    def checkouts_current_workload(self) -> tp.List[int]:
        return self._supermarket.current_checkouts_workload

    def current_checkouts_customer_progress(self) -> tp.List[int]:
        return self._supermarket.current_checkouts_customer_progress
