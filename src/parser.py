import requests
import re
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def get_voyager_date():
    """Returns the launch date of Voyager 1 spacecraft in YYYYMMDD format."""

    url = "https://science.nasa.gov/mission/voyager/voyager-1/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    text = text.split()
    launch_index = text.index("launch")
    voyager_date = (text[launch_index+1] + text[launch_index+2] + text[launch_index+3]).replace("Sept.", "Sep ").replace(",", " ")
    voyager_date = datetime.strptime(voyager_date, "%b %d %Y")
    voyager_date = voyager_date.strftime("%Y%m%d")
    return voyager_date

def get_rfc_date():
    """Returns the publication date of RFC 1149 in YYYYMMDD format."""

    url = "https://datatracker.ietf.org/doc/html/rfc1149"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    rfc_date = re.search(r"\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}", text)
    rfc_date = rfc_date.group(0)
    dt = datetime.strptime(rfc_date, "%d %B %Y")
    rfc_date = dt.strftime("%Y%m%d")
    return rfc_date

def get_brain_emoji():
    """Returns the hexadecimal codepoint of the brain emoji without U+ prefix."""

    url = "https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt"
    response = requests.get(url)

    for line in response.text.split('\n'):
        if 'BRAIN' in line:
            match = re.match(r'^([0-9A-F]+)', line.strip())
            if match:
                return match.group(1).upper()

def get_btc_date():
    """Returns the genesis block date of Bitcoin in YYYYMMDD format."""

    # Bitcoin Core's chainparams.cpp source file from the official GitHub repository
    url = "https://raw.githubusercontent.com/bitcoin/bitcoin/9a29b2d331eed5b4cbd6922f63e397b68ff12447/src/kernel/chainparams.cpp"
    
    try:
        response = requests.get(url)
        content = response.text
        
        match = re.search(r'CreateGenesisBlock\(\s*(\d+)', content)
        
        if match:
            timestamp = int(match.group(1))
            
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            
            return dt.strftime('%Y%m%d')

    except Exception as e:
        return f"Error fetching file: {e}"

def get_ISBN_10():
    """Returns the ISBN-10 number of "The C Programming Language" 2nd edition without hyphens"""

    url = "https://www.cs.princeton.edu/~bwk/cbook.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    text = text.split()
    ISBN_10_index = text.index("ISBN")
    ISBN_10 = text[ISBN_10_index+1].replace("-", "")
    return ISBN_10

def check_correct():
    """Check the correctness of extracted data by computing SHA-256 hash."""

    FLAG = f"FLAG{{{get_voyager_date()}-{get_rfc_date()}-{get_brain_emoji()}-{get_btc_date()}-{get_ISBN_10()}}}"
    hash_object = hashlib.sha256(FLAG.encode())
    hash_hex = hash_object.hexdigest()
    if hash_hex == "d311f26ea1a995af669a62758ad5e0ce2583331059fbfc5c04cc84b2d41f4aed":
        return True
    else:
        return False

print(check_correct())
