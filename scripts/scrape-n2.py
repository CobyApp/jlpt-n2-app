"""nihonez.com 에서 JLPT N2 모의고사 11회차 크롤링.

URL 패턴:
  https://nihonez.com/jlpt-test/jlpt-n2-past-test-{month-year}-real-exam/

생성물:
  assets/data/exams/n2_<id>.json
  assets/audio/n2_<id>/<mondai-type>.mp3

이 스크립트는 N1 의 scrape-listening.py 와 같은 패턴.
실제 실행 전에 다음 의존성 설치 필요:
  pip install requests beautifulsoup4 lxml
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUT_DATA = Path(__file__).resolve().parent.parent / "assets" / "data" / "exams"
OUT_AUDIO = Path(__file__).resolve().parent.parent / "assets" / "audio"
OUT_DATA.mkdir(parents=True, exist_ok=True)
OUT_AUDIO.mkdir(parents=True, exist_ok=True)

# nihonez 의 N2 페이지 슬러그들 (실제 사이트에서 확인 후 채워야 함)
EXAM_URLS = [
    # (id, url)
    ("n2_2025-07", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-july-2025-real-exam/"),
    ("n2_2024-12", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-december-2024-real-exam/"),
    ("n2_2024-07", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-july-2024-real-exam/"),
    ("n2_2023-12", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-december-2023-real-exam/"),
    ("n2_2023-07", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-july-2023-real-exam/"),
    ("n2_2022-12", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-december-2022-real-exam/"),
    ("n2_2022-07", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-july-2022-real-exam/"),
    ("n2_2021-12", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-december-2021-real-exam/"),
    ("n2_2021-07", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-july-2021-real-exam/"),
    ("n2_2020-12", "https://nihonez.com/jlpt-test/jlpt-n2-past-test-december-2020-real-exam/"),
    ("n2_2018-vol2", "https://nihonez.com/jlpt-test/jlpt-n2-mock-test-vol-2/"),
]


def fetch_html(url):
    r = requests.get(url, timeout=30, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    r.raise_for_status()
    return r.text


def parse_exam(html, exam_id, source_url):
    """페이지 HTML 에서 reading questions + passages + listening 추출.

    NOTE: 실제 nihonez DOM 구조에 맞춰 채워야 함. N1 의 scrape 패턴 참고:
    - 어휘/문법/독해 questions: .question-wrap 같은 클래스
    - 청해: admin-ajax 로 별도 호출 (q_id 별 정답)
    - 음원: <audio> 태그의 src

    이 스크립트는 outline 만 — 실제 selector 채워야 함.
    """
    soup = BeautifulSoup(html, "lxml")
    # TODO: 실제 selector 분석 후 채움
    return {
        "test_id": exam_id,
        "title": f"JLPT N2 Mock Test — {exam_id}",
        "source_url": source_url,
        "scraped_at": "",
        "passages": {},
        "questions": [],
        "listening": None,  # 추후 채움
    }


def main():
    for exam_id, url in EXAM_URLS:
        out = OUT_DATA / f"{exam_id}.json"
        if out.exists():
            sys.stderr.write(f"skip {exam_id} (already exists)\n")
            continue
        sys.stderr.write(f"fetch {url}\n")
        try:
            html = fetch_html(url)
        except Exception as e:
            sys.stderr.write(f"  failed: {e}\n")
            continue
        data = parse_exam(html, exam_id, url)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        sys.stderr.write(f"  wrote {out}\n")


if __name__ == "__main__":
    main()
