
# Novi: AI 뉴스 요약/검색 서비스

Novi는 네이버/구글 뉴스 API를 활용해 최신 뉴스를 한 번에 검색하고, AI 기반 요약 및 가독성 높은 카드 UI로 보여주는 오픈소스 프로젝트입니다.

## 주요 기능
- 키워드/프롬프트 기반 뉴스 통합 검색 (네이버/구글)
- 오늘 날짜 뉴스만 필터링, 기사 등록일시 표시
- 뉴스 카드 UI, 더보기, 출처/언론사/기사 바로가기 제공
- HTML 태그 제거, 가독성 개선, 반응형 디자인

## 기술 스택
- 프론트엔드: React + TypeScript + Tailwind CSS
- 백엔드: Python Flask (API 서버)
- 크롤러: 네이버 오픈API, 구글 Custom Search API

## 설치 및 실행
### 1. 프론트엔드
```
npm install
npm start
```
접속: http://localhost:3000

### 2. 백엔드(API 서버)
```
pip install -r requirements.txt
python news_api.py
```
접속: http://localhost:5000

## API 구조
- `/api/search?q=검색어` : 네이버/구글 뉴스 동시 조회 및 통합 결과 반환 (JSON)

## 환경 변수 예시
- NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
- GOOGLE_API_KEY, GOOGLE_CSE_ID

## 폴더 구조
- src/ : React 프론트엔드
- naver_news_crawler.py, google_news_crawler.py : 뉴스 크롤러
- news_api.py : Flask API 서버

## 기여 및 문의
이슈/PR 환영합니다! (by KIM-SOOHYUN1)
