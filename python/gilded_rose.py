# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class ItemUpdateStrategy(ABC):
    @abstractmethod
    def update(self,item):
        """update sell_in and quality  % rules """
        pass

class NormalItemStrategy(ItemUpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        if item.sell_in >= 0:
            item.quality = max(0, item.quality - 1)
        else:
            item.quality = max(0, item.quality - 2)


class AgedBrieStrategy(ItemUpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        if item.quality < 50:
            item.quality += 1


class SulfurasStrategy(ItemUpdateStrategy):
    def update(self, item):
        pass


class BackstagePassStrategy(ItemUpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        
        if item.sell_in < 0:
            item.quality = 0
        elif item.quality < 50:
            item.quality += 1
            
            if item.sell_in < 10 and item.quality < 50:
                item.quality += 1
            if item.sell_in < 5 and item.quality < 50:
                item.quality += 1


class ConjuredStrategy(ItemUpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        if item.sell_in >= 0:
            item.quality = max(0, item.quality - 2)
        else:
            item.quality = max(0, item.quality - 4)


class ItemStrategyFactory:
    @staticmethod
    def create_strategy(item_name):
        """return the custom strategy"""
        if item_name == "Aged Brie":
            return AgedBrieStrategy()
        elif item_name == "Sulfuras, Hand of Ragnaros":
            return SulfurasStrategy()
        elif item_name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassStrategy()
        elif "Conjured" in item_name:
            return ConjuredStrategy()
        else:
            return NormalItemStrategy()


    
class GildedRose(object):

    def __init__(self, items):
        self.items = items
        self.factory = ItemStrategyFactory()

    def update_quality(self):
        for item in self.items:
            strategy = self.factory.create_strategy(item.name)
            strategy.update(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
