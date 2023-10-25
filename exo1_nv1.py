from bs4 import BeautifulSoup
from requests import Response, get


def get_soup(url: str) -> BeautifulSoup:
    r: Response = get(url)
    return BeautifulSoup(r.content, "html.parser")


def extract_from_tag(tag: BeautifulSoup) -> dict:
    country: str = tag.find("h3", {"class": "country-name"}).text.strip()
    capital: str = tag.find("span", {"class": "country-capital"}).text.strip()
    population: str = tag.find("span", {"class": "country-population"}).text.strip()
    area: str = tag.find("span", {"class": "country-area"}).text.strip()
    return {"country": country, "capital": capital, "population": population, "area": area}


if __name__ == "__main__":
    url: str = "https://www.scrapethissite.com/pages/simple/"
    soup: BeautifulSoup = get_soup(url)
    for country in map(extract_from_tag, soup.find_all("div", {"class": "country"})):
        print(country.get("country"))
