import requests
from bs4 import BeautifulSoup

# main.py 의 내용을 이용해 함수를 만들어준다.

LIMIT = 50  # 이런 식으로 변하는 값들을 구분해두면 나중에 옵션을 변경할 때 수월하게 가능하다.
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'  # 기본 url, 변수를 모두 대문자로 강조.
# 문자열이기 때문에 + 'start=어쩌고' 이용해 새로운 페이지의 url 을 만들 수 있다.


def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("ul", {"class": "pagination-list"})
    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        pages.append(int(link.find('span').string))

    max_page = pages[-1]

    return max_page


"""
    이제 이 파일을 이용하면 main 에서 복잡하게 코드를 쓰지 않고 indeed.py 를 import 해 간단하게 
    max_page 를 얻어 올 수 있다.
    
    원래는 main 을 비우고 해야하지만 강의 메모가 현재 main.py 에 모두 적혀져있어서 
    next_main 으로 넘어가겠다.
"""

# 이제 next_main.py 에서 indeed 를 import 해 한번에 max page 를 얻을 수 있게 되었다.
# main 에는 indeed 관련 코드를 넣는 것이 아님. 이제 max page 만큼 request 하면서 직업을 추출하는 함수를 만들것임.
# 이와 같은 방법으로 파일을 나눠서 main 에서는 종합적인 처리를 하자.


def extract_indeed_jobs(last_pages):
    job = []  # job 들을 추출해서 이 리스트에 담을거임.
    # 이렇게 오래걸리는 작업할 때 Tip. for 문을 주석처리해 하나씩만 돌아가게 해두고 정상작동 확인하면 주석 풀기.
    # for page in range(last_pages):
    result = requests.get(f'{URL}&start={0*LIMIT}')  # 이제 모든 페이지에 요청을 보낼 수 있게 되었다.
    soup = BeautifulSoup(result.text, 'html.parser')  # soup 만들기 -> inspect 이용해 job 찾기.
    results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})  # job 이 들어있는 클래스를 뽑아 리스트를 만들어줌.
    for result in results:
        title = result.find('h2', {'class': 'title'})  # title 클래스를 거기도 또 가져옴.
        anchor = title.find('a')['title']  # title 클래스의 anchor 안의 title 속성을 가져온거임.
        # string 으로 하기엔 사이트의 html 이 너무 지저분하게 되어있음.
        # title 클래스의 anchor 안의 title 속성에도 직무가 전부 나와있다. 이렇게 모든 직무를 얻을 수 있게 됨.
        # 웹 스크래핑을 할 때는 이런 식으로 찾고, 그 안에서 찾고, 그 안에서 찾고를 반복함.
        # 이제 회사명을 스크래핑하자.
        company = result.find('span', {'class': 'company'})
        # find, find_all 차이는 find 는 첫 결과만 가져옴.
        # <span> 의 company 는 가져왔다. 그런데 링크가 있는 회사는 anchor 가 있고, 링크가 없는 회사는 anchor 없음. if else 구문을 이용.
        company_anchor = company.find('a')
        if company_anchor is not None:
            company = str(company_anchor.string)  # soup 이기 때문에 str 을 써서 텍스트로 바꿔준다.
        else:
            company = str(company.string)
        company = company.strip()  # 빈 칸 없애주기
        print(company)
    return job


extract_indeed_jobs(extract_indeed_pages())

""" 정보를 처리하려면 함수 길이가 매우 길어질거임.
    직업 이름과 회사명 뽑는 코드를 따로 뽑아서 함수로 처리할건데 
    여기서 그렇게 하면 주석때문에 혼란스러우니 그대로 indeed.py_2 로 넘어가서 진행하겠음"""
