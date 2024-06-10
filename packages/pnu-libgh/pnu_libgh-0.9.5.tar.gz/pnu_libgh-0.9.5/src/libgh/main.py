#!/usr/bin/env python3
""" libgh - GitHub scraping library
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import json
import logging
import os
import pprint
import sys

import libpnu

from .common import CACHE_DIR, CACHE_DAYS
from .accounts import load_account, load_accounts
from .repositories import load_repository, load_repositories
from .libpnu2 import get_url_bdata, get_url_data, prune_cache, collection2xml

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: libgh - GitHub scraping tool v0.9.5 (June 9, 2024) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "Prune cache": False,
    "Force fetching URL": False,
    "Cache days": CACHE_DAYS,
    "Complete partial": [],
    "JSON output": False,
    "XML output": False,
}


####################################################################################################
def _display_help():
    """ Display usage and help """
    #pylint: disable=C0301
    print("usage: libgh [--debug] [--help|-?] [--version]", file=sys.stderr)
    print("       [--from] [--json|-j] [--topics] [--xml|-x]", file=sys.stderr)
    print("       [--days|-d DAYS] [--force|-f] [--prune|-p]", file=sys.stderr)
    print("       [--] account_or_repo [...]", file=sys.stderr)
    print("  ------------------  --------------------------------------------------", file=sys.stderr)
    print("  --days|-d DAYS      Set number of caching days (0=don't use cache)", file=sys.stderr)
    print("  --force|-f          Force fetching URL instead of using cache", file=sys.stderr)
    print("  --from              Load repositories when forked_from is blank", file=sys.stderr)
    print("  --json|-j           Switch to JSON output instead of plain text", file=sys.stderr)
    print("  --prune|-p          Prune cache items olday than DAYS and cache index", file=sys.stderr)
    print("  --topics            Load repositories when there are missing topics", file=sys.stderr)
    print("  --xml|-x            Switch to XML output instead of plain text", file=sys.stderr)
    print("  --debug             Enable debug mode", file=sys.stderr)
    print("  --help|-?           Print usage and this help message and exit", file=sys.stderr)
    print("  --version           Print version and exit", file=sys.stderr)
    print("  --                  Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)
    #pylint: enable=C0301


####################################################################################################
def _process_command_line():
    """ Process command line options """
    #pylint: disable=C0103, W0602
    global parameters
    #pylint: enable=C0103, W0602

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "d:fjpx?"
    string_options = [
        "days=",
        "debug",
        "force",
        "from",
        "help",
        "json",
        "prune",
        "topics",
        "version",
        "xml",
    ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        _display_help()
        sys.exit(1)

    for option, argument in options:

        if option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            _display_help()
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

        elif option in ("--days", "-d"):
            try:
                parameters["Cache days"] = int(argument)
            except ValueError:
                logging.critical("--days|-d parameter is not an integer number")
                sys.exit(1)
            if parameters["Cache days"] < 0:
                logging.critical("--days|-d parameter is not a positive integer number")
                sys.exit(1)

        elif option in ("--force", "-f"):
            parameters["Force fetching URL"] = True

        elif option == "--from":
            parameters["Complete partial"].append("forked_from")

        elif option in ("--json", "-j"):
            parameters["JSON output"] = True
            parameters["XML output"] = False

        elif option in ("--prune", "-p"):
            parameters["Prune cache"] = True

        elif option == "--topics":
            parameters["Complete partial"].append("topics")

        elif option in ("--xml", "-x"):
            parameters["XML output"] = True
            parameters["JSON output"] = False

    return remaining_arguments


####################################################################################################
def main():
    """ The program's main entry point """
    program_name = os.path.basename(sys.argv[0])

    libpnu.initialize_debugging(program_name)
    libpnu.handle_interrupt_signals(libpnu.interrupt_handler_function)
    arguments = _process_command_line()

    if parameters["Prune cache"]:
        prune_cache(CACHE_DIR, parameters["Cache days"])

    if not arguments:
        _display_help()

    else:
        accounts = []
        repositories = []
        for argument in arguments:
            if '/' in argument:
                repositories.append(argument)
            else:
                accounts.append(argument)

        data = {}
        if accounts:
            data = load_accounts(
                accounts,
                parameters["Cache days"],
                force_fetch=parameters["Force fetching URL"],
                complete=parameters["Complete partial"],
            )
        if repositories:
            data2 = load_repositories(
                repositories,
                parameters["Cache days"],
                force_fetch=parameters["Force fetching URL"],
            )

            # Performing nested dictionary update
            for account, account_value in data2.items():
                if account in data:
                    for repository, repository_value in account_value["repositories"].items():
                        data[account]["repositories"][repository] = repository_value
                else:
                    data[account] = account_value

        if parameters["JSON output"]:
            json.dump(data, sys.stdout)
            print()
        elif parameters["XML output"]:
            xml = collection2xml(data, name="GitHub")
            for line in xml:
                print(line)
        else:
            pprint.pprint(data, sort_dicts=False)

    sys.exit(0)


if __name__ == "__main__":
    main()
