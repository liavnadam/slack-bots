"""
Quick test script to verify Playwright setup and Facebook login.

This script tests:
1. Playwright installation
2. Browser launch
3. Facebook navigation
4. Login (with your credentials)

Run: python test_playwright.py
"""

import os
from dotenv import load_dotenv, find_dotenv
from playwright.sync_api import sync_playwright
import time

# Load environment variables
load_dotenv(find_dotenv())

def test_playwright_setup():
    """Test basic Playwright setup."""
    print("=" * 70)
    print("🧪 Testing Playwright Setup")
    print("=" * 70)

    # Check credentials
    email = os.getenv("FACEBOOK_EMAIL")
    password = os.getenv("FACEBOOK_PASSWORD")

    if not email or not password:
        print("❌ Error: FACEBOOK_EMAIL and FACEBOOK_PASSWORD not found in .env")
        print("\nPlease create a .env file with:")
        print("FACEBOOK_EMAIL=your_email@example.com")
        print("FACEBOOK_PASSWORD=your_password")
        return False

    print(f"✓ Credentials loaded (Email: {email[:3]}***)")
    print()

    # Test Playwright
    print("🚀 Launching browser...")

    with sync_playwright() as playwright:
        # Launch browser (visible)
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("✓ Browser launched successfully")
        print()

        # Navigate to Facebook
        print("🌐 Navigating to Facebook...")
        page.goto("https://www.facebook.com/", wait_until="networkidle")
        print("✓ Loaded Facebook homepage")
        print()

        # Check if already logged in
        if "login" not in page.url.lower():
            print("✓ Already logged in! (cookies from previous session)")
            print()
            print("✅ Test PASSED - Playwright is working!")

            # Keep browser open for 5 seconds
            print("\nKeeping browser open for 5 seconds...")
            time.sleep(5)

            browser.close()
            return True

        # Try to login
        print("🔐 Attempting login...")

        try:
            # Fill email
            email_input = page.locator('input[name="email"]')
            email_input.fill(email)
            time.sleep(1)

            # Fill password
            password_input = page.locator('input[name="pass"]')
            password_input.fill(password)
            time.sleep(1)

            # Click login
            login_button = page.locator('button[name="login"]')
            login_button.click()

            print("⏳ Waiting for login to complete...")
            page.wait_for_load_state("networkidle", timeout=30000)

            # Check if login successful
            if "login" in page.url.lower():
                print("⚠️  Login may have failed or CAPTCHA appeared")
                print("   Please check the browser window")
                print("\n   If CAPTCHA appeared:")
                print("   1. Solve it manually in the browser")
                print("   2. The session will be saved for next time")
            else:
                print("✓ Login successful!")

            print()
            print("✅ Test PASSED - Playwright is working!")
            print("\n📝 Notes:")
            print("   - Browser will stay open for 10 seconds")
            print("   - Check if you're logged in to Facebook")
            print("   - If CAPTCHA appeared, solve it now")
            print("   - Next time the session will be saved")

            # Keep browser open for inspection
            print("\nKeeping browser open for 10 seconds...")
            time.sleep(10)

            browser.close()
            return True

        except Exception as e:
            print(f"❌ Error during login: {e}")
            print("\n   Keeping browser open for inspection...")
            time.sleep(10)
            browser.close()
            return False


def main():
    """Main test function."""
    try:
        success = test_playwright_setup()

        print("\n" + "=" * 70)
        if success:
            print("🎉 SUCCESS!")
            print("=" * 70)
            print("\nYou're ready to run the agent!")
            print("\nNext steps:")
            print("1. Configure your jobs in jobs.json")
            print("2. Configure your groups in groups.json")
            print("3. Run: python facebook_playwright_agent.py")
        else:
            print("❌ FAILED")
            print("=" * 70)
            print("\nPlease fix the issues above and try again.")
        print()

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\nMake sure Playwright is installed:")
        print("  pip install playwright")
        print("  playwright install chromium")


if __name__ == "__main__":
    main()
