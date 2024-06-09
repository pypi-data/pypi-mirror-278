from playwright.sync_api import sync_playwright
from random import choice
from time import sleep
import re


PHONE_REGEX = re.compile(r"\+1 \(\d{3}\) \d{3}-\d{4}")


def remove_non_numeric(input_string):
    return re.sub(r'\D', '', input_string)


class PhoneNumber:
    def __enter__(self):
        self._playwright = sync_playwright()
        self._playwright = self._playwright.__enter__()
        self._browser = self._playwright.firefox.launch()
        self._page = self._browser.new_page()
        self._page.goto("https://www.textverified.com/free")

        self._page.wait_for_load_state()

        for _ in range(30):
            sleep(1)

            choices = []

            for num in self._page.query_selector_all("div[class='mx-auto flex w-full min-h-64 flex-col justify-between rounded-md bg-slate-50 shadow-md py-4 px-8']"):
                html_code = str(num.inner_html())

                if "<p>Online</p>" not in html_code:
                    continue

                if len(PHONE_REGEX.findall(html_code)) > 0:
                    choices.append((num, html_code))

            if len(choices) < 1:
                continue

            chosen_number_element, chosen_number = choice(choices)
            self.number_formatted = PHONE_REGEX.findall(chosen_number)[0].strip()
            self.number_country_code = self.number_formatted.split(" ")[0].strip("+")
            self.number_plain = self.number_formatted.split(" ")[0]
            self.number_plain = remove_non_numeric(self.number_formatted.replace(self.number_plain + " ", "", 1))
            self.carrier = chosen_number.split("</h2>")[0].split(">")[-1]
            chosen_number_element.query_selector("button").click()

            self._page.wait_for_load_state()

            for _ in range(30):
                sleep(1)

                self._tbody = self._page.query_selector("tbody")
                if self._tbody is None:
                    continue

                if "Loading your free number!" in self._tbody.inner_text():
                    continue

                return self

            raise TimeoutError  # This likely means the code is patched :C

        raise TimeoutError  # This likely means the code is patched :C

    def messages(self) -> list[tuple[str, str, str]]:
        messages_received = []

        for tr in self._tbody.query_selector_all("tr"):
            tds = tr.query_selector_all("td")
            messages_received.append((tds[0].inner_text(), tds[1].inner_text(), tds[2].inner_text()))

        return messages_received

    def __str__(self):
        return f"Number: {self.number_formatted}, Carrier: {self.carrier}"

    def __exit__(self, *args):
        self._browser.close()
