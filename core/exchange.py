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

###############################################################################

class Exchange:

    # CONSTRUCTOR
    def __init__(self, config: Configuration):
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
