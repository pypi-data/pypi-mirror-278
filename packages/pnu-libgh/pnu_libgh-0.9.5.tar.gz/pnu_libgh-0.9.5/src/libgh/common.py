#!/usr/bin/env python3
""" libgh - GitHub scraping library and tool
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

# GitHub address
GITHUB_URL = "https://github.com"

# Caching
CACHE_DIR = "libgh"
CACHE_DAYS = 7

# Rate limits for GitHub
# See https://docs.github.com
#    /fr/apps/creating-github-apps/registering-a-github-app/rate-limits-for-github-apps
REQUESTS_MIN_DELAY = 1 # second(s) between Web requests
REQUESTS_PER_HOUR = 60 # requests per hour
