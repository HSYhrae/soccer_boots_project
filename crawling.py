import pandas as pd
import numpy as np
import re
import requests
from bs4 import BeautifulSoup

# 축구화 특징 데이터 호출
df_f = pd.read_csv('./data/football_boots_feature.csv')

# 축구화 데이터 크롤링
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_main_image(soup):
    img_tag = soup.select_one('.itemDetailPage-main-img img')
    if img_tag:
        img_url = img_tag.get('src')
        return f"https://www.crazy11.co.kr{img_url}" if img_url.startswith('/') else img_url
    return None

def extract_section_value(items, section_name):
    for item in items:
        if item.find('div', class_='mTC leftT') and item.find('div', class_='mTC leftT').text.strip() == section_name:
            values = item.find_all('div', class_='mcie on')
            return ", ".join([value.text.strip() for value in values]) if values else None
    return None

def extract_score(sections, score_name):
    for section in sections:
        if section.find('div', class_='bTC leftT') and section.find('div', class_='bTC leftT').text.strip() == score_name:
            inTB_elements = section.find_all('div', class_='inTB')
            for index, element in enumerate(inTB_elements, start=1):
                if 'on' in element.get('class', []):
                    return index
    return None

def extract_original_price(soup):
    price_span = soup.find("span", class_="itemDetailPage-price txtc-e4 txts-30")
    if price_span:
        original_price_span = price_span.find("span", class_="psale txts-18 txtc-a1")
        if original_price_span:
            return original_price_span.text.strip().replace(" 원", "").replace(",", "")
    return None

def extract_sale_price(soup):
    price_span = soup.find("span", class_="itemDetailPage-price txtc-e4 txts-30")
    if price_span:
        sale_price_text = price_span.contents[0].strip()
        return sale_price_text.replace(" 원", "").replace(",", "")
    return None

def extract_weight(soup):
    weight_sections = soup.find_all("span", class_="itembasic-bg")
    for section in weight_sections:
        title = section.find("span", class_="itembasic-tit")
        weight_text = section.find("span", class_="itembasic-txt")
        if title and weight_text and title.text.strip() == "무게":
            match = re.search(r'(\d+\.?\d*)g', weight_text.text.strip())
            if match:
                return match.group(1) + "g"
    return None

def crazy(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'cp949'
    soup = BeautifulSoup(response.text, "html.parser")

    title_div = soup.find("div", class_="itemDetailPage-main-tit txts-22 txts-fontB txtc-46")
    title = title_div.text.strip() if title_div else "Unknown Title"

    items = soup.find_all('div', class_='mTR')
    upper = extract_section_value(items, '갑피')
    ground = extract_section_value(items, '구장')

    sections = soup.find_all('div', class_='bTR')
    len_score = extract_score(sections, '길이')
    foot_score = extract_score(sections, '발볼')

    original_price = extract_original_price(soup)
    sale_price = extract_sale_price(soup)
    weight = extract_weight(soup)
    image_url = extract_main_image(soup)

    result = {
        'title': title,
        'original_price': original_price,
        'sale_price': sale_price,
        'upper': upper,
        'ground': ground,
        'len_score': len_score,
        'foot_score': foot_score,
        'weight': weight,
        'image_url': image_url,
        'url': url
    }
    return result

# 크롤링할 기본 URL
base_url = "https://www.crazy11.co.kr/shop/shopbrand.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
all_links = []

# 페이지 번호를 1부터 10까지 반복
for page in range(1, 11):
    params = {
        "type": "Y",
        "xcode": "257",
        "sort": "",
        "page": str(page),
    }
    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    for a_tag in soup.select('a.itemInfo'):
        href = a_tag.get('href')
        if href and href.startswith('/shop/shopdetail.html'):
            full_url = "https://www.crazy11.co.kr" + href
            all_links.append(full_url)

data_list = []
for url in all_links:
    try:
        result = crazy(url)
        data_list.append(result)
    except Exception as e:
        print(f"Error: {url}: {e}")

df_b = pd.DataFrame(data_list)

# 데이터 전처리
# NaN 값 제거
if 'len_score' in df_b.columns:
    df_b = df_b.dropna(subset=['len_score'])

# upper 컬럼의 NaN 값을 '인조가죽 + 니트'로 채우기
df_b['upper'] = df_b['upper'].fillna('인조가죽 + 니트')

# 불필요한 컬럼 삭제
df_b = df_b.drop(columns=['Unnamed: 0'], errors='ignore')

# 인덱스 재설정
df_b = df_b.reset_index(drop=True)

# title 컬럼 전처리
df_b['title'] = df_b['title'].str.replace('신발끈|전용쌕|#|수입|/|신발주걱|인솔|UT 니트장갑 증정 EVENT|\.|,0', '', regex=True)
df_b['title'] = df_b['title'].str.replace(r'\[[^\]]+\] ', '', regex=True)
df_b["title"] = df_b["title"].str.replace(r"\s*\(.*?\)", "", regex=True)

# title, original_price 중복 제거
df_b = df_b.drop_duplicates(subset=["title", "original_price"], keep="first")

# 특정 키워드 포함된 행 삭제
df_b = df_b[~df_b["title"].str.contains("트루삭스", na=False)]
df_b = df_b[~df_b["title"].str.contains("우먼스", na=False)]

# weight 컬럼에서 숫자만 추출하고 컬럼명 변경
df_b.rename(columns={'weight': 'weight(g)'}, inplace=True)
df_b['weight(g)'] = df_b['weight(g)'].astype(str).str.extract(r'(\d+)')

# 조건에 따라 'silo' 값 설정
def extract_silo(title):
    split_title = title.split(' ')  # 공백 기준 분리
    if ('더' in split_title or '줌' in split_title):
        return split_title[2]  # 두번째 단어 반환
    elif ('킹' in split_title):
        return ' '.join(split_title[1:3])  # 두번째와 세번째 단어를 합쳐 반환
    elif (split_title[1] == '모렐리아' and split_title[2] == '네오'):
        return ' '.join(split_title[1:3])
    return split_title[1]  # 첫번째 단어만 반환

# 'silo' 컬럼 생성
df_b['silo'] = df_b['title'].apply(extract_silo)