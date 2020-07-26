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

# 3RD PARTY IMPORTS
import numpy as np

###############################################################################

class Pair:
    # CONSTRUCTOR
    def __init__(self, name: str):
        self.name = name

    # METHODS
    def updateCandlesticks(self, open: list, high: list,
                           low: list, close: list,
                           volume: list) -> None:
        self.open = np.array(open)
        self.high = np.array(high)
        self.low = np.array(low)
        self.close = np.array(close)
        self.volume = np.array(volume)

    def getLastPrice(self) -> None:
        return self.close[0]

    def calculateMeanVolume(self) -> float:
        volumeSum = 0.0
        for v in self.volume:
            volumeSum += v
        return volumeSum / len(self.volume)