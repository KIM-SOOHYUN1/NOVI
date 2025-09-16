
import React, { useState } from "react";
// HTML 태그 제거 함수
function stripHtml(html: string) {
  const tmp = document.createElement("div");
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || "";
}

interface NewsItem {
  id?: number;
  title: string;
  summary: string;
  source?: string;
  date?: string;
  press?: string; // 언론사
  link?: string; // 기사 URL
  sourceType?: string; // 네이버/구글
  pubDate?: string; // 네이버 기사 등록일시
}

const mockNews: NewsItem[] = [
  {
    id: 1,
    title: "AI Revolutionizes Global News",
    summary: "AI is transforming how news is summarized and delivered worldwide.",
    source: "BBC",
    date: "2025-09-16",
  },
  {
    id: 2,
    title: "한국 AI 뉴스 요약 서비스 급성장",
    summary: "AI 기반 뉴스 요약 서비스가 한국에서 빠르게 성장하고 있습니다.",
    source: "조선일보",
    date: "2025-09-15",
  },
];


function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<NewsItem[]>([]);
  const [visibleCount, setVisibleCount] = useState(5);

  const handleSearch = async () => {
    if (!query.trim()) return;
    const res = await fetch(`http://localhost:5000/api/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    setResults(data);
    setVisibleCount(5);
  };

  const handleShowMore = () => {
    setVisibleCount((prev) => prev + 5);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-2 text-blue-700">Novi 검색</h1>
      <p className="mb-6 text-gray-600">키워드로 뉴스를 검색하세요.</p>
      <div className="flex w-full max-w-xl mb-8">
        <input
          type="text"
          className="flex-1 px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="예: AI, 글로벌 경제, 비트코인..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button
          className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-r-md hover:bg-blue-700 transition"
          onClick={handleSearch}
        >
          검색
        </button>
      </div>
      <div className="w-full max-w-xl">
        {results.length === 0 ? (
          <div className="text-gray-400 text-center">검색 결과가 없습니다.</div>
        ) : (
          <>
            <ul>
              {results.slice(0, visibleCount).map((news, idx) => (
                <li
                  key={news.id || idx}
                  className="mb-6 bg-white rounded-2xl shadow-md hover:shadow-xl border border-gray-200 transition group p-6 flex flex-col gap-2"
                >
                  <div className="flex items-center gap-3 mb-2">
                    {/* 플랫폼 */}
                    {news.sourceType && (
                      <span className={
                        news.sourceType === "네이버"
                          ? "text-xs font-semibold text-green-700 bg-green-100 px-2 py-0.5 rounded"
                          : "text-xs font-semibold text-yellow-700 bg-yellow-100 px-2 py-0.5 rounded"
                      }>
                        {news.sourceType}
                      </span>
                    )}
                    {/* 기사로 이동 버튼 및 등록일시 */}
                    {news.link && (
                      <>
                        <a
                          href={news.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="ml-1 text-xs px-2 py-0.5 rounded bg-blue-100 text-blue-700 font-semibold hover:bg-blue-200 transition border border-blue-200"
                        >
                          기사로 이동
                        </a>
                        {/* 등록일시: pubDate(네이버), date(구글) */}
                        {(news.pubDate || news.date) && (
                          <span className="ml-2 text-xs text-gray-400">
                            {news.pubDate || news.date}
                          </span>
                        )}
                      </>
                    )}
                  </div>
                  <div className="flex items-center gap-2 mb-1">
                    {/* 아이콘 */}
                    <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-blue-100 text-blue-600">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 21H5a2 2 0 01-2-2V7a2 2 0 012-2h4l2-2h4a2 2 0 012 2v12a2 2 0 01-2 2z" /></svg>
                    </span>
                    <span className="font-bold text-xl text-gray-900 group-hover:text-blue-700 transition-colors break-words">
                      {/* URL 패턴이 타이틀에 남아있으면 제거 */}
                      {stripHtml(news.title).replace(/https?:\/\/[\w\-._~:/?#[\]@!$&'()*+,;=%]+/g, "").trim()}
                    </span>
                  </div>
                  <div className="text-gray-700 text-base mb-2 whitespace-pre-line break-words">
                    {stripHtml(news.summary)}
                  </div>
                  {/* 기사 URL(기사 바로가기) 버튼 제거됨 */}
                </li>
              ))}
            </ul>
            {visibleCount < results.length && (
              <div className="flex justify-center my-4">
                <button
                  className="px-6 py-2 bg-gray-200 text-gray-700 rounded hover:bg-blue-100 hover:text-blue-700 transition font-semibold"
                  onClick={handleShowMore}
                >
                  더보기
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;