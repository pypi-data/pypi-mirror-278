#!/usr/bin/env python3
""" libgh - GitHub scraping library and tool
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import logging

from bs4 import BeautifulSoup

from .common import GITHUB_URL, CACHE_DIR, REQUESTS_MIN_DELAY, REQUESTS_PER_HOUR
from .libpnu2 import get_url_data

####################################################################################################
def load_repository(account_name, repository_name, cache_days, force_fetch=False):
    """ Returns a dictionary of repository information """
    repository = {}

    try:
        data, response = get_url_data(
            f"{GITHUB_URL}/{account_name}/{repository_name}",
            CACHE_DIR,
            cache_days=cache_days,
            cache_index=True,
            force_fetch=force_fetch,
            min_delay=REQUESTS_MIN_DELAY,
            max_per_hour=REQUESTS_PER_HOUR
        )
    except (LookupError, PermissionError) as error:
        logging.error("libgh: %s", error)
        return repository
    for item in response:
        if item[0].startswith("x-ratelimit"):
            logging.debug("libgh: HTTP response: %s=%s", item[0], item[1])

    soup = BeautifulSoup(data, "html.parser")

    #html = soup.select_one('[itemprop="author"]')
    #html = soup.select_one('[itemprop="name"]')

    # Forked from (if relevant)
    html = soup.select_one('[data-hovercard-type="repository"]')
    if html is not None:
        repository["forked_from"] = html.get("href")[1:]

    # Forks
    html = soup.select_one('[id="repo-network-counter"]')
    if html is not None:
        fork = html.get("title").replace(",", "")
        try:
            forks_count = int(fork)
            repository["forks_count"] = forks_count
        except ValueError:
            pass

    # Stars
    html = soup.select_one('[id="repo-stars-counter-star"]')
    if html is not None:
        star = html.get("title").replace(",", "")
        try:
            stargazers_count = int(star)
            repository["stargazers_count"] = stargazers_count
        except ValueError:
            pass

    # Issues
    html = soup.select_one('[id="issues-repo-tab-count"]')
    if html is not None:
        issues = html.get("title").replace(",", "")
        try:
            issues_count = int(issues)
            repository["issues_count"] = issues_count
        except ValueError:
            pass

    # Pull requests
    html = soup.select_one('[id="pull-requests-repo-tab-count"]')
    if html is not None:
        pull_requests = html.get("title").replace(",", "")
        try:
            pull_requests_count = int(pull_requests)
            repository["pull_requests_count"] = pull_requests_count
        except ValueError:
            pass

    # Description
    html = soup.select_one('[class="f4 my-3"]')
    if html is not None:
        repository["description"] = html.text.strip()

    # Web site
    html = soup.select_one('[role="link"]')
    if html is not None:
        repository["website"] = html.get("href")

    # License or "specific"
    html = soup.select('[class="sr-only"]')
    for item in html:
        if item.text.strip() == "License":
            html2 = item.next_sibling.next_sibling
            html3 = html2.select_one('a')
            repository["license"] = html3.text.strip()
            if repository["license"] == "View license":
                repository["license"] = "specific"
            break

    # Topics
    html = soup.select('[class="topic-tag topic-tag-link"]')
    if html is not None:
        topics = []
        for item in html:
            topics.append(item.get("title").split()[1])
        repository["topics"] = topics
        repository["topics_count"] = len(topics)

    # Watching
    html = soup.select('[class="Link Link--muted"]')
    for item in html:
        if item.get("href").endswith("/watchers"):
            html2 = item.select_one('strong')
            if html2 is not None:
                try:
                    repository["watching_count"] = int(html2.text.strip())
                except ValueError:
                    pass
            break

    # Releases and Packages
    html = soup.select('[class="BorderGrid-cell"]')
    for item in html:
        html2 = item.select_one('[class*="Link--primary"]')
        if html2 is not None:
            href = html2.get("href")
            html3 = html2.select_one('[class*="Counter"]')
            if href.endswith("/releases"):
                if html3 is not None:
                    try:
                        repository["releases_count"] = int(html3.text.strip().replace(",", ""))
                    except ValueError:
                        pass

                    # Last release name & date
                    html4 = item.select_one('[class*="css-truncate"]')
                    if html4 is not None:
                        repository["last_release_name"] = html4.text.strip()
                    html4 = item.select_one('relative-time')
                    if html4 is not None:
                        repository["last_release_date"] = html4.get("datetime")

                else:
                    repository["releases_count"] = 0
            elif "/packages" in href:
                if html3 is not None:
                    try:
                        repository["packages_count"] = int(html3.text.strip().replace(",", ""))
                    except ValueError:
                        pass

    # Is sponsorable?
    html = soup.select('h2[class="h4 mb-3"]')
    repository["is_sponsorable"] = False
    for item in html:
        text = item.text.strip()
        if text == "Sponsor this project":
            repository["is_sponsorable"] = True

    # Contributors
    html = soup.select_one('[class="Counter ml-1"]')
    if html is not None:
        contributors = html.get("title").replace(",", "")
        try:
            contributors_count = int(contributors)
            repository["contributors_count"] = contributors_count
        except ValueError:
            pass

    # Languages
    html = soup.select('[itemprop="keywords"]')
    if html is not None:
        languages = {}
        repository["programming_language"] = ""
        for item in html:
            value = item.get("aria-label").split()
            language = " ".join(value[:-1])
            percentage = value[-1]
            try:
                languages[language] = float(percentage)
            except ValueError:
                languages[language] = percentage
            if not repository["programming_language"]:
                repository["programming_language"] = language
        repository["languages"] = languages

    # Commits
    html = soup.select('span[class*="Text-sc-"]')
    for item in html:
        content = item.text.strip().replace(",", "")
        if content.endswith(" Commits"):
            try:
                repository["commits_count"] = int(content[:-8])
            except ValueError:
                pass
        elif content == "1 Commit":
            repository["commits_count"] = 1

    return repository

####################################################################################################
def load_repositories(repositories_list, cache_days, force_fetch=False):
    """ Returns a dictionary of repositories information """
    accounts = {}

    for item in repositories_list:
        if item.count('/') == 1:
            account = item.split('/')[0]
            repository = item.split('/')[1]

            if account not in accounts:
                accounts[account] = {"repositories":{}}

            accounts[account]["repositories"][repository] = load_repository(
                account,
                repository,
                cache_days,
                force_fetch=force_fetch
            )
        else:
            logging.error(
                "libgh: Repositories parameters must be in 'account/repo' form. '%s' discarded",
                item
            )

    return accounts
