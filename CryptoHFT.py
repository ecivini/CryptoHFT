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
import argparse
import sys

# CORE IMPORTS
from core.configuration import Configuration
from core.exchange import Exchange

###############################################################################

# CONSTANTS AND PATHS
CONFIG_FILE_PATH = "config.json"

###############################################################################

# MAIN
def main() -> None:
    # create the argument parser
    ap = argparse.ArgumentParser(prog="CryptoHFT.py")
    ap.add_argument("-w", "--warranty",
                    help="shows the details about the warranty.",
                    action="store_true")
    ap.add_argument("-c", "--conditions",
                    help="shows the details about the redistribution.",
                    action="store_true")
    ap.add_argument("-i", "--init",
                    help="create a new configuration.",
                    action="store_true")

    # retrieve the arguments
    args = ap.parse_args()

    # check if the -w flag or the -c flag has been written
    shownWarrantyOrConditions = False
    if args.conditions:
        printConditions()
        shownWarrantyOrConditions = True

    if args.warranty:
        printWarranty()
        shownWarrantyOrConditions = True

    if shownWarrantyOrConditions:
        sys.exit(0)

    # shows the license
    printLicense()

    # check if it's necessary to create a new configuration file
    if args.init:
        Configuration.createConfiguration(CONFIG_FILE_PATH)

    # load the configuration
    userConfig = Configuration(CONFIG_FILE_PATH)
    exchange = Exchange(userConfig)
    exchange.getAvailablePairs()

###############################################################################

# FUNCTIONS
def printLicense() -> None:
    print("CryptoHFT Copyright (C) 2020 Emanuele Civini - ciwines\n"
            "This program comes with ABSOLUTELY NO WARRANTY; "
            "for details type '--warranty' or '-w'.\n"
            "This is free software, and you are welcome to redistribute it\n"
            "under certain conditions; type '--conditions' or '-c' for details.\n")

def printConditions() -> None:
    print("Details about the conditions:\n"
            "IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY "
            "COPYRIGHT HOLDER,\nOR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS "
            "PERMITTED ABOVE\nBE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, "
            "INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING\nOUT OF THE USE OR INABILITY TO USE THE "
            "PROGRAM (INCLUDING BUT NOT LIMITED TO\nLOSS OF DATA OR DATA BEING RENDERED INACCURATE "
            "OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES\nOR A FAILURE OF THE PROGRAM TO OPERATE "
            "WITH ANY OTHER PROGRAMS),\nEVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF "
            "THE POSSIBILITY OF SUCH DAMAGES.\n")

def printWarranty() -> None:
    print("Details about the warranty:\n"
            "THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.\n"
            "EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES "
            "PROVIDE THE PROGRAM “AS IS”\nWITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, "
            "INCLUDING, BUT NOT LIMITED TO,\nTHE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS "
            "FOR A PARTICULAR PURPOSE.\nTHE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE "
            "PROGRAM IS WITH YOU.\nSHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL "
            "NECESSARY SERVICING, REPAIR OR CORRECTION.")

###############################################################################

if __name__ == "__main__":
    main()
