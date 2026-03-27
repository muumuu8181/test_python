from playwright.sync_api import sync_playwright

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to dashboard...")
        page.goto("http://127.0.0.1:8000/")

        print("Verifying title...")
        assert "ERP System" in page.title()

        print("Verifying content...")
        assert page.get_by_role("heading", name="業務システムへようこそ").is_visible()
        assert page.get_by_text("現在の受注件数").is_visible()

        print("Taking screenshot...")
        page.screenshot(path="erp_system/verification/dashboard.png")

        browser.close()
        print("Verification complete!")

if __name__ == "__main__":
    verify_dashboard()
