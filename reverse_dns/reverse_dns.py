import requests
from urllib import request, parse
from bs4 import BeautifulSoup

class Domain():
    def __init__(self, domain_name, creation_date, registrar):
        self.domain_name = domain_name
        self.creation_date = creation_date
        self.registrar = registrar


def find_domains_from_html(html):
    try:
        soup = BeautifulSoup(html, "html.parser")

        tables = soup.findAll('table', {"border": "1"})
        rows = tables[0].findAll("tr")[1:]

        domains = []

        for row in rows:
            cols = row.findAll('td')
            params = []
            for col in cols:
                params.append(col.text)

            domain = Domain(params[0], params[1], params[2])
            domains.append(domain)

        print(f"{len(domains)} domains found.")
        for domain in domains:
            print("=========================")
            print(f"Domain Name:\t{domain.domain_name}")
            print(f"Creation Date:\t{domain.creation_date}")
            print(f"Registrar:\t{domain.registrar}")
            print("")
    except IndexError:
        print("No domains found.")
        

def reverse_lookup(name):
    query = parse.urlencode({"q": name})
    url = f"https://viewdns.info/reversewhois/?{query}"

    req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    with request.urlopen(req) as resp:
        html = resp.read()

        find_domains_from_html(html)


def main():
    print('''
     _  .-')     ('-.        (`-.      ('-.  _  .-')    .-')      ('-.          _ .-') _       .-') _   .-')    
( \( -O )  _(  OO)     _(OO  )_  _(  OO)( \( -O )  ( OO ).  _(  OO)        ( (  OO) )     ( OO ) ) ( OO ).  
 ,------. (,------.,--(_/   ,. \(,------.,------. (_)---\_)(,------.        \     .'_ ,--./ ,--,' (_)---\_) 
 |   /`. ' |  .---'\   \   /(__/ |  .---'|   /`. '/    _ |  |  .---'  .-')  ,`'--..._)|   \ |  |\ /    _ |  
 |  /  | | |  |     \   \ /   /  |  |    |  /  | |\  :` `.  |  |    _(  OO) |  |  \  '|    \|  | )\  :` `.  
 |  |_.' |(|  '--.   \   '   /, (|  '--. |  |_.' | '..`''.)(|  '--.(,------.|  |   ' ||  .     |/  '..`''.) 
 |  .  '.' |  .--'    \     /__) |  .--' |  .  '.'.-._)   \ |  .--' '------'|  |   / :|  |\    |  .-._)   \ 
 |  |\  \  |  `---.    \   /     |  `---.|  |\  \ \       / |  `---.        |  '--'  /|  | \   |  \       / 
 `--' '--' `------'     `-'      `------'`--' '--' `-----'  `------'        `-------' `--'  `--'   `-----'  
    ''')

    name = input("Enter name to reverse lookup: ")
    reverse_lookup(name)
        


if __name__ == "__main__":
    main()