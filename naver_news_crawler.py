
import requests
import os

def naver_news_crawl(query: str):
    # 네이버 오픈API 키를 환경변수 또는 직접 입력
    client_id = os.environ.get("NAVER_CLIENT_ID", "rYr5ZK4qWoMaZrE54Jjp")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET", "BKzU9lcQS2")
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    from datetime import datetime
    today = datetime.now().strftime("%Y.%m.%d")
    params = {
        "query": query,
        "display": 10,
        "sort": "date"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        results = []
        from email.utils import parsedate_to_datetime
        from bs4 import BeautifulSoup
        import re
        for item in data.get("items", []):
            # pubDate 포맷 변환 (Tue, 16 Sep 2025 14:58:00 +0900 → 2025.09.16 14:58)
            raw_pubdate = item.get("pubDate", "")
            formatted_pubdate = ""
            pubdate_only = ""
            # 1차: pubDate 필드 사용
            if raw_pubdate:
                try:
                    dt = parsedate_to_datetime(raw_pubdate)
                    formatted_pubdate = dt.strftime("%Y.%m.%d %H:%M")
                    pubdate_only = dt.strftime("%Y.%m.%d")
                except Exception:
                    formatted_pubdate = raw_pubdate
            # 2차: pubDate가 없으면 실제 기사 링크에서 추출 시도
            if not formatted_pubdate and item.get("link"):
                try:
                    art_res = requests.get(item["link"], timeout=3)
                    soup = BeautifulSoup(art_res.text, "html.parser")
                    # og:article:published_time, og:pubdate, meta[name='date'] 등에서 날짜 추출
                    meta_date = (
                        soup.find("meta", {"property": "article:published_time"}) or
                        soup.find("meta", {"property": "og:pubdate"}) or
                        soup.find("meta", {"name": "date"}) or
                        soup.find("meta", {"property": "og:updated_time"})
                    )
                    date_val = meta_date["content"] if meta_date and meta_date.has_attr("content") else ""
                    # ISO/UTC 포맷 → yyyy.MM.dd HH:mm 변환
                    dt = None
                    if date_val:
                        try:
                            # 2025-08-21T14:09:00-07:00 등 ISO
                            from dateutil import parser as dtparser
                            dt = dtparser.parse(date_val)
                            formatted_pubdate = dt.strftime("%Y.%m.%d %H:%M")
                            pubdate_only = dt.strftime("%Y.%m.%d")
                        except Exception:
                            # yyyy-mm-dd 등 단순 포맷
                            m = re.match(r"(\d{4})[-.](\d{2})[-.](\d{2})", date_val)
                            if m:
                                formatted_pubdate = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
                                pubdate_only = formatted_pubdate
                    # 일부 언론사: <time> 태그 활용
                    if not formatted_pubdate:
                        t = soup.find("time")
                        if t and t.has_attr("datetime"):
                            try:
                                from dateutil import parser as dtparser
                                dt = dtparser.parse(t["datetime"])
                                formatted_pubdate = dt.strftime("%Y.%m.%d %H:%M")
                                pubdate_only = dt.strftime("%Y.%m.%d")
                            except Exception:
                                pass
                except Exception:
                    pass
            # 오늘 날짜와 일치하는 기사만 추가
            if pubdate_only == today:
                results.append({
                    "title": item.get("title", ""),
                    "summary": item.get("description", ""),
                    "link": item.get("link", ""),
                    "press": item.get("originallink", ""),
                    "pubDate": formatted_pubdate  # 기사 등록일시(한국형)
                })
        return results
    except Exception as e:
        print(f"[ERROR] naver_news_crawl (openapi): {e}")
        return []

