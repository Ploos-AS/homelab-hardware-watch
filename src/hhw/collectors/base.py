from abc import ABC, abstractmethod
from hhw.models import Candidate


class Collector(ABC):
    vendor_id: str

    @abstractmethod
    def collect(self) -> list[Candidate]:
        raise NotImplementedError
