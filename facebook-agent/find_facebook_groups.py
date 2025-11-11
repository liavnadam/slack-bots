"""
Helper script to find Facebook Group IDs easily.

This script opens Facebook groups in your browser and shows you where to find the Group ID.
You'll copy the IDs manually and paste them into groups.json

Usage:
    python find_facebook_groups.py
"""

import webbrowser
import time
from typing import List, Dict

# Popular Israeli job search groups (Hebrew)
RECOMMENDED_GROUPS = [
    {
        "search_term": "דרושים פתח תקווה",
        "description": "קבוצת דרושים ספציפית לפתח תקווה",
        "category": "Local - Petah Tikva"
    },
    {
        "search_term": "דרושים אזור המרכז",
        "description": "משרות במרכז הארץ",
        "category": "Regional - Center"
    },
    {
        "search_term": "חיפוש עבודה ישראל",
        "description": "חיפוש עבודה כללי בישראל",
        "category": "National"
    },
    {
        "search_term": "דרושים במרכז",
        "description": "משרות באזור המרכז",
        "category": "Regional - Center"
    },
    {
        "search_term": "משרות ישראל",
        "description": "משרות כלליות בישראל",
        "category": "National"
    },
    {
        "search_term": "job opportunities israel",
        "description": "English-speaking job seekers in Israel",
        "category": "English"
    },
    {
        "search_term": "דרושים בתחום ההייטק",
        "description": "משרות היי-טק",
        "category": "Tech"
    },
    {
        "search_term": "דרושים מכירות ושירות",
        "description": "משרות במכירות ושירות",
        "category": "Sales & Service"
    }
]


def print_header():
    """Print a nice header."""
    print("=" * 80)
    print("🔍 Facebook Group ID Finder")
    print("=" * 80)
    print()
    print("This tool will help you find Facebook Group IDs for your agent.")
    print()


def print_instructions():
    """Print instructions for finding Group IDs."""
    print("📖 HOW TO FIND GROUP IDs:")
    print("-" * 80)
    print()
    print("Option 1: FROM GROUP URL")
    print("  1. Go to the Facebook group")
    print("  2. Look at the URL in your browser")
    print("  3. The URL format is: facebook.com/groups/{GROUP_ID}/")
    print("     Example: facebook.com/groups/123456789/")
    print("     The Group ID is: 123456789")
    print()
    print("Option 2: FROM GROUP PAGE")
    print("  1. Go to the group")
    print("  2. Right-click on the page")
    print("  3. Click 'View Page Source' or 'Inspect'")
    print("  4. Search for 'group_id' (Ctrl+F)")
    print("  5. Copy the number")
    print()
    print("Option 3: USE THIS SCRIPT")
    print("  1. This script will open Facebook search for you")
    print("  2. Find groups you want to join")
    print("  3. Copy the Group IDs from URLs")
    print("  4. Paste them into groups.json")
    print()
    print("-" * 80)
    print()


def search_facebook_groups(interactive=True):
    """Help user find Facebook groups."""
    print_header()
    print_instructions()

    print("🎯 RECOMMENDED GROUPS TO SEARCH FOR:")
    print("-" * 80)
    print()

    for i, group in enumerate(RECOMMENDED_GROUPS, 1):
        print(f"{i}. {group['search_term']}")
        print(f"   Category: {group['category']}")
        print(f"   {group['description']}")
        print()

    print("-" * 80)
    print()

    if not interactive:
        print("ℹ️  Run in interactive mode to open Facebook searches")
        return

    # Interactive mode
    choice = input("Do you want to open Facebook searches in your browser? (y/n): ").strip().lower()

    if choice != 'y':
        print("\n✅ No problem! You can search for these groups manually on Facebook.")
        print("\nTo search manually:")
        print("1. Go to facebook.com")
        print("2. Use the search bar")
        print("3. Search for each group name above")
        print("4. Click on 'Groups' tab in search results")
        print("5. Find the group and copy the ID from URL")
        return

    print("\n🌐 Opening Facebook searches...")
    print("⚠️  Make sure you're logged in to Facebook!")
    print()

    for i, group in enumerate(RECOMMENDED_GROUPS):
        print(f"\n{i+1}. Opening search for: {group['search_term']}")

        # URL encode the search term
        search_url = f"https://www.facebook.com/search/groups/?q={group['search_term'].replace(' ', '%20')}"

        try:
            webbrowser.open(search_url)
            print(f"   ✓ Opened in browser")

            if i < len(RECOMMENDED_GROUPS) - 1:
                print(f"\n   Waiting 3 seconds before next search...")
                time.sleep(3)
        except Exception as e:
            print(f"   ✗ Error opening browser: {e}")
            print(f"   Manual URL: {search_url}")

    print("\n" + "=" * 80)
    print("✅ DONE!")
    print("=" * 80)
    print()
    print("📝 NEXT STEPS:")
    print("1. Look at the browser tabs that opened")
    print("2. Find groups you want to join")
    print("3. Join the groups (important! Must be a member)")
    print("4. Copy the Group ID from each group's URL")
    print("5. Run: python configure_groups.py")
    print("   This will help you build your groups.json file")
    print()


def show_example_groups_json():
    """Show an example groups.json structure."""
    print("\n" + "=" * 80)
    print("📄 EXAMPLE groups.json FORMAT:")
    print("=" * 80)
    print("""
[
  {
    "group_id": "123456789",
    "name": "דרושים פתח תקווה",
    "city": "Petah Tikva",
    "description": "Local job search group for Petah Tikva"
  },
  {
    "group_id": "987654321",
    "name": "חיפוש עבודה ישראל",
    "city": "Petah Tikva",
    "description": "National job search group"
  }
]
""")
    print("=" * 80)
    print()


def main():
    """Main function."""
    import sys

    interactive = True
    if len(sys.argv) > 1 and sys.argv[1] == '--no-browser':
        interactive = False

    search_facebook_groups(interactive=interactive)

    if interactive:
        show_groups = input("\nWould you like to see an example groups.json format? (y/n): ").strip().lower()
        if show_groups == 'y':
            show_example_groups_json()
    else:
        show_example_groups_json()

    print("💡 TIP: Once you have Group IDs, use:")
    print("   python configure_groups.py")
    print("   to build your groups.json file interactively!")
    print()


if __name__ == "__main__":
    main()
