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

# IMPORTS
import json
import sys

###############################################################################

class Configuration:
    # CONSTRUCTOR
    def __init__(self, configFilePath: str):
        print("[+] Loading user configuration.")

        # reads the configuration from the standard file
        try:
            with open(configFilePath, "r") as configFile:
                data = json.load(configFile)

                # stores the configuration
                self.apiKey = data["apiKey"]
                self.apiSecret = data["apiSecret"]
                self.username = data["username"]
                self.against = data["against"]

        # if the configuration file doesn't exist, then stop the execution
        except FileNotFoundError:
            print("[-] Configuration file not found. Restart the program with -i.")
            sys.exit(0)

    # STATIC METHODS
    @staticmethod
    def createConfiguration(configFilePath: str) -> None:
        inputIsValid = False

        print("Creating a new configuration.")
        # get the parameters from the user
        while not inputIsValid:
            print("Please enter the following parameters:")
            apiKey = input("\tAPI Key: ")
            apiSecret = input("\tAPI Secret: ")
            username = input("\tUsername: ")
            against = input("\tAgainst: [BTC/USDT] ")

            # let the user check if the parameters are correct
            print("You have entered: ")
            print("\tAPI Key: " + apiKey)
            print("\tAPI Secret: " + apiSecret)
            print("\tUsername: " + username)
            print("\tAgainst: " + against)

            cmd = input("Are these parameters correct? [y/n] ")
            if cmd == "y" or cmd == "Y":
                inputIsValid = True

        # store the new parameters in the configuration file
        with open(configFilePath, "w+") as configFile:
            # user configuration
            data = {
                "apiKey": apiKey,
                "apiSecret": apiSecret,
                "username": username,
                "against": against
            }

            # write the configuration file
            json.dump(data, configFile, indent=4)

        print("[+] Configuration completed. Please restart the program.")
        sys.exit(0)