#!/usr/bin/env python3
""" libgh - GitHub scraping library and tool
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import logging

from bs4 import BeautifulSoup

from .common import GITHUB_URL, CACHE_DIR, REQUESTS_MIN_DELAY, REQUESTS_PER_HOUR
from .libpnu2 import get_url_data
from .personal_account import load_user_account
from .organization_account import load_org_account

####################################################################################################
def load_account(account_name, cache_days, force_fetch=False, complete=[]):
    """ Returns a dictionary of account information """
    account = {}

    try:
        data, response = get_url_data(
            f"{GITHUB_URL}/{account_name}",
            CACHE_DIR,
            cache_days=cache_days,
            cache_index=True,
            force_fetch=force_fetch,
            min_delay=REQUESTS_MIN_DELAY,
            max_per_hour=REQUESTS_PER_HOUR
        )
    except (LookupError, PermissionError) as error:
        logging.error("libgh: %s", error)
        return account
    for item in response:
        if item[0].startswith("x-ratelimit"):
            logging.debug("libgh: HTTP response: %s=%s", item[0], item[1])

    soup = BeautifulSoup(data, "html.parser")

    organization = soup.find("meta", attrs={"name":"hovercard-subject-tag"})
    if organization is None:
        account = load_user_account(
            account_name,
            soup,
            cache_days,
            force_fetch=force_fetch,
            complete=complete
        )
    else:
        account = load_org_account(
            account_name,
            soup,
            cache_days,
            force_fetch=force_fetch,
            complete=complete
        )

    return account

####################################################################################################
def load_accounts(accounts_list, cache_days, force_fetch=False, complete=[]):
    """ Returns a dictionary of accounts information """
    accounts = {}

    for account_name in accounts_list:
        accounts[account_name] = load_account(
            account_name,
            cache_days,
            force_fetch=force_fetch,
            complete=complete
        )

    return accounts
