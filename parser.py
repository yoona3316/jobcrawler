import requests
from bs4 import BeautifulSoup
import datetime
from datetime import datetime as dt

import get_specific_page as get_page
from send_email import send_email

ref_date = dt.now()
career_url = 'http://career.snu.ac.kr/student/employment/list.jsp?page={page}&category_code=3'
cse_url = 'https://cse.snu.ac.kr/department-notices?page={page}'
cse_page_url = 'https://cse.snu.ac.kr{path}'

# 경력개발센터 채용 공고 크롤링
# page를 돌아가면서 새로 업로드된 데이터를 크롤링. page 중간에 새로 업로드된 데이터가 끝나면 -1을 리턴
def get_career_data(page, text):
    req = requests.get(career_url.format(page=page))
    html = req.text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.find("table", {"summary": "게시판"}).find("tbody")
    datas = table.find_all("tr")

    for data in datas:
        lines = data.find_all("td")
        title = lines[1].get_text()
        upload_date = lines[2].get_text()
        upload_date = dt.strptime(upload_date, "%Y-%m-%d")
        until = lines[3].get_text()
        if upload_date >= ref_date:
            text.append(f'{title} 기한: {until}\n')
        else:
            return -1
        # try:
        #     until = datetime.strptime(until, "%Y-%m-%d")
        #     if upload_date > datetime.now():
        #         text.append(f'지원하자! {title} {until}\n')
        # except ValueError:
        #     text.append(f'지원하자! {title} {until}\n')
        #     pass
    return 0

# 컴퓨터 공학부 홈페이지 채용 정보 크롤링
# page를 돌아가면서 새로 업로드된 데이터를 크롤링, page 맨 마지막 데이터가 새로 업로드된 것이 아니면 -1을 리턴
def get_cse_data(page, text):
    keywords = ("채용", "모집", "공고", "선발", "인턴쉽", "인턴십")

    req = requests.get(cse_url.format(page=page))
    html = req.text
    soup = BeautifulSoup(html, features="html.parser")

    table = soup.find("div", {"id": "block-system-main"}).find("tbody")

    datas = table.find_all("tr")
    for data in datas:
        title = data.find("a").get_text()
        upload_date = data.find("td", {"class": "views-field-created"}).get_text()
        upload_date = upload_date.strip()
        upload_date = dt.strptime(upload_date, "%Y/%m/%d")
        for keyword in keywords:
            if title.find(keyword)>0:
                path = data.find("a")['href']
                until = get_page.get_cse_page(path)
                link = cse_page_url.format(path=path)
                if until is None:
                    text.append(f'{title} {link}')
                else:
                    text.append(f'{title} 기한: {until} {link}')
                break

    if upload_date >= ref_date:
        return 0
    return -1


res = {"경력개발센터": [], "컴공 홈페이지":[]}

for page in range(1, 10):
    if get_career_data(page, res.get("경력개발센터")) == -1:
        break

for page in range(2, 10):
    if get_cse_data(page, res.get("컴공 홈페이지")) == -1:
        break

resStr = ""
content_format = '<p>{item}\n</p>'

resStr += "<h3>경력개발센터\n" + career_url.format(page=1) + "\n</h3>"
for item in res.get("경력개발센터"):
    resStr += content_format.format(item=item)

resStr += "<h3>컴공 홈페이지\n" + cse_url.format(page=2) + "\n</h3>"

for item in res.get("컴공 홈페이지"):
    resStr += content_format.format(item=item)

send_email(resStr)
