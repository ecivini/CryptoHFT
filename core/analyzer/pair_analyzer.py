"""
CryptoHFT is a software that lets you trade cryptocurrencies on Binance
using an high-frequency-trading like algorithm.

Copyright (C) 2020 Emanuele Civini - ciwines - emanuelecivini11@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

###############################################################################

# CORE IMPORTS
from core.pair import Pair

###############################################################################

class PairAnalyzer:
    # CONSTRUCTOR
    def __init__(self, pairList: list[Pair], priceThreshold: float):
        self.pairList = pairList
        self.priceThreshold = priceThreshold

    # METHODS
    def getMostSuitable(self) -> Pair:
        # internal comparison function
        def getPairVolume(pair: Pair) -> float:
            return pair.calculateMeanVolume()

        # sort the pair list based on the volume
        self.pairList.sort(key=getPairVolume)

        # return the first element that has a price greater or equal to
        # the price threshold
        for pair in self.pairList:
            if pair.getLastPrice() >= self.priceThreshold:
                return pair
        return None