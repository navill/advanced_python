from typing import List


class Pizza:
    def __init__(self, toppings: List) -> None:
        self.toppings = toppings

    def __repr__(self):
        return "Pizza with " + " and ".join(self.toppings)

    @classmethod
    def recommend(cls):
        """Recommend some pizza with arbitrary toppings,"""
        return cls(['spam', 'ham', 'eggs'])


class VikingPizza(Pizza):
    @classmethod
    def recommend(cls):
        """Use same recommendation as super but add extra spam"""
        recommended = super(cls, VikingPizza).recommend()
        for _ in range(5):
            recommended.toppings.append('spam')
        return recommended


p = Pizza(['hot source'])
print(p)
print(p.recommend())
vp = VikingPizza(['cheese'])
print(vp)
print(vp.recommend())
