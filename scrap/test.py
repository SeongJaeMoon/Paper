# # from requests import Request, Session
# import requests
# from bs4 import BeautifulSoup as bs
# from time import sleep
# from time import time

# COOKIE = {
#     '_ga':'GA1.2.1497042209.1536590508', 
#     'LastDownCtNo':'a0ebd33868c49b24ffe0bdc3ef48d419', 
#     'JSESSIONID':'AG4bZM5OJCf4wsf4Om2TJwtDpcIZM974y1r2KdTJkZwGp7pi0BurGB2cTMy83kvy.risswas1_servlet_engine1',
#     '_gid':'GA1.2.1744150057.1537054265',
#     'TodayView':'be54d9b8bc7cdb09_a0ebd33868c49b24ffe0bdc3ef48d419_%ED%8C%8C%EC%9D%B4%EC%8D%AC+%EC%96%B8%EC%96%B4%EB%A5%BC+%EC%9D%B4.+.+.,be54d9b8bc7cdb09_a0ebd33868c49b24ffe0bdc3ef48d419_%ED%8C%8C%EC%9D%B4%EC%8D%AC+%EC%96%B8%EC%96%B4%EB%A5%BC+%EC%9D%B4%EC%9A%A9%ED%95%9C...',
#     '__atuvc':'41%7C37%2C1%7C38', 
#     'wcs_bt':'2e819ec0169a:1537056639'
# }

# HEADER = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
# }

# def links():
#     # s = Session()
#     URL = 'http://www.riss.kr/search/download/Downloading.do?loading_mat_type=be54d9b8bc7cdb09&loading_seq_code=dcfe1838ca1bc295&loading_univCode=dcfe1838ca1bc295&loading_fulltext_kind=a8cb3aaead67ab5b&loading_url=f89318728d65c0b80cde5e983be0935e7eecc17e357729e91461824817c3326a90d3d8a76e879f08765344beaadae45a34ac1eea4400c5ef87ed727aa82efb6a'
#     '''
#     http://www.riss.kr/search/download/Downloading.do?loading_mat_type=be54d9b8bc7cdb09&loading_seq_code=dcfe1838ca1bc295&loading_univCode=dcfe1838ca1bc295&loading_fulltext_kind=a8cb3aaead67ab5b&loading_url=f89318728d65c0b80cde5e983be0935e7eecc17e357729e91461824817c3326a90d3d8a76e879f08765344beaadae45a34ac1eea4400c5ef87ed727aa82efb6a
#     http://www.riss.kr/search/download/Downloading.do?loading_mat_type=be54d9b8bc7cdb09&loading_seq_code=dcfe1838ca1bc295&loading_univCode=dcfe1838ca1bc295&loading_fulltext_kind=a8cb3aaead67ab5b&loading_url=f89318728d65c0b80cde5e983be0935e7eecc17e357729e91461824817c3326a90d3d8a76e879f08765344beaadae45a34ac1eea4400c5ef87ed727aa82efb6a
#     http://www.riss.kr/search/download/Downloading.do?loading_mat_type=be54d9b8bc7cdb09&loading_seq_code=4d4f2fcd1b9ec83a&loading_univCode=4d4f2fcd1b9ec83a&loading_fulltext_kind=a8cb3aaead67ab5b&loading_url=f89318728d65c0b80cde5e983be0935ee42d7d3c4a59bb3764a4bc3c775846911e72b21776dba131ecffcaa5434b52c617d3e4409a370ad2be04aa3bc7d3a04549b69143cf3190d8bd28808c2e1d3e9f
#     http://www.riss.kr/search/download/Downloading.do?loading_mat_type=be54d9b8bc7cdb09&loading_seq_code=4d4f2fcd1b9ec83a&loading_univCode=4d4f2fcd1b9ec83a&loading_fulltext_kind=a8cb3aaead67ab5b&loading_url=f89318728d65c0b80cde5e983be0935ee42d7d3c4a59bb3764a4bc3c775846911e72b21776dba131ecffcaa5434b52c617d3e4409a370ad2be04aa3bc7d3a04549b69143cf3190d8ea01fd25d654a478
#     '''
#     req = requests.get(URL, headers = HEADER, cookies = COOKIE, verify = False, stream = True)
#     if req.status_code == 200:
#         soup = bs(req.text, 'html.parser')
#         div = soup.find('div', attrs={'class':'fulltext_btn'})
#         if div is None:
#             for i in range(3):
#                 req = requests.get(URL, headers = HEADER, cookies = COOKIE, verify = False, stream = True)    
#                 soup = bs(req.text, 'html.parser')
#                 div = soup.find('div', attrs={'class':'fulltext_btn'})
#                 if div is not None:
#                     link = div.find('a')
#                     link = link.get('href')
#                     return link
#                     # print(i, div.find('a'))
#         else:
#             link = div.find('a')
#             link = link.get('href')
#             return link


# def test():
#     public = '/public_resource/pdf/'
#     temp = links()
#     s = requests.Session()
#     link = s.get(temp, headers = HEADER, cookies = COOKIE ,verify = False)
#     new_url = temp.split('kr')[0]
#     new_url += 'kr'
#     filename = str(link.text)
#     filename = filename.split('"fileRealName" value="')[1]
#     filename = filename.split('.pdf')[0]
#     ret_link = new_url + public + filename + '.pdf'
#     print(ret_link)
#     gets = s.get(ret_link, headers = HEADER, cookies = COOKIE, verify = False)
    
def test():    
    test = '안ㄴ#안ㄴ\\안ㄴ\\안ㄴ/안ㄴ:안ㄴ*안ㄴ?안ㄴ"안ㄴ<안ㄴ>안ㄴ|안ㄴ'

    oldchar = '#\\/:*?"<>|'
    newchar = ''
    # {ord(x): y for x, y in zip(oldchar, newchar)
    test = test.translate({ord('#'):'', ord('\\'):'', ord('/'):'', ord(':'):'', ord('*'):'', ord('?'):'', ord('"'):'', ord('<'):'', ord('>'):'', ord('|'):''})
    print(test)