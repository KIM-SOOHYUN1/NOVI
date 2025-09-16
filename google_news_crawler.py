import requests
import os

def google_news_crawl(query: str):
    # Google Custom Search API 키와 엔진 ID 필요
    api_key = os.environ.get("GOOGLE_API_KEY", "AIzaSyDkXPZCaHVefljWub5bScYcbtdaHBpmK2o")
    cx = os.environ.get("GOOGLE_CSE_ID", "36403c973aa654d05")
    url = "https://www.googleapis.com/customsearch/v1"
    from datetime import datetime
    today = datetime.now().strftime("%Y.%m.%d")
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": 10,
        "gl": "kr",
        "hl": "ko",
        "dateRestrict": "d1",  # 오늘만
        "sort": "date:D:S"     # 최신순
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        results = []
        from dateutil import parser as dtparser
        from bs4 import BeautifulSoup
        import re
        import pytz
        KST = pytz.timezone('Asia/Seoul')
        today_only = datetime.now().strftime("%Y.%m.%d")
        for item in data.get("items", []):
            pagemap = item.get("pagemap", {})
            metatags = pagemap.get("metatags", [{}])[0]
            press = (
                item.get("displayLink") or
                metatags.get("publisher") or
                metatags.get("site_name") or
                metatags.get("og:site_name") or
                ""
            )
            press_url = None
            if metatags.get("og:url"):
                press_url = metatags.get("og:url")
            elif item.get("displayLink"):
                press_url = f"https://{item.get('displayLink')}"
            else:
                press_url = ""
            # 날짜 변환
            raw_date = metatags.get("article:published_time", "")
            formatted_date = ""
            if raw_date:
                try:
                    dt = dtparser.parse(raw_date)
                    # UTC → KST 변환
                    if dt.tzinfo:
                        dt = dt.astimezone(KST)
                    else:
                        dt = KST.localize(dt)
                    formatted_date = dt.strftime("%Y.%m.%d %H:%M")
                except Exception:
                    formatted_date = raw_date
            # date가 없으면 실제 기사 링크에서 추출 시도
            if not formatted_date and item.get("link"):
                try:
                    art_res = requests.get(item["link"], timeout=3)
                    soup = BeautifulSoup(art_res.text, "html.parser")
                    meta_date = (
                        soup.find("meta", {"property": "article:published_time"}) or
                        soup.find("meta", {"property": "og:pubdate"}) or
                        soup.find("meta", {"name": "date"}) or
                        soup.find("meta", {"property": "og:updated_time"})
                    )
                    date_val = meta_date["content"] if meta_date and meta_date.has_attr("content") else ""
                    dt = None
                    if date_val:
                        try:
                            dt = dtparser.parse(date_val)
                            if dt.tzinfo:
                                dt = dt.astimezone(KST)
                            else:
                                dt = KST.localize(dt)
                            formatted_date = dt.strftime("%Y.%m.%d %H:%M")
                        except Exception:
                            m = re.match(r"(\d{4})[-.](\d{2})[-.](\d{2})", date_val)
                            if m:
                                formatted_date = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
                    if not formatted_date:
                        t = soup.find("time")
                        if t and t.has_attr("datetime"):
                            try:
                                dt = dtparser.parse(t["datetime"])
                                if dt.tzinfo:
                                    dt = dt.astimezone(KST)
                                else:
                                    dt = KST.localize(dt)
                                formatted_date = dt.strftime("%Y.%m.%d %H:%M")
                            except Exception:
                                pass
                except Exception:
                    pass
            # 오늘 날짜와 일치하는 기사만 추가 (날짜가 없으면 오늘로 간주)
            date_only = ""
            if formatted_date:
                date_only = formatted_date.split(" ")[0]
            else:
                date_only = today_only
            if date_only == today_only:
                results.append({
                    "title": item.get("title", ""),
                    "summary": item.get("snippet", ""),
                    "link": item.get("link", ""),
                    "press": press,
                    "press_url": press_url,
                    "date": formatted_date
                })
        return results
    except Exception as e:
        print(f"[ERROR] google_news_crawl (api): {e}")
        return []
