#!/usr/bin/env python3
""" libgh - GitHub scraping library and tool
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import json
import logging

from bs4 import BeautifulSoup

from .common import GITHUB_URL, CACHE_DIR, REQUESTS_MIN_DELAY, REQUESTS_PER_HOUR
from .libpnu2 import get_url_data
from .repositories import load_repository

####################################################################################################
def load_org_repositories(
    account_name,
    cache_days,
    force_fetch=False,
    complete=[],
    repos_type="all"
):
    """ Returns a dictionary of user's repositories """
    repos = {}
    page = 1

    while True:
        try:
            data, response = get_url_data(
                f"{GITHUB_URL}/orgs/{account_name}/repositories?type={repos_type}&page={page}",
                CACHE_DIR,
                cache_days=cache_days,
                cache_index=True,
                force_fetch=force_fetch,
                min_delay=REQUESTS_MIN_DELAY,
                max_per_hour=REQUESTS_PER_HOUR
            )
        except (LookupError, PermissionError) as error:
            logging.error("libgh: %s", error)
            return repos
        for item in response:
            if item[0].startswith("x-ratelimit"):
                logging.debug("libgh: HTTP response: %s=%s", item[0], item[1])

        soup = BeautifulSoup(data, "html.parser")

        # repositories list
        json_data = soup.find(
            "script",
            attrs={"type":"application/json", "data-target":"react-app.embeddedData"}
        )
        if json_data is not None:
            j = json.loads(json_data.text)
        else:
            # We received JSON data instead of HTML!
            j = json.loads(data)

        for repository in j["payload"]["repositories"]:
            name = repository["name"]
            repos[name] = {}
            uncomplete = False

            # forked from
            if repository["isFork"]:
                repos[name]["forked_from"] = "" # The original location is not provided
                if "forked_from" in complete:
                    uncomplete = True

            # topics
            if "allTopics" in repository:
                repos[name]["topics"] = repository["allTopics"]
                repos[name]["topics_count"] = len(repository["allTopics"])
            elif "topicNames" in repository:
                repos[name]["topics"] = repository["topicNames"]
                repos[name]["topics_count"] = len(repository["topicNames"])
                if "topicsNotShown" in repository:
                    repos[name]["topics_count"] += repository["topicsNotShown"]
            else:
                repos[name]["topics"] = []
                if "topicsNotShown" in repository:
                    repos[name]["topics_count"] = repository["topicsNotShown"]
            if "topicsNotShown" in repository and repository["topicsNotShown"] and "topics" in complete:
                uncomplete = True

            if uncomplete:
                repos[name] = load_repository(account_name, name, cache_days, force_fetch)

            else:
                # description
                if repository["description"]:
                    repos[name]["description"] = repository["description"]

                # programming language
                if repository["primaryLanguage"] is not None:
                    repos[name]["programming_language"] = repository["primaryLanguage"]["name"]

                # stargazers
                repos[name]["stargazers"] = {}
                repos[name]["stargazers_count"] = repository["starsCount"]

                # forks
                repos[name]["forks"] = {}
                repos[name]["forks_count"] = repository["forksCount"]

                # issues
                repos[name]["issues_count"] = repository["issueCount"]

                # pull requests
                repos[name]["pull_requests_count"] = repository["pullRequestCount"]

                # license
                if repository["license"] is not None:
                    repos[name]["license"] = repository["license"]

            # last updated
            repos[name]["last_updated"] = repository["lastUpdated"]["timestamp"]

            # archived?
            if repos_type == "archived":
                repos[name]["archived"] = True

        # is there a next page?
        next_page = soup.select_one('[aria-label="Next Page"]')
        if next_page is not None:
            try:
                next_page.get("href")
            except AttributeError:
                break
        elif page == j["payload"]["pageCount"]:
            break

        page += 1

    return repos

####################################################################################################
def load_org_account(account_name, soup, cache_days, force_fetch=False, complete=[]):
    """ Returns a dictionary of organization account information """
    account = {}

    # the number of Repositories, Teams and (public) People is not available from the tabs pane

    # account type
    account["account_type"] = "organization"

    # avatar
    html = soup.select_one('[itemprop="image"]')
    if html is not None:
        account["avatar"] = html.get("src")

    # organization name
    html2 = html.parent.next_sibling.next_sibling.contents[1]
    if html2 is not None:
        text = html2.text.strip()
        if text:
            account["name"] = text

    # "biography": organization sub title
    html2 = html.parent.next_sibling.next_sibling.contents[3]
    if html2 is not None:
        text = html2.text.strip()
        if text:
            account["biography"] = text

    # followers
    account["followers"] = {}
    html = soup.select('[class*="Link--secondary"]')
    for item in html:
        href = item.get("href")
        if href is None:
            continue
        if "followers" in href:
            number = [x.strip() for x in item.text.split("\n") if x][0]
            try:
                account["followers_count"] = int(number)
            except ValueError:
                if number.endswith('k'):
                    account["followers_count"] = int(float(number[:-1]) * 1000)
                elif number.endswith('m'):
                    account["followers_count"] = int(float(number[:-1]) * 1000000)
                else:
                    account["followers_count"] = 0

    # location
    html = soup.select_one('[itemprop="location"]')
    if html is not None:
        account["location"] = html.text.strip()

    # profile website URL
    html = soup.select_one('[itemprop="url"]')
    if html is not None:
        account["website"] = html.text.strip()

    # social media
    account["social"] = {}
    html = soup.select('[class*="Link--primary"]')
    for item in html:
        ident = item.text.strip()
        href = item.get("href")
        if "facebook.com/" in href:
            account["social"]["facebook"] = {"id": ident, "url": href}
        elif href.startswith("https://www.instagram.com/"):
            account["social"]["instagram"] = {"id": ident, "url": href}
        elif href.startswith("https://www.linkedin.com/"):
            account["social"]["linkedin"] = {"id": ident, "url": href}
        elif href.startswith("https://mastodon.social/"):
            account["social"]["mastodon"] = {"id": ident, "url": href}
        elif href.startswith("https://mozilla.social/"):
            account["social"]["mozilla"] = {"id": ident, "url": href}
        elif href.startswith("https://twitter.com/"):
            account["social"]["x"] = {"id": ident, "url": href}
        elif href.startswith("https://www.youtube.com/"):
            account["social"]["youtube"] = {"id": ident, "url": href}
        elif not href.startswith("http"):
            pass
        else:
            if "url" in account["social"]:
                account["social"]["url"].append(href)
            else:
                account["social"]["url"] = [href]

    # repositories
    account["repositories"] = {}
    html = soup.select_one('[data-autosearch-results]')
    if html is not None:
        number = html.text.split()[3]
        try:
            account["repositories_count"] = int(number)
        except ValueError:
            pass
        account["repositories"] = load_org_repositories(
            account_name,
            cache_days,
            force_fetch=force_fetch,
            complete=complete
        )
        if len(account["repositories"]) != account["repositories_count"]:
            account["repositories"].update(
                load_org_repositories(
                    account_name,
                    cache_days,
                    force_fetch=force_fetch,
                    complete=complete,
                    repos_type="archived"
                )
            )
    else:
        account["repositories_count"] = 0

    # repositories stars (computed)
    stars = 0
    for repo in account["repositories"]:
        stars += account["repositories"][repo]["stargazers_count"]
    account["repositories_stars"] = stars

    # the details of "People", "Top languages" and "Most used topics" are not available
    # from the right pane

    # top languages (computed)
    top_languages = {}
    for repo in account["repositories"]:
        if "programming_language" in account["repositories"][repo]:
            language = account["repositories"][repo]["programming_language"]
            if language in top_languages:
                top_languages[language] += 1
            else:
                top_languages[language] = 1
    account["top_languages"] = dict(sorted(
        top_languages.items(),
        key=lambda item: item[1],
        reverse=True
    ))

    # most used topics (computed)
    most_used_topics = {}
    for repo in account["repositories"]:
        if "topics" in account["repositories"][repo]:
            topics = account["repositories"][repo]["topics"]
            for topic in topics:
                if topic in most_used_topics:
                    most_used_topics[topic] += 1
                else:
                    most_used_topics[topic] = 1
    account["most_used_topics"] = dict(sorted(
        most_used_topics.items(),
        key=lambda item: item[1],
        reverse=True
    ))

    if len(account["repositories"]) != account["repositories_count"]:
        logging.warning(
            "libgh: Loaded %d/%d repositories for account '%s'",
            len(account["repositories"]),
            account["repositories_count"],
            account_name
        )

    return account
