import requests
from bs4 import BeautifulSoup

def naver_weather():
    resp= requests.get('https://search.naver.com/search.naver?sm=top_sug.pre&fbm=0&acr=1&acq=skfT&qdt=0&ie=utf8&query=%EB%82%A0%EC%94%A8')
    soup= BeautifulSoup(resp.text, 'html.parser')

    find_address=     '현재 위치: ' + soup.find('span', class_='btn_select').text
    find_currenttemp= '현재 온도: ' + soup.find('span', class_='todaytemp').text
    find_dust=        '현재 미세먼지: ' + soup.find('dl', class_='indicator').find_all('span', class_='num')[0].text
    find_ultra_dust=  '현재 초미세먼지: ' + soup.find('dl', class_='indicator').find_all('span', class_='num')[1].text
    find_ozone=       '현재 오존지수: ' +  soup.find('dl', class_='indicator').find_all('span', class_='num')[2].text

    myList1 = [find_address, find_currenttemp, find_dust, find_ultra_dust, find_ozone]

    return  myList1


def ranking():
    resp1= requests.get('https://www.myprotein.co.kr/nutrition/kr-bestsellers.list')
    soup1= BeautifulSoup(resp1.text, 'html.parser')

    myList2=[] 
    myList2_href=[]
    
    for i in soup1.find_all('h3', class_="athenaProductBlock_productName"):
        myList2.append(i.text)
        myList2_href.append('http://www.myprotein.co.kr' + i.find_parent('a', class_="athenaProductBlock_linkImage")['href'])
    
    return myList2, myList2_href


if __name__ == '__main__':
    print(naver_weather())
    print(ranking())
    
