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
import sys

# 3RD PARTY IMPORTS
from binance.client import Client

# CORE IMPORTS
from core.configuration import Configuration
from core.pair import Pair

###############################################################################

class Exchange:

    # CONSTRUCTOR
    def __init__(self, config: Configuration):
        # store the trading configuration
        self.against = config.against

        # try to connect to Binance
        print("[+] Connecting to Binance.")
        self.client = Client(config.apiKey, config.apiSecret)

        # test the connection
        if self.client.ping() == {}:
            print("[+] Connection established.")
        else:
            print("[-] Cannot connect to Binance. Check your internet connection"
                  " and your api parameters.")
            sys.exit(0)

    # METHODS
    def printAvailablePairs(self) -> None:
        for pair in self.availablePairs:
            print("[+] Added " + pair.name + ".")

    def getAvailablePairs(self) -> None:
        # get a list of all the pairs on binance
        tickers = self.client.get_all_tickers()

        # create the pairs from the ticker
        allBinancePairs = []
        for ticker in tickers:
            allBinancePairs.append(Pair(ticker["symbol"]))

        # filter function
        def filterPairByAgainst(pair: Pair) -> bool:
            againstLen = len(self.against)
            return pair.name[-againstLen:] == self.against

        # filter the pairs the are not against what the user choose
        filteredPairsIterator = filter(filterPairByAgainst, allBinancePairs)

        # store the filtered list of pairs
        self.availablePairs = list(filteredPairsIterator)
        self.printAvailablePairs()

        # update the members of all the available pairs
        for pair in self.availablePairs:
            open = []
            high = []
            low = []
            close = []
            volume = []
            for kline in self.client.get_historical_klines_generator(pair.name,
                                                                    Client.KLINE_INTERVAL_1MINUTE,
                                                                    "4 hours ago UTC"):
                open.append(float(kline[1]))
                high.append(float(kline[2]))
                low.append(float(kline[3]))
                close.append(float(kline[4]))
                volume.append(float(kline[5]))

            pair.updateCandlesticks(open, high, low, close, volume)
            print("[+] " + pair.name + " updated.")
