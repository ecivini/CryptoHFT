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

# STANDARD IMPORTS
from enum import Enum

# CORE IMPORTS
from core.pair_data import PairData

###############################################################################

class TrendDirection(Enum):
    UP = 1
    DOWN = -1
    USELESS = 0

###############################################################################

class TrendAnalyzer:
    # CONSTRUCTOR
    def __init__(self, data: PairData):
        self.data = data

    # METHODS
    def updatePairData(self, data: PairData) -> None:
        self.data = data

    def getTrend(self) -> TrendDirection:
        # calculate three angular coefficients
        # one from 0 - 60 candlesticks (1 hour)
        # one from 0 - 120 candlesticks (2 hours)
        # one from 0 - 240 candlesticks (4 hours)
        def changeRate(currentPrice: float, prevPrice: float,
                       currentTime: int, prevTime: int) -> float:
            return (currentPrice - prevPrice) / (currentTime - prevTime)

        # sanity check
        if len(self.data.close) < 240:
            return TrendDirection.USELESS

        oneHourRate = changeRate(self.data.close[0], self.data.close[10 - 1],
                                 self.data.closeTime[0], self.data.closeTime[10 - 1])
        twoHoursRate = changeRate(self.data.close[0], self.data.close[30 - 1],
                                  self.data.closeTime[0], self.data.closeTime[30 - 1])
        fourHoursRate = changeRate(self.data.close[0], self.data.close[120 - 1],
                                   self.data.closeTime[0], self.data.closeTime[12 - 1])

        # print("10m rate -> " + str(oneHourRate))
        # print("30m rate -> " + str(twoHoursRate))
        # print("1h rate -> " + str(fourHoursRate))

        # take a direction if the one hour and the two hours trend goes opposite
        # to the 4 hours trend
        angularCoefficientThreshold = 0.0
        if oneHourRate >= angularCoefficientThreshold and twoHoursRate >= angularCoefficientThreshold:
            if fourHoursRate <= -angularCoefficientThreshold:
                return TrendDirection.UP
            else:
                return TrendDirection.USELESS
        elif oneHourRate <= -angularCoefficientThreshold and twoHoursRate <= -angularCoefficientThreshold:
            if fourHoursRate >= angularCoefficientThreshold:
                return TrendDirection.DOWN
            else:
                return TrendDirection.USELESS

        return TrendDirection.USELESS
