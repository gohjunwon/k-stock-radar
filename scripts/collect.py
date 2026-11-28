#!/usr/bin/env python3
"""국내주식 호재 레이더 - 자동 수집 스크립트 (GitHub Actions에서 실행)

  --mode news : 뉴스·관심종목만 (AI 사용 안 함, 장중 10분마다)
  --mode full : 위 + 상장사 목록·실적 갱신 (하루 1번)

AI는 서버에서 쓰지 않습니다. AI 탭은 방문자가 각자 연결한 AI로 브라우저에서 정리합니다.
뉴스·실적·주가는 네이버 증권과 언론사 RSS에서 가져옵니다(키 필요 없음).
"""
import argparse
import datetime as dt
import email.utils
import html
import json
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


VOLATILE = ('updatedAt', 'checked')


def _strip(o):
    if isinstance(o, dict):
        return {k: _strip(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [_strip(v) for v in o]
    return o


def save(name, obj):
    """내용이 그대로면(갱신 시각만 다르면) 파일을 다시 쓰지 않습니다 → 의미 없는 커밋 방지."""
    DATA.mkdir(exist_ok=True)
    old = load(name, None)
    if old is not None and _strip(old) == _strip(obj):
        return False
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding='utf-8')
    return True


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
        r = self.find_pos(title)
        return r[1] if r else None

    def find_pos(self, title):
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
        return best

    def lookup(self, key):
        key = str(key).strip()
        if re.fullmatch(r'\d{6}', key):
            return self.by_code.get(key)
        return self.by_name.get(key)


# ───────────── 호재 판별 (AI 없이 키워드) ─────────────
# 분류별 (어디에 있어도 되는 확실한 표현, 종목명 바로 옆에 있을 때만 인정하는 넓은 표현)
CATEGORIES = [
    ('기술수출', ['기술수출', '기술 수출', '기술이전', '라이선스 아웃', '라이선스 계약'], ['라이선스']),
    ('수주·계약', ['공급계약', '공급 계약', '공사계약', '공사 계약', '수주', '계약 체결', '계약체결', '판매계약'], ['납품']),
    ('임상·허가', ['임상', '품목허가', '허가 획득', 'FDA', '식약처', '판매허가'], []),
    ('실적', ['최대 실적', '최대실적', '어닝 서프라이즈', '어닝서프라이즈', '깜짝 실적', '흑자전환', '흑자 전환', '호실적', '실적 개선', '역대 최대'], []),
    ('주주환원', ['자사주', '소각', '배당 확대', '고배당', '주주환원', '무상증자', '특별배당', '역대급 배당', '배당 증액', '추가 환원'], []),
    ('M&A·투자', ['M&A', '투자 유치', '지분 투자', '공장 증설'], ['인수', '합병', '증설']),
    ('급등·특징주', ['상한가', '신고가'], ['급등', '특징주', '강세', '상승세', '%↑', '% ↑', '上', '들썩']),
    ('정책·수혜', ['정책 지원', '국책과제'], ['수혜', '선정']),
]
# 있으면 무조건 악재로 보는 강한 표현
STRONG_NEG = ['급락', '하한가', '상장폐지', '거래정지', '횡령', '배임', '유상증자', '감자', '폭락', '압수수색', '기소', '불성실',
              '과징금', '리콜', '쇼크', '목표가 하향', '매도 리포트', '무산', '불발', '좌초', '적자전환', '적자 전환', '계약 해지', '임상 실패']
# 종목명 바로 근처에서 부정 뜻으로 쓰였을 때만 악재로 보는 약한 표현
WEAK_NEG = ['하락', '약세', '철회', '해지', '취소', '소송', '적자', '실패', '중단', '반려', '경고', '우려', '손실', '제재', '부진',
            '하향', '공매도', '지연', '관건']
# 약한 악재어 바로 뒤에 오면 부정 뜻이 아님 ("하락장에도 수주", "우려 해소", "적자 축소")
NEG_UNDO = ['에도', '져도', '어도', '아도', '해도', '는데도', '불구', '딛', '뚫', '극복', '해소', '축소', '벗어', '멈', '반등', '완화', '털고', '이겨', '개선', '탈출']
# '우려 속 강세'의 '속'만 인정 ('적자 지속'의 '속'은 아님)
NEG_UNDO_SOK = re.compile(r'^\S{0,2}\s*(?<![지계연후])속(?:\s|에|$)')
# '감자칩' 같은 낱말 속 '감자'는 악재(자본 감소)가 아님
STRONG_NEG_EXCEPT = re.compile(r'감자(?:칩|튀김|탕|빵|전분|깡|밭|농사|값)')
SEGMENT_SPLIT = re.compile(r'\s*(?:…|\.\.\.|;| - |·{2,})\s*')  # 쉼표·'|'는 '종목, 내용' 형태라 나누지 않음
NEAR = 30  # 종목명과 이 글자 수 안에 있어야 '근처'


def _segments(title):
    """제목을 구절로 나누고 (시작 위치, 구절) 목록을 돌려줍니다."""
    out, pos = [], 0
    for m in SEGMENT_SPLIT.finditer(title):
        out.append((pos, title[pos:m.start()]))
        pos = m.end()
    out.append((pos, title[pos:]))
    return out


def _near(title, name_pos, name_len, word):
    """word가 종목명과 같은 구절 안, NEAR 글자 안에 있는지."""
    if name_pos is None:
        return False
    for st, seg in _segments(title):
        if not (st <= name_pos < st + len(seg)):
            continue
        i = seg.find(word)
        while i >= 0:
            a = st + i
            gap = a - (name_pos + name_len) if a >= name_pos else name_pos - (a + len(word))
            if gap <= NEAR:
                return True
            i = seg.find(word, i + 1)
    return False


def _weak_neg_near(title, name_pos, name_len):
    for w in WEAK_NEG:
        i = title.find(w)
        while i >= 0:
            tail = title[i + len(w): i + len(w) + 5]
            undone = any(u in tail for u in NEG_UNDO) or bool(NEG_UNDO_SOK.match(tail)) or title[max(0, i - 3):i].endswith('흑자')
            if not undone and (name_pos is None or _near(title, name_pos, name_len, w)):
                return True
            i = title.find(w, i + 1)
    return False


def judge(title, name=None, name_pos=None):
    """'neg'(악재) / 분류 이름(호재) / None(해당 없음)."""
    title = title or ''
    if name and name_pos is None:
        p = title.find(name)
        name_pos = p if p >= 0 else None
    nlen = len(name or '')
    plain = STRONG_NEG_EXCEPT.sub('', title)
    if any(w in plain for w in STRONG_NEG):
        return 'neg'
    if _weak_neg_near(title, name_pos, nlen):
        return 'neg'
    for cat, strict, broad in CATEGORIES:
        if any(w in title for w in strict):
            return cat
        if any(_near(title, name_pos, nlen, w) for w in broad):
            return cat
    return None


def category_of(title, name=None, name_pos=None):
    j = judge(title, name, name_pos)
    return None if j in (None, 'neg') else j


# ───────────── 뉴스 출처들 ─────────────
RSS_FEEDS = [
    ('한국경제', 'https://www.hankyung.com/feed/finance'),
    ('매일경제', 'https://www.mk.co.kr/rss/50200011/'),
    ('연합뉴스', 'https://www.yna.co.kr/rss/economy.xml'),
    ('이데일리', 'http://rss.edaily.co.kr/edaily_news.xml'),  # 옛 주소 /rss/stock.xml 은 홈페이지로 바뀜
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
    body = r.content.lstrip(b'\xef\xbb\xbf \r\n\t')
    try:
        items = list(ET.fromstring(body).iter('item'))
    except ET.ParseError:  # 형식이 조금 깨진 RSS도 읽도록 <item> 단위로 다시 시도
        items = []
        for chunk in re.findall(rb'<item>.*?</item>', body, re.S):
            try:
                items.append(ET.fromstring(re.sub(rb'&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', b'&amp;', chunk)))
            except ET.ParseError:
                continue
    for it in items:
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
    pool, ok, report = [], [], []
    jobs = [('네이버 주요뉴스', fetch_naver_main)]
    jobs += [(name, (lambda u=u, n=name: fetch_rss(u, n))) for name, u in RSS_FEEDS]
    for q in GOOGLE_QUERIES:
        u = f'https://news.google.com/rss/search?q={requests.utils.quote(q + " when:1d")}&hl=ko&gl=KR&ceid=KR:ko'
        jobs.append((f'구글뉴스:{q}', (lambda u=u: fetch_rss(u))))
    for name, fn in jobs:
        try:
            items = fn()
            pool += items
            # 네이버·언론사 RSS가 0건이거나 가장 최근 기사가 3일 넘게 지났으면 주소가 바뀌었거나 멈춘 것 → 실패로 표시
            stale = None
            if not name.startswith('구글뉴스'):
                ts = [x['t'] for x in items if x.get('t')]
                if not items:
                    stale = '기사 0건 (주소가 바뀌었거나 막힘)'
                elif ts and now() - max(ts) > dt.timedelta(days=3):
                    stale = f"최근 기사가 오래됨 ({max(ts).strftime('%m-%d %H:%M')})"
            if stale:
                log(f'  [출처 멈춤] {name}: {stale}')
                report.append({'name': name, 'count': len(items), 'ok': False, 'error': stale})
                continue
            ok.append(name)
            report.append({'name': name, 'count': len(items), 'ok': True})
        except Exception as e:  # noqa: BLE001
            log(f'  [출처 실패] {name}: {e}')
            report.append({'name': name, 'count': 0, 'ok': False, 'error': str(e)[:160]})
    log('[뉴스 출처]', ', '.join(f"{r['name']}({r['count']})" for r in report))
    return pool, ok, report


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
    pool, sources, report = gather_pool()
    if not pool:  # 모든 출처가 실패하면 이전 결과를 지우지 않고 그대로 둡니다
        log('[오늘의 호재] 모든 출처 실패 — 이전 결과 유지')
        return load('news.json', {}).get('catalysts', []), report
    cutoff = t0 - dt.timedelta(hours=24)
    found = []
    for a in pool:
        t = a['t'] or t0
        if t < cutoff or t > t0 + dt.timedelta(minutes=30):
            continue
        hit = matcher.find_pos(a['title'])
        if not hit:
            continue
        pos, s = hit
        cat = category_of(a['title'], s['n'], pos)
        if not cat:
            continue
        found.append({'ts': t.isoformat(), 'date': t.strftime('%Y-%m-%d'), 'time': t.strftime('%H:%M'),
                      'name': s['n'], 'code': s['c'], 'market': s.get('m', ''), 'sector': s.get('s', '') or '기타',
                      'category': cat, 'title': a['title'], 'desc': a.get('desc', ''), 'press': a['press'], 'link': a['link']})

    # 앞서 모은 것(24시간 이내)도 이어서 보관 — RSS는 최신 몇십 건만 주기 때문
    old = load('news.json', {}).get('catalysts', [])
    for o in old:
        if parse_time(o.get('ts')) and parse_time(o['ts']) >= cutoff and category_of(o.get('title', ''), o.get('name')):
            o['category'] = category_of(o['title'], o.get('name'))  # 규칙이 바뀌어도 다시 판정
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
    return catalysts, report


# ───────────── 2) 관심종목 ─────────────
def run_watch(matcher):
    cfg = load_watchlist()
    prev = {w.get('code'): w for w in load('watch.json', {}).get('stocks', [])}
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
            items = None
        if items is None:  # 실패하면 이전에 받아 둔 뉴스·가격을 그대로 유지
            if s['c'] in prev:
                out.append(prev[s['c']])
            continue
        week = now() - dt.timedelta(days=7)
        news, seen = [], set()
        for a in items:
            k = re.sub(r'[^가-힣A-Za-z0-9]', '', a['title'])[:16]
            if k in seen or (a['t'] and a['t'] < week):
                continue
            seen.add(k)
            j = judge(a['title'], s['n'])
            cat, neg = (j if j != 'neg' else None), j == 'neg'
            news.append({'time': a['t'].strftime('%m-%d %H:%M') if a['t'] else '', 'title': a['title'], 'press': a['press'],
                         'link': a['link'], 'desc': a['desc'], 'tone': 'positive' if cat else ('negative' if neg else 'neutral')})
        price = fetch_price(s['c']) or {k: v for k, v in prev.get(s['c'], {}).items() if k in ('price', 'ratio', 'market')}
        out.append({'name': s['n'], 'code': s['c'], 'sector': s.get('s', ''), **price, 'news': news[:12]})
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


# ───────────── 실행 ─────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['news', 'full'], default='news')
    mode = ap.parse_args().mode
    log(f'== {stamp()} KST · mode={mode} ==')

    stocks = get_stocks(refresh=(mode == 'full'))
    matcher = Matcher(stocks)

    catalysts, report = run_news(matcher)
    run_watch(matcher)

    codes = []
    for c in [*(matcher.lookup(k)['c'] for k in load_watchlist() if matcher.lookup(k)),
              *(c['code'] for c in catalysts[:15])]:
        if c and c not in codes:
            codes.append(c)
    run_earnings(matcher, codes, only_missing=(mode == 'news'))

    write_status(mode, report)
    log('== 완료 ==')


def in_market_window(t):
    """평일 08:00~16:00 KST (10분마다 수집하는 시간대)."""
    return t.weekday() < 5 and 8 * 60 <= t.hour * 60 + t.minute < 16 * 60


def write_status(mode, report):
    """수집 확인 기록. 실패 출처가 바뀌었거나, 마지막 기록이 오래됐을 때만 다시 씁니다
    (장중 30분 · 그 밖 3시간) — 사이트의 '갱신 지연' 판단과 출처별 건수 표시에 씁니다."""
    t = now()
    failed = sorted(r['name'] for r in report if not r['ok'])
    old = load('status.json', {})
    last = parse_time((old.get('checkedAt') or '').replace(' ', 'T') + ':00+09:00') if old.get('checkedAt') else None
    beat = dt.timedelta(minutes=30) if in_market_window(t) else dt.timedelta(hours=3)
    if last and old.get('failed') == failed and old.get('mode') == mode and t - last < beat:
        return
    (DATA / 'status.json').write_text(json.dumps({
        'checkedAt': stamp(), 'updatedAt': stamp(), 'mode': mode, 'failed': failed,
        'fullAt': stamp() if mode == 'full' else old.get('fullAt', ''),  # 아침 전체 갱신(장 시작 전) 확인용
        'sources': report, 'newsUpdatedAt': load('news.json', {}).get('updatedAt', ''),
    }, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    sys.exit(main())
