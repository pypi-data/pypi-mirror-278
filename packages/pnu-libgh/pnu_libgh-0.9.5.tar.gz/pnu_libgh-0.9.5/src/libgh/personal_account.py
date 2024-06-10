#!/usr/bin/env python3
""" libgh - GitHub scraping libraryaand tool
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import logging
import re

from bs4 import BeautifulSoup

from .common import GITHUB_URL, CACHE_DIR, REQUESTS_MIN_DELAY, REQUESTS_PER_HOUR
from .libpnu2 import get_url_data
from .repositories import load_repository

####################################################################################################
def load_user_repositories(user_name, url, page, cache_days, force_fetch=False, complete=[]):
    """ Returns a dictionary of user's repositories """
    repos = {}

    try:
        data, response = get_url_data(
            url,
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
    repos_list = soup.select_one('[id="user-repositories-list"]')
    items = repos_list.select("li")
    for item in items:
        # name
        html = item.select_one('[itemprop="name codeRepository"]')
        name = html.text.strip()
        repos[name] = {}

        # topics
        repos[name]["topics"] = []
        html = item.select('[data-octo-click="topic_click"]')
        if html is not None:
            for html2 in html:
                repos[name]["topics"].append(html2.text.strip())

        # when there are 7 topics, it's probable than GitHub is only showing the first ones
        # (can also happen with less when the topics character length is large)
        if "topics" in repos[name] and len(repos[name]["topics"]) == 7 and "topics" in complete:
            repos[name] = load_repository(user_name, name, cache_days, force_fetch)

        else:
            # archived?
            li_class = item.get("class")
            if "archived" in li_class:
                repos[name]["archived"] = True

            # forked from
            html = item.select_one('[class="Link--muted Link--inTextBlock"]')
            if html is not None:
                repos[name]["forked_from"] = html.text.strip()

            # description
            html = item.select_one('[itemprop="description"]')
            if html is not None:
                repos[name]["description"] = html.text.strip()

            # programming language
            html = item.select_one('[itemprop="programmingLanguage"]')
            if html is not None:
                repos[name]["programming_language"] = html.text.strip()

            # stargazers
            repos[name]["stargazers"] = {}
            html = item.select_one('[class="octicon octicon-star"]')
            if html is None:
                repos[name]["stargazers_count"] = 0
            else:
                html2 = html.next_sibling
                repos[name]["stargazers_count"] = int(html2.text.strip().replace(',', ''))

            # forks
            repos[name]["forks"] = {}
            html = item.select_one('[class="octicon octicon-repo-forked"]')
            if html is None:
                repos[name]["forks_count"] = 0
            else:
                html2 = html.next_sibling
                repos[name]["forks_count"] = int(html2.text.strip().replace(',', ''))

            # license
            html = item.select_one('[class*="octicon octicon-law"]')
            if html is not None:
                html2 = html.next_sibling
                repos[name]["license"] = html2.text.strip()

        # updated
        html = item.select_one('relative-time')
        if html is not None:
            repos[name]["last_updated"] = html.get("datetime")

    # is there a next page?
    next_page = soup.select_one('[class="next_page"]')
    try:
        href = next_page.get("href")
    except AttributeError:
        href = ""
    if href:
        repos.update(
            load_user_repositories(
                user_name,
                GITHUB_URL + href,
                page + 1,
                cache_days,
                force_fetch=force_fetch
            )
        )

    return repos


####################################################################################################
def load_user_account(account_name, soup, cache_days, force_fetch=False, complete=[]):
    """ Returns a dictionary of personal account information """
    account = {}

    # account type
    account["account_type"] = "personal"

    # avatar
    html = soup.select_one('[itemprop="image"]')
    if html is not None:
        account["avatar"] = html.get("href")

    # (full)name
    html = soup.select_one('[itemprop="name"]')
    if html is not None:
        account["name"] = html.text.strip()

    # pronouns: not provided while unauthenticated
    #html = soup.select_one('[itemprop="pronouns"]')

    # bio(graphy)
    html = soup.select_one('[class*="p-note user-profile-bio"]')
    if html is not None:
        html_text = html.text.strip()
        if html_text:
            account["biography"] = html_text

    # sponsor
    html = soup.select_one('[class*="octicon octicon-heart icon-sponsor"]')
    if html is not None:
        account["sponsor"] = True

    # followers & following
    account["followers"] = {}
    account["following"] = {}
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
        if "following" in href:
            number = [x.strip() for x in item.text.split("\n") if x][0]
            try:
                account["following_count"] = int(number)
            except ValueError:
                if number.endswith('k'):
                    account["following_count"] = int(float(number[:-1]) * 1000)
                elif number.endswith('m'):
                    account["following_count"] = int(float(number[:-1]) * 1000000)
                else:
                    account["following_count"] = 0

    # company
    html = soup.select_one('[class="p-org"]')
    if html is not None:
        account["company"] = html.text.strip()

    # location
    html = soup.select_one('[itemprop="homeLocation"]')
    if html is not None:
        account["location"] = html.text.strip()

    # (localtime and) timezone
    html = soup.select_one('[itemprop="localTime"]')
    if html is not None:
        timezone = html.text.strip().split('\n')[1].strip()
        if timezone.startswith('('):
            account["timezone"] = timezone[1:-1]
        else:
            account["timezone"] = timezone

    # public email: not provided while unauthenticated
    #html = soup.select_one('[itemprop="email"]')

    # profile website URL
    html = soup.select_one('[data-test-selector="profile-website-url"]')
    if html is not None:
        account["website"] = html.text.strip()

    # social media
    account["social"] = {}
    html = soup.select('[itemprop="social"]')
    for item in html:
        anchor = item.select_one('[class="Link--primary"]')
        if anchor is not None:
            ident = anchor.text.strip()
            href = anchor.get("href")
            if href.startswith("https://www.facebook.com/"):
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
            else:
                if "url" in account["social"]:
                    account["social"]["url"].append(href)
                else:
                    account["social"]["url"] = [href]

    # achievements
    account["achievements"] = {}
    html = soup.select('[class="position-relative"]')
    for item in html:
        href = item.get("href")
        if href is not None:
            if "?achievement=" in href:
                achievement = re.sub(r".*achievement=", "", href)
                achievement = re.sub(r"&.*", "", achievement)
                if achievement not in account["achievements"]:
                    account["achievements"][achievement] = {}

                    badge = item.select_one('[class="achievement-badge-sidebar"]')
                    if badge is not None:
                        account["achievements"][achievement]["badge"] = badge.get("src")

                    tier = item.select_one('[class*="Label achievement-tier-label"]')
                    count = 1
                    if tier is not None:
                        if tier.text.strip().startswith('x'):
                            count = int(tier.text.strip()[1:])
                    account["achievements"][achievement]["count"] = count

    # highlights
    account["highlights"] = []
    html = soup.select('[class="h4 mb-2"]')
    for item in html:
        if item.text.strip() == "Highlights":
            subitems = item.parent.select("li")
            for subitem in subitems:
                account["highlights"].append(subitem.text.strip())

    # organizations
    account["organizations"] = {}
    html = soup.select('[itemprop="follows"]')
    for item in html:
        org = item.get("href")[1:] # without the leading /
        account["organizations"][org] = {}

        img = item.select_one("img")
        if img is not None:
            avatar = img.get("src")
            account["organizations"][org]["avatar"] = avatar

    # repositories
    account["repositories"] = {}
    html = soup.select_one('[data-tab-item="repositories"]')
    if html is not None:
        try:
            account["repositories_count"] = int([x.strip() for x in html.text.split("\n") if x][-1])
        except ValueError:
            account["repositories_count"] = 0
        account["repositories"] = load_user_repositories(
            account_name,
            f"{GITHUB_URL}/{account_name}?tab=repositories",
            1,
            cache_days,
            force_fetch=force_fetch,
            complete=complete
        )
    else:
        account["repositories_count"] = 0

    # repositories stars (computed)
    stars = 0
    for repo in account["repositories"]:
        stars += account["repositories"][repo]["stargazers_count"]
    account["repositories_stars"] = stars

    # stars
    account["stars"] = {}
    html = soup.select_one('[data-tab-item="stars"]')
    if html is not None:
        try:
            account["stars_count"] = int([x.strip() for x in html.text.split("\n") if x][-1])
        except ValueError:
            account["stars_count"] = 0
    else:
        account["stars_count"] = 0

    # sponsoring
    html = soup.select_one('[data-tab-item="sponsoring"]')
    if html is not None:
        account["sponsoring"] = {}

    # yearly contributions: not included in what we load
    #html = soup.select_one('[class="js-yearly-contributions"]')

    # member since: not included in what we load
    # would be the last year in the timeline

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
