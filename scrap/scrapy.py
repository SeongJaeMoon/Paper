import requests
from bs4 import BeautifulSoup as bs
from random import randint
from time import sleep
from time import strftime as strf
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import walk
from os.path import curdir
from os.path import pardir
from os import chdir
import shutil
import re

# Path
URL = "http://www.ndsl.kr/ndsl/search/list/article/articleSearchResultList.do?page={}&query={}&prefixQuery=&collectionQuery=&showQuery=%ED%8C%8C%EC%9D%B4%EC%8D%AC&resultCount=10&sortName=RANK&sortOrder=DESC&colType=scholar&colTypeByUser=&filterValue="
# font
PATH = '/Library/Fonts/NanumGothic.ttf'
# Chrome Driver Path
DRIVER_DIR = '/Users/moonseongjae/chromedriver'
PDF_DIR = '/Users/moonseongjae/Project_NDSL/ndslsaver/data/pdfs/'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
COOKIE = {
    '_ga':'GA1.2.1497042209.1536590508', 
    'LastDownCtNo':'a0ebd33868c49b24ffe0bdc3ef48d419', 
    'JSESSIONID':'AG4bZM5OJCf4wsf4Om2TJwtDpcIZM974y1r2KdTJkZwGp7pi0BurGB2cTMy83kvy.risswas1_servlet_engine1',
    '_gid':'GA1.2.1744150057.1537054265',
    'TodayView':'be54d9b8bc7cdb09_a0ebd33868c49b24ffe0bdc3ef48d419_%ED%8C%8C%EC%9D%B4%EC%8D%AC+%EC%96%B8%EC%96%B4%EB%A5%BC+%EC%9D%B4.+.+.,be54d9b8bc7cdb09_a0ebd33868c49b24ffe0bdc3ef48d419_%ED%8C%8C%EC%9D%B4%EC%8D%AC+%EC%96%B8%EC%96%B4%EB%A5%BC+%EC%9D%B4%EC%9A%A9%ED%95%9C...',
    '__atuvc':'41%7C37%2C1%7C38', 
    'wcs_bt':'2e819ec0169a:1537056639'
}
# title, author, link, abstract
def get_link(keyword: 'search keyword'):
    datas = {}
    for page in range(1, 15):
        req = requests.get(URL.format(str(page), keyword))
        code = req.status_code
        print(code)
        if code == 200:
            soup = bs(req.text, 'html.parser')
            div = soup.find_all('div', attrs= {'class':'list_con'})
            for data in div:
                link = get_detail(data.find('ul', attrs={'class':'add_menu'}))
                if link is not None:
                    title = data.find('a', attrs={'title': '상세화면'})
                    title = title.get_text()        
                    title = title.replace('\n', '').replace('\t', '')
                    abstract = data.find('div', attrs = {'class':'box_st1'})
                    abstract = abstract.get_text()
                    author = get_author(data)
                    temp = [author, abstract, link]
                    datas[title] = temp
        else:
            raise Exception('HTTP Status Error: ' + str(code))
    return datas

# 저자 정보 가져오는 함수
def get_author(data: 'div.list_con'):
    step1 = str(data).split('<!-- 저자 정보 str -->')[1]
    step2 = step1.split('<!-- 저자 정보 end -->')[0]
    ret = ''.join(step2.split()).replace('<p>','').replace('</p>','').replace('<br>','\n').replace('<br/>', '\n')
    return ret

def get_detail(data: 'ul of content table') -> 'URL':
    isA = data.find('a', attrs={'class':'view_og'})
    if isA is not None:
        return isA['href'] + 'a' # a 태그에서 찾은 것 색인 -> selenium 접근 필요
    isB = data.find('button', attrs={'class':'view_og'})
    if isB is not None:
        href = isB['onclick']
        # kci급 논문 -> 원문 구분 필요
        if 'kci' in href:
            href = href.split(',')[3].replace("'", '').replace(");return false;", '').replace(" ", '').replace(');', '')
        else:
            direct = "http://www.ndsl.kr/ndsl/commons/util/ndslOriginalView.do?dbt={0}&cn={1}&oCn={2}&journal={3}"
            dbt = href.split(',')[1].replace("'", '').replace(" ", '')
            cn = href.split(',')[0].replace("'", '').replace("fncOrgDown(", '')
            oCn = href.split(',')[0].replace("'", '').replace("fncOrgDown(", '')
            journal = href.split(',')[3].replace("'", '').replace(");return false;", '').replace(" ", '')
            href = direct.format(dbt, cn, oCn, journal) + 'b' # button으로 찾은 것 색인 -> pdf 바로 접근 가능
        return href
    else:
        return None

def save_pdf(title, data: 'kci unique code', isKCI = False) -> 'SAVE PDF':
    download_path = ''
    out_file = ''
    # kci download path
    kci_url = 'https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiOrteServHistIFrame.kci?sereArticleSearchBean.artiId={}&sereArticleSearchBean.orteFileId={}'
    if isKCI:
        download_path = kci_url.format('ART' + str(data), 'KCI_FI' + str(data))
    else:  
        download_path = data

    res = requests.get(download_path, headers = HEADER, stream = True, cookies = COOKIE, verify = False)
    code = res.status_code
    if code == 200:
        try:
            with open(PDF_DIR + ''.join(title.split()) + '.pdf', 'wb') as f:
                res.raw.decode_content = True   
                shutil.copyfileobj(res.raw, f)
        except Exception as err:
            print(err, data)
    else:
        print('HTTP error: ', code)

def get_pdf_by_alink(title, URL: 'selenium link'):
    req = requests.get(URL, headers = HEADER, cookies = COOKIE, verify = False, stream = True)
    link = ''
    if req.status_code == 200:
        soup = bs(req.text, 'html.parser')
        div = soup.find('div', attrs={'class':'fulltext_btn'})
        if div is None:
            for i in range(3):
                req = requests.get(URL, headers = HEADER, cookies = COOKIE, verify = False, stream = True)    
                soup = bs(req.text, 'html.parser')
                div = soup.find('div', attrs={'class':'fulltext_btn'})
                if div is not None:
                    temp = div.find('a')
                    link = temp.get('href')
        else:
            temp = div.find('a')
            link = temp.get('href')
    if link != '':        
        public = '/public_resource/pdf/'
        s = requests.Session()
        req = s.get(link, headers = HEADER, cookies = COOKIE ,verify = False)
        code = req.status_code
        if code == 200:
            isKr = link.find('.kr') >= 1
            new_url = isKr and link.split('kr')[0] or link.split('net')[0]  
            if isKr:
                if link.find('ajou') >= 1:
                    new_url += 'kr:9080'
                else:
                    new_url += 'kr'
            else:
                new_url += 'net'
            filename = str(req.text)
            filename = filename.split('"fileRealName" value="')[1]
            filename = filename.split('.pdf')[0]
            ret_link = new_url + public + filename + '.pdf'
                
            print('a: ', title)
            print(ret_link)
            save_pdf(title, ret_link, isKCI = False)
        else:
            print('http status code: ', code)
    else:
        print('error')
# Selenium 사용 보류 -> a 태그의 링크만 따로 타고 들어갈 수 있는지 확인!
def get_a_selenium(links):
    # options = webdriver.ChromeOptions()
    get_url = 'http://www.riss.kr/search/download/FullTextDownload.do'
    driver = webdriver.Chrome(DRIVER_DIR)
    driver.implicitly_wait(5)
    try:
        for link in links:
            driver.get(str(link[1]))
            sleep(1)
            try:
                source = driver.page_source
                soup = bs(source, 'html.parser')
                if soup is not None:
                    form = soup.find('form', attrs={'id':'f'})
                    inputs = form.find_all('input')
                    values = {}
                    for i in inputs:
                        values[i.get('name')] = i.get('value')
                    # get selenium link
                    req = requests.get(get_url, params = values, verify = False)
                    _find = bs(req.text, 'html.parser')    
                    iframe = _find.find('iframe', attrs={'id':'download_frm'})
                    iframe = iframe.get('src')           
                    src = iframe.replace('Downloading.do?', '')
                    req_url = 'http://www.riss.kr/search/download/Downloading.do?' + src                    
                    get_pdf_by_alink(link[0], req_url)
            except Exception as e:
                print('selenium1', e)
                pass
    except Exception as e:
        print('selenium2', e)
        pass
    finally:
        driver.close()
# kci 등재 논문        
def save_kci(links: 'kci links'):
    for link in links:
        ids = link[1].split('artiId=ART')[1]
        print('kci: ', link[0])
        print(ids)
        # title, id, is this KCI?
        save_pdf(link[0], str(ids), isKCI = True)

def save_blinks(links: 'b link'):
    for link in links:
        title, ids = link[0], link[1]
        print('b: ',title)
        print(ids)
        save_pdf(title, str(ids), isKCI = False)

def get_realpath(keyword: 'search keyword'):
    data = get_link(keyword)
    alinks = []
    blinks = []
    kcilinks = []
    for k, v in data.items():
        # \ / : * ? " < > | -> 파일 이름에 들어갈 수 없는 기호
        k = k.translate({ord('#'):'', ord('\\'):'', ord('/'):'', ord(':'):'', ord('*'):'', ord('?'):'', ord('"'):'', ord('<'):'', ord('>'):'', ord('|'):''})
        link = v[2] # link
        if link.endswith('a'):
            temp = [k, link.rstrip('a')]            
            alinks.append(temp)
        else:
            if 'kci' in link :
                temp = [k, link.rstrip('b')]
                kcilinks.append(temp)
            else:
                link = link.rstrip('b')
                link += '.pdf'
                temp = [k, link]
                blinks.append(temp)    
    save_kci(kcilinks) # kci 저장
    save_blinks(blinks) # blink 저장
    get_a_selenium(alinks) # alink 저장


