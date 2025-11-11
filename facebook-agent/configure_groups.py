"""
Interactive tool to build your groups.json file.

This script helps you create a properly formatted groups.json
with the Facebook Group IDs you found.

Usage:
    python configure_groups.py
"""

import json
import os
from typing import List, Dict


def print_header():
    """Print header."""
    print("=" * 80)
    print("⚙️  Facebook Groups Configuration Tool")
    print("=" * 80)
    print()


def load_existing_groups(filename: str = "groups.json") -> List[Dict]:
    """Load existing groups if file exists."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Could not load {filename}: {e}")
            return []
    return []


def add_group_interactive() -> Dict:
    """Add a group interactively."""
    print("\n📝 Add a new group:")
    print("-" * 80)

    # Get Group ID
    while True:
        group_id = input("Group ID (numbers only, from URL): ").strip()
        if group_id and group_id.isdigit():
            break
        print("❌ Invalid! Please enter only numbers (e.g., 123456789)")

    # Get Group Name
    name = input("Group Name (e.g., דרושים פתח תקווה): ").strip()
    if not name:
        name = f"Group {group_id}"

    # Get City
    print("\nCity (for job matching):")
    print("  Examples: Petah Tikva, Tel Aviv, Jerusalem, Haifa, Beer Sheva")
    city = input("City: ").strip()
    if not city:
        city = "Israel"

    # Get Description (optional)
    description = input("Description (optional, press Enter to skip): ").strip()
    if not description:
        description = f"Job search group in {city}"

    group = {
        "group_id": group_id,
        "name": name,
        "city": city,
        "description": description
    }

    print("\n✅ Group added:")
    print(json.dumps(group, indent=2, ensure_ascii=False))

    return group


def save_groups(groups: List[Dict], filename: str = "groups.json"):
    """Save groups to JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(groups, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Saved to {filename}")
        return True
    except Exception as e:
        print(f"\n❌ Error saving: {e}")
        return False


def display_groups(groups: List[Dict]):
    """Display all groups."""
    if not groups:
        print("\nℹ️  No groups configured yet.")
        return

    print(f"\n📋 Current groups ({len(groups)}):")
    print("-" * 80)
    for i, group in enumerate(groups, 1):
        print(f"\n{i}. {group['name']}")
        print(f"   ID: {group['group_id']}")
        print(f"   City: {group['city']}")
        print(f"   Description: {group['description']}")
    print("-" * 80)


def quick_setup_petah_tikva() -> List[Dict]:
    """Quick setup for Petah Tikva with placeholder IDs."""
    print("\n🚀 Quick Setup - Petah Tikva Template")
    print("-" * 80)
    print("This will create a template with common group names.")
    print("⚠️  You'll need to replace the Group IDs with real ones!")
    print()

    groups = [
        {
            "group_id": "REPLACE_ME_1",
            "name": "דרושים פתח תקווה",
            "city": "Petah Tikva",
            "description": "Local job search - Petah Tikva"
        },
        {
            "group_id": "REPLACE_ME_2",
            "name": "משרות אזור המרכז",
            "city": "Petah Tikva",
            "description": "Jobs in central region"
        },
        {
            "group_id": "REPLACE_ME_3",
            "name": "חיפוש עבודה ישראל",
            "city": "Petah Tikva",
            "description": "National job search group"
        },
        {
            "group_id": "REPLACE_ME_4",
            "name": "דרושים במרכז הארץ",
            "city": "Petah Tikva",
            "description": "Jobs in center of Israel"
        }
    ]

    display_groups(groups)

    print("\n⚠️  IMPORTANT: Replace 'REPLACE_ME_X' with actual Group IDs!")
    print("Use: python find_facebook_groups.py")
    print("To find the real Group IDs from Facebook.")

    return groups


def main():
    """Main interactive configuration."""
    print_header()

    # Load existing groups
    groups = load_existing_groups()

    if groups:
        print(f"✓ Found existing configuration with {len(groups)} groups")
        display_groups(groups)

        choice = input("\nWhat would you like to do? (add/replace/view/quit): ").strip().lower()
        if choice == 'quit':
            return
        elif choice == 'view':
            display_groups(groups)
            return
        elif choice == 'replace':
            groups = []
            print("\n🔄 Starting fresh configuration...")
    else:
        print("ℹ️  No existing configuration found. Let's create one!")

    # Main menu
    while True:
        print("\n" + "=" * 80)
        print("MENU:")
        print("=" * 80)
        print("1. Add a group manually (you have the Group ID)")
        print("2. Use Petah Tikva template (you'll add IDs later)")
        print("3. View current groups")
        print("4. Remove a group")
        print("5. Save and exit")
        print("6. Exit without saving")
        print()

        choice = input("Choose (1-6): ").strip()

        if choice == '1':
            # Add group manually
            group = add_group_interactive()
            groups.append(group)
            print(f"\n✅ Total groups: {len(groups)}")

        elif choice == '2':
            # Use template
            if groups:
                print("\n⚠️  You already have groups. This will REPLACE them!")
                confirm = input("Continue? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue

            groups = quick_setup_petah_tikva()
            print(f"\n✅ Template created with {len(groups)} groups")
            print("⚠️  Don't forget to replace the placeholder IDs!")

        elif choice == '3':
            # View groups
            display_groups(groups)

        elif choice == '4':
            # Remove group
            display_groups(groups)
            if not groups:
                continue

            try:
                num = int(input("\nEnter group number to remove (0 to cancel): ").strip())
                if num > 0 and num <= len(groups):
                    removed = groups.pop(num - 1)
                    print(f"\n✅ Removed: {removed['name']}")
                elif num != 0:
                    print("❌ Invalid number")
            except ValueError:
                print("❌ Invalid input")

        elif choice == '5':
            # Save and exit
            if not groups:
                print("\n⚠️  No groups to save!")
                continue

            display_groups(groups)
            print()
            confirm = input("Save these groups? (y/n): ").strip().lower()

            if confirm == 'y':
                if save_groups(groups):
                    print("\n" + "=" * 80)
                    print("🎉 SUCCESS!")
                    print("=" * 80)
                    print(f"\nSaved {len(groups)} groups to groups.json")
                    print("\n📝 NEXT STEPS:")
                    print("1. If you used a template, replace placeholder IDs with real ones")
                    print("2. Make sure you're a MEMBER of all these groups on Facebook")
                    print("3. Set up your .env file with credentials")
                    print("4. Run: python test_playwright.py")
                    print("5. Run: python facebook_playwright_agent.py")
                    print()
                    break
            else:
                print("\n❌ Not saved. Returning to menu...")

        elif choice == '6':
            # Exit without saving
            print("\n👋 Exiting without saving...")
            break

        else:
            print("\n❌ Invalid choice. Please enter 1-6.")

    print("\n" + "=" * 80)
    print("Done! 👍")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
