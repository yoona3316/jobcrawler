import requests
from bs4 import BeautifulSoup
import io

def get_cse_page(path):
    keywords = ("지원기간:", "접수기간:", "지원기간 :", "접수기간 :",
                "지원 기간:", "접수 기간:", "지원 기간 :", "접수 기간 :",
                "모집기간:", "모집기간 :", "모집 기간:", "모집 기간 :")
    date_keywords = ("년", "월", "일")
    day_keywords = ("월", "화", "수", "목", "금", "토", "일")

    cse_url = f'https://cse.snu.ac.kr{path}'
    req = requests.get(cse_url.format(path=path))
    html = req.text
    soup = BeautifulSoup(html, features="html.parser")

    content = soup.find("div", {"id": "content"}).text
    for keyword in keywords:
        pos = content.find(keyword)
        if pos == -1:
            continue
        lines = io.StringIO(content[pos:]).readlines()
        for line in lines:
            for day in day_keywords:
                if line.find(day)>0:
                    return line
            for date in date_keywords:
                if line.find(date)>0:
                    return line
    return None

