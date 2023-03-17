from dataclasses import dataclass


@dataclass
class Customer:
    time_entered: int
    service_time: int
    profit: int
