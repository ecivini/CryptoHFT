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
from time import sleep
from datetime import datetime

# CORE IMPORTS
from core.configuration import Configuration
from core.pair import Pair
from core.exchange import Exchange
from core.analyzer.trend_analyzer import TrendDirection

###############################################################################

class Bot:

    balanceIncrease = 0.0
    tradingFee = 0.1
    positiveTrades = 0
    negativeTrades = 0

    # CONSTRUCTOR
    def __init__(self, config: Configuration):
        # store the trading configuration
        self.config = config
        self.exchange = Exchange(self.config)
        self.prevPair = Pair(""
                             "")

    # METHODS
    def setup(self) -> None:
        print("[+] Setting up the bot.")

    # target and stopLoss must be passed as percentages
    def goShort(self, pair: Pair, target: float, stopLoss: float) -> None:
        buyPrice = self.exchange.getLastPrice(pair)
        print("[+] Shorting " + pair.name + " at " + str(buyPrice))

        # shorting loop
        while True:
            # wait 5 seconds
            sleep(5)

            # check if we have reached the target or the stop loss
            currentPrice = self.exchange.getLastPrice(pair)
            if currentPrice <= buyPrice * (1 - target / 100.0):
                self.balanceIncrease += target - self.tradingFee
                self.positiveTrades += 1
                print("[+] Trade gone well!")
                break
            elif currentPrice >= buyPrice * (1 + stopLoss / 100.0):
                self.balanceIncrease -= stopLoss + self.tradingFee
                self.negativeTrades += 1
                print("[+] Trade gone bad!")
                pair.disable()
                break
            # else:
                #print("[+]\tCurrent price is: " + str(currentPrice) + " | target: " + str(buyPrice * (1 - target)) + " | stoploss: " + str(buyPrice * (1 + stopLoss)))
        print("CURRENT BALANCE: " + str(self.balanceIncrease) + "% | Positive Trades = " + str(self.positiveTrades) + " | Negative Trades = " + str(self.negativeTrades))

    # target and stopLoss must be passed as percentages
    def goLong(self, pair: Pair, target: float, stopLoss: float) -> None:
        buyPrice = self.exchange.getLastPrice(pair)

        print("[+] Buying " + pair.name + " at " + str(buyPrice))

        inTrade = True
        while inTrade:
            # wait 5 seconds
            sleep(5)

            # check if we have reached the target or the stop loss
            currentPrice = self.exchange.getLastPrice(pair)
            if currentPrice >= buyPrice * (1 + target / 100.0):
                self.balanceIncrease += target - self.tradingFee
                self.positiveTrades += 1
                print("[+] Trade gone well!")
                inTrade = False
            elif currentPrice <= buyPrice * (1 - stopLoss / 100.0):
                self.balanceIncrease -= stopLoss + self.tradingFee
                self.negativeTrades += 1
                print("[+] Trade gone bad!")
                inTrade = False
                pair.disable()
            # else:
                # print("[+]\tCurrent price is: " + str(currentPrice) + " | target: " + str(buyPrice * (1 + target)) + " | stoploss: " + str(buyPrice * (1 - stopLoss)))
        print("CURRENT BALANCE: " + str(self.balanceIncrease) + "% | Positive Trades = " + str(self.positiveTrades) + " | Negative Trades = " + str(self.negativeTrades))

    def tradeLoop(self) -> None:
        print("[+] Entering trading loop.")

        while True:
            # update each pair and calculate the trend direction for each one
            self.exchange.updateAvailablePairs()

            # check the pairs that have a clear direction
            for pair in self.exchange.availablePairs:
                if pair.currentDirection == TrendDirection.DOWN and pair.usable:
                    if self.prevPair.name != pair.name:
                        self.goShort(pair, 0.6, 0.25)
                        self.prevPair = pair
                    break
                elif pair.currentDirection == TrendDirection.UP and pair.usable:
                    if self.prevPair.name != pair.name:
                        self.goLong(pair, 0.6, 0.25)
                        self.prevPair = pair
                    break

            sleep(30)
