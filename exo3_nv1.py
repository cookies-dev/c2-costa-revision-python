from bs4 import BeautifulSoup
from requests import Session, Response
from time import sleep



def post_init(session_req: Session, sexe: int = 0) -> None:
    url = "http://annuairesante.ameli.fr/recherche.html"
    payload = f"es_actes_maladies=&es_actes_maladies_label=&es_nom=&es_specialite=&es_specialite_label=&es_type=3&localisation_category=departements&ps_acte=&ps_acte_label=&ps_carte_vitale=2&ps_localisation=HERAULT%20(34)&ps_nom=&ps_profession=34&ps_profession_label=M%C3%A9decin%20g%C3%A9n%C3%A9raliste&ps_proximite=on&ps_sexe={sexe}&ps_type_honoraire=indifferent&submit_final=Rechercher&type=ps&pageCible=2"
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "host": "annuairesante.ameli.fr",
    }
    session_req.headers = headers
    session_req.post(url, headers=headers, data=payload)


def get_soup(session_req: Session, page: int) -> BeautifulSoup:
    url = f"http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-{page}-par_page-20-tri-nom_asc.html"
    response: Response = session_req.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return BeautifulSoup(response.text, "html.parser")


def get_med(sexe: int = 0) -> list[BeautifulSoup]:
    page, last_page = 0, float("inf")
    rows: list[BeautifulSoup] = list()
    session_req: Session = Session()
    post_init(session_req, sexe)
    while True:
        page += 1
        soup: BeautifulSoup = get_soup(session_req, page)
        if soup is None:
            sleep(5)
            continue
        if last_page == float("inf"):
            last_page = int(soup.find("div", {"class": "pagination"}).find("form").text.strip().replace("Page", "").replace("sur", ""))
        rows.extend(soup.find_all("div", {"class": "item-professionnel"}))
        if page == last_page:
            break
    return rows


def extract_from_tag(tag: BeautifulSoup) -> dict:
    last_name: str = tag.find("h2", {"class": "ignore-css"}).find("strong").text.strip()
    first_name: str = tag.find("h2", {"class": "ignore-css"}).text.strip().replace(last_name, "").strip()
    if phone := tag.find("div", {"class": "tel"}):
        phone: str = phone.text.replace("\xa0", " ").strip()
    address: str = tag.find("div", {"class": "adresse"}).text.strip()
    return {"last_name": last_name, "first_name": first_name, "phone": phone, "address": address}


if __name__ == "__main__":
    rows: list[BeautifulSoup] = get_med(0)
    rows.extend(get_med(1))
    meds = list(map(extract_from_tag, rows))
