import os
import json
import time
import random
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstagramBot:
    def __init__(self, username: str, password: str, cookie_file: str = "instagram_cookie.json"):
        """Initialize Instagram bot with credentials and JSON cookie file."""
        self.username = username
        self.password = password
        self.cookie_file = cookie_file
        self.driver = self._init_driver()

    def _init_driver(self):
        """Initialize SeleniumBase WebDriver with undetected mode."""
        options = {
            "headless": False,  # Set to True to run in the background
            "uc": True,  # Undetected ChromeDriver
        }
        return Driver(**options)

    def login(self):
        """Login to Instagram using cookies if available, otherwise manually."""
        self.driver.maximize_window()
        self.driver.get("https://www.instagram.com/")
        time.sleep(random.uniform(2, 4))

        if self._load_cookies():
            print("[INFO] Logged in using saved cookies.")
            return

        print("[INFO] Logging in manually...")
        self._manual_login()

    def _manual_login(self):
        """Perform manual login and save cookies."""
        try:
            # Wait up to 10 seconds for the username/email input field
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
            )
            
            # Wait up to 10 seconds for the password input field
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))
            )

            self._simulate_typing(username_input, self.username)
            self._simulate_typing(password_input, self.password)
            password_input.send_keys(Keys.RETURN)

            time.sleep(random.uniform(5, 7))

            if "challenge" in self.driver.current_url:
                print("[WARNING] Instagram detected unusual login attempt. Manual verification required.")
                return
            
            self._save_cookies()
            print("[INFO] Login successful and cookies saved.")
        except Exception as e:
            print(f"[ERROR] Failed to login: {e}")

    def _save_cookies(self):
        """Save cookies to a JSON file."""
        cookies = self.driver.get_cookies()
        with open(self.cookie_file, "w") as f:
            json.dump(cookies, f, indent=4)
        print(f"[INFO] Cookies saved to {self.cookie_file}")

    def _load_cookies(self):
        """Load cookies from JSON file if available and not empty."""
        if not os.path.exists(self.cookie_file):
            return False

        try:
            with open(self.cookie_file, "r") as f:
                cookies = json.load(f)

            if not cookies:
                return False

            self.driver.get("https://www.instagram.com/")
            time.sleep(random.uniform(2, 4))

            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            time.sleep(random.uniform(3, 5))

            return "instagram.com" in self.driver.current_url
        except:
            return False

    def _simulate_typing(self, element, text: str):
        """Simulate human-like typing into an input field."""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

    def follow_user(self, target_username: str):
        """Go to the user's profile and follow them if not already followed."""
        profile_url = f"https://www.instagram.com/{target_username}/"
        self.driver.get(profile_url)
        time.sleep(random.uniform(3, 6))

        try:
            follow_button = self.driver.find_element(By.XPATH, '//button[@class=" _acan _acap _acas _aj1- _ap30"]')
            follow_button.click()
            print(f"[INFO] Followed {target_username}.")
            time.sleep(random.uniform(2, 5))  # Simulate natural delay
        except:
            print(f"[INFO] {target_username} is already followed or button not found.")

        
    def search_and_comment(self, keyword, comment):
        """Searches for a keyword, clicks first post, and comments"""
        search_url = f"https://www.instagram.com/explore/search/keyword/?q=%23{keyword}"
        self.driver.get(search_url)
        time.sleep(5)
    
        # Click the first search result
        first_post = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@role="link"]'))
        )
        first_post.click()
        time.sleep(3)
    
        # Wait for the comment field to appear
        comment_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[contains(@class, "x1i0vuye")]'))
        )
        comment_field.click()
        time.sleep(1)

        # Wait for the comment field to appear
        comment_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[contains(@class, "x1i0vuye")]'))
        )

        # Type and post the comment
        comment_field.send_keys(comment)
        comment_field.send_keys(Keys.RETURN)
        time.sleep(3)

    def quit(self):
        """Close the browser."""
        self.driver.quit()


if __name__ == "__main__":
    # 🛑 PROMOTIONAL MESSAGE 🛑
    print("\n" + "="*60)
    print("🔥 INSTAGRAM AUTOMATION BOT 🔥")
    print("🚀 Automate your Instagram actions (Login, Follow, Comment) 🚀")
    print("💰 Want a custom bot or automation for your business?")
    print("📩 Contact me on Telegram: @mysteredev")
    print("="*60 + "\n")
    
    # Get user input
    email = input("Enter your Instagram email: ")
    password = input("Enter your Instagram password: ")
    user_to_follow = input("Enter the username to follow: ")
    topic = input("Enter the topic to comment on (e.g., 'css'): ")
    comment = input("Enter your comment: ")

    bot = InstagramBot(email, password)
    bot.login()
    bot.follow_user(user_to_follow)
    bot.search_and_comment(topic, comment)
    bot.quit()
