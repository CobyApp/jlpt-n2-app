# scripts/

N2 컨텐츠 크롤링/처리 스크립트.

## 의존성

```bash
pip install requests beautifulsoup4 lxml
```

## 실행 순서

1. **`scrape-n2.py`** — nihonez.com 에서 reading 문제 + listening URL 수집 →
   `assets/data/exams/n2_*.json` 생성
2. **음원 다운로드** — listening 의 `audio_url` 을 `assets/audio/n2_*/` 로 받음
3. **transcribe** (옵션) — Whisper 로 listening script 생성
4. **한국어 해설 작성** — 사람이 직접 또는 LLM 으로

## 현재 상태

`scrape-n2.py` 는 URL 목록과 스켈레톤만 작성. 실제 nihonez N2 페이지의 DOM
selector 를 분석해서 `parse_exam` 의 TODO 부분을 채워야 함. N1 의
`/Users/doyoung_kim/Documents/Git/jlpt/scripts/` 에 있는 패턴 참고.

## index.json 갱신

크롤링된 exam JSON 이 추가되면 `assets/data/index.json` 도 다시 빌드해야 함
(exam 메타데이터 + category_totals). N1 의 `sync-data.mjs` 패턴 사용.
