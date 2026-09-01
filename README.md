# shop-lab

NOVERA shop에 대한 코드를 저장합니다.

## mobile-home

`shop.novera.town` 홈 화면 개편 **모바일 프로토타입**.

| | |
|---|---|
| 디자인 | Figma [\[NOVERA\] Shop / Handoff / Mobile](https://www.figma.com/design/Li8im2dMEZygQo0p7s4ea2/-NOVERA--Shop?node-id=5612-54824) (`5612:54824`) |
| 디자인 시스템 | Storybook `develop--693fcc16142e19f5d9fb6f9c.chromatic.com` — Foundation(Colors·Icon·Typo·Rounded·Spacing) + Components(Badge·Avatar·Tabs) |
| 데이터 | `shop.novera.town` 실제 상품 / `shop-api.novera.town` |

### 구조

```
mobile-home/
├── build.py                        # 빌더 — 에셋을 data URI 로 인라인해 단일 HTML 생성
├── data.json                       # 섹션별 상품 데이터 (API 스냅샷) + event_at(이벤트 일시)
├── assets/
│   ├── nds_icons.json              # NDS 아이콘 (viewBox 0 0 24 24)
│   ├── artist/                     # 아티스트 아바타
│   ├── banner/                     # 메인·인라인·컬렉션 배너
│   ├── brand/                      # 로고 / SNS SVG
│   └── prod/                       # 상품 썸네일
└── NOVERA_shop_home_mobile.html    # 빌드 결과물 (단일 파일, 그대로 열면 동작)
```

### 빌드

```bash
cd mobile-home && python3 build.py
```

의존성은 표준 라이브러리만 사용합니다. 에셋을 갱신하려면 `assets/` 를 교체한 뒤 다시 빌드하세요.

### 화면 구성

TopNavigation → 카테고리 탭 → 메인 배너(자동 슬라이드 4장) → 이벤트 바로가기 →
Meet Your Artist Event!(쇼케이스 배너 + 카운트다운) → Fan's Pick!(TOP 3) →
Now Trending → New Arrival → 인라인 배너 → NOVERA shop Collection(탭) →
Footer → BottomNavigation

### 메인 배너 모션

Figma 모션 타임라인(16.4s 루프 / 4장)을 슬라이드 1장 단위(4,100ms)로 옮겼습니다.

| 구간 | 시간 | 값 |
|---|---|---|
| 정지 | 0 → 3,300ms | — |
| 텍스트·페이지네이션 페이드아웃 | 3,300 → 3,500ms | 200ms `ease-out` |
| 슬라이드 이동 | 3,500 → 4,100ms | 600ms `cubic-bezier(.33,0,.1,1)` |
| 새 슬라이드 텍스트 페이드인 | 4,100 → 4,400ms | 300ms `ease-out` |

이동 구간에는 어느 슬라이드의 텍스트도 보이지 않는 것이 시안의 의도입니다.
Fan's Pick 시상대도 같은 방식으로 시안 키프레임(시상대 → 콘텐츠, 3위 → 2위 → 1위)을
그대로 옮겼고, 스프링 곡선은 `linear()` 이징을 지원하는 브라우저에서 원본 곡선으로 올라갑니다.

**배너 이미지** — `assets/banner/` 에 아래 파일이 있으면 자동으로 얹히고, 없으면 시안에서
실측한 배경 그라디언트만 남습니다 (확장자는 `.webp/.jpg/.jpeg/.png` 순으로 탐색).

| 슬라이드 | 파일 | 상태 |
|---|---|---|
| VARI(베리) VIDEO CALL EVENT | `main_vari.*` | **미포함** — Figma export 필요 |
| 코스모시 x 귀멸의 칼날 | `main3.jpg` | 포함 |
| BE BOYS(비보이즈) UNIT CALL EVENT | `main_beboys.*` | **미포함** — Figma export 필요 |
| WELCOME COUPON | `main1.webp` | 포함 |

### Meet Your Artist Event (Figma `5749:63751`)

시안의 *Concept 3 - Showcase Banner* 를 그대로 옮겼습니다.

| 블록 | Figma | 내용 |
|---|---|---|
| Banner Area | `5749:63752` | blue-700→blue-500 바탕 + 아티스트 컷 + `black80→mask` 오버레이, LIVE MD 뱃지 / 전체보기 / 타이틀 22 Bold / 아티스트 / 구매 종료까지 카운트다운 |
| Overlapping Cards | `5749:63783` | 배너 위로 30px 올라탄 가로형 ProductCard 2장 (썸네일 80, VIDEO CALL 뱃지, Inline Meta Row) |
| NextArtistPreview | `5749:63826` | 다음 아티스트 칩 (가로 스크롤, 가장 임박한 칩만 100% 불투명) |

**날짜 동기화** — `data.json` 의 `event_at`(ISO 8601, KST) 을 HTML 로 넘기고, 브라우저가
볼 때마다 **가장 가까운 미래** 일시를 골라 1초 단위로 카운트다운합니다. 다음 아티스트 칩의
"오늘 오후 8:00 / 내일 오후 8:00 / 9.30 오후 8:00" 문구와 카드의 `📅 09.05` 도 같은 값에서
만들어집니다. 남은 이벤트가 없으면 `00`에서 멈추고 "예정된 이벤트가 없어요"로 바뀝니다.

현재 `event_at` 은 상품명 앞머리의 `[09.05 …]` 를 승격시킨 값이고, 시각 정보는 상품명에
없어 비디오콜·팬사인 통상 시작 시각인 **20:00 (KST)** 을 썼습니다. API 가 실제 이벤트
일시를 내려주면 `event_at` 필드만 갈아끼우면 됩니다.

**아직 데이터가 없는 항목** — 시안 카드의 `30명 한정`·`미공개 포토카드` 는 목업 값입니다.
상품에 `limit_count`(정수)·`perk`(문자열) 필드가 들어오면 뱃지와 Inline Meta Row 에
자동으로 붙도록 해 뒀고, 없으면 실제로 가진 값(날짜·NEW)만 그립니다. 다음 아티스트 칩도
현재 데이터에 이벤트가 `최성윤 09.05` 하나뿐이라 1개만 표시됩니다.

**아티스트 이미지** — 시안은 아티스트 컷을 쓰지만 프록시가 figma.com 을 차단해 내려받지
못했습니다. 지금은 대표 이벤트 상품 이미지를 배너 배경·아바타로 쓰고 있습니다.
