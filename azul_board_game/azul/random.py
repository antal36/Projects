from random import choice
from typing import List
from azul.interfaces import RandomInterface

class Random(RandomInterface):
    def permutation(self, length: int) -> List[int]:
        result: List[int] = []
        while len(result) != 4:
            element: int = choice(range(length))
            if element not in result:
                result.append(element)
        return result
