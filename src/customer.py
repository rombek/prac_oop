from dataclasses import dataclass


@dataclass
class Customer:
    service_time: int
    remaining_service_time: int
    purchase_cost: int
