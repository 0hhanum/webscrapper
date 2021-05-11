import requests
from bs4 import BeautifulSoup


indeed_result = requests.get(
    'https://www.indeed.com/jobs?q=python&limit=50'
)  # url 의 html 을 전부 긁어옴.

indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')  # BeautifulSoup 이용해 text 정렬
pagination = indeed_soup.find("ul", {"class": "pagination-list"})  # 크롬 inspect 이용 페이지 html 찾음

links = pagination.find_all('a')  # anchor 들 찾아줌 -> find_all 들을 이용하면 리스트로 출력된다.

# a 안의 span 을 가져올거임. list 로 출력되기 때문에 for 문을 사용. 마지막에 next 값이 있기때문에 그를 없애줘야함.
# a 는 anchor (닻) 을 뜻하는 html 문법. 여기서는 각 페이지로 넘어가는 링크들이 a 에 걸려있다.

pages = []
for link in links[:-1]:  # 마지막 값이 next 이기 때문에 그걸 빼준다.
    pages.append(int(link.find('span').string))
    # .string 을 이용해 html 의 외계어를 제외하고 텍스트만 뽑을 수 있다.
    # 결과적으로 페이지 수만 남게된다.
    # /// 그런데 사실, span 을 가져오지 않고 그냥 link 에서 string 을 이용해도 페이지 수만 추출됨.
    # 크롬을 이용해 html 을 살펴보면 페이지 수 이외에는 그 외계어로 둘러싸여있기 때문인듯?

# 여기까지가 2-3 강의 내용인데 indeed 사이트의 ui 가 변경되어 약간의 코드 수정이 필요함.
# 강의 찍을 시점에는 1페이지에서 마지막 페이지까지 확인 할 수 있었지만 이제는 5페이지까지밖에 안나옴.
# 위의 과정을 진행하는 함수를 만들고, for 문을 이용해 끝 페이지까지 url 변경하면서 함수에 넣는 방법이 있음 (코멘트)

max_page = pages[-1]

# 마지막 페이지를 알았으니 마지막 페이지까지 계속 request 를 보내야함.
# 각 페이지를 넘기며 url 이 어떤 방식으로 변하는 지 확인하고 그에 맞게 for 문을 이용해 수동으로 request 한다.

for i in range(max_page):
    print(f'start={i * 50}')

# 기본 url 에 위 문자열을 붙이면 각 페이지로 넘어갈 수 있다.
# 함수를 이용해 넣어줄 것임. indeed.py 에 위의 내용을 복사해 함수를 만들어준다.
