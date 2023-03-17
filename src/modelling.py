import typing as tp

from src.customer import Customer
from src.supermarket import Supermarket
from src.utils import Weekday


class SupermarketModel:
    ADS_FLOW_INCREASE = 10
    ADS_COST_TO_FLOW_INCREASE = 7000

    DISCOUNT_FLOW_INCREASE = 0.5
    DISCOUNT_COST_TO_FLOW_INCREASE = 1

    def __init__(
        self,
        total_checkouts: int,
        max_checkout_capacity: int,
        time_between_customers_range: tp.Tuple[int, int],
        customer_service_time_range: tp.Tuple[int, int],
        customer_purchase_price_range: tp.Tuple[int, int],
        ads_price_per_day: int,
        discount_percent: float,
        seller_salary_per_day: int,
        tick_time: int,
    ):
        self._supermarket = Supermarket(
            checkouts_num=total_checkouts,
            max_checkout_capacity=max_checkout_capacity
        )
        self._time_between_customers_range = time_between_customers_range
        self._customer_service_time_range = customer_service_time_range
        self._customer_purchase_price_range = customer_purchase_price_range
        self._ads_price_per_day = ads_price_per_day
        self._seller_salary_per_day = seller_salary_per_day
        self._discount_percent = discount_percent
        self._tick_time = tick_time

        self.current_weekday = Weekday.MONDAY
        self._total_generated_customers = 0
        self._summary_checkouts_workload = [0 for _ in range(total_checkouts)]

    def _get_workload_stats(self) -> tp.Dict:
        """Statistics using in customer generation"""
        stats = {
            'checkout_workload': self._supermarket.get_checkouts_workload(),
            'weekday': self.current_weekday,
            'ads_customers_flow':
                (self._ads_price_per_day // self.ADS_COST_TO_FLOW_INCREASE) * self.ADS_FLOW_INCREASE,
            'discount_customers_flow':
                (self._discount_percent // self.DISCOUNT_COST_TO_FLOW_INCREASE) * self.DISCOUNT_FLOW_INCREASE
        }
        return stats

    def _generate_customers(self, current_workload_stats: tp.Dict) -> tp.List[Customer]:
        """
        Generate customer with given random parameters, don't forget to apply discount.
        Customer.profit -> pure profit from discounted purchase
        """
        self._total_generated_customers += 1
        raise NotImplementedError

    def tick(self):
        """
        Grab statistics about checkouts current workload,
        generate new customers based on this, weekday, ads and discounts.
        Then makes supermarket tick.
        """
        current_workload_stats = self._get_workload_stats()
        generated_customers = self._generate_customers(current_workload_stats)
        for customer in generated_customers:
            self._supermarket.recieve_customer(customer)
        self._supermarket.tick(self._tick_time)

    @property
    def total_served_customers(self) -> int:
        return self._supermarket.served_customers

    def total_potential_customers(self) -> int:
        return self._total_generated_customers

    def total_earnings(self) -> int:
        return self._supermarket.total_earnings

    def checkouts_current_workload(self) -> tp.List[int]:
        return self._supermarket.get_checkouts_workload()
