# License GPLv3 by balestek
import json
import os
import re
import sys
from pathlib import Path
from random import choice
from runpy import run_module

import httpx
from dotenv import load_dotenv, set_key
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from rich.console import Console

from alwaysOn.__about__ import __version__

c = Console(highlight=False)


class Onoff:
    def __init__(self):
        self.path = Path(__file__).resolve().parent
        load_dotenv()
        self.mobileToken = self.originToken = os.getenv("TOKEN")
        self.stat = None
        self.headers = {
            "Host": "production-server.onoffapp.net",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "X-User-Agent": "onoff-wsj/3.9.0",
            "Origin": "https://subscribe.onoff.app",
            "Connection": "keep-alive",
            "Referer": "https://subscribe.onoff.app/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Priority": "u=1",
            "TE": "trailers",
        }
        self.endpoint = "https://production-server.onoffapp.net/mobile/v2/check-email"
        self.email = None

    def header_random_agent(self) -> None:
        with open(Path(self.path, self.path, "user-agents.json")) as f:
            user_agents = [agent["ua"] for agent in json.load(f)]
        user_agent = choice(user_agents)
        self.headers["User-Agent"] = user_agent

    @staticmethod
    def is_valid_email(email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(email_regex, email))

    def save_token(self, token: str) -> None:
        set_key(Path(self.path, ".env"), "TOKEN", token)

    def grab_token(self, response):
        if (
            "https://production-server.onoffapp.net/mobile/captcha/verify-and-register-token"
            in response.url
        ):
            if response.json().get("mobileToken"):
                self.mobileToken = response.json()["mobileToken"]
                self.save_token(self.mobileToken)

    def get_token(self, headless: bool = True) -> str:
        self.stat.update(f"Retrieving token from Onoff.app webpage...")
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=headless, timeout=120000)
            context = browser.new_context(locale="en-GB")
            page = context.new_page()
            page.on("response", self.grab_token)
            stealth_sync(page)
            page.goto("https://subscribe.onoff.app/")
            if headless is False and self.mobileToken == "":
                with page.expect_request(
                    "https://production-server.onoffapp.net/mobile/purchase/anonymous/products/get-prices",
                    timeout=120000,
                ) as e:
                    pass
            else:
                try:
                    with page.expect_response(
                        "https://production-server.onoffapp.net/mobile/captcha/verify-and-register-token",
                        timeout=4000,
                    ) as e:
                        pass
                except:
                    pass
        if self.mobileToken != self.originToken and self.mobileToken != "":
            self.stat.stop()
            self.stat = None
            c.print(f":green_circle: [green]Token {self.mobileToken} saved.[/green]")
            return self.mobileToken
        else:
            self.stat.stop()
            c.print(
                ":yellow_circle: [yellow]Token not retrieved. Solve manually the captcha please.[/yellow]"
            )
            input("   Press Enter to continue...")
            self.get_token(headless=False)

    def check(self, email: str, *token: str) -> None:
        self.email = email
        if not self.is_valid_email(email):
            c.print(
                f"\n:red_circle: [red]{email} is not a valid email address.[/red]\n"
            )
            exit(0)
        self.stat = c.status("Checking token", spinner="dots")
        self.stat.start()
        if token:
            if token[0] == self.mobileToken:
                self.stat.stop()
                c.print(
                    f":yellow_circle: [yellow]Token is the same as the one already saved.[/yellow\n"
                    f"  [yellow]You don't need to use the argument token until the token expiration.[/yellow]"
                )
            else:
                self.mobileToken = token[0]
                self.save_token(self.mobileToken)
                self.stat.stop()
        elif not token and self.mobileToken == "":
            self.get_token()
        self.stat.stop() if self.stat else None
        self.stat = c.status("Checking email...", spinner="dots")
        self.header_random_agent()
        payload = f"""{{"email":"{email}","mobileToken":"{self.mobileToken}","locale":"en"}}"""
        response = httpx.post(self.endpoint, content=payload, headers=self.headers)
        if "emailAlreadyRegistered" in response.json():
            if response.json().get("emailAlreadyRegistered") is True:
                c.print(
                    f"\n:green_circle: [green][bold]{email}[/bold] is already registered on Onoff.app.[/green]\n"
                )
                exit(0)
            elif (
                not response.json().get("emailAlreadyRegistered")
                or response.json().get("emailAlreadyRegistered") is False
            ):
                c.print(
                    f"\n:red_circle: [red][bright_yellow]{email}[/bright_yellow] is not registered on Onoff.app.[/red]\n"
                )
                exit(0)
        elif (
            "mobile-token.not-verified" in response.text
            or "mobileToken.invalid" in response.text
        ):
            c.print(
                "\n:yellow_circle: [yellow]Token expired or invalid, you need a new one.[/yellow]\n"
            )
            self.save_token("")
            self.mobileToken = ""
            self.check(email)
        elif "email-check.not-exists" in response.text:
            c.print(
                "\n:red_circle: [red]Email domain is not supported by Onoff.[/red]\n"
            )
            exit(0)
        else:
            c.print(
                f"\n:red_circle: [red]alwaysOn can't check [bright_yellow]{email}[/bright_yellow].[/red]\n"
            )
            exit(0)

    @staticmethod
    def install_firefox():
        sys.argv = ["playwright", "install", "firefox"]
        run_module("playwright", run_name="__main__")


def main():
    c.print(
        f"""
            ██                                              [dodger_blue1]  █████  [/dodger_blue1]           
            ██                                              [dodger_blue1]███   ███[/dodger_blue1]           
   █████    ██   █          █    ██████   █      █   ████   [dodger_blue1]██     ██[/dodger_blue1]  ██████    
 ██   ███   ██   ██   ██   ██  ███  ███   ██    ██  ██  ██  [dodger_blue1]██ ███ ██[/dodger_blue1]  ███  ███  
██     ██   ██    █   ██   ██  ██    ██    ██  ██   ███     [dodger_blue1]██ ███ ██[/dodger_blue1]  ██    ██  
██     ██   ██    █   ██   ██  ██    ██     █  ██      ███  [dodger_blue1]██     ██[/dodger_blue1]  ██    ██  
 ██   ███   ██    ██  ███  ██  ███  ███     ████    ██  ██  [dodger_blue1]███   ███[/dodger_blue1]  ██    ██  
   ███  ██    █     ██  ███       ███  █     ██      ███    [dodger_blue1]  █████  [/dodger_blue1]  ██      █ 
                                            ██         b y  j m  b a l e s t e k               
                                          ███                            v{__version__}
    """
    )
    c.print(
        ":bulb: [dodger_blue1][bold]alwaysOn[/bold], email checker for Onoff.app[/dodger_blue1]\n"
    )
    c.print(
        ":information: Usage: [bold]alwaysOn <email>[/bold]  Check the email on Onoff.app"
    )
    c.print(
        "         [bold]alwaysOn install[/bold]  Install the browser if alwaysOn has been installed with pipx\n"
    )

    if len(sys.argv) == 1 or len(sys.argv) > 2:
        c.print(
            ":red_circle: [red]See Usage[/red] :backhand_index_pointing_up_medium-light_skin_tone:\n"
        )
        exit(0)
    if sys.argv[1] == "install":
        Onoff().install_firefox()
        c.print(
            ":green_circle: [green]Firefox installed successfully. You can now use the alwaysOn.[/green]"
        )
        exit(0)
    else:
        Onoff().check(sys.argv[1])


if __name__ == "__main__":
    main()
