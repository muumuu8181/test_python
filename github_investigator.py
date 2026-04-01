import argparse
import os
import sys
import json
import urllib.request
import urllib.parse
from collections import Counter

def search_repositories(keywords, use_or=False):
    """
    Search GitHub repositories based on keywords.
    """
    base_url = "https://api.github.com/search/repositories"

    # URL encode keywords to handle special characters
    encoded_keywords = [urllib.parse.quote(k) for k in keywords]

    if use_or:
        q = "+OR+".join(encoded_keywords)
    else:
        q = "+".join(encoded_keywords)

    url = f"{base_url}?q={q}"

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")

    token = os.environ.get('GITHUB_TOKEN')
    if token:
        req.add_header("Authorization", f"token {token}")

    try:
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            return data.get('items', [])
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        return []
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        return []

def classify_results(repositories):
    """
    Classify and print the results.
    """
    if not repositories:
        print("No repositories found.")
        return

    print(f"\nFound {len(repositories)} repositories.")

    languages = Counter()
    stars = Counter()
    topics = Counter()

    for repo in repositories:
        # Language
        lang = repo.get('language')
        if lang:
            languages[lang] += 1
        else:
            languages['Unknown'] += 1

        # Stars
        stargazers_count = repo.get('stargazers_count', 0)
        if stargazers_count < 100:
            stars['< 100'] += 1
        elif stargazers_count < 1000:
            stars['100 - 1000'] += 1
        elif stargazers_count < 10000:
            stars['1000 - 10000'] += 1
        else:
            stars['> 10000'] += 1

        # Topics
        repo_topics = repo.get('topics', [])
        for topic in repo_topics:
            topics[topic] += 1

    print("\n--- Classification by Language ---")
    for lang, count in languages.most_common():
        print(f"{lang}: {count}")

    print("\n--- Classification by Stars ---")
    # Sort order for stars
    star_order = ['< 100', '100 - 1000', '1000 - 10000', '> 10000']
    for range_key in star_order:
        if stars[range_key] > 0:
            print(f"{range_key}: {stars[range_key]}")

    print("\n--- Top 10 Topics ---")
    for topic, count in topics.most_common(10):
        print(f"{topic}: {count}")

def main():
    parser = argparse.ArgumentParser(description='GitHub Repository Investigator')
    parser.add_argument('keywords', nargs='+', help='Search keywords')
    parser.add_argument('--or', dest='use_or', action='store_true', help='Use OR search logic')
    args = parser.parse_args()

    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Warning: GITHUB_TOKEN not found. Requests may be rate-limited.", file=sys.stderr)

    print(f"Searching for: {args.keywords} (OR: {args.use_or})")

    results = search_repositories(args.keywords, args.use_or)
    classify_results(results)

if __name__ == "__main__":
    main()
