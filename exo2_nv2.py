from bs4 import BeautifulSoup
from requests import Response, get
import csv


def get_soup(url: str) -> BeautifulSoup:
    r: Response = get(url)
    return BeautifulSoup(r.content, "html.parser")


def get_columns(tag: BeautifulSoup, columns: str) -> dict[str, str]:
    return {columns: tag.find("td", {"class": columns}).text.strip()}


def extract_from_tag(tag: BeautifulSoup) -> dict[str, str]:
    data: dict = dict()
    keys: list = ["name", "year", "wins", "losses", "ot-losses", "pct", "gf", "ga", "diff"]
    for key in keys:
        data.update(get_columns(tag, key))
    return data


def write_csv(rows: list[BeautifulSoup]) -> None:
    with open("exo2_nv2.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "year", "wins", "losses", "ot-losses", "pct", "gf", "ga", "diff"])
        writer.writeheader()
        for team in map(extract_from_tag, rows):
            if int(team.get("diff")) > 0:
                writer.writerow(team)


if __name__ == "__main__":
    rows: list[BeautifulSoup] = list()
    url: str = "https://www.scrapethissite.com/pages/forms/?page_num={}&per_page=25"
    page = 1
    while True:
        soup: BeautifulSoup = get_soup(url.format(page))
        rows.extend(soup.find_all("tr", {"class": "team"}))
        if (soup.find("a", {"aria-label": "Next"})) is None or page == 10:
            break
        page += 1
    write_csv(rows)
