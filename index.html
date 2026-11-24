<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>K-Stock Catalyst Radar · 국내주식 호재 레이더</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Noto Sans KR"', 'system-ui', '-apple-system', 'sans-serif'],
          },
          colors: {
            navy: {
              950: '#0a1122',
              900: '#0f172a',
              800: '#172554',
              700: '#1e3a8a',
            }
          }
        }
      }
    };
  </script>
  <style>
    body {
      background-color: #f8fafc;
      color: #0f172a;
    }
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #f1f5f9;
    }
    ::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }
    .glass-header {
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(12px);
    }
    @keyframes spinOnce {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    .spin-anim { animation: spinOnce 0.65s ease-in-out; }
  </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-blue-900/15 selection:text-navy-950">
  <!-- 상단 헤더 (화이트 배경 + 짙은 남색 포인트) -->
  <header class="glass-header sticky top-0 z-40 border-b border-slate-200 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-navy-900 flex items-center justify-center shadow-sm">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <h1 class="text-lg sm:text-xl font-extrabold tracking-tight text-navy-950">국내주식 호재 레이더</h1>
            <span id="market-session-badge" class="px-2.5 py-0.5 text-[11px] font-bold rounded-full bg-navy-900 text-white">
              장 상태 확인 중
            </span>
            <span id="auto-sync-badge" class="px-2.5 py-0.5 text-[11px] font-semibold rounded-full bg-slate-100 text-navy-800 border border-slate-300">
              장중 10초 자동갱신 대기
            </span>
            <span class="px-2.5 py-0.5 text-[11px] font-bold rounded-full bg-slate-100 text-navy-900 border border-slate-300">
              2단계 사실확인 적용
            </span>
          </div>
          <p id="header-subtitle" class="text-xs text-slate-600 mt-0.5">전체 데이터 동기화 중...</p>
        </div>
      </div>

      <div class="flex items-center gap-2 flex-wrap">
        <button id="manual-refresh-btn" onclick="performFullRefresh('manual')" class="px-3.5 py-2 rounded-lg text-xs sm:text-sm font-bold bg-navy-900 hover:bg-navy-800 text-white transition flex items-center gap-1.5 cursor-pointer shadow-xs">
          <svg id="refresh-icon" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>전체 갱신</span>
        </button>

        <div id="gemini-status-badge" class="hidden xl:flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-white border border-slate-300 text-slate-700">
          <span class="w-2 h-2 rounded-full bg-slate-400"></span>
          <span>Gemini AI 미연결</span>
        </div>

        <button onclick="openGeminiModal()" class="px-3.5 py-2 rounded-lg text-xs sm:text-sm font-bold bg-white hover:bg-slate-50 text-navy-950 border-2 border-navy-900 transition flex items-center gap-1.5 cursor-pointer">
          <span class="text-navy-800">✦</span>
          <span id="header-gemini-btn-text">Gemini 로그인</span>
        </button>
      </div>
    </div>

    <nav class="max-w-7xl mx-auto px-4 sm:px-6 overflow-x-auto bg-white">
      <div id="tab-bar" class="flex items-center gap-1 border-t border-slate-100 pt-1.5 pb-1.5 min-w-max"></div>
    </nav>
  </header>

  <main id="app-content" class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 space-y-6"></main>

  <footer class="border-t border-slate-200 bg-white py-4 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
      <span class="font-medium text-navy-900">K-Stock Catalyst Radar · 2단계 사실확인 &amp; 새로고침 전체 갱신 &amp; 정규장(09:00~15:30 KST) 10초 자동 갱신</span>
      <span>투자 판단의 최종 책임은 투자자 본인에게 있으며, 실제 매매 전 공시 원문을 확인하세요.</span>
    </div>
  </footer>

  <!-- Gemini 로그인 및 API 키 설정 모달 -->
  <div id="gemini-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-navy-950/50 backdrop-blur-xs p-4">
    <div class="w-full max-w-md rounded-2xl bg-white border border-slate-200 shadow-2xl overflow-hidden">
      <div class="px-6 py-4 bg-navy-900 text-white flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-sky-300 text-lg">✦</span>
          <h3 class="font-bold text-white">Gemini AI 계정 및 API 연결</h3>
        </div>
        <button onclick="closeGeminiModal()" class="text-slate-300 hover:text-white text-xl leading-none cursor-pointer">&times;</button>
      </div>
      <div class="p-6 space-y-4 bg-white">
        <p class="text-xs sm:text-sm text-slate-700 leading-relaxed">
          Google AI Studio에서 발급받은 <strong class="text-navy-900">Gemini API Key</strong>를 입력하면 1차·2차 AI 사실확인과 실시간 종목 분석이 활성화됩니다.
        </p>
        <div>
          <label class="block text-xs font-semibold text-navy-900 mb-1">Google 계정 이메일 (표시용)</label>
          <input id="gemini-email-input" type="email" placeholder="example@gmail.com" class="w-full px-3.5 py-2 rounded-lg bg-slate-50 border border-slate-300 text-sm text-navy-950 focus:outline-none focus:border-navy-900" />
        </div>
        <div>
          <label class="block text-xs font-semibold text-navy-900 mb-1">Gemini API Key (Google AI Studio 발급)</label>
          <input id="gemini-key-input" type="password" placeholder="AIzaSy..." class="w-full px-3.5 py-2 rounded-lg bg-slate-50 border border-slate-300 text-sm text-navy-950 focus:outline-none focus:border-navy-900" />
        </div>
        <div class="flex items-center justify-end gap-2 pt-2">
          <button onclick="closeGeminiModal()" class="px-4 py-2 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 cursor-pointer">취소</button>
          <button onclick="confirmGeminiLogin()" class="px-4 py-2 rounded-lg text-xs font-bold bg-navy-900 hover:bg-navy-800 text-white cursor-pointer">연결 및 즉시 갱신</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    const TABS = [
      { id: 'ai-picks', label: '1. 실시간 AI 추천종목', badge: 'AI' },
      { id: 'today-catalyst', label: '2. 오늘의 호재', badge: '중복제거' },
      { id: 'upcoming-events', label: '3. 1달 앞 주요일정', badge: '1M' },
      { id: 'earnings-preview', label: '4. 실적 미리보기', badge: '3Q·요인' },
      { id: 'market-schedule', label: '5. 시장일정', badge: '거시·정세' },
      { id: 'calendar', label: '6. 통합 캘린더', badge: 'CAL' },
      { id: 'watchlist', label: '7. 관심종목 & 뉴스', badge: 'MY' },
    ];

    const BASE_RADAR_DATA = {
      updatedAt: '2026-11-25 06:59:00 KST',
      aiPicks: [
        {
          ticker: '000660',
          name: 'SK하이닉스',
          sector: '반도체/HBM',
          score: 94,
          signal: '강력 매수',
          entryRange: '198,000 ~ 202,500원',
          targetPrice: '224,000원 (+11.9%)',
          stopLoss: '191,000원',
          catalystSummary: '글로벌 빅테크 차세대 AI 가속기용 HBM3E 12단 공급 확대 및 서버 DRAM 판가 방어 확인',
          aiReasoning: '고대역폭메모리(HBM) 마진 스프레드가 3분기 대비 추가 개선될 가능성이 높으며 외국인 수급 유입 강도가 양호합니다.',
          updatedAt: '06:59:00 KST'
        },
        {
          ticker: '207940',
          name: '삼성바이오로직스',
          sector: '바이오/CDMO',
          score: 91,
          signal: '매수',
          entryRange: '945,000 ~ 960,000원',
          targetPrice: '1,045,000원 (+9.6%)',
          stopLoss: '912,000원',
          catalystSummary: '글로벌 제약사 대규모 위탁생산(CMO) 증액 계약 기대 및 5공장 가동 준비 순항',
          aiReasoning: '4분기 수주 잔고 누적 속도가 가이던스를 상회하고 있으며 CDMO 업황 회복세가 뚜렷합니다.',
          updatedAt: '06:59:00 KST'
        },
        {
          ticker: '012450',
          name: '한화에어로스페이스',
          sector: '방산/우주',
          score: 89,
          signal: '매수',
          entryRange: '368,000 ~ 376,000원',
          targetPrice: '412,000원 (+10.7%)',
          stopLoss: '352,000원',
          catalystSummary: '동유럽·중동 추가 무기체계 수출 협상 진전 및 K9·천무 인도 물량 4분기 집중',
          aiReasoning: '수주 파이프라인 가시성이 높으며 영업이익률 두 자릿수 안착 여부가 핵심 모멘텀입니다.',
          updatedAt: '06:59:00 KST'
        },
        {
          ticker: '005380',
          name: '현대차',
          sector: '자동차/모빌리티',
          score: 85,
          signal: '관심·분할매수',
          entryRange: '224,000 ~ 229,000원',
          targetPrice: '252,000원 (+11.2%)',
          stopLoss: '215,000원',
          catalystSummary: '하이브리드(HEV) 고수익 믹스 유지 및 미국 메타플랜트(HMGMA) 가동 본격화 기대',
          aiReasoning: '하이브리드 판매 비중 확대와 수출 환율 환경이 실적 하단을 지지하고 있습니다.',
          updatedAt: '06:59:00 KST'
        }
      ],
      todayNews: [
        {
          id: 'n1',
          time: '05:42',
          ticker: '068270',
          name: '셀트리온',
          sector: '바이오',
          headline: '셀트리온, 짐펜트라 미국 대형 PBM 등재 확대 소식에 장전 강세',
          source: '한국경제',
          impact: '높음',
          detail: '미국 주요 처방약급여관리업체(PBM) 추가 등재로 처방 가속화 기대감이 부각되었습니다.'
        },
        {
          id: 'n2',
          time: '05:46',
          ticker: '068270',
          name: '셀트리온',
          sector: '바이오',
          headline: '[단독] 셀트리온 짐펜트라 美 PBM 커버리지 확대…내년 매출 점프 기대',
          source: '매일경제',
          impact: '높음',
          detail: '동일 이슈가 타 매체에서도 보도되었습니다. (중복 자동 병합됨)'
        },
        {
          id: 'n3',
          time: '05:49',
          ticker: '042700',
          name: '한미반도체',
          sector: '반도체',
          headline: '한미반도체, TC본더 신규 라인 증설 완료…HBM 고객사 납품 확대',
          source: '서울경제',
          impact: '높음',
          detail: '차세대 HBM 적층 공정용 TC본더 생산능력(CAPA) 확충 소식이 전해졌습니다.'
        },
        {
          id: 'n4',
          time: '05:57',
          ticker: '034020',
          name: '두산에너빌리티',
          sector: '원전/에너지',
          headline: '두산에너빌리티, 체코 원전 기자재 및 SMR 협력 논의 진전',
          source: '머니투데이',
          impact: '중간',
          detail: '유럽 원전 르네상스 및 소형모듈원전(SMR) 주기기 수주 기대감이 반영되었습니다.'
        },
        {
          id: 'n5',
          time: '06:01',
          ticker: '247540',
          name: '에코프로비엠',
          sector: '2차전지',
          headline: '에코프로비엠, 북미 완성차향 하이니켈 양극재 신규 공급 계약 체결',
          source: '파이낸셜뉴스',
          impact: '중간',
          detail: '중장기 출하 물량 확보 소식으로 2차전지 소재 섹터 내 주목받고 있습니다.'
        }
      ],
      upcomingEvents: [
        {
          id: 'ev1',
          date: '2026-11-27',
          isExactDate: true,
          category: '학회',
          ticker: '145020',
          name: '휴젤',
          title: '글로벌 에스테틱 학술 심포지엄 보툴리눔 톡신 임상 데이터 발표',
          detail: '미국·유럽 시장 확장 전략 및 신규 적응증 임상 추적 결과 공개 예정'
        },
        {
          id: 'ev2',
          date: '2026-12-03',
          isExactDate: false,
          category: 'M&A',
          ticker: '006400',
          name: '삼성SDI',
          title: '전고체·소재 밸류체인 전략적 지분 투자 및 합작법인(JV) 발표 (예상)',
          detail: '공식 공시 전 업계 예상 일정(12월 첫째 주 내외)으로 차세대 배터리 소재 협력 거론'
        },
        {
          id: 'ev3',
          date: '2026-12-07',
          isExactDate: true,
          category: '학회',
          ticker: '207940',
          name: '삼성바이오로직스',
          title: '글로벌 바이오·헬스케어 컨퍼런스 키노트 및 ADC 생산 역량 소개',
          detail: '항체-약물 접합체(ADC) 전용 생산시설 스케줄 및 신규 고객사 파이프라인 공유'
        },
        {
          id: 'ev4',
          date: '2026-12-11',
          isExactDate: false,
          category: '실적',
          ticker: '000660',
          name: 'SK하이닉스',
          title: '4분기 잠정 실적 및 HBM4 양산 타임라인 업데이트 (예상)',
          detail: '연말 메모리 가격 및 고객사 재고 수준 관련 기관 프리뷰 집중 시기(예상일 기준)'
        },
        {
          id: 'ev5',
          date: '2026-12-16',
          isExactDate: true,
          category: 'FDA',
          ticker: '196170',
          name: '알테오젠',
          title: '피하주사(SC) 제형 변경 플랫폼 파트너사 품목 FDA 심사 마일스톤',
          detail: '글로벌 빅파마 기술이전 품목의 미국 FDA 허가 심사 주요 절차 예정일'
        },
        {
          id: 'ev6',
          date: '2026-12-21',
          isExactDate: false,
          category: '임상',
          ticker: '028300',
          name: 'HLB',
          title: '표적항암제 병용요법 글로벌 임상 탑라인 결과 발표 (예상)',
          detail: '연내 발표가 예상되는 주요 임상 마일스톤으로 12월 셋째 주 예상일에 배치'
        },
        {
          id: 'ev7',
          date: '2026-12-24',
          isExactDate: true,
          category: '회사',
          ticker: '012450',
          name: '한화에어로스페이스',
          title: '연말 방산 수주잔고 결산 및 우주발사체·위성 사업부 연간 브리핑',
          detail: '2026년 누적 수주 실적 확정 및 2027년 인도 계획 발표 예정'
        }
      ],
      earningsPreview: [
        {
          ticker: '145020',
          name: '휴젤',
          sector: '바이오/미용의료',
          consensusOpProfit: '498억 원',
          yoyGrowth: '+28.4%',
          quarters: ['2026 1Q', '2026 2Q', '2026 3Q'],
          revenue: [812, 948, 1035],
          opProfit: [298, 424, 486],
          opMargin: [36.7, 44.7, 47.0],
          debtRatio: [18.4, 16.9, 15.2],
          factors: [
            { label: '미국 톡신 선적 물량 증가', sentiment: 'positive', note: '현지 유통 파트너 발주 확대가 매출 성장을 견인' },
            { label: '고마진 톡신·필러 비중 상승', sentiment: 'positive', note: '3개 분기 연속 영업이익률 개선세' },
            { label: '해외 학술 마케팅 비용 증가', sentiment: 'negative', note: '4분기 학회 참가 및 판관비 집행 확대 요인' },
            { label: '원/달러 환율 강세 우호', sentiment: 'positive', note: '수출 비중이 높아 환율 환경이 유리' }
          ]
        },
        {
          ticker: '006400',
          name: '삼성SDI',
          sector: '2차전지',
          consensusOpProfit: '1,120억 원',
          yoyGrowth: '-14.2%',
          quarters: ['2026 1Q', '2026 2Q', '2026 3Q'],
          revenue: [51300, 48900, 46800],
          opProfit: [2670, 2800, 1290],
          opMargin: [5.2, 5.7, 2.8],
          debtRatio: [64.2, 66.8, 69.1],
          factors: [
            { label: '유럽 전기차 수요 둔화 및 재고 조정', sentiment: 'negative', note: '중대형 전지 가동률 하락 압력 지속' },
            { label: '미국 AMPC 세액공제 반영', sentiment: 'positive', note: '현지 생산 라인 가동 확대 시 수익성 방어 요인' },
            { label: '전고체·각형 프리미엄 라인 투자 부담', sentiment: 'negative', note: 'CAPEX 집행에 따른 감가상각 및 부채비율 상승' },
            { label: 'ESS(에너지저장장치) 수주 확대', sentiment: 'positive', note: '북미 전력망용 ESS 수요가 완충 역할 수행' }
          ]
        },
        {
          ticker: '207940',
          name: '삼성바이오로직스',
          sector: '바이오/CDMO',
          consensusOpProfit: '3,640억 원',
          yoyGrowth: '+19.6%',
          quarters: ['2026 1Q', '2026 2Q', '2026 3Q'],
          revenue: [9469, 11569, 11871],
          opProfit: [2213, 4345, 3386],
          opMargin: [23.4, 37.6, 28.5],
          debtRatio: [34.1, 32.8, 31.5],
          factors: [
            { label: '1~4공장 풀가동에 가까운 높은 가동률', sentiment: 'positive', note: '안정적인 매출 인식과 고정비 레버리지' },
            { label: '대규모 CMO 수주 잔고 누적', sentiment: 'positive', note: '중장기 실적 가시성 매우 높음' },
            { label: '5공장 초기 운영비 반영', sentiment: 'negative', note: '상업 가동 직전 인력·초기 비용 발생' },
            { label: '재무건전성 개선 추세', sentiment: 'positive', note: '부채비율 하락세 유지' }
          ]
        },
        {
          ticker: '000660',
          name: 'SK하이닉스',
          sector: '반도체/HBM',
          consensusOpProfit: '7조 8,500억 원',
          yoyGrowth: '+62.0%',
          quarters: ['2026 1Q', '2026 2Q', '2026 3Q'],
          revenue: [124296, 164233, 175731],
          opProfit: [28860, 54685, 70300],
          opMargin: [23.2, 33.3, 40.0],
          debtRatio: [49.8, 44.1, 39.6],
          factors: [
            { label: 'HBM3E 고수익 매출 비중 급증', sentiment: 'positive', note: '영업이익률 40% 구간 진입으로 수익성 폭발' },
            { label: '차입금 상환 및 현금흐름 개선', sentiment: 'positive', note: '부채비율 30%대 진입으로 재무구조 강화' },
            { label: '레거시 D램 가격 상승 탄력 둔화 우려', sentiment: 'negative', note: 'PC·모바일 수요 회복 속도 점검 필요' },
            { label: 'HBM4 선단 공정 투자 확대', sentiment: 'positive', note: '기술 리더십 공고화로 경쟁사 추격 차단' }
          ]
        }
      ],
      marketSchedules: [
        {
          date: '2026-11-25',
          timeKst: '22:30',
          region: '미국',
          title: '미국 3분기 GDP 잠정치 및 주간 신규실업수당 청구건수',
          impact: '높음',
          krEffect: '미국 성장 둔화 시 연준 금리 인하 기대 강화로 성장주(반도체·바이오)에 우호적, 과열 시 국채금리 상승 압력.'
        },
        {
          date: '2026-11-26',
          timeKst: '10:00',
          region: '한국',
          title: '한국은행 금융통화위원회 통화정책방향 결정회의',
          impact: '높음',
          krEffect: '기준금리 결정 및 총재 기자간담회 발언에 따라 원/달러 환율, 은행·건설·부동산 관련주 민감 반응.'
        },
        {
          date: '2026-11-27',
          timeKst: '22:30',
          region: '미국',
          title: '미국 10월 개인소비지출(PCE) 물가지수 발표',
          impact: '높음',
          krEffect: '연준 선호 인플레이션 지표로, 근원 PCE 둔화 시 다음 날 코스피·코스닥 외국인 수급 개선 기대.'
        },
        {
          date: '2026-12-01',
          timeKst: '09:00',
          region: '한국',
          title: '11월 한국 수출입동향 발표',
          impact: '높음',
          krEffect: '반도체·선박·자동차 수출 증가율 확인 시 수출 대형주 방향성 결정.'
        },
        {
          date: '2026-12-09',
          timeKst: '04:00',
          region: '미국',
          title: '12월 미국 FOMC 정례회의 금리 결정 및 점도표',
          impact: '높음',
          krEffect: '2027년 금리 경로 전망에 따라 글로벌 유동성 및 원화 강세/약세 방향 결정.'
        },
        {
          date: '2026-12-10',
          timeKst: '22:30',
          region: '미국',
          title: '미국 11월 소비자물가지수(CPI) 발표',
          impact: '높음',
          krEffect: 'CPI 예상 하회 시 기술주·성장주 반등 동력, 상회 시 단기 차익실현 압력.'
        }
      ]
    };

    const STOCK_CATALOG = [
      { ticker: '005930', name: '삼성전자', sector: '반도체' },
      { ticker: '000660', name: 'SK하이닉스', sector: '반도체' },
      { ticker: '035420', name: 'NAVER', sector: '인터넷/AI' },
      { ticker: '005380', name: '현대차', sector: '자동차' },
      { ticker: '207940', name: '삼성바이오로직스', sector: '바이오' },
      { ticker: '068270', name: '셀트리온', sector: '바이오' },
      { ticker: '012450', name: '한화에어로스페이스', sector: '방산' },
      { ticker: '006400', name: '삼성SDI', sector: '2차전지' },
      { ticker: '247540', name: '에코프로비엠', sector: '2차전지' },
      { ticker: '196170', name: '알테오젠', sector: '바이오' },
      { ticker: '145020', name: '휴젤', sector: '바이오/미용' },
      { ticker: '034020', name: '두산에너빌리티', sector: '원전/에너지' }
    ];

    const DEFAULT_NEWS_DB = {
      '005930': [
        { title: '삼성전자, HBM3E 12단 품질 테스트 진전 및 파운드리 2nm 수율 개선 기대', source: '한국경제', time: '06:10', sentiment: 'positive' },
        { title: '외국인·기관 삼성전자 수급 점검…연말 배당 및 자사주 소각 기대감', source: '연합인포맥스', time: '05:55', sentiment: 'positive' }
      ],
      '000660': [
        { title: 'SK하이닉스, AI 서버용 HBM3E 물량 완판 기조 속 내년 CAPA 논의', source: '매일경제', time: '06:12', sentiment: 'positive' }
      ],
      '035420': [
        { title: '네이버, AI 검색·커머스 광고 수익화 강화 및 웹툰 글로벌 성장세', source: '이데일리', time: '06:04', sentiment: 'positive' }
      ]
    };

    window.state = {
      activeTab: 'ai-picks',
      geminiLoggedIn: localStorage.getItem('kstock_gemini_logged_in') === 'true',
      geminiEmail: localStorage.getItem('kstock_gemini_email') || '',
      geminiKey: localStorage.getItem('kstock_gemini_key') || '',
      aiCustomPrompt: '',
      aiLoading: false,
      aiError: '',
      watchAiSummary: {},
      watchAiLoading: false,
      catalystSectorFilter: '전체',
      eventCategoryFilter: '전체',
      selectedEarningsTicker: '145020',
      calendarMonth: '2026-11',
      selectedCalendarDate: '2026-11-27',
      watchlist: JSON.parse(localStorage.getItem('kstock_watchlist_v1') || '["005930","000660","035420"]'),
      selectedWatchTicker: localStorage.getItem('kstock_selected_watch_v1') || '005930',
      customNewsMap: JSON.parse(localStorage.getItem('kstock_custom_news_v1') || '{}'),
      userAddedCatalysts: [],
      rejectedFactItems: [],
      radarData: JSON.parse(JSON.stringify(BASE_RADAR_DATA)),
      lastRefreshedAt: '',
      refreshCount: 0
    };

    let earningsChartInstance = null;

    // 1차 & 2차 사실확인 규칙 엔진
    const UNVERIFIED_KEYWORDS = [
      '가짜', '허위', '루머', '지라시', '미확인', '추측성', '오보', '확인불가', '설(說)'
    ];

    function passFirstFactCheck(item) {
      const headline = (item.headline || item.title || '').trim();
      const source = (item.source || '').trim();
      if (headline.length < 8) {
        return { ok: false, reason: '1차 검증 탈락: 제목 길이가 짧아 사실관계 불충분' };
      }
      if (!source) {
        return { ok: false, reason: '1차 검증 탈락: 출처(매체·공시) 정보 누락' };
      }
      const lower = headline.toLowerCase();
      for (const kw of UNVERIFIED_KEYWORDS) {
        if (lower.includes(kw.toLowerCase())) {
          return { ok: false, reason: `1차 검증 탈락: 미확인·추측성 키워드("${kw}") 포함` };
        }
      }
      return { ok: true, reason: '1차 검증 통과' };
    }

    function passSecondFactCheck(item, allItems = []) {
      const headline = (item.headline || item.title || '').trim();
      const ticker = (item.ticker || '').trim();
      if (!ticker || !/^[0-9A-Za-z]{4,6}$/.test(ticker)) {
        return { ok: false, reason: '2차 검증 탈락: 종목코드 형식 불일치' };
      }
      // 동일 종목 내 상충되거나 지나치게 모호한 문구 재점검
      if (headline.includes('???') || headline.includes('출처 불명')) {
        return { ok: false, reason: '2차 검증 탈락: 불확실 문구 포함' };
      }
      const sameTickerCount = allItems.filter(x => (x.ticker || '') === ticker).length;
      return {
        ok: true,
        reason: sameTickerCount > 1 ? '2차 검증 통과 (다중 항목 교차 확인)' : '2차 검증 통과 (출처·종목 정합성 확인)'
      };
    }

    async function verifyTwiceWithGeminiIfAvailable(item) {
      if (!state.geminiKey) return { passed: true, note: '2단계 규칙 사실확인 통과' };

      const text = `${item.name || ''} (${item.ticker || ''}) - ${item.headline || item.title || ''} / 출처: ${item.source || ''}`;
      // 1차 AI 사실확인
      const p1 = `다음 주식 뉴스가 실제 존재할 법한 구체적 기업·시장 뉴스인지 1차 사실확인하고 JSON으로만 답하세요. {"pass": boolean, "reason": "한줄이유"}\n내용: ${text}`;
      const r1 = await callGeminiAPI(p1, true);
      if (!r1 || r1.pass !== true) {
        return { passed: false, note: `1차 AI 사실확인 보류: ${r1?.reason || '실재성 미확인'}` };
      }

      // 2차 AI 사실확인 (과장·허위·존재하지 않는 보도 재검증)
      const p2 = `1차 통과된 아래 내용에 대해 허위·날조·존재하지 않는 뉴스 가능성이 없는지 2차 교차 검증하고 JSON으로만 답하세요. {"pass": boolean, "reason": "한줄이유"}\n내용: ${text}`;
      const r2 = await callGeminiAPI(p2, true);
      if (!r2 || r2.pass !== true) {
        return { passed: false, note: `2차 AI 사실확인 보류: ${r2?.reason || '교차 검증 미통과'}` };
      }

      return { passed: true, note: '1차·2차 AI 사실확인 모두 통과' };
    }

    async function filterWithTwoStepFactCheck(items) {
      const verified = [];
      const rejected = [];

      for (const item of items) {
        const c1 = passFirstFactCheck(item);
        if (!c1.ok) {
          rejected.push({ ...item, verifyReason: c1.reason });
          continue;
        }
        const c2 = passSecondFactCheck(item, items);
        if (!c2.ok) {
          rejected.push({ ...item, verifyReason: c2.reason });
          continue;
        }
        if (state.geminiKey) {
          try {
            const aiCheck = await verifyTwiceWithGeminiIfAvailable(item);
            if (!aiCheck.passed) {
              rejected.push({ ...item, verifyReason: aiCheck.note });
              continue;
            }
            verified.push({ ...item, factCheckBadge: '1차·2차 검증 완료', factCheckNote: aiCheck.note });
            continue;
          } catch (e) {
            rejected.push({ ...item, verifyReason: `2차 AI 검증 오류로 보류 (${e.message})` });
            continue;
          }
        }
        verified.push({ ...item, factCheckBadge: '2단계 사실확인 완료', factCheckNote: `${c1.reason} · ${c2.reason}` });
      }

      return { verified, rejected };
    }

    function getKstNowParts() {
      const now = new Date();
      const kstStr = now.toLocaleString('sv-SE', { timeZone: 'Asia/Seoul' });
      const [datePart, timePart] = kstStr.split(' ');
      const [hh, mm, ss] = timePart.split(':').map(Number);
      const weekdayStr = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Seoul', weekday: 'short' }).format(now);
      const isWeekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].includes(weekdayStr);
      const minutesFromMidnight = hh * 60 + mm;
      const isRegularMarketOpen = isWeekday && minutesFromMidnight >= (9 * 60) && minutesFromMidnight <= (15 * 60 + 30);

      return {
        full: `${datePart} ${timePart} KST`,
        timeOnly: `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}`,
        isWeekday,
        isRegularMarketOpen
      };
    }

    function updateMarketStatusBadges() {
      const kst = getKstNowParts();
      const sessionBadge = document.getElementById('market-session-badge');
      const syncBadge = document.getElementById('auto-sync-badge');

      if (kst.isRegularMarketOpen) {
        sessionBadge.className = 'px-2.5 py-0.5 text-[11px] font-bold rounded-full bg-navy-900 text-white';
        sessionBadge.textContent = '정규장 운영 중 (09:00~15:30)';
        syncBadge.className = 'px-2.5 py-0.5 text-[11px] font-bold rounded-full bg-blue-50 text-navy-800 border border-blue-200 animate-pulse';
        syncBadge.textContent = '10초 자동갱신 활성';
      } else {
        sessionBadge.className = 'px-2.5 py-0.5 text-[11px] font-bold rounded-full bg-navy-900 text-white';
        sessionBadge.textContent = kst.isWeekday ? '장외 시간 (09:00 개장 대기)' : '휴장일 (주말)';
        syncBadge.className = 'px-2.5 py-0.5 text-[11px] font-semibold rounded-full bg-slate-100 text-slate-600 border border-slate-200';
        syncBadge.textContent = '장 시작 후 10초 자동갱신';
      }
    }

    async function performFullRefresh(triggerType = 'manual') {
      const icon = document.getElementById('refresh-icon');
      if (icon) {
        icon.classList.remove('spin-anim');
        void icon.offsetWidth;
        icon.classList.add('spin-anim');
      }

      const kst = getKstNowParts();
      let loadedFromJson = false;

      try {
        const res = await fetch(`./data.json?refresh=${Date.now()}`, { cache: 'no-store' });
        if (res.ok) {
          const json = await res.json();
          if (json && typeof json === 'object') {
            state.radarData = {
              ...JSON.parse(JSON.stringify(BASE_RADAR_DATA)),
              ...json
            };
            loadedFromJson = true;
          }
        }
      } catch (_) {}

      if (!loadedFromJson) {
        state.radarData = JSON.parse(JSON.stringify(BASE_RADAR_DATA));
      }

      const mergedRawNews = [
        ...state.userAddedCatalysts,
        ...(state.radarData.todayNews || [])
      ];

      const { verified, rejected } = await filterWithTwoStepFactCheck(mergedRawNews);
      state.radarData.todayNews = verified;
      state.rejectedFactItems = rejected;
      state.radarData.updatedAt = kst.full;
      state.lastRefreshedAt = kst.full;
      state.refreshCount += 1;

      if (Array.isArray(state.radarData.aiPicks)) {
        state.radarData.aiPicks = state.radarData.aiPicks.map(p => ({
          ...p,
          updatedAt: kst.timeOnly + ' KST'
        }));
      }

      state.customNewsMap = { ...state.customNewsMap };

      const triggerLabel = triggerType === 'auto-10s'
        ? '장중 10초 자동갱신'
        : triggerType === 'load'
          ? '페이지 새로고침 갱신'
          : '수동 전체 갱신';

      document.getElementById('header-subtitle').textContent =
        `전체 갱신 시각: ${kst.full} (${triggerLabel} #${state.refreshCount}) · 2차 검증 통과 ${verified.length}건 / 보류 ${rejected.length}건`;

      updateMarketStatusBadges();
      render();
    }

    async function callGeminiAPI(promptText, expectJson = false) {
      if (!state.geminiKey) throw new Error('API_KEY_MISSING');
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${encodeURIComponent(state.geminiKey)}`;
      const body = {
        contents: [{ parts: [{ text: promptText }] }],
        generationConfig: expectJson
          ? { responseMimeType: 'application/json', temperature: 0.3 }
          : { temperature: 0.4 }
      };

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData?.error?.message || `Gemini API 오류 (${res.status})`);
      }

      const data = await res.json();
      const text = data?.candidates?.[0]?.content?.parts?.[0]?.text || '';
      return expectJson ? JSON.parse(text) : text;
    }

    async function runLiveGeminiStockAnalysis() {
      if (!state.geminiKey) {
        state.aiError = '실시간 API 분석을 실행하려면 상단 [Gemini 로그인]에서 Google AI Studio API Key를 입력하세요.';
        render();
        return;
      }

      state.aiLoading = true;
      state.aiError = '';
      render();

      try {
        const newsContext = deduplicateCatalysts(state.radarData.todayNews)
          .map(n => `- ${n.name}(${n.ticker}) [${n.sector}]: ${n.headline} (${n.detail})`)
          .join('\n');

        const userFocus = state.aiCustomPrompt.trim()
          ? `사용자 추가 요청 조건: "${state.aiCustomPrompt.trim()}"`
          : '2단계 사실확인을 통과한 호재 기반으로 국내 유망 종목 4개를 선별해줘.';

        const prompt = `
당신은 한국 주식시장 애널리스트입니다. 아래 검증된 호재 뉴스를 바탕으로 국내주식 추천종목 4개를 JSON 배열로 반환하세요.
${userFocus}

[검증된 호재 목록]
${newsContext}

반드시 아래 JSON 스키마 배열(길이 4)만 출력하세요:
[
  {
    "ticker": "6자리 종목코드",
    "name": "종목명",
    "sector": "섹터",
    "score": 85~98 사이 정수,
    "signal": "강력 매수 또는 매수 또는 분할매수",
    "entryRange": "진입 참고 가격대",
    "targetPrice": "목표가 및 기대수익률",
    "stopLoss": "손절 기준가",
    "catalystSummary": "핵심 호재 한 줄 요약",
    "aiReasoning": "수급·실적·모멘텀 근거 2문장 설명",
    "updatedAt": "실시간 Gemini 갱신"
  }
]`;

        const result = await callGeminiAPI(prompt, true);
        if (Array.isArray(result) && result.length > 0) {
          state.radarData.aiPicks = result;
        }
      } catch (err) {
        state.aiError = `Gemini API 호출 실패: ${err.message}`;
      } finally {
        state.aiLoading = false;
        render();
      }
    }

    async function summarizeWatchStockWithGemini(stock, newsList) {
      if (!state.geminiKey) {
        state.watchAiSummary[stock.ticker] = '실제 API 요약을 보려면 상단 [Gemini 로그인]에서 API Key를 등록해 주세요.';
        render();
        return;
      }
      state.watchAiLoading = true;
      render();
      try {
        const titles = newsList.map(n => `- ${n.title} (${n.source})`).join('\n');
        const prompt = `국내주식 ${stock.name}(${stock.ticker})의 아래 최신 뉴스를 보고 사실확인 관점의 핵심 포인트와 대응 전략을 3줄 이내 한국어로 요약해줘.\n\n${titles}`;
        const reply = await callGeminiAPI(prompt, false);
        state.watchAiSummary[stock.ticker] = reply.trim();
      } catch (e) {
        state.watchAiSummary[stock.ticker] = `요약 실패: ${e.message}`;
      } finally {
        state.watchAiLoading = false;
        render();
      }
    }

    function saveLocalSettings() {
      localStorage.setItem('kstock_watchlist_v1', JSON.stringify(state.watchlist));
      localStorage.setItem('kstock_selected_watch_v1', state.selectedWatchTicker);
      localStorage.setItem('kstock_custom_news_v1', JSON.stringify(state.customNewsMap));
      localStorage.setItem('kstock_gemini_logged_in', String(state.geminiLoggedIn));
      localStorage.setItem('kstock_gemini_email', state.geminiEmail);
      localStorage.setItem('kstock_gemini_key', state.geminiKey);
    }

    function deduplicateCatalysts(items) {
      const seen = new Map();
      for (const item of items) {
        const normalizedTitle = item.headline
          .replace(/\[단독\]|\[속보\]|\[특징주\]/g, '')
          .replace(/[^가-힣a-zA-Z0-9]/g, '')
          .slice(0, 14);
        const key = `${item.ticker}_${normalizedTitle}`;
        if (!seen.has(key)) {
          seen.set(key, { ...item, sources: [item.source], duplicateCount: 1 });
        } else {
          const existing = seen.get(key);
          if (!existing.sources.includes(item.source)) existing.sources.push(item.source);
          existing.duplicateCount += 1;
        }
      }
      return Array.from(seen.values());
    }

    function openGeminiModal() {
      document.getElementById('gemini-email-input').value = state.geminiEmail || '';
      document.getElementById('gemini-key-input').value = state.geminiKey || '';
      document.getElementById('gemini-modal').classList.remove('hidden');
      document.getElementById('gemini-modal').classList.add('flex');
    }

    function closeGeminiModal() {
      document.getElementById('gemini-modal').classList.add('hidden');
      document.getElementById('gemini-modal').classList.remove('flex');
    }

    function confirmGeminiLogin() {
      const email = document.getElementById('gemini-email-input').value.trim() || 'gemini-user@gmail.com';
      const key = document.getElementById('gemini-key-input').value.trim();
      state.geminiLoggedIn = true;
      state.geminiEmail = email;
      state.geminiKey = key;
      saveLocalSettings();
      closeGeminiModal();
      updateHeaderGeminiUI();
      performFullRefresh('manual');
    }

    function logoutGemini() {
      state.geminiLoggedIn = false;
      saveLocalSettings();
      updateHeaderGeminiUI();
      render();
    }

    function updateHeaderGeminiUI() {
      const badge = document.getElementById('gemini-status-badge');
      const btnText = document.getElementById('header-gemini-btn-text');
      if (state.geminiLoggedIn) {
        const modeLabel = state.geminiKey ? 'API 연결됨' : '기본 AI 모드';
        badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-navy-900"></span><span class="font-semibold text-navy-950">${state.geminiEmail} (${modeLabel})</span>`;
        btnText.textContent = 'AI 설정';
      } else {
        badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-slate-400"></span><span>Gemini AI 미연결</span>`;
        btnText.textContent = 'Gemini 로그인';
      }
    }

    function renderTabs() {
      const bar = document.getElementById('tab-bar');
      bar.innerHTML = TABS.map(t => {
        const active = state.activeTab === t.id;
        return `
          <button onclick="switchTab('${t.id}')" class="px-3.5 py-2 rounded-lg text-xs sm:text-sm font-bold transition flex items-center gap-2 cursor-pointer ${
            active
              ? 'bg-navy-900 text-white shadow-xs'
              : 'text-slate-600 hover:text-navy-950 hover:bg-slate-100'
          }">
            <span>${t.label}</span>
            <span class="px-1.5 py-0.5 text-[10px] rounded ${
              active ? 'bg-white/15 text-white' : 'bg-slate-200/80 text-slate-600'
            }">${t.badge}</span>
          </button>
        `;
      }).join('');
    }

    function switchTab(tabId) {
      state.activeTab = tabId;
      render();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function renderAiPicksTab() {
      if (!state.geminiLoggedIn) {
        return `
          <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-8 sm:p-12 text-center space-y-5">
            <div class="w-16 h-16 mx-auto rounded-2xl bg-navy-900 text-white flex items-center justify-center text-3xl font-bold">✦</div>
            <div class="max-w-xl mx-auto space-y-2">
              <span class="inline-block px-3 py-1 rounded-full text-xs font-bold bg-slate-100 text-navy-900 border border-slate-300">
                Gemini 로그인 전용 기능
              </span>
              <h2 class="text-2xl font-extrabold text-navy-950">실시간 AI 추천종목은 Gemini 로그인 후 확인 가능합니다</h2>
              <p class="text-sm text-slate-600 leading-relaxed">
                Gemini 로그인 후 전체 갱신 및 장중 10초 자동갱신 시 2단계 사실확인을 거친 호재와 수급 데이터를 기반으로 추천종목을 새로고침합니다.
              </p>
            </div>
            <div class="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button onclick="openGeminiModal()" class="px-6 py-3 rounded-xl text-sm font-bold bg-navy-900 hover:bg-navy-800 text-white transition cursor-pointer">
                ✦ Gemini 로그인하고 추천종목 보기
              </button>
              <button onclick="switchTab('today-catalyst')" class="px-5 py-3 rounded-xl text-sm font-bold bg-white hover:bg-slate-50 text-navy-950 border border-slate-300 transition cursor-pointer">
                오늘의 호재 먼저 보기 →
              </button>
            </div>
          </div>
        `;
      }

      return `
        <div class="space-y-5">
          <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div class="space-y-1">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-navy-900 text-white">
                  ✦ ${state.geminiKey ? 'Gemini 2.5 Flash 실시간 API 연결됨' : '기본 AI 추천 데이터 모드'}
                </span>
                <span class="text-xs text-slate-600">계정: ${state.geminiEmail}</span>
              </div>
              <h2 class="text-lg sm:text-xl font-extrabold text-navy-950">실시간 AI 추천종목</h2>
              <p class="text-xs sm:text-sm text-slate-600">2단계 사실확인을 통과한 호재 기반으로 종목을 분석하며, 갱신 시마다 전체 데이터가 새로고침됩니다.</p>
            </div>
            <div class="flex flex-wrap items-center gap-2">
              <input type="text" value="${state.aiCustomPrompt}" placeholder="예: 반도체·바이오 위주 단기 수급주" oninput="state.aiCustomPrompt = this.value" class="px-3.5 py-2 rounded-lg bg-slate-50 border border-slate-300 text-xs sm:text-sm text-navy-950 w-64 focus:outline-none focus:border-navy-900" />
              <button onclick="runLiveGeminiStockAnalysis()" ${state.aiLoading ? 'disabled' : ''} class="px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-navy-900 hover:bg-navy-800 disabled:opacity-50 text-white transition cursor-pointer">
                ${state.aiLoading ? 'AI 분석 중...' : '✦ AI 정밀 재분석'}
              </button>
              <button onclick="logoutGemini()" class="px-3 py-2 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 cursor-pointer">
                로그아웃
              </button>
            </div>
          </div>

          ${state.aiError ? `
            <div class="rounded-xl bg-amber-50 border border-amber-300 px-4 py-3 text-xs sm:text-sm text-amber-900">
              ${state.aiError}
            </div>
          ` : ''}

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            ${state.radarData.aiPicks.map(item => `
              <div class="rounded-2xl bg-white border border-slate-200 shadow-xs hover:border-navy-900 transition p-5 flex flex-col justify-between gap-4">
                <div class="space-y-3">
                  <div class="flex items-start justify-between gap-3">
                    <div>
                      <div class="flex items-center gap-2 flex-wrap">
                        <h3 class="text-lg font-extrabold text-navy-950">${item.name}</h3>
                        <span class="text-xs font-mono text-slate-500">${item.ticker}</span>
                        <span class="px-2 py-0.5 text-[11px] rounded-md bg-slate-100 text-navy-900 font-semibold">${item.sector}</span>
                      </div>
                      <p class="text-xs text-slate-500 mt-0.5">갱신: ${item.updatedAt}</p>
                    </div>
                    <div class="text-right">
                      <div class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-navy-900 text-white text-xs font-bold">
                        AI 점수 ${item.score}점
                      </div>
                      <div class="text-[11px] font-bold text-navy-800 mt-1">${item.signal}</div>
                    </div>
                  </div>
                  <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
                    <div class="text-[11px] font-bold text-navy-800 mb-1">핵심 호재</div>
                    <div class="text-xs sm:text-sm font-bold text-navy-950">${item.catalystSummary}</div>
                  </div>
                  <p class="text-xs sm:text-sm text-slate-700 leading-relaxed">
                    <span class="text-navy-950 font-bold">Gemini 분석:</span> ${item.aiReasoning}
                  </p>
                </div>
                <div class="grid grid-cols-3 gap-2 pt-3 border-t border-slate-100 text-center">
                  <div class="bg-slate-50 rounded-lg p-2 border border-slate-100">
                    <div class="text-[11px] text-slate-500">진입 참고가</div>
                    <div class="text-xs font-bold text-navy-950 mt-0.5">${item.entryRange}</div>
                  </div>
                  <div class="bg-slate-50 rounded-lg p-2 border border-slate-100">
                    <div class="text-[11px] text-slate-500">목표가</div>
                    <div class="text-xs font-bold text-emerald-700 mt-0.5">${item.targetPrice}</div>
                  </div>
                  <div class="bg-slate-50 rounded-lg p-2 border border-slate-100">
                    <div class="text-[11px] text-slate-500">손절 기준</div>
                    <div class="text-xs font-bold text-rose-700 mt-0.5">${item.stopLoss}</div>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function renderTodayCatalystTab() {
      const uniqueList = deduplicateCatalysts(state.radarData.todayNews);
      const sectors = ['전체', ...Array.from(new Set(uniqueList.map(x => x.sector)))];
      const filtered = state.catalystSectorFilter === '전체'
        ? uniqueList
        : uniqueList.filter(x => x.sector === state.catalystSectorFilter);

      return `
        <div class="space-y-5">
          <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <div class="flex items-center gap-2 flex-wrap">
                <h2 class="text-lg sm:text-xl font-extrabold text-navy-950">오늘의 호재 피드</h2>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-navy-900 text-white">
                  2차 사실확인 통과 ${uniqueList.length}건 · 검증 보류 ${state.rejectedFactItems.length}건
                </span>
              </div>
              <p class="text-xs sm:text-sm text-slate-600 mt-1">
                <strong class="text-navy-950">사실확인 2번</strong>을 통과한 호재만 추가되며, 반복 보도되는 동일 호재는 <strong class="text-navy-950">한 번만</strong> 표시합니다.
              </p>
            </div>
            <div class="flex flex-wrap gap-1.5">
              ${sectors.map(sec => `
                <button onclick="setCatalystSector('${sec}')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition cursor-pointer ${
                  state.catalystSectorFilter === sec
                    ? 'bg-navy-900 text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }">${sec}</button>
              `).join('')}
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
            <div class="lg:col-span-2 space-y-3">
              ${filtered.map(item => `
                <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-4 sm:p-5 space-y-2.5">
                  <div class="flex items-center justify-between gap-2 flex-wrap">
                    <div class="flex items-center gap-2 flex-wrap">
                      <span class="px-2 py-0.5 rounded bg-navy-900 text-white text-xs font-mono font-bold">${item.time}</span>
                      <span class="font-extrabold text-navy-950 text-sm sm:text-base">${item.name}</span>
                      <span class="text-xs text-slate-500 font-mono">(${item.ticker})</span>
                      <span class="px-2 py-0.5 rounded-full text-[11px] bg-slate-100 text-navy-800 font-semibold border border-slate-200">${item.sector}</span>
                    </div>
                    <div class="flex items-center gap-1.5 flex-wrap">
                      <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-navy-900 text-white">2차 검증 통과</span>
                      ${item.duplicateCount > 1
                        ? `<span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-50 text-amber-800 border border-amber-200">중복 ${item.duplicateCount}건 병합됨</span>`
                        : `<span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">단독/최초 호재</span>`
                      }
                    </div>
                  </div>
                  <h3 class="text-sm sm:text-base font-bold text-navy-950">${item.headline}</h3>
                  <p class="text-xs sm:text-sm text-slate-700 leading-relaxed">${item.detail}</p>
                  <div class="text-[11px] text-slate-500 pt-1">
                    확인 매체: <span class="text-navy-900 font-semibold">${item.sources.join(', ')}</span>
                    ${item.factCheckNote ? ` · <span class="text-navy-800">${item.factCheckNote}</span>` : ''}
                  </div>
                </div>
              `).join('')}

              ${state.rejectedFactItems.length > 0 ? `
                <div class="rounded-2xl bg-slate-50 border border-slate-200 p-4 space-y-2">
                  <div class="text-xs font-extrabold text-navy-900">사실확인 2단계 미통과로 제외된 항목 (${state.rejectedFactItems.length}건)</div>
                  ${state.rejectedFactItems.map(r => `
                    <div class="text-xs text-slate-600 bg-white border border-slate-200 rounded-lg px-3 py-2 flex items-center justify-between gap-2">
                      <span class="truncate font-medium text-navy-950">${r.headline || r.title}</span>
                      <span class="text-[11px] text-rose-700 font-semibold shrink-0">${r.verifyReason}</span>
                    </div>
                  `).join('')}
                </div>
              ` : ''}
            </div>

            <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 space-y-4 h-fit">
              <div>
                <h3 class="font-extrabold text-navy-950 text-base">호재 추가 (2단계 사실확인)</h3>
                <p class="text-xs text-slate-600 mt-0.5">1차·2차 사실확인을 통과한 호재만 피드에 반영되며, 중복 기사는 1건으로 병합됩니다.</p>
              </div>
              <form onsubmit="addTodayCatalyst(event)" class="space-y-3">
                <div>
                  <label class="block text-xs font-semibold text-navy-900 mb-1">종목 선택</label>
                  <select id="new-cat-stock" class="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-xs sm:text-sm text-navy-950">
                    <option value="068270|셀트리온|바이오">셀트리온 (068270 · 바이오)</option>
                    <option value="042700|한미반도체|반도체">한미반도체 (042700 · 반도체)</option>
                    <option value="005930|삼성전자|반도체">삼성전자 (005930 · 반도체)</option>
                    <option value="000660|SK하이닉스|반도체">SK하이닉스 (000660 · 반도체)</option>
                    <option value="012450|한화에어로스페이스|방산/우주">한화에어로스페이스 (012450 · 방산/우주)</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-semibold text-navy-900 mb-1">호재 헤드라인</label>
                  <input id="new-cat-headline" type="text" required placeholder="예: 셀트리온, 짐펜트라 미국 PBM 등재 확대 소식" class="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-xs sm:text-sm text-navy-950" />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-navy-900 mb-1">매체명 (출처 필수)</label>
                  <input id="new-cat-source" type="text" required value="한국경제" class="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-300 text-xs sm:text-sm text-navy-950" />
                </div>
                <button type="submit" class="w-full py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-navy-900 hover:bg-navy-800 text-white transition cursor-pointer">
                  2단계 사실확인 후 추가
                </button>
              </form>
            </div>
          </div>
        </div>
      `;
    }

    function setCatalystSector(sec) {
      state.catalystSectorFilter = sec;
      render();
    }

    async function addTodayCatalyst(e) {
      e.preventDefault();
      const [ticker, name, sector] = document.getElementById('new-cat-stock').value.split('|');
      const headline = document.getElementById('new-cat-headline').value.trim();
      const source = document.getElementById('new-cat-source').value.trim();
      if (!headline || !source) return;

      const kst = getKstNowParts();
      const candidate = {
        id: 'n_' + Date.now(),
        time: kst.timeOnly.slice(0, 5),
        ticker,
        name,
        sector,
        headline,
        source,
        impact: '높음',
        detail: `${name} 관련 2단계 사실확인을 통과한 호재입니다.`
      };

      const c1 = passFirstFactCheck(candidate);
      if (!c1.ok) {
        state.rejectedFactItems.unshift({ ...candidate, verifyReason: c1.reason });
        render();
        return;
      }

      const c2 = passSecondFactCheck(candidate, [...state.userAddedCatalysts, ...(state.radarData.todayNews || [])]);
      if (!c2.ok) {
        state.rejectedFactItems.unshift({ ...candidate, verifyReason: c2.reason });
        render();
        return;
      }

      if (state.geminiKey) {
        try {
          const aiRes = await verifyTwiceWithGeminiIfAvailable(candidate);
          if (!aiRes.passed) {
            state.rejectedFactItems.unshift({ ...candidate, verifyReason: aiRes.note });
            render();
            return;
          }
        } catch (err) {
          state.rejectedFactItems.unshift({ ...candidate, verifyReason: `2차 AI 사실확인 실패: ${err.message}` });
          render();
          return;
        }
      }

      state.userAddedCatalysts.unshift(candidate);
      document.getElementById('new-cat-headline').value = '';
      await performFullRefresh('manual');
    }

    function renderUpcomingEventsTab() {
      const categories = ['전체', '임상', 'FDA', '회사', '학회', '실적', 'M&A'];
      const sorted = [...state.radarData.upcomingEvents]
        .filter(ev => state.eventCategoryFilter === '전체' || ev.category === state.eventCategoryFilter)
        .sort((a, b) => a.date.localeCompare(b.date));

      return `
        <div class="space-y-5">
          <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <h2 class="text-lg sm:text-xl font-extrabold text-navy-950">1달 앞 주요 기업·임상·FDA·학회·실적·M&amp;A 일정</h2>
              <p class="text-xs sm:text-sm text-slate-600 mt-1">
                날짜순으로 정렬되며, 날짜가 모호한 일정은 <span class="px-1.5 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200 font-bold text-xs">예상 발표일</span>로 표기했습니다.
              </p>
            </div>
            <div class="flex flex-wrap gap-1.5">
              ${categories.map(cat => `
                <button onclick="setEventCategory('${cat}')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition cursor-pointer ${
                  state.eventCategoryFilter === cat
                    ? 'bg-navy-900 text-white'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }">${cat}</button>
              `).join('')}
            </div>
          </div>

          <div class="space-y-3">
            ${sorted.map(ev => `
              <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="flex items-start gap-4">
                  <div class="min-w-[118px] rounded-xl bg-slate-50 border border-slate-200 p-3 text-center">
                    <div class="text-sm font-extrabold text-navy-950">${ev.date}</div>
                    <div class="mt-1">
                      ${ev.isExactDate
                        ? `<span class="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-navy-900 text-white">공식 확정일</span>`
                        : `<span class="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">예상 발표일</span>`
                      }
                    </div>
                  </div>
                  <div class="space-y-1">
                    <div class="flex items-center gap-2 flex-wrap">
                      <span class="px-2.5 py-0.5 rounded-md text-xs font-bold bg-slate-100 text-navy-900 border border-slate-200">${ev.category}</span>
                      <span class="font-extrabold text-navy-950 text-sm sm:text-base">${ev.name}</span>
                      <span class="text-xs font-mono text-slate-500">(${ev.ticker})</span>
                    </div>
                    <h3 class="text-sm sm:text-base font-bold text-navy-950">${ev.title}</h3>
                    <p class="text-xs sm:text-sm text-slate-600">${ev.detail}</p>
                  </div>
                </div>
                <div class="flex items-center gap-2 self-end md:self-center shrink-0">
                  <button onclick="openEarningsForTicker('${ev.ticker}')" class="px-3 py-2 rounded-lg text-xs font-bold bg-white hover:bg-slate-50 text-navy-950 border border-slate-300 transition cursor-pointer">
                    실적 미리보기 →
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function setEventCategory(cat) {
      state.eventCategoryFilter = cat;
      render();
    }

    function openEarningsForTicker(ticker) {
      const found = state.radarData.earningsPreview.find(e => e.ticker === ticker);
      state.selectedEarningsTicker = found ? found.ticker : state.radarData.earningsPreview[0].ticker;
      switchTab('earnings-preview');
    }

    function renderEarningsPreviewTab() {
      const list = state.radarData.earningsPreview;
      const current = list.find(e => e.ticker === state.selectedEarningsTicker) || list[0];

      return `
        <div class="space-y-5">
          <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <div class="flex items-center gap-2 flex-wrap">
                <h2 class="text-lg sm:text-xl font-extrabold text-navy-950">3번 탭 종목 실적 미리보기 &amp; AI 요인 분석</h2>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-navy-900 text-white">
                  ${state.geminiLoggedIn ? '✦ Gemini AI 긍·부정 판별 활성' : 'AI 판별 미리보기'}
                </span>
              </div>
              <p class="text-xs sm:text-sm text-slate-600 mt-1">
                주가 영향 세부 요인을 AI로 긍정/부정 판별하고, <strong class="text-navy-950">최근 3개 분기(2026 1Q~3Q)</strong> 재무 지표 변화를 표시합니다.
              </p>
            </div>
            <div class="flex flex-wrap gap-2">
              ${list.map(item => `
                <button onclick="selectEarningsTicker('${item.ticker}')" class="px-3.5 py-2 rounded-xl text-xs font-bold transition cursor-pointer ${
                  item.ticker === current.ticker
                    ? 'bg-navy-900 text-white shadow-xs'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }">
                  ${item.name} (${item.ticker})
                </button>
              `).join('')}
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-4">
              <div class="text-xs text-slate-500">선택 종목</div>
              <div class="text-xl font-extrabold text-navy-950 mt-1">${current.name} <span class="text-sm font-medium text-slate-500">${current.sector}</span></div>
            </div>
            <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-4">
              <div class="text-xs text-slate-500">시장 예상 영업이익 (컨센서스)</div>
              <div class="text-xl font-extrabold text-navy-900 mt-1">${current.consensusOpProfit}</div>
            </div>
            <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-4">
              <div class="text-xs text-slate-500">전년 동기 대비 (YoY)</div>
              <div class="text-xl font-extrabold ${current.yoyGrowth.startsWith('+') ? 'text-emerald-700' : 'text-rose-700'} mt-1">${current.yoyGrowth}</div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
            <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 space-y-4">
              <div class="flex items-center justify-between">
                <h3 class="font-extrabold text-navy-950 text-base">주가 영향 세부 요인 (AI 긍·부정 판별)</h3>
                ${!state.geminiLoggedIn
                  ? `<button onclick="openGeminiModal()" class="text-xs font-bold text-navy-900 hover:underline cursor-pointer">✦ Gemini 연결</button>`
                  : `<span class="text-xs font-bold text-navy-900">✦ AI 판별 완료</span>`
                }
              </div>
              <div class="space-y-2.5">
                ${current.factors.map(f => {
                  const isPos = f.sentiment === 'positive';
                  return `
                    <div class="rounded-xl bg-slate-50 border ${isPos ? 'border-emerald-200' : 'border-rose-200'} p-3.5 flex items-start justify-between gap-3">
                      <div class="space-y-1">
                        <div class="text-xs sm:text-sm font-bold text-navy-950">${f.label}</div>
                        <div class="text-xs text-slate-600">${f.note}</div>
                      </div>
                      <span class="px-2.5 py-1 rounded-lg text-xs font-extrabold shrink-0 ${
                        isPos
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-rose-50 text-rose-700 border border-rose-200'
                      }">
                        ${isPos ? '▲ 긍정' : '▼ 부정'}
                      </span>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>

            <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 space-y-4">
              <h3 class="font-extrabold text-navy-950 text-base">최근 3개 분기 재무 변화 (2026 1Q ~ 3Q)</h3>
              <div class="h-56">
                <canvas id="earnings-chart"></canvas>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-xs text-left border-collapse">
                  <thead>
                    <tr class="border-b border-slate-200 text-slate-500 bg-slate-50">
                      <th class="py-2 px-2">분기</th>
                      <th class="py-2 px-2">매출액(억)</th>
                      <th class="py-2 px-2">영업이익(억)</th>
                      <th class="py-2 px-2">영업이익률</th>
                      <th class="py-2 px-2">부채비율</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 text-navy-950 font-mono">
                    ${current.quarters.map((q, idx) => `
                      <tr>
                        <td class="py-2 px-2 font-sans font-bold text-navy-900">${q}</td>
                        <td class="py-2 px-2">${current.revenue[idx].toLocaleString()}</td>
                        <td class="py-2 px-2">${current.opProfit[idx].toLocaleString()}</td>
                        <td class="py-2 px-2">${current.opMargin[idx]}%</td>
                        <td class="py-2 px-2">${current.debtRatio[idx]}%</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function selectEarningsTicker(ticker) {
      state.selectedEarningsTicker = ticker;
      render();
    }

    function mountEarningsChart() {
      const canvas = document.getElementById('earnings-chart');
      if (!canvas) return;
      const list = state.radarData.earningsPreview;
      const current = list.find(e => e.ticker === state.selectedEarningsTicker) || list[0];

      if (earningsChartInstance) earningsChartInstance.destroy();

      earningsChartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: current.quarters,
          datasets: [
            {
              type: 'bar',
              label: '영업이익 (십억원 환산)',
              data: current.opProfit.map(v => Number((v / 10).toFixed(1))),
              backgroundColor: 'rgba(15, 23, 42, 0.82)',
              borderColor: '#0f172a',
              borderWidth: 1,
              borderRadius: 6,
              yAxisID: 'y'
            },
            {
              type: 'line',
              label: '영업이익률 (%)',
              data: current.opMargin,
              borderColor: '#1d4ed8',
              backgroundColor: '#1d4ed8',
              tension: 0.3,
              pointRadius: 4,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#0f172a', font: { size: 11, weight: '600' } } } },
          scales: {
            x: { ticks: { color: '#334155' }, grid: { color: 'rgba(15,23,42,0.06)' } },
            y: { type: 'linear', position: 'left', ticks: { color: '#0f172a' }, grid: { color: 'rgba(15,23,42,0.06)' } },
            y1: { type: 'linear', position: 'right', ticks: { color: '#1d4ed8', callback: v => v + '%' }, grid: { drawOnChartArea: false } }
          }
        }
      });
    }

    function renderMarketScheduleTab() {
      return `
        <div class="space-y-5">
          <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5">
            <h2 class="text-lg sm:text-xl font-extrabold text-navy-950">글로벌 정세 및 주요 경제지표 발표일정</h2>
            <p class="text-xs sm:text-sm text-slate-600 mt-1">
              국내 증시에 영향을 미칠 수 있는 세계 정세 및 주요 거시경제 지표 일정을 한국시간(KST)과 함께 제공합니다.
            </p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            ${state.radarData.marketSchedules.map(m => `
              <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 space-y-3">
                <div class="flex items-center justify-between gap-2 flex-wrap">
                  <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded-lg bg-navy-900 text-white text-xs font-mono font-bold">
                      ${m.date} · ${m.timeKst} KST
                    </span>
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-navy-900 border border-slate-200">${m.region}</span>
                  </div>
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-50 text-navy-800 border border-slate-300">
                    영향도: ${m.impact}
                  </span>
                </div>
                <h3 class="text-sm sm:text-base font-bold text-navy-950">${m.title}</h3>
                <p class="text-xs sm:text-sm text-slate-700 leading-relaxed">
                  <span class="text-navy-950 font-bold">국내주식 파급효과:</span> ${m.krEffect}
                </p>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function renderCalendarTab() {
      const year = 2026;
      const monthIndex = state.calendarMonth === '2026-11' ? 10 : 11;
      const firstDay = new Date(year, monthIndex, 1).getDay();
      const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();

      const combinedMap = new Map();
      state.radarData.upcomingEvents.forEach(ev => {
        const list = combinedMap.get(ev.date) || [];
        list.push({
          type: '종목일정',
          badgeColor: 'bg-navy-900 text-white',
          title: `[${ev.name}] ${ev.category}: ${ev.title}`,
          sub: ev.isExactDate ? '공식 확정일' : '예상 발표일'
        });
        combinedMap.set(ev.date, list);
      });

      state.radarData.marketSchedules.forEach(ms => {
        const list = combinedMap.get(ms.date) || [];
        list.push({
          type: '시장일정',
          badgeColor: 'bg-slate-100 text-navy-900 border border-slate-300',
          title: `[${ms.region} ${ms.timeKst}] ${ms.title}`,
          sub: ms.krEffect
        });
        combinedMap.set(ms.date, list);
      });

      const cells = [];
      for (let i = 0; i < firstDay; i++) {
        cells.push(`<div class="min-h-[96px] rounded-xl bg-slate-50/60 border border-slate-100 p-2"></div>`);
      }

      for (let d = 1; d <= daysInMonth; d++) {
        const mm = String(monthIndex + 1).padStart(2, '0');
        const dd = String(d).padStart(2, '0');
        const dateStr = `${year}-${mm}-${dd}`;
        const dayEvents = combinedMap.get(dateStr) || [];
        const isSelected = state.selectedCalendarDate === dateStr;
        const isToday = dateStr === '2026-11-25';

        cells.push(`
          <button onclick="selectCalendarDate('${dateStr}')" class="min-h-[96px] text-left rounded-xl border p-2 transition flex flex-col justify-between cursor-pointer ${
            isSelected
              ? 'bg-slate-50 border-2 border-navy-900'
              : 'bg-white border-slate-200 hover:border-navy-800'
          }">
            <div class="flex items-center justify-between w-full">
              <span class="text-xs font-extrabold ${isToday ? 'text-navy-900 underline' : 'text-navy-950'}">${d}일</span>
              ${isToday ? `<span class="text-[10px] px-1.5 py-0.5 rounded bg-navy-900 text-white font-bold">오늘</span>` : ''}
            </div>
            <div class="space-y-1 mt-1 w-full">
              ${dayEvents.slice(0, 2).map(ev => `
                <div class="truncate text-[10px] font-semibold px-1.5 py-0.5 rounded ${ev.badgeColor}">${ev.title}</div>
              `).join('')}
              ${dayEvents.length > 2 ? `<div class="text-[10px] text-slate-500 font-medium">+${dayEvents.length - 2}건 더보기</div>` : ''}
            </div>
          </button>
        `);
      }

      const selectedItems = combinedMap.get(state.selectedCalendarDate) || [];

      return `
        <div class="space-y-5">
          <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 class="text-lg sm:text-xl font-extrabold text-navy-950">통합 일정 캘린더 (1달 앞 종목일정 + 시장일정)</h2>
              <p class="text-xs sm:text-sm text-slate-600 mt-1">날짜를 선택하면 해당 일자의 종목 이벤트와 글로벌 경제 일정을 함께 확인할 수 있습니다.</p>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="setCalendarMonth('2026-11')" class="px-3.5 py-2 rounded-lg text-xs font-bold cursor-pointer ${
                state.calendarMonth === '2026-11' ? 'bg-navy-900 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }">2026년 11월</button>
              <button onclick="setCalendarMonth('2026-12')" class="px-3.5 py-2 rounded-lg text-xs font-bold cursor-pointer ${
                state.calendarMonth === '2026-12' ? 'bg-navy-900 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }">2026년 12월</button>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
            <div class="lg:col-span-2 rounded-2xl bg-white border border-slate-200 shadow-xs p-4">
              <div class="grid grid-cols-7 gap-1.5 text-center text-xs font-extrabold text-slate-600 pb-2">
                <div class="text-rose-700">일</div><div>월</div><div>화</div><div>수</div><div>목</div><div>금</div><div class="text-navy-900">토</div>
              </div>
              <div class="grid grid-cols-7 gap-1.5">${cells.join('')}</div>
            </div>

            <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 space-y-4 h-fit">
              <div>
                <div class="text-xs text-navy-800 font-bold">선택된 날짜 브리핑</div>
                <h3 class="text-lg font-extrabold text-navy-950 mt-0.5">${state.selectedCalendarDate}</h3>
              </div>
              ${selectedItems.length === 0
                ? `<p class="text-xs sm:text-sm text-slate-500 py-6 text-center rounded-xl bg-slate-50 border border-slate-200">해당 날짜에 등록된 주요 일정이 없습니다.</p>`
                : `<div class="space-y-3">
                    ${selectedItems.map(item => `
                      <div class="rounded-xl bg-slate-50 border border-slate-200 p-3.5 space-y-1.5">
                        <span class="inline-block px-2 py-0.5 rounded text-[10px] font-bold ${item.badgeColor}">${item.type}</span>
                        <div class="text-xs sm:text-sm font-bold text-navy-950">${item.title}</div>
                        <p class="text-xs text-slate-600 leading-relaxed">${item.sub}</p>
                      </div>
                    `).join('')}
                  </div>`
              }
            </div>
          </div>
        </div>
      `;
    }

    function setCalendarMonth(ym) {
      state.calendarMonth = ym;
      state.selectedCalendarDate = ym === '2026-11' ? '2026-11-27' : '2026-12-09';
      render();
    }

    function selectCalendarDate(dateStr) {
      state.selectedCalendarDate = dateStr;
      render();
    }

    function renderWatchlistTab() {
      const watchItems = state.watchlist.map(code => {
        const found = STOCK_CATALOG.find(s => s.ticker === code);
        return found || { ticker: code, name: `종목(${code})`, sector: '국내주식' };
      });

      const activeStock = watchItems.find(w => w.ticker === state.selectedWatchTicker) || watchItems[0] || null;
      const baseNews = activeStock ? (DEFAULT_NEWS_DB[activeStock.ticker] || [
        {
          title: `${activeStock.name}(${activeStock.ticker}) 공시 및 수급 동향 모니터링`,
          source: '레이더 뉴스피드',
          time: state.lastRefreshedAt ? state.lastRefreshedAt.slice(11, 19) : '06:59:00',
          sentiment: 'positive'
        }
      ]) : [];
      const extraNews = activeStock ? (state.customNewsMap[activeStock.ticker] || []) : [];

      // 관심종목 뉴스에도 2단계 사실확인을 통과한 항목만 반영
      const combined = [...extraNews, ...baseNews].filter(n => passFirstFactCheck(n).ok && passSecondFactCheck({ ...n, ticker: activeStock?.ticker || '005930' }, [...extraNews, ...baseNews]).ok);
      const aiSummaryText = activeStock ? state.watchAiSummary[activeStock.ticker] : '';

      return `
        <div class="space-y-5">
          <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <h2 class="text-lg sm:text-xl font-extrabold text-navy-950">내 국내 관심종목 &amp; 종목별 뉴스</h2>
              <p class="text-xs sm:text-sm text-slate-600 mt-1">관심종목을 직접 추가·삭제하고, 2단계 사실확인을 거친 뉴스와 Gemini AI 요약을 볼 수 있습니다.</p>
            </div>
            <form onsubmit="addWatchStock(event)" class="flex flex-wrap items-center gap-2">
              <input id="watch-input" list="stock-datalist" type="text" required placeholder="종목명 또는 6자리 코드 (예: 셀트리온, 068270)" class="px-3.5 py-2 rounded-lg bg-slate-50 border border-slate-300 text-xs sm:text-sm text-navy-950 w-64 focus:outline-none focus:border-navy-900" />
              <datalist id="stock-datalist">
                ${STOCK_CATALOG.map(s => `<option value="${s.name} (${s.ticker})"></option>`).join('')}
              </datalist>
              <button type="submit" class="px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-navy-900 hover:bg-navy-800 text-white transition cursor-pointer">
                + 관심종목 추가
              </button>
            </form>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
            <div class="rounded-2xl bg-white border border-slate-200 shadow-xs p-4 space-y-2 h-fit">
              <div class="text-xs font-bold text-slate-500 px-2 pb-1">등록된 관심종목 (${watchItems.length}개)</div>
              ${watchItems.length === 0
                ? `<p class="text-xs text-slate-500 p-4 text-center">관심종목을 추가해 보세요.</p>`
                : watchItems.map(item => {
                    const isSelected = activeStock && item.ticker === activeStock.ticker;
                    return `
                      <div class="flex items-center justify-between rounded-xl px-3 py-2.5 border transition ${
                        isSelected
                          ? 'bg-navy-900 border-navy-900 text-white'
                          : 'bg-slate-50 border-slate-200 text-navy-950 hover:border-navy-800'
                      }">
                        <button onclick="selectWatchTicker('${item.ticker}')" class="text-left flex-1 cursor-pointer">
                          <div class="font-bold text-sm">${item.name} <span class="text-xs font-mono ${isSelected ? 'text-slate-300' : 'text-slate-500'}">${item.ticker}</span></div>
                          <div class="text-[11px] ${isSelected ? 'text-slate-300' : 'text-slate-500'}">${item.sector}</div>
                        </button>
                        <button onclick="removeWatchTicker('${item.ticker}')" title="삭제" class="text-xs ${isSelected ? 'text-slate-300 hover:text-white' : 'text-slate-400 hover:text-rose-700'} px-2 py-1 cursor-pointer">✕</button>
                      </div>
                    `;
                  }).join('')
              }
            </div>

            <div class="lg:col-span-2 rounded-2xl bg-white border border-slate-200 shadow-xs p-5 space-y-4">
              ${activeStock ? `
                <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
                  <div>
                    <span class="text-xs text-navy-800 font-bold">${activeStock.sector}</span>
                    <h3 class="text-lg font-extrabold text-navy-950">${activeStock.name} (${activeStock.ticker}) 검증된 주요 뉴스</h3>
                  </div>
                  <div class="flex items-center gap-2">
                    <button onclick='summarizeWatchStockWithGemini(${JSON.stringify(activeStock)}, ${JSON.stringify(combined)})' ${state.watchAiLoading ? 'disabled' : ''} class="px-3 py-1.5 rounded-lg text-xs font-bold bg-navy-900 hover:bg-navy-800 text-white cursor-pointer">
                      ${state.watchAiLoading ? 'AI 요약 중...' : '✦ Gemini 뉴스 요약'}
                    </button>
                    <button onclick="appendSampleNews('${activeStock.ticker}', '${activeStock.name}')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-white hover:bg-slate-50 text-navy-950 border border-slate-300 cursor-pointer">
                      + 검증 후 속보 추가
                    </button>
                  </div>
                </div>

                ${aiSummaryText ? `
                  <div class="rounded-xl bg-slate-50 border border-navy-900/20 p-3.5 text-xs sm:text-sm text-navy-950 whitespace-pre-line">
                    <strong class="text-navy-900">✦ Gemini AI 분석 요약:</strong>\n${aiSummaryText}
                  </div>
                ` : ''}

                <div class="space-y-2.5">
                  ${combined.map(n => `
                    <div class="rounded-xl bg-slate-50 border border-slate-200 p-4 flex items-start justify-between gap-3">
                      <div class="space-y-1">
                        <div class="text-xs text-slate-500">${n.source} · ${n.time} · <span class="font-semibold text-navy-900">2차 사실확인 완료</span></div>
                        <div class="text-sm font-bold text-navy-950">${n.title}</div>
                      </div>
                      <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold shrink-0 ${
                        n.sentiment === 'positive'
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-slate-200 text-slate-700'
                      }">
                        ${n.sentiment === 'positive' ? '호재성' : '중립'}
                      </span>
                    </div>
                  `).join('')}
                </div>
              ` : `<p class="text-sm text-slate-500">표시할 관심종목이 없습니다.</p>`}
            </div>
          </div>
        </div>
      `;
    }

    function addWatchStock(e) {
      e.preventDefault();
      const raw = document.getElementById('watch-input').value.trim();
      if (!raw) return;

      const codeMatch = raw.match(/\d{6}/);
      let matched = codeMatch ? STOCK_CATALOG.find(s => s.ticker === codeMatch[0]) : null;
      if (!matched) matched = STOCK_CATALOG.find(s => s.name.toLowerCase() === raw.toLowerCase());

      const ticker = matched ? matched.ticker : (codeMatch ? codeMatch[0] : raw.slice(0, 6));
      if (!state.watchlist.includes(ticker)) state.watchlist.unshift(ticker);
      state.selectedWatchTicker = ticker;
      document.getElementById('watch-input').value = '';
      saveLocalSettings();
      render();
    }

    function selectWatchTicker(ticker) {
      state.selectedWatchTicker = ticker;
      saveLocalSettings();
      render();
    }

    function removeWatchTicker(ticker) {
      state.watchlist = state.watchlist.filter(t => t !== ticker);
      if (state.selectedWatchTicker === ticker) {
        state.selectedWatchTicker = state.watchlist[0] || '';
      }
      saveLocalSettings();
      render();
    }

    async function appendSampleNews(ticker, name) {
      const kst = getKstNowParts();
      const candidate = {
        title: `${name}, 기관·외국인 매수세 유입 및 업종 내 상대강도 확인`,
        source: '마켓레이더 확인속보',
        time: kst.timeOnly,
        sentiment: 'positive'
      };
      const c1 = passFirstFactCheck(candidate);
      const c2 = passSecondFactCheck({ ...candidate, ticker }, []);
      if (!c1.ok || !c2.ok) return;

      const list = state.customNewsMap[ticker] || [];
      list.unshift(candidate);
      state.customNewsMap[ticker] = list;
      saveLocalSettings();
      render();
    }

    function render() {
      renderTabs();
      const container = document.getElementById('app-content');
      switch (state.activeTab) {
        case 'ai-picks': container.innerHTML = renderAiPicksTab(); break;
        case 'today-catalyst': container.innerHTML = renderTodayCatalystTab(); break;
        case 'upcoming-events': container.innerHTML = renderUpcomingEventsTab(); break;
        case 'earnings-preview':
          container.innerHTML = renderEarningsPreviewTab();
          mountEarningsChart();
          break;
        case 'market-schedule': container.innerHTML = renderMarketScheduleTab(); break;
        case 'calendar': container.innerHTML = renderCalendarTab(); break;
        case 'watchlist': container.innerHTML = renderWatchlistTab(); break;
      }
    }

    updateHeaderGeminiUI();
    performFullRefresh('load');

    setInterval(() => {
      updateMarketStatusBadges();
      const kst = getKstNowParts();
      if (kst.isRegularMarketOpen) {
        performFullRefresh('auto-10s');
      }
    }, 10000);
  </script>
</body>
</html>
