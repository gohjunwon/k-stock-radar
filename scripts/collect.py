#!/usr/bin/env python3
"""국내주식 호재 레이더 - 자동 수집 스크립트 (GitHub Actions에서 실행)

  --mode news : 뉴스·관심종목만 (AI 사용 안 함, 장중 10분마다)
  --mode full : 위 + 상장사 목록·실적 갱신 + AI(일정·시장일정·추천) 하루 1번

AI(Gemini)는 full 모드에서만, 하루 3번 호출합니다.
뉴스·실적·주가는 네이버 증권과 언론사 RSS에서 가져옵니다(키 필요 없음).
"""
import argparse
import datetime as dt
import email.utils
import html
import json
import os
import re
import sys
import time
from pathlib import Path
from xml.etree import ElementTree as ET

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
KST = dt.timezone(dt.timedelta(hours=9))
UA = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
    'Referer': 'https://m.stock.naver.com/',
}
NAVER = 'https://m.stock.naver.com'


# ───────────── 공통 ─────────────
def now():
    return dt.datetime.now(KST)


def stamp():
    return now().strftime('%Y-%m-%d %H:%M')


def log(*a):
    print(*a, flush=True)


def get(url, timeout=20, tries=2):
    last = None
    for i in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=timeout)
            if r.status_code == 200:
                return r
            last = f'HTTP {r.status_code}'
        except Exception as e:  # noqa: BLE001
            last = str(e)
        time.sleep(1 + i)
    raise RuntimeError(f'{url} -> {last}')


def get_json(url):
    return get(url).json()


def load(name, default):
    p = DATA / name
    if p.exists():
        try:
            return json.loads(p.read_text(encoding='utf-8'))
        except Exception:  # noqa: BLE001
            pass
    return default


def save(name, obj):
    DATA.mkdir(exist_ok=True)
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding='utf-8')


def clean(text):
    text = html.unescape(re.sub(r'<[^>]+>', '', str(text or '')))
    return re.sub(r'\s+', ' ', text).strip()


def num(v):
    s = re.sub(r'[^0-9.\-]', '', str(v or ''))
    try:
        return float(s) if s not in ('', '-', '.') else None
    except ValueError:
        return None


def naver_article(oid, aid):
    return f'https://n.news.naver.com/mnews/article/{oid}/{aid}'


# ───────────── 상장사 목록 (KIND) ─────────────
FALLBACK_STOCKS = [
    ('삼성전자', '005930'), ('SK하이닉스', '000660'), ('NAVER', '035420'), ('카카오', '035720'),
    ('현대차', '005380'), ('기아', '000270'), ('삼성바이오로직스', '207940'), ('셀트리온', '068270'),
    ('한화에어로스페이스', '012450'), ('삼성SDI', '006400'), ('LG에너지솔루션', '373220'),
    ('알테오젠', '196170'), ('휴젤', '145020'), ('두산에너빌리티', '034020'),
]


def update_stocks():
    try:
        from bs4 import BeautifulSoup
        r = get('https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', timeout=40)
        soup = BeautifulSoup(r.content.decode('cp949', 'replace'), 'html.parser')
        rows = soup.find_all('tr')
        head = [c.get_text(strip=True) for c in rows[0].find_all(['th', 'td'])]
        i_name, i_code = head.index('회사명'), head.index('종목코드')
        i_mkt = head.index('시장구분') if '시장구분' in head else None
        i_sec = head.index('업종') if '업종' in head else None
        out = []
        for tr in rows[1:]:
            c = [x.get_text(strip=True) for x in tr.find_all('td')]
            if len(c) <= i_code:
                continue
            code = c[i_code].zfill(6)
            if not re.fullmatch(r'\d{6}', code):
                continue
            out.append({'n': c[i_name], 'c': code,
                        'm': c[i_mkt] if i_mkt is not None else '',
                        's': c[i_sec] if i_sec is not None else ''})
        if len(out) > 1000:
            save('stocks.json', {'updatedAt': stamp(), 'stocks': out})
            log(f'[상장사] {len(out)}개 저장')
            return out
        log('[상장사] 목록이 너무 적어 저장하지 않음', len(out))
    except Exception as e:  # noqa: BLE001
        log('[상장사] 실패:', e)
    return None


def get_stocks(refresh=False):
    if refresh:
        s = update_stocks()
        if s:
            return s
    cached = load('stocks.json', {}).get('stocks')
    if cached:
        return cached
    s = update_stocks()
    return s or [{'n': n, 'c': c, 'm': '', 's': ''} for n, c in FALLBACK_STOCKS]


# ───────────── 기사 제목에서 종목 찾기 ─────────────
TWO_CHAR_OK = {'기아', '효성', '농심', '풍산', '한샘', '대웅', '영풍', '휴젤', '삼양', '한미', '동서', '하림', '빙그레', '오리온'}
PARTICLES = ('은', '는', '이', '가', '을', '를', '의', '에', '와', '과', '도', '만', '로', '측', '株', '으로')


def is_word(ch):
    return bool(re.match(r'[0-9A-Za-z가-힣]', ch))


class Matcher:
    def __init__(self, stocks):
        names = []
        for s in stocks:
            n = s['n'].strip()
            if len(n) < 2 or (len(n) == 2 and n not in TWO_CHAR_OK):
                continue
            names.append((n, s))
        names.sort(key=lambda x: -len(x[0]))
        self.names = names
        self.by_code = {s['c']: s for s in stocks}
        self.by_name = {s['n']: s for s in stocks}

    def find(self, title):
        best = None
        for n, s in self.names:
            start = 0
            while True:
                i = title.find(n, start)
                if i < 0:
                    break
                start = i + 1
                before = title[i - 1] if i > 0 else ' '
                after = title[i + len(n):]
                if is_word(before):
                    continue
                if after and is_word(after[0]) and not after.startswith(PARTICLES):
                    continue
                if best is None or i < best[0]:
                    best = (i, s)
                break
        return best[1] if best else None

    def lookup(self, key):
        key = str(key).strip()
        if re.fullmatch(r'\d{6}', key):
            return self.by_code.get(key)
        return self.by_name.get(key)


# ───────────── 호재 판별 (AI 없이 키워드) ─────────────
CATEGORIES = [
    ('기술수출', ['기술수출', '기술 수출', '기술이전', '라이선스']),
    ('수주·계약', ['공급계약', '공급 계약', '수주', '납품', '계약 체결', '계약체결', '판매계약']),
    ('임상·허가', ['임상', '품목허가', '허가 획득', 'FDA', '승인', '식약처', '판매허가']),
    ('실적', ['최대 실적', '최대실적', '어닝 서프라이즈', '어닝서프라이즈', '깜짝 실적', '흑자전환', '흑자 전환', '호실적', '실적 개선', '역대 최대']),
    ('주주환원', ['자사주', '소각', '배당 확대', '고배당', '주주환원', '무상증자']),
    ('M&A·투자', ['인수', '합병', 'M&A', '투자 유치', '지분 투자', '공장 증설', '증설']),
    ('급등·특징주', ['상한가', '급등', '신고가', '특징주', '강세']),
    ('정책·수혜', ['수혜', '정책 지원', '국책과제', '선정']),
]
NEGATIVE = ['급락', '하락', '약세', '철회', '해지', '취소', '소송', '적자', '불성실', '상장폐지', '거래정지', '감자', '유상증자',
            '횡령', '배임', '실패', '중단', '하한가', '반려', '경고', '우려', '손실', '리콜', '제재', '과징금', '부진', '쇼크',
            '하향', '폭락', '압수수색', '기소', '공매도', '매도 리포트', '목표가 하향']


def category_of(title):
    if any(w in title for w in NEGATIVE):
        return None
    for cat, words in CATEGORIES:
        if any(w in title for w in words):
            return cat
    return None


# ───────────── 뉴스 출처들 ─────────────
RSS_FEEDS = [
    ('한국경제', 'https://www.hankyung.com/feed/finance'),
    ('매일경제', 'https://www.mk.co.kr/rss/50200011/'),
    ('연합뉴스', 'https://www.yna.co.kr/rss/economy.xml'),
    ('이데일리', 'https://www.edaily.co.kr/rss/stock.xml'),
]
GOOGLE_QUERIES = ['공급계약 체결', '수주 계약', '임상 성공', '품목허가', '기술수출', '자사주 소각', '최대 실적', '흑자전환', '상한가 특징주', '신고가 특징주']


def parse_time(s):
    s = str(s or '').strip()
    if not s:
        return None
    if re.fullmatch(r'\d{12}(\d{2})?', s):
        return dt.datetime.strptime(s[:12], '%Y%m%d%H%M').replace(tzinfo=KST)
    try:
        t = email.utils.parsedate_to_datetime(s)
        return (t if t.tzinfo else t.replace(tzinfo=KST)).astimezone(KST)
    except Exception:  # noqa: BLE001
        pass
    try:
        t = dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
        return (t if t.tzinfo else t.replace(tzinfo=KST)).astimezone(KST)
    except Exception:  # noqa: BLE001
        return None


def fetch_rss(url, press=None):
    out = []
    r = get(url)
    root = ET.fromstring(r.content)
    for it in root.iter('item'):
        title = clean(it.findtext('title'))
        link = (it.findtext('link') or '').strip()
        src = it.find('source')
        p = press or (src.text.strip() if src is not None and src.text else '')
        if not press and ' - ' in title:  # 구글 뉴스: "제목 - 언론사"
            title, p2 = title.rsplit(' - ', 1)
            p = p or p2
        t = parse_time(it.findtext('pubDate') or it.findtext('{http://purl.org/dc/elements/1.1/}date'))
        desc = clean(it.findtext('description'))[:160]
        if title and link:
            out.append({'title': title, 'link': link, 'press': p, 't': t, 'desc': desc})
    return out


def fetch_naver_main():
    out = []
    j = get_json(f'{NAVER}/api/news/list?category=mainnews&pageSize=40&page=1')
    for a in j if isinstance(j, list) else []:
        out.append({'title': clean(a.get('tit')), 'link': naver_article(a.get('oid'), a.get('aid')),
                    'press': a.get('ohnm', ''), 't': parse_time(a.get('dt')), 'desc': clean(a.get('subcontent'))[:160]})
    return out


def fetch_naver_category(cat, size=100):
    out = []
    j = get_json(f'{NAVER}/api/news/list?category={cat}&pageSize={size}&page=1')
    for a in j if isinstance(j, list) else []:
        out.append({'title': clean(a.get('tit')), 'link': naver_article(a.get('oid'), a.get('aid')),
                    'press': a.get('ohnm', ''), 't': parse_time(a.get('dt')), 'desc': clean(a.get('subcontent'))[:160]})
    return out


def fetch_stock_news(code, size=20):
    out = []
    j = get_json(f'{NAVER}/api/news/stock/{code}?pageSize={size}&page=1')
    for grp in j if isinstance(j, list) else []:
        for a in grp.get('items', []):
            out.append({'title': clean(a.get('titleFull') or a.get('title')),
                        'link': a.get('mobileNewsUrl') or naver_article(a.get('officeId'), a.get('articleId')),
                        'press': a.get('officeName', ''), 't': parse_time(a.get('datetime')),
                        'desc': clean(a.get('body'))[:160]})
    return out


def fetch_price(code):
    try:
        j = get_json(f'{NAVER}/api/stock/{code}/basic')
        sign = -1 if (j.get('compareToPreviousPrice') or {}).get('name') in ('FALLING', 'LOWER_LIMIT') else 1
        ratio = num(j.get('fluctuationsRatio'))
        return {'price': j.get('closePrice', ''), 'ratio': None if ratio is None else abs(ratio) * sign,
                'market': j.get('stockExchangeName', '')}
    except Exception as e:  # noqa: BLE001
        log('  가격 실패', code, e)
        return {}


def gather_pool():
    """여러 출처에서 최근 기사를 모읍니다. 하나가 실패해도 나머지로 계속."""
    pool, ok = [], []
    jobs = [('네이버 주요뉴스', fetch_naver_main)]
    jobs += [(f'네이버 {c}', (lambda c=c: fetch_naver_category(c))) for c in ('flashnews',)]
    jobs += [(name, (lambda u=u, n=name: fetch_rss(u, n))) for name, u in RSS_FEEDS]
    for q in GOOGLE_QUERIES:
        u = f'https://news.google.com/rss/search?q={requests.utils.quote(q + " when:1d")}&hl=ko&gl=KR&ceid=KR:ko'
        jobs.append((f'구글뉴스:{q}', (lambda u=u: fetch_rss(u))))
    for name, fn in jobs:
        try:
            items = fn()
            pool += items
            ok.append(f'{name}({len(items)})')
        except Exception as e:  # noqa: BLE001
            log(f'  [출처 실패] {name}: {e}')
    log('[뉴스 출처]', ', '.join(ok))
    return pool, ok


# ───────────── 같은 사건 합치기 ─────────────
def bigrams(s):
    s = re.sub(r'[^0-9A-Za-z가-힣]', '', s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


def similar(a, b):
    A, B = bigrams(a), bigrams(b)
    if not A or not B:
        return False
    return len(A & B) / len(A | B) >= 0.4


def merge_catalysts(items):
    merged = []
    for it in sorted(items, key=lambda x: x['ts']):
        t = parse_time(it['ts'])

        def same_event(m):
            if m['code'] != it['code']:
                return False
            if m['title'] == it['title'] or similar(m['title'], it['title']):
                return True
            # 같은 종목·같은 종류의 호재가 3시간 안에 또 나오면 같은 사건의 다른 보도로 봄
            mt = parse_time(m['ts'])
            return m['category'] == it['category'] and mt and t and abs((t - mt).total_seconds()) <= 3 * 3600

        dup = next((m for m in merged if same_event(m)), None)
        if dup:
            if it['press'] and it['press'] not in dup['presses']:
                dup['presses'].append(it['press'])
            if it['link'] not in [l['url'] for l in dup['links']] and len(dup['links']) < 4:
                dup['links'].append({'url': it['link'], 'press': it['press']})
            dup['count'] = len(dup['links'])
        else:
            it = dict(it)
            it['presses'] = [it['press']] if it['press'] else []
            it['links'] = [{'url': it['link'], 'press': it['press']}]
            it['count'] = 1
            merged.append(it)
    return sorted(merged, key=lambda x: x['ts'], reverse=True)


# ───────────── 1) 오늘의 호재 + 시장 주요뉴스 ─────────────
def run_news(matcher):
    t0 = now()
    pool, sources = gather_pool()
    cutoff = t0 - dt.timedelta(hours=24)
    found = []
    for a in pool:
        t = a['t'] or t0
        if t < cutoff or t > t0 + dt.timedelta(minutes=30):
            continue
        cat = category_of(a['title'])
        if not cat:
            continue
        s = matcher.find(a['title'])
        if not s:
            continue
        found.append({'ts': t.isoformat(), 'date': t.strftime('%Y-%m-%d'), 'time': t.strftime('%H:%M'),
                      'name': s['n'], 'code': s['c'], 'market': s.get('m', ''), 'sector': s.get('s', '') or '기타',
                      'category': cat, 'title': a['title'], 'desc': a.get('desc', ''), 'press': a['press'], 'link': a['link']})

    # 앞서 모은 것(24시간 이내)도 이어서 보관 — RSS는 최신 몇십 건만 주기 때문
    old = load('news.json', {}).get('catalysts', [])
    for o in old:
        if parse_time(o.get('ts')) and parse_time(o['ts']) >= cutoff:
            for l in o.get('links', []):
                found.append({**{k: o[k] for k in ('ts', 'date', 'time', 'name', 'code', 'market', 'sector', 'category', 'title', 'desc')},
                              'press': l.get('press', ''), 'link': l['url']})
    catalysts = merge_catalysts(found)[:80]

    headlines, seen = [], set()
    for a in sorted([p for p in pool if p.get('t')], key=lambda x: x['t'], reverse=True):
        key = re.sub(r'[^가-힣A-Za-z0-9]', '', a['title'])[:16]
        if key in seen or a['t'] < cutoff:
            continue
        seen.add(key)
        if a['link'].startswith('https://n.news.naver.com') or a['press'] in ('한국경제', '매일경제', '연합뉴스', '이데일리'):
            headlines.append({'time': a['t'].strftime('%m-%d %H:%M'), 'title': a['title'], 'press': a['press'], 'link': a['link']})
        if len(headlines) >= 25:
            break

    save('news.json', {'updatedAt': stamp(), 'sources': sources, 'catalysts': catalysts, 'headlines': headlines})
    log(f'[오늘의 호재] {len(catalysts)}건 / 시장 뉴스 {len(headlines)}건')
    return catalysts


# ───────────── 2) 관심종목 ─────────────
def run_watch(matcher):
    cfg = load_watchlist()
    out = []
    for key in cfg:
        s = matcher.lookup(key)
        if not s:
            log('  [관심종목] 찾을 수 없음:', key)
            continue
        try:
            items = fetch_stock_news(s['c'], 20)
        except Exception as e:  # noqa: BLE001
            log('  [관심종목] 뉴스 실패', s['n'], e)
            items = []
        week = now() - dt.timedelta(days=7)
        news, seen = [], set()
        for a in items:
            k = re.sub(r'[^가-힣A-Za-z0-9]', '', a['title'])[:16]
            if k in seen or (a['t'] and a['t'] < week):
                continue
            seen.add(k)
            cat = category_of(a['title'])
            neg = any(w in a['title'] for w in NEGATIVE)
            news.append({'time': a['t'].strftime('%m-%d %H:%M') if a['t'] else '', 'title': a['title'], 'press': a['press'],
                         'link': a['link'], 'desc': a['desc'], 'tone': 'positive' if cat else ('negative' if neg else 'neutral')})
        out.append({'name': s['n'], 'code': s['c'], 'sector': s.get('s', ''), **fetch_price(s['c']), 'news': news[:12]})
        time.sleep(0.3)
    save('watch.json', {'updatedAt': stamp(), 'stocks': out})
    log(f'[관심종목] {len(out)}개')


def load_watchlist():
    p = ROOT / 'watchlist.json'
    try:
        j = json.loads(p.read_text(encoding='utf-8'))
        return [str(x) for x in (j.get('stocks') if isinstance(j, dict) else j)]
    except Exception:  # noqa: BLE001
        return ['삼성전자', 'SK하이닉스', 'NAVER']


# ───────────── 3) 실적 (네이버 증권, AI 없음) ─────────────
def fetch_earnings(s):
    j = get_json(f'{NAVER}/api/stock/{s["c"]}/finance/quarter')
    info = j.get('financeInfo') or {}
    cols = info.get('trTitleList') or []
    rows = {r.get('title', '').strip(): r.get('columns', {}) for r in info.get('rowList') or []}

    def row(*names):
        for n in names:
            if n in rows:
                return rows[n]
        return {}

    actual = [c for c in cols if c.get('isConsensus') != 'Y']
    cons = [c for c in cols if c.get('isConsensus') == 'Y']
    rev, op = row('매출액', '영업수익'), row('영업이익')
    margin, debt = row('영업이익률'), row('부채비율')
    val = lambda r, c: num((r.get(c['key']) or {}).get('value'))  # noqa: E731
    last3 = actual[-3:]
    item = {
        'name': s['n'], 'code': s['c'], 'sector': s.get('s', ''),
        'quarters': [c['title'].rstrip('.') for c in last3],
        'revenue': [val(rev, c) for c in last3],
        'opProfit': [val(op, c) for c in last3],
        'opMargin': [val(margin, c) for c in last3],
        'debtRatio': [val(debt, c) for c in last3],
    }
    if item['opMargin'] and all(v is None for v in item['opMargin']):
        item['opMargin'] = [round(o / r * 100, 1) if o is not None and r else None for o, r in zip(item['opProfit'], item['revenue'])]
    if cons:
        c = cons[0]
        item['next'] = {'quarter': c['title'].rstrip('.'), 'revenue': val(rev, c), 'opProfit': val(op, c)}
    if len(actual) >= 5:  # 최근 분기 vs 1년 전 같은 분기
        a, b = val(op, actual[-1]), val(op, actual[-5])
        if a is not None and b:
            item['yoy'] = round((a - b) / abs(b) * 100, 1)
    return item


def run_earnings(matcher, codes, only_missing=False):
    cache = {e['code']: e for e in load('earnings.json', {}).get('items', [])}
    todo = [c for c in codes if not (only_missing and c in cache)]
    for code in todo[:25]:
        s = matcher.by_code.get(code)
        if not s:
            continue
        try:
            cache[code] = {**fetch_earnings(s), 'checked': stamp()}
        except Exception as e:  # noqa: BLE001
            log('  [실적] 실패', s['n'], e)
        time.sleep(0.3)
    keep = [cache[c] for c in codes if c in cache]  # 지금 관심 대상 순서대로
    save('earnings.json', {'updatedAt': stamp(), 'items': keep[:30]})
    log(f'[실적] {len(keep)}개 (새로 조회 {len(todo[:25])}개)')


# ───────────── 4) AI (하루 1번) ─────────────
MODELS = ['gemini-flash-latest', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']


def gemini(prompt):
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('NO_KEY')
    last = None
    for m in MODELS:
        r = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent',
                          headers={'x-goog-api-key': key, 'Content-Type': 'application/json'},
                          json={'contents': [{'role': 'user', 'parts': [{'text': prompt}]}],
                                'tools': [{'google_search': {}}], 'generationConfig': {'temperature': 0.2}},
                          timeout=180)
        if r.status_code == 404:
            last = f'{m} 없음'
            continue
        if r.status_code != 200:
            raise RuntimeError(f'Gemini {r.status_code}: {r.text[:200]}')
        cand = (r.json().get('candidates') or [{}])[0]
        text = ''.join(p.get('text', '') for p in (cand.get('content') or {}).get('parts', []))
        meta = cand.get('groundingMetadata') or {}
        chunks = [{'title': (c.get('web') or {}).get('title', '출처'), 'uri': (c.get('web') or {}).get('uri', '')} for c in meta.get('groundingChunks', [])]
        return text, chunks, meta.get('groundingSupports', [])
    raise RuntimeError(last or 'Gemini 모델 없음')


def parse_json_array(text):
    t = re.sub(r'```(json)?', '', text).strip()
    a, b = t.find('['), t.rfind(']')
    if a < 0 or b <= a:
        raise ValueError('JSON 배열 없음')
    body = t[a:b + 1]
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return json.loads(re.sub(r',\s*([\]}])', r'\1', body))


def link_sources(item, fields, chunks, supports):
    keys = [str(item.get(f) or '').strip()[:12] for f in fields]
    keys = [k for k in keys if len(k) >= 2]
    idx = []
    for s in supports:
        t = (s.get('segment') or {}).get('text', '')
        if any(k in t for k in keys):
            idx += s.get('groundingChunkIndices', [])
    seen, out = set(), []
    for i in idx:
        if i < len(chunks) and chunks[i]['uri'] and chunks[i]['uri'] not in seen:
            seen.add(chunks[i]['uri'])
            out.append(chunks[i])
    return out[:3]


def run_ai(matcher, catalysts):
    today = now().strftime('%Y-%m-%d')
    until = (now() + dt.timedelta(days=31)).strftime('%Y-%m-%d')
    prev = load('daily.json', {})
    result = {'updatedAt': stamp(), 'status': 'ok', 'error': '',
              'events': prev.get('events', []), 'market': prev.get('market', []), 'picks': prev.get('picks', [])}

    def fix_code(it):
        s = matcher.lookup(it.get('code') or '') or matcher.lookup(it.get('name') or '')
        if s:
            it['code'], it['name'] = s['c'], s['n']
        else:
            it['code'] = ''
        return it

    tasks = {
        'events': (f"""오늘: {today} (KST)
Google 검색으로 {today} ~ {until} 사이 예정된 국내 상장사 주요 일정 8~12건을 찾아 주세요.
분야: 임상(결과 발표), FDA·식약처 허가, 회사(신제품·주총·상장·배당 등), 학회, 실적 발표, M&A
검색에서 확인한 일정만 쓰고, 날짜가 확정이 아니면 "exact": false.
설명 없이 JSON 배열만 출력:
[{{"date":"YYYY-MM-DD","exact":true,"category":"임상|FDA|회사|학회|실적|M&A","name":"종목명","code":"6자리","title":"일정 제목","detail":"한 문장"}}]""", ['title', 'name']),
        'market': (f"""오늘: {today} (KST)
Google 검색으로 {today} ~ {until} 사이 국내 증시에 영향을 줄 경제지표·정세 일정 8~12건을 찾아 주세요.
(FOMC, 미국 CPI·고용, 한국은행 금리 결정, 수출입 통계, 옵션 만기일, 주요 정상회담·선거 등). 시간은 한국시간, 모르면 빈 문자열.
설명 없이 JSON 배열만 출력:
[{{"date":"YYYY-MM-DD","timeKst":"HH:MM","region":"미국|한국|글로벌","title":"일정명","impact":"높음|중간","krEffect":"국내 증시 영향 한두 문장"}}]""", ['title']),
    }
    base = '\n'.join(f"- {c['name']}: {c['title']}" for c in catalysts[:12]) or '(없음 — 오늘 국내 증시 주도 업종을 검색해 판단)'
    tasks['picks'] = (f"""현재: {stamp()} (KST)
아래는 네이버·언론 RSS에서 모은 오늘의 국내 호재 뉴스입니다. Google 검색으로 사실·주가·수급을 확인해 관심 가질 만한 종목 3~5개를 골라 주세요.
위험 요인도 꼭 적으세요. 가격을 확인 못 하면 "확인 필요".
{base}
설명 없이 JSON 배열만 출력:
[{{"name":"종목명","code":"6자리","strength":"강|중|약","catalyst":"핵심 호재 한 줄","reasoning":"근거 2문장","risk":"위험 요인 한 줄","entry":"진입 참고","target":"목표가","stop":"손절 기준"}}]""", ['name', 'catalyst'])

    for name, (prompt, fields) in tasks.items():
        try:
            text, chunks, supports = gemini(prompt)
            items = []
            for it in parse_json_array(text):
                if not isinstance(it, dict):
                    continue
                it = fix_code(it)
                it['links'] = link_sources(it, fields, chunks, supports)
                items.append(it)
            if name in ('events', 'market'):
                items = sorted([i for i in items if re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(i.get('date', ''))) and i['date'] >= today],
                               key=lambda i: (i['date'], i.get('timeKst') or ''))
            result[name] = items
            log(f'[AI {name}] {len(items)}건')
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            result['status'] = 'no_key' if msg == 'NO_KEY' else 'error'
            result['error'] = '' if msg == 'NO_KEY' else msg[:300]
            log(f'[AI {name}] 건너뜀:', msg[:200])
            if msg == 'NO_KEY':
                break
    # 지난 일정은 정리
    result['events'] = [e for e in result['events'] if e.get('date', '') >= today]
    result['market'] = [m for m in result['market'] if m.get('date', '') >= today]
    save('daily.json', result)
    return result


# ───────────── 실행 ─────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['news', 'full'], default='news')
    mode = ap.parse_args().mode
    log(f'== {stamp()} KST · mode={mode} ==')

    stocks = get_stocks(refresh=(mode == 'full'))
    matcher = Matcher(stocks)

    catalysts = run_news(matcher)
    run_watch(matcher)

    if mode == 'full':
        daily = run_ai(matcher, catalysts)
    else:
        daily = load('daily.json', {})

    codes = []
    for c in [*(matcher.lookup(k)['c'] for k in load_watchlist() if matcher.lookup(k)),
              *(p.get('code') for p in daily.get('picks', [])),
              *(e.get('code') for e in daily.get('events', []) if e.get('category') == '실적'),
              *(c['code'] for c in catalysts[:15])]:
        if c and c not in codes:
            codes.append(c)
    run_earnings(matcher, codes, only_missing=(mode == 'news'))

    save('status.json', {'updatedAt': stamp(), 'mode': mode})
    log('== 완료 ==')


if __name__ == '__main__':
    sys.exit(main())
