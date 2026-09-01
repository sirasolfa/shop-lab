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

### 배포 (Vercel)

`vercel.json` 이 저장소 루트와 `mobile-home/` 양쪽에 있어, Vercel 프로젝트의
**Root Directory** 를 어느 쪽으로 잡아도 동작합니다. 빌드는 커밋된 단일 HTML 을
`public/index.html` 로 옮기는 것뿐이라 별도 런타임이 필요 없습니다.

```
buildCommand : mkdir -p public && cp <빌드결과 HTML> public/index.html
outputDirectory : public
```

HTML 은 에셋을 전부 data URI 로 품고 있어 이 파일 하나면 완결됩니다. 소스를 고쳤다면
**커밋 전에 `python3 build.py` 를 돌려** 산출물을 갱신해야 배포본에 반영됩니다.

### 데스크톱 브레이크포인트 (Figma `5461:140412`)

`1200px` 이상에서 시안의 3단 레이아웃으로 전환합니다. 안쪽 폭을 1200 으로 잡고 가운데
정렬하면 1440 뷰포트에서 좌우 거터가 정확히 120px 이 됩니다.

```
120 거터 | 232 사이드바 | 64 | 520 본문 | 64 | 320 장바구니 | 120 거터
```

| 영역 | 내용 |
|---|---|
| 헤더 | 풀블리드. 로고 + 검색 입력창 + 좋아요·장바구니 + KO + 회원가입\|로그인 |
| 좌측 | 사이드 내비게이션 (sticky). 카테고리 탭바·하단 탭바는 숨김 |
| 본문 | 520px 컬럼. 배너는 520×280 으로, 모바일 이미지를 **가로폭에 맞춰 늘리고 위쪽 기준 정렬** |
| 우측 | 장바구니 패널 (sticky, Figma `5477:75370`) — 프로토타입이라 Empty 상태만 |

1200px 미만은 모바일 레이아웃(단일 컬럼 + 하단 탭바 + 드로어)을 그대로 씁니다.

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

**배너 이미지** — 시안 Background Image 레이어를 375×320 @3x 로 내보낸 파일입니다.
export 에 그라디언트가 이미 구워져 있어 네 장 모두 같은 규칙(`object-fit:cover`)으로 채웁니다.

| 슬라이드 | 파일 |
|---|---|
| VARI(베리) VIDEO CALL EVENT | `assets/banner/main_vari.webp` |
| 코스모시 x 귀멸의 칼날 | `assets/banner/main_kimetsu.webp` |
| BE BOYS(비보이즈) UNIT CALL EVENT | `assets/banner/main_beboys.webp` |
| WELCOME COUPON | `assets/banner/main_coupon.webp` |

데스크톱(520×280)에서는 같은 이미지를 가로폭에 맞춰 늘리고 위쪽 기준으로 정렬해 아래가
잘립니다. 파일이 없으면 시안에서 실측한 배경 그라디언트만 남습니다.

### Meet Your Artist Event (Figma `5749:63751`)

시안의 *Concept 3 - Showcase Banner* 를 그대로 옮겼습니다.

| 블록 | Figma | 내용 |
|---|---|---|
| Banner Area | `5749:63752` | blue-700→blue-500 바탕 + 아티스트 컷 + `black80→mask` 오버레이, LIVE MD 뱃지 / 전체보기 / 타이틀 22 Bold / 아티스트 / 구매 종료까지 카운트다운 |
| Overlapping Cards | `5749:63783` | 배너 위로 30px 올라탄 가로형 ProductCard 2장 (썸네일 80, VIDEO CALL 뱃지, Inline Meta Row) |
| NextArtistPreview | `5749:63826` | 다음 아티스트 칩 (가로 스크롤, 가장 임박한 칩만 100% 불투명) |

**상품** — `data.json` 의 `sections.livemd` 두 건입니다. 값은 시안 카드(`5749:63784` ·
`5749:63801`) 실측 그대로이고, 상품명은 짧게 두고 시안 1행의 이벤트 시리즈명은 `sub` 로
분리했습니다.

| id | 아티스트 | sub | 상품명 | 가격 | 뱃지 |
|---|---|---|---|---|---|
| 306 | 장한음 | [DAYDREAM] 스페셜 비디오콜 이벤트 | 할리갈리 게임 이벤트 | ₩39,000 | VIDEO CALL |
| 307 | 장한음 | [DAYDREAM] 스페셜 대면 이벤트 | 대면 부채 만들기 이벤트 | ₩39,000 | 대면 이벤트 |

**날짜 동기화** — `event_at`(ISO 8601, KST) 을 HTML 로 넘기고, 브라우저가 볼 때마다
**가장 가까운 미래** 일시를 골라 1초 단위로 카운트다운합니다. 카드의 `📅 09.20` 과
다음 아티스트 칩의 "오늘 오후 8:00 / 내일 오후 8:00 / 9.20 오후 8:00" 문구도 같은 값에서
만들어집니다. 남은 이벤트가 없으면 `00`에서 멈추고 "예정된 이벤트가 없어요"로 바뀝니다.

시안이 주는 날짜는 Inline Meta Row 의 `09.20` 하나뿐입니다. 같은 [DAYDREAM] 시리즈
안에서 대면 행사와 비디오콜이 같은 시각일 수는 없어 **대면 14:00 · 비디오콜 20:00 (KST)**
으로 두었습니다. API 가 실제 일시를 내려주면 `event_at` 필드만 갈아끼우면 됩니다.

**다음 아티스트 칩** 은 모든 섹션에서 `event_at` 이 있는 상품을 모아 아티스트당 가장 임박한
일정 하나씩만 임박한 순으로 보여줍니다.

### LIVE MD 이미지 — Figma 스크린샷으로 직접 캡처

`figma.com` 이 조직 egress 정책으로 차단돼(403) `download_assets` 의 원본 다운로드 URL은
받을 수 없었지만, `get_screenshot` 응답에 실리는 픽셀(base64)은 받을 수 있어서 그 경로로
채웠습니다.

| 파일 | 캡처한 노드 | 용도 |
|---|---|---|
| `assets/prod/306.png` · `307.png` | `5749:63786` / `5749:63803` (ProductCard 안의 `Ratio`) | LIVE MD 카드 썸네일 — 시안에 실제로 같은 사진이 두 카드에 그대로 쓰여 두 상품이 이 파일 하나를 공유합니다 |
| `assets/artist/장한음.png` | `5749:65086` (Avatar) | 아티스트 아바타(헤더 배지 · 다음 아티스트 칩). 원본이 20×20 이라 160×160 으로 업스케일했습니다 |

**배너 배경(`assets/banner/livemd_장한음.jpg`)은 이 아바타 사진을 확대·블러 처리해 만든
대체 이미지입니다.** Banner Area(`5749:63752`) 자체를 스크린샷하면 그 프레임의 다른 자식
레이어(`Meet Your Artist Event!` 타이틀·타이머 숫자 등)까지 그림 위에 이미 구워져 나오는데,
그 위에 우리 쪽 실시간 HTML 텍스트를 또 얹으면 같은 문구가 두 겹으로 겹쳐 보였습니다
(먼저 이렇게 반영했다가 겹침을 발견하고 원상복구했습니다). 배경 전용 원본 사진을 구할 방법이
없어 아바타 사진으로 대신했습니다 — 더 나은 원본이 생기면 같은 경로에 덮어쓰면 됩니다.

### 아직 채워지지 않은 에셋

| 경로 | 쓰이는 곳 |
|---|---|
| `assets/artist/nct.*` · `seventeen.*` | Fan's Pick 1·2위 아바타 |

메인 배너 4장, LIVE MD 상품 썸네일·아바타는 채워졌습니다.

확장자는 `.webp / .jpg / .jpeg / .png` 순으로 탐색합니다. 파일이 없으면 배너는 시안에서
실측한 배경 그라디언트만, 아바타·썸네일은 이니셜 자리표시로 떨어집니다.
