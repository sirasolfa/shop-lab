#!/usr/bin/env python3
"""NOVERA shop — 모바일 홈 개편 프로토타입 빌더 (v2).

Figma  : [NOVERA] Shop / Handoff / Mobile (4869:77378)
DS     : Storybook(develop--693fcc16142e19f5d9fb6f9c.chromatic.com)
         - Foundation/Colors  → primitive + semantic 토큰
         - Foundation/Icon    → viewBox 0 0 24 24, size 16/20/24/32/48
         - Foundation/Typo    → display1~caption2 19종
         - Foundation/Rounded → none/xxs/xs/sm/md/lg/xl/full
         - Components/Badge, Avatar, Tabs
Data   : shop.novera.town 실제 상품 / shop-api.novera.town
출력   : ./NOVERA_shop_home_mobile.html  (에셋 전부 data URI 인라인)
"""
from __future__ import annotations

import base64
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
ASSETS = ROOT / "assets"
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
NDS_ICONS = json.loads((ASSETS / "nds_icons.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- helpers
def datauri(path: pathlib.Path) -> str:
    mime = {
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }[path.suffix]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def icon(name: str, size: int, cls: str = "") -> str:
    """NDS 아이콘. 모든 글리프는 24×24 viewBox 기준 — DS Foundation/Icon 규격."""
    d = NDS_ICONS[name]
    extra = f" {cls}" if cls else ""
    return (
        f'<svg class="ico{extra}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" aria-hidden="true"><path fill="currentColor" d="{d}"/></svg>'
    )


def brand_svg(name: str) -> str:
    return (ASSETS / "brand" / f"{name}.svg").read_text(encoding="utf-8").replace("\n", "")


def quickmenu_icon(name: str) -> str:
    """퀵메뉴용 풀컬러 3D 스타일 아이콘 (직접 제작, gradient 기반). 36px 기준."""
    return (ASSETS / "quickmenu" / f"{name}.svg").read_text(encoding="utf-8").replace("\n", "")


def sidenav_icon(name: str, size: int = 20) -> str:
    """사이드 내비 아이콘 — Figma Left Sidebar(5443:57347)에서 그대로 받은 SVG.
    아이콘마다 viewBox 가 제각각이라 원본 viewBox 는 살리고 렌더 박스만 고정한다.
    색은 하드코딩돼 있어 currentColor 로 바꿔 활성/비활성 상태를 CSS 로 제어한다.
    preserveAspectRatio="none" 는 정사각 박스에 넣으면 찌그러지므로 제거."""
    svg = (ASSETS / "sidenav" / f"{name}.svg").read_text(encoding="utf-8").replace("\n", "")
    svg = svg.replace(' preserveAspectRatio="none"', "")
    svg = re.sub(r'fill="#(?:697180|4F7CFF)"', 'fill="currentColor"', svg, flags=re.I)
    svg = re.sub(r'^<svg[^>]*?width="[^"]*"', "<svg", svg, count=1)
    svg = re.sub(r'\sheight="[\d.]+"(?=[^>]*viewBox)', " ", svg, count=1)
    return svg.replace(
        "<svg", f'<svg class="sn-ico" width="{size}" height="{size}" aria-hidden="true"', 1
    )


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def won(n: int) -> str:
    return f"{n:,}"


# ---------------------------------------------------------------- 컴포넌트
def product_card(p: dict, badge: str | None = None) -> str:
    """NDS ProductCard (140px). Image Area 1:1 + Bottom Container."""
    img = datauri(ASSETS / "prod" / f"{p['id']}.jpg")
    top_badge = ""
    if badge:
        top_badge = f'<span class="pc-badge">{esc(badge)}</span>'
    elif p.get("best"):
        top_badge = '<span class="pc-badge">BEST</span>'

    chips = []
    if p.get("free"):
        chips.append(
            '<span class="badge badge--positive">'
            + icon("Delivery", 14)
            + "무료배송</span>"
        )
    if p.get("new"):
        chips.append('<span class="badge badge--warning">NEW</span>')
    if p.get("soon"):
        chips.append('<span class="badge badge--warning">품절임박</span>')

    # 이벤트 상품은 event_at 을 카드에 실어 둔다 — 섹션 카운트다운이 이 값을 읽는다
    at = f' data-event-at="{esc(p["event_at"])}"' if p.get("event_at") else ""

    # 카드 전체가 상품 상세로 이동 (실제 서비스와 동일 경로)
    return f"""<a class="pcard" href="https://shop.novera.town/products/{p['id']}"{at}>
  <div class="pcard-img">
    <img src="{img}" alt="{esc(p['name'])}" loading="lazy">
    {top_badge}
    <span class="pcard-scrim"></span>
    <button class="pcard-wish" type="button" aria-label="찜하기">{icon('Heart', 20)}</button>
  </div>
  <div class="pcard-body">
    <div class="pcard-title">
      <p class="pcard-brand">{esc(p['brand'])}</p>
      <p class="pcard-name">{esc(p['name'])}</p>
    </div>
    <div class="pcard-price-area">
      <p class="price"><span class="price-cur">KRW</span><span class="price-sym">₩</span><span class="price-num">{won(p['price'])}</span></p>
      <div class="badges">{''.join(chips)}</div>
    </div>
  </div>
</a>"""


def section_header(title: str, sub: str | None = None, action: str | None = None) -> str:
    action_html = ""
    if action:
        action_html = (
            f'<button class="text-btn" type="button">{esc(action)}'
            + icon("ChevronRight", 18)
            + "</button>"
        )
    sub_html = f'<p class="sec-sub">{esc(sub)}</p>' if sub else ""
    return f"""<div class="sec-head">
  <div class="sec-head-text"><h2 class="sec-title">{esc(title)}</h2>{sub_html}</div>
  {action_html}
</div>"""


def product_row(items, badge=None) -> str:
    cards = "".join(product_card(p, badge) for p in items)
    # 마지막 카드 뒤 우측 거터(20px) 스페이서 — flex 스크롤 컨테이너에서
    # padding-right 가 무시되는 브라우저 이슈 방지
    return f'<div class="prow">{cards}<i class="row-end"></i></div>'


# ---------------------------------------------------------------- 섹션 데이터
S = DATA["sections"]

# Figma 4872:80651 업데이트: "Who's Your Bias?" 아티스트 아바타 행이
# 카테고리 바로가기 "퀵메뉴"로 교체됨 (48px 라운드 스퀘어 + 라벨, 2행×5열로
# 같은 5개 항목이 반복 배치돼 있었음 — 자리 채우기용 목업으로 보고 1행 5개로 정리).
# 아이콘은 Figma 쪽에 아직 채워지지 않은 빈 그라디언트 사각형이라 직접 제작.
# 링크는 라이브 사이트 실제 카테고리 경로.
# Figma 5612:54901 기준 라벨 — 카테고리 바로가기에서 "이벤트 바로가기"로 성격이 바뀌었다.
# 시안의 아이콘 자리는 아직 빈 그라디언트 사각형이라 앞의 3종은 직접 제작했다.
# 이벤트 3종은 라이브 사이트에 대응 카테고리 경로가 아직 없어 LIVE MD(PCTGY3)로 보낸다.
QUICKMENU = [
    ("videocall", "비디오콜", "https://shop.novera.town/categories/PCTGY3"),
    ("fansign", "팬사인회", "https://shop.novera.town/categories/PCTGY3"),
    ("offline_event", "대면 이벤트", "https://shop.novera.town/categories/PCTGY3"),
    ("photocard", "포토/카드", "https://shop.novera.town/categories/PCTGY2/PCTGY2_2"),
    ("lightstick", "응원봉", "https://shop.novera.town/categories/PCTGY2/PCTGY2_5"),
]

# Fan's Pick TOP3 — 실제 아티스트 + Figma 시안의 찜 수치(실 데이터 미제공)
PODIUM = [
    dict(key="kep1er", name="케플러", count=9820, rank="2nd", place="second"),
    dict(key="tws", name="투어스", count=12456, rank="1st", place="first"),
    dict(key="babymonster", name="베이비몬스터", count=8120, rank="3rd", place="third"),
]

# hero 배경색은 각 배너 이미지 가장자리에서 실측한 색 (PIL 로 좌우 6열 평균) --
# object-fit:contain 으로 바뀌면서 생기는 좌우 여백을 그 배너 고유 톤으로 자연스럽게 채움
COLLECTIONS = [
    dict(key="zo", tab="ZO&FRIENDS", hero="col_zo", hero_bg="#46a9f6", overlay=False,
         title="ZO&FRIENDS Collection",
         desc="사랑스러운 조앤프렌즈를 NOVERA shop에서 만나보세요",
         items=S["col_zo"]),
    dict(key="km", tab="귀멸의 칼날", hero="col_km", hero_bg="#05060b", overlay=True,
         badge="New release", headline="귀멸의 칼날<br>COLLECTION",
         title="귀멸의 칼날 Collection",
         desc="전집중! 귀살대 굿즈를 NOVERA shop에서 만나보세요",
         items=S["col_km"]),
    dict(key="doy", tab="도영", hero="col_doy", hero_bg="#eddda3", overlay=False,
         title="도영 [ Yours ] Collection",
         desc="2025 DOYOUNG ENCORE CONCERT 공식 MD",
         items=S["col_doy"]),
    dict(key="yjs", tab="윤종신", hero="col_yjs", hero_bg="#a7a4a5", overlay=False,
         title="〈윤종신 그리고 나〉 Collection",
         desc="윤종신의 행보 시리즈를 NOVERA shop에서 만나보세요",
         items=S["col_yjs"]),
    dict(key="kep", tab="Kep1asia", hero="col_kep", hero_bg="#d64d1f", overlay=False,
         title="케플러 Kep1asia Official MD",
         desc="2025 Kep1er CONCERT TOUR 공식 MD",
         items=S["col_kep"]),
]

CAT_TABS = [
    ("HOME", True, False),
    ("LIVE MD", False, True),
    ("COLLECTION", False, False),
    ("ARTIST", False, False),
    ("SPHERE", False, True),
]

# Figma 5612:54824 / Main Banner(5664:102707·102734·102763·102792) 4장.
# bg 는 각 슬라이드 Background Image 프레임의 그라디언트 실측값 — 사진이 없어도
# 배너가 시안의 톤 그대로 서 있게 하는 바탕이다.
# img 는 assets/banner/ 에 있으면 얹고 없으면 그라디언트만 남긴다 (파일명 규칙만
# 지켜 두면 Figma export 를 넣는 순간 그대로 반영된다).
MAIN_BANNERS = [
    dict(kind="vari", label="1st SINGLE [Dear]",
         title="VARI(베리)<br>VIDEO CALL EVENT",
         bg="linear-gradient(180deg,#ebfcff 0%,#08a2c2 100%)",
         img="main_vari"),
    dict(kind="kimetsu", label="코스모시 x 귀멸의 칼날",
         title="코스모시와 함께<br>전집중전 전시 팝업 관람!",
         bg="linear-gradient(180deg,#6ac3f0 42.57%,#0072e4 100%)",
         img="main3"),
    dict(kind="beboys", label="1st SINGLE [BE:2]",
         title="BE BOYS (비보이즈)<br>UNIT CALL EVENT",
         bg="linear-gradient(180deg,#d1e9ff 0%,#1871bf 100%)",
         img="main_beboys"),
    # 쿠폰 배너는 Background Image 프레임을 통째로 내보낸 이미지라
    # 그라디언트·카드·그림자가 이미 합쳐져 있다
    dict(kind="coupon", label="WELCOME COUPON",
         title="회원가입만 해도<br>전상품 1,000원 즉시 할인!",
         bg="linear-gradient(180deg,#ebfcff 0%,#08a2c2 100%)",
         img="main1"),
]

# 배너 이미지 확장자 탐색 순서 — Figma export 가 무엇으로 떨어지든 집어 오도록
BANNER_EXTS = (".webp", ".jpg", ".jpeg", ".png")


def banner_img(stem: str) -> str | None:
    """assets/banner/<stem>.<ext> 가 있으면 data URI, 없으면 None."""
    for ext in BANNER_EXTS:
        p = ASSETS / "banner" / f"{stem}{ext}"
        if p.exists():
            return datauri(p)
    return None


def build_banners() -> str:
    """Figma Bottom Container(5664:102715) 구조 그대로 —
    텍스트와 페이지네이션이 같은 컨테이너 안에 있고 함께 페이드된다."""
    out = []
    total = len(MAIN_BANNERS)
    for i, b in enumerate(MAIN_BANNERS):
        src = banner_img(b["img"])
        img = f'<img src="{src}" alt="">' if src else ""
        out.append(
            f"""<div class="mb-slide" data-slide="{i}" role="button" tabindex="0"
     aria-label="메인 배너 {i + 1} — 눌러서 배너 등록 화면 열기">
  <div class="mb-bg mb-bg--{b['kind']}" style="background:{b['bg']}">{img}</div>
  <div class="mb-dim"></div>
  <div class="mb-bottom">
    <div class="mb-text"><p class="mb-label">{b['label']}</p><p class="mb-title">{b['title']}</p></div>
    <div class="mb-pagination" aria-hidden="true"><span class="mb-page-cur">{i + 1:02d}</span>"""
            f"""<span class="mb-page-sep">|</span><span class="mb-page-tot">{total:02d}</span></div>
  </div>
</div>"""
        )
    return "".join(out)


# ------------------------------ Meet Your Artist Event (Showcase Banner)
# Figma 5749:63751 "Concept 3 - Showcase Banner"
#   Banner Area(5749:63752)       다크 쇼케이스 배너 + 구매 종료 카운트다운
#   Overlapping Cards(5749:63783) 배너 위로 30px 올라탄 가로형 카드 2장
#   NextArtistPreview(5749:63826) 다음 아티스트 칩 (가로 스크롤)
#
# 시안의 "01 : 02 : 40 : 30" 과 "오늘 오후 8:00" 은 목업 숫자다. 여기서는
# data.json 의 event_at(상품명 앞머리 "[09.05 …]" 를 승격시킨 ISO 일시) 을 넘겨주고,
# 브라우저가 볼 때마다 가장 가까운 미래를 골라 실제로 카운트다운하고 상대 시각을 만든다.
CD_UNITS = [("d", "DAY"), ("h", "HRS"), ("m", "MIN"), ("s", "SEC")]

# 시안이 카드에 얹는 칩 수 — Overlapping Cards 는 2장이다
SHOWCASE_CARDS = 2


def event_items() -> list[dict]:
    """event_at 이 있는 이벤트 상품을 임박한 순으로."""
    return sorted(
        (p for p in S["event"] if p.get("event_at")), key=lambda p: p["event_at"]
    )


def _meta_row(p: dict) -> str:
    """Inline Meta Row(5749:63813) — 달력·인원·혜택.
    실제 데이터에 있는 값만 그린다. 인원(limit_count)·혜택(perk) 은 API 가
    내려주기 시작하면 그대로 채워진다."""
    cells = [
        f'<span class="em-cell">{icon("Calendar", 12)}'
        f'<span>{p["event_at"][5:10].replace("-", ".")}</span></span>'
    ]
    if p.get("limit_count"):
        cells.append(
            f'<span class="em-cell">{icon("User", 12)}'
            f'<span>{esc(p["limit_count"])}명</span></span>'
        )
    if p.get("perk"):
        cells.append(
            f'<span class="em-cell">{icon("Gift", 12)}<span>{esc(p["perk"])}</span></span>'
        )
    sep = '<i class="em-sep"></i>'
    return f'<div class="ecard-meta">{sep.join(cells)}</div>'


def _event_card(p: dict) -> str:
    img = datauri(ASSETS / "prod" / f"{p['id']}.jpg")
    chips = []
    if p.get("perk"):
        chips.append(
            f'<span class="ebadge ebadge--primary">{icon("Gift", 12)}'
            f'{esc(p["perk"])}</span>'
        )
    if p.get("limit_count"):
        chips.append(
            f'<span class="ebadge ebadge--warning">{icon("User", 12)}'
            f'{esc(p["limit_count"])}명 한정</span>'
        )
    elif p.get("new"):
        chips.append('<span class="ebadge ebadge--warning">NEW</span>')
    chip_html = f'<div class="ecard-chips">{"".join(chips)}</div>' if chips else ""

    return f"""<a class="ecard" href="https://shop.novera.town/products/{p['id']}"
   data-event-at="{esc(p['event_at'])}">
  <span class="ecard-img">
    <img src="{img}" alt="" loading="lazy">
    <span class="ecard-kind">VIDEO CALL</span>
  </span>
  <span class="ecard-body">
    <span class="ecard-head">
      <span class="ecard-brand-row">
        <span class="ecard-brand">{esc(p['brand'])}</span>{chip_html}
      </span>
      <span class="ecard-name">{esc(p['name'])}</span>
    </span>
    <span class="ecard-price-area">
      <span class="price"><span class="price-cur">KRW</span><span class="price-sym">₩</span><span class="price-num">{won(p['price'])}</span></span>
      {_meta_row(p)}
    </span>
  </span>
</a>"""


def _next_artists(items: list[dict]) -> str:
    """다음 아티스트 칩 — (아티스트, 일시) 중복을 걷어내고 임박한 순으로.
    시각 문구는 보는 시점에 따라 달라지므로 JS 가 data-at 으로 만든다."""
    seen, chips = set(), []
    for p in items:
        key = (p["brand"], p["event_at"])
        if key in seen:
            continue
        seen.add(key)
        img = datauri(ASSETS / "prod" / f"{p['id']}.jpg")
        chips.append(
            f'<div class="na-item" data-at="{esc(p["event_at"])}">'
            f'<span class="na-avatar"><img src="{img}" alt=""></span>'
            f'<span class="na-text"><span class="na-name">{esc(p["brand"])}</span>'
            f'<span class="na-time">--</span></span></div>'
        )
    if not chips:
        return ""
    return f'<div class="sb-next" id="nextArtists">{"".join(chips)}</div>'


def build_event_showcase() -> str:
    items = event_items()
    if not items:
        return ""
    lead = items[0]
    hero = datauri(ASSETS / "prod" / f"{lead['id']}.jpg")

    tiles = []
    for i, (key, cap) in enumerate(CD_UNITS):
        if i:
            tiles.append('<span class="cd-colon" aria-hidden="true">:</span>')
        tiles.append(
            f'<span class="cd-unit"><span class="cd-num" data-cd="{key}">--</span>'
            f'<span class="cd-cap">{cap}</span></span>'
        )
    deadlines = html.escape(
        json.dumps(sorted({p["event_at"] for p in items})), quote=True
    )
    cards = "".join(_event_card(p) for p in items[:SHOWCASE_CARDS])

    return f"""<section class="sec--showcase">
  <div class="sb-banner">
    <div class="sb-bg"><img src="{hero}" alt=""></div>
    <div class="sb-scrim"></div>
    <div class="sb-inner">
      <div class="sb-head">
        <div class="sb-toprow">
          <span class="sb-kind">LIVE MD</span>
          <button class="sb-more" type="button">전체보기{icon('ChevronRight', 14)}</button>
        </div>
        <div class="sb-titles">
          <p class="sb-title">Meet Your Artist Event!</p>
          <p class="sb-desc">최애 아티스트를 만날 수 있는 특별한 이벤트</p>
        </div>
      </div>
      <div class="sb-meta">
        <div class="sb-artist">
          <p class="sb-cap">아티스트</p>
          <div class="sb-artist-row">
            <span class="sb-artist-avatar"><img src="{hero}" alt=""></span>
            <p class="sb-artist-name">{esc(lead['brand'])}</p>
          </div>
        </div>
        <div class="sb-timer" id="eventCountdown" data-deadlines="{deadlines}">
          <p class="sb-cap" id="cdLabelText">구매 종료까지</p>
          <div class="cd-clock" role="timer" aria-live="off">{''.join(tiles)}</div>
        </div>
      </div>
    </div>
  </div>
  <div class="sb-cards">{cards}</div>
  {_next_artists(items)}
</section>"""


QUICKMENU_STAGGER = 70  # 셀당 등장 간격(ms) — 좌 → 우


def build_quickmenu() -> str:
    cells = []
    for i, (icon_key, label, href) in enumerate(QUICKMENU):
        cells.append(
            f"""<a class="qm-item" href="{href}" target="_blank" rel="noreferrer" style="--d:{i * QUICKMENU_STAGGER}ms">
  <span class="qm-sq">{quickmenu_icon(icon_key)}</span>
  <span class="qm-label">{esc(label)}</span>
</a>"""
        )
    return f'<div class="qm-list" id="quickmenu-list">{"".join(cells)}</div>'


# Fan's Pick 등장 타임라인 — Figma 모션 키프레임(5612:54981·54990·54992·55002·
# 55004·55013, 16.4s 타임라인 기준)에서 그대로 옮긴 값.
#   ① 시상대(Rectangle)가 아래에서 올라오며 페이드인 (opacity 300ms / y 500ms 스프링)
#   ② 그 위 콘텐츠(아바타·순위 뱃지·이름·찜 수)가 위에서 톡 내려앉음
#      (opacity 300ms / y -8→0 400ms / scale .7→1 450ms 스프링)
# 순서는 3위 → 2위 → 1위.
PODIUM_TIMING = {           # place: (시상대 delay, 콘텐츠 delay, 시상대 시작 y)
    "third":  (0,   200, 40),
    "second": (250, 500, 55),
    "first":  (500, 750, 80),
}


def build_podium() -> str:
    stands = []
    for p in PODIUM:
        img = datauri(ASSETS / "artist" / f"{p['key']}.jpg")
        crown = '<span class="crown">👑</span>' if p["place"] == "first" else ""
        d_bar, d_content, from_y = PODIUM_TIMING[p["place"]]
        style = f"--d-bar:{d_bar}ms;--d-content:{d_content}ms;--bar-from:{from_y}px"
        stands.append(
            f"""<div class="stand stand--{p['place']}" style="{style}" data-delay="{d_content}">
  <div class="stand-top">
    <div class="stand-avatar">{crown}
      <span class="avatar avatar--48"><img src="{img}" alt="{esc(p['name'])}"></span>
      <span class="rank rank--{p['place']}">{p['rank']}</span>
    </div>
    <div class="stand-meta">
      <p class="stand-name">{esc(p['name'])}</p>
      <p class="stand-count">{icon('HeartFill', 14)}<span class="count" data-to="{p['count']}">0</span></p>
    </div>
  </div>
  <div class="stand-block-wrap"><div class="stand-block"></div></div>
</div>"""
        )
    return f'<div class="podium" id="podium">{"".join(stands)}</div>'


def build_collections() -> str:
    tabs, panels = [], []
    for i, c in enumerate(COLLECTIONS):
        active = " is-active" if i == 0 else ""
        tabs.append(
            f'<button class="tab{active}" type="button" data-col="{c["key"]}">'
            f'<span class="tab-label">{esc(c["tab"])}</span><span class="tab-underline"></span></button>'
        )
        hero_src = datauri(ASSETS / "banner" / f"{c['hero']}.jpg")
        overlay = ""
        if c.get("overlay"):
            overlay = f"""<div class="col-hero-text">
  <span class="col-hero-badge">{esc(c['badge'])}</span>
  <p class="col-hero-headline">{c['headline']}</p>
</div>"""
        panels.append(
            f"""<div class="col-panel{active}" data-col="{c['key']}">
  <div class="col-hero{' col-hero--overlay' if c.get('overlay') else ''}" style="--col-bg:{c['hero_bg']}">
    <img src="{hero_src}" alt="{esc(c['title'])}">{overlay}
  </div>
  <div class="col-body">
    <div class="col-head">
      <h3 class="col-title">{esc(c['title'])}</h3>
      <p class="col-desc">{esc(c['desc'])}</p>
    </div>
    {product_row(c['items'])}
  </div>
</div>"""
        )
    return f"""<section class="sec sec--collection">
  <div class="col-top">
    <h2 class="sec-title">NOVERA shop Collection</h2>
  </div>
  <div class="tabbar tabbar--collection"><div class="tabs"><div class="tabs-inner">{''.join(tabs)}</div></div></div>
  <div class="col-panels">{''.join(panels)}</div>
</section>"""


def build_cat_tabs() -> str:
    out = []
    for label, active, new in CAT_TABS:
        cls = " is-active" if active else ""
        badge = '<span class="tab-n">N</span>' if new else ""
        out.append(
            f'<button class="tab{cls}" type="button"><span class="tab-label">{esc(label)}{badge}</span>'
            '<span class="tab-underline"></span></button>'
        )
    return ('<nav class="tabbar tabbar--category"><div class="tabs">'
            f'<div class="tabs-inner">{"".join(out)}</div></div></nav>')


def build_footer() -> str:
    """Figma Footer(5257:59492). 메뉴 13/600 #888e9c, 개인정보처리방침만 14/600 #a6acb7.
    <b> 태그는 쓰지 않는다 — Pretendard Variable 에서 bolder 가 900 으로 해석됨."""
    menu = ["공지사항", "FAQ", "이용약관"]
    menu_html = "".join(f'<a class="ft-menu-item" href="#">{esc(m)}</a>' for m in menu)
    menu_html += '<a class="ft-menu-item ft-menu-item--strong" href="#">개인정보처리방침</a>'

    def pair(label, value, link=None):
        v = f'<span class="ft-val">{value}</span>'
        if link:
            v += f'<a class="ft-link" href="{link[1]}">{esc(link[0])}</a>'
        return f'<span class="ft-pair"><span class="ft-key">{esc(label)}</span>{v}</span>'

    sep = ""
    row1 = sep.join([
        pair("상호", "(주)다날엔터테인먼트"),
        pair("대표이사", "현능호"),
        pair("주소", "(13595) 경기도 성남시 분당구 백현로 93, 11층(수내동, 후너스빌딩)"),
        pair("사업자등록번호", "129-86-70437"),
        pair("통신판매업신고번호", "2012-경기성남-0116", ("정보확인", "#")),
    ])
    row2 = sep.join([
        pair("개인정보보호관리책임자", "현능호"),
        pair("호스팅 제공자", "아마존웹서비스(AWS)"),
        f'<span class="ft-pair"><span class="ft-key">CS센터/문의</span>'
        f'<a class="ft-link" href="mailto:cs@novera.town">cs@novera.town</a></span>',
    ])

    return f"""<footer class="footer">
  <div class="ft-divider"></div>
  <div class="ft-contents">
    <div class="ft-top">
      <div class="ft-logo">{brand_svg('danal')}</div>
      <nav class="ft-menu">{menu_html}</nav>
    </div>
    <div class="ft-info">
      <div class="ft-info-row">{row1}</div>
      <div class="ft-info-row">{row2}</div>
    </div>
    <div class="ft-sns">
      <a class="ft-sns-item" href="#" aria-label="X">{brand_svg('x')}</a>
      <a class="ft-sns-item" href="#" aria-label="Instagram">{brand_svg('insta')}</a>
    </div>
    <div class="ft-rights">
      <div class="ft-divider"></div>
      <p class="ft-copy">© 2026 DANAL Entertainment.Co., Ltd. All rights reserved.</p>
    </div>
  </div>
</footer>"""


def build_banner_sheet() -> str:
    """메인 배너를 누르면 열리는 어드민 등록 시트.
    배경 이미지 + 텍스트만 입력하면 딤/타이포/페이지네이션은 자동 합성된다."""
    return f"""<div class="scrim" id="bnScrim" hidden></div>
<section class="sheet" id="bnSheet" role="dialog" aria-modal="true" aria-labelledby="bnSheetTitle" hidden>
  <div class="sheet-grip"></div>
  <header class="sheet-head">
    <div class="sheet-head-text">
      <h2 class="sheet-title" id="bnSheetTitle">메인 배너 등록</h2>
      <p class="sheet-desc">배경 이미지와 텍스트만 입력하면 나머지는 자동으로 만들어져요.</p>
    </div>
    <button class="sheet-close" type="button" id="bnClose" aria-label="닫기">{icon('X', 20)}</button>
  </header>

  <div class="sheet-body">
    <div class="field">
      <p class="field-label">미리보기</p>
      <div class="bn-preview" id="bnPreview">
        <div class="mb-bg mb-bg--coupon"><img id="bnPvImg" src="" alt=""></div>
        <div class="mb-dim"></div>
        <div class="mb-bottom mb-bottom--preview">
          <div class="mb-text">
            <p class="mb-label" id="bnPvLabel"></p>
            <p class="mb-title" id="bnPvTitle"></p>
          </div>
          <div class="mb-pagination-inline"><span class="mb-page-cur" id="bnPvPage">01</span><span class="mb-page-sep">|</span><span class="mb-page-tot">{len(MAIN_BANNERS):02d}</span></div>
        </div>
      </div>
    </div>

    <div class="field">
      <p class="field-label">배경 이미지<span class="field-req">필수</span></p>
      <label class="upload" for="bnFile">
        <input type="file" id="bnFile" accept="image/*" hidden>
        <span class="upload-thumb"><img id="bnThumb" src="" alt=""></span>
        <span class="upload-text">
          <span class="upload-title">이미지 업로드</span>
          <span class="upload-hint">권장 750×640 (2x) · JPG / PNG / WebP</span>
        </span>
      </label>
      <p class="upload-check" id="bnCheck" hidden></p>
    </div>

    <div class="field">
      <p class="field-label">라벨<span class="field-count" id="bnLabelCount">0/24</span></p>
      <input class="input" id="bnLabel" maxlength="24" placeholder="예) WELCOME COUPON">
    </div>

    <div class="field">
      <p class="field-label">타이틀<span class="field-count" id="bnTitleCount">0/60</span></p>
      <textarea class="input input--area" id="bnTitle" rows="2" maxlength="60"
        placeholder="예) 회원가입만 해도&#10;전상품 1,000원 즉시 할인!"></textarea>
    </div>

    <div class="field">
      <p class="field-label">연결 링크<span class="field-hint">선택</span></p>
      <input class="input" id="bnLink" placeholder="https://shop.novera.town/...">
    </div>

    <div class="auto-note">
      <p class="auto-note-title">{icon('Notice', 16)}자동으로 적용되는 항목</p>
      <ul class="auto-note-list">
        <li>업로드한 이미지가 배너 전체를 꽉 채움 (가로세로 비율은 유지, 넘치는 부분만 크롭)</li>
        <li>하단 그라데이션 딤 (0% → 16% → 64%)</li>
        <li>라벨 12·SemiBold / 타이틀 20·Bold 타이포와 좌우 여백</li>
        <li>슬라이드 순번 페이지네이션과 4초 자동 롤링</li>
      </ul>
    </div>
  </div>

  <footer class="sheet-foot">
    <button class="btn btn--ghost" type="button" id="bnCancel">취소</button>
    <button class="btn btn--solid" type="button" id="bnApply">배너 적용</button>
  </footer>
</section>
<div class="bn-toast" id="bnToast">{icon('CircleCheckFill', 16)}<span id="bnToastMsg">배너가 적용되었어요</span></div>"""


# Figma Left Sidebar(5443:57347) 항목 순서 그대로. (아이콘, 라벨, 링크, NEW배지)
SIDENAV_MAIN = [
    ("home", "홈", "https://shop.novera.town/", False),
    ("album", "ALBUM", "https://shop.novera.town/categories/PCTGY1", False),
    ("livemd", "LIVE MD", "https://shop.novera.town/categories/PCTGY3", True),
    ("collection", "COLLECTION", "https://shop.novera.town/exhibitions", False),
    ("profile", "ARTIST", "https://shop.novera.town/artists", False),
    ("sphere", "SPHERE", "https://shop.novera.town/kimetsu_ex_kr", True),
    ("event", "EVENT", "https://shop.novera.town/categories/PCTGY3", False),
]
SIDENAV_BOTTOM = [
    ("bag", "장바구니", "https://shop.novera.town/cart"),
    ("heart", "좋아요", "https://shop.novera.town/likes"),
    ("user", "마이페이지", "https://shop.novera.town/sign-in"),
]


def build_sidenav() -> str:
    """486px 위에서 노출되는 고정 사이드 내비게이션.
    Figma Left Sidebar(5443:57347) 실측: 폭 280 / 그룹 padding 24·16 / 항목 gap 2 /
    항목 padding 12·16, gap 12, rounded 8 / 라벨 Action/2 (14 SemiBold, tracking-1) /
    활성 항목만 bg #eef3ff + text #4f7cff, 나머지는 #4b5465."""
    def row(ic, label, href, new, active=False):
        badge = '<span class="sn-n">N</span>' if new else ""
        cls = " is-active" if active else ""
        return (
            f'<a class="sn-item{cls}" href="{href}" target="_blank" rel="noreferrer">'
            f'{sidenav_icon(ic)}<span class="sn-label">{esc(label)}{badge}</span></a>'
        )

    main = "".join(
        row(ic, label, href, new, active=(i == 0))
        for i, (ic, label, href, new) in enumerate(SIDENAV_MAIN)
    )
    bottom = "".join(row(ic, label, href, False) for ic, label, href in SIDENAV_BOTTOM)
    return f"""<aside class="sidenav" aria-label="사이드 내비게이션">
  <nav class="sn-group">{main}</nav>
  <div class="sn-divider"></div>
  <nav class="sn-group">{bottom}</nav>
</aside>"""


def build_notice_bar() -> str:
    """상단 고지 배너 — Figma Inline Banner(5439:86728) 레이아웃을 그대로 따르되
    (가운데 정렬 텍스트 + 우측 20px 닫기 아이콘 20px, Label/3 13·SemiBold/tracking-1)
    색상만 요청대로 블랙 배경 · 화이트 텍스트로 바꿨다."""
    return f"""<div class="noticebar" id="noticeBar" role="status">
  <p class="noticebar-text">디자인 시안으로 제작된 프로토타입입니다.</p>
  <button class="noticebar-close" type="button" id="noticeClose" aria-label="안내 닫기">{icon('X', 20)}</button>
</div>"""


SITE = "https://shop.novera.town"

# 라이브 사이트 GNB 와 동일한 라벨/링크
DRAWER_MENU = [
    ("ALBUM", f"{SITE}/categories/PCTGY1", False),
    ("MD", f"{SITE}/categories/PCTGY2", False),
    ("LIVE MD", f"{SITE}/categories/PCTGY3", False),
    ("COLLECTION", f"{SITE}/exhibitions", False),
    ("ARTIST", f"{SITE}/artists", False),
    ("SPHERE", f"{SITE}/kimetsu_ex_kr", True),
]

DRAWER_UTIL = [
    ("User", "로그인", f"{SITE}/sign-in"),
    ("Heart", "좋아요", f"{SITE}/likes"),
    ("Bag", "장바구니", f"{SITE}/cart"),
]


def build_drawer() -> str:
    """좌측 사이드 드로어 내비게이션. 헤더의 햄버거 버튼으로 열고,
    스크림 탭 / ESC / 링크 선택 시 닫힌다. 라벨·링크는 라이브 GNB 와 동일."""
    menu = "".join(
        f'<a class="dw-item" href="{href}" target="_blank" rel="noreferrer">'
        f'<span class="dw-item-label">{esc(label)}'
        f'{"<span class=" + chr(34) + "dw-n" + chr(34) + ">N</span>" if new else ""}</span>'
        f'{icon("ChevronRight", 16, "dw-caret")}</a>'
        for label, href, new in DRAWER_MENU
    )
    util = "".join(
        f'<a class="dw-util" href="{href}" target="_blank" rel="noreferrer">'
        f'{icon(ic, 20)}<span>{esc(label)}</span></a>'
        for ic, label, href in DRAWER_UTIL
    )
    return f"""<div class="dw-scrim" id="dwScrim" hidden></div>
<aside class="drawer" id="drawer" aria-label="전체 메뉴" aria-hidden="true" hidden>
  <header class="dw-head">
    <a class="dw-logo" href="{SITE}/" target="_blank" rel="noreferrer">{brand_svg('logo-novera-shop')}</a>
    <button class="dw-close" type="button" id="dwClose" aria-label="메뉴 닫기">{icon('X', 20)}</button>
  </header>
  <div class="dw-search">{icon('Search', 18)}<span>검색어를 입력해 주세요</span></div>
  <nav class="dw-menu">{menu}</nav>
  <div class="dw-divider"></div>
  <nav class="dw-utils">{util}</nav>
  <div class="dw-foot">
    <button class="lang" type="button">{icon('Globe', 16)}KO</button>
  </div>
</aside>"""


def build_bottom_nav() -> str:
    # (아이콘, 라벨, 활성, 요소 id) — 카테고리가 사이드 드로어를 여는 진입점이다
    items = [
        ("HomeFill", "홈", True, None),
        ("Category", "카테고리", False, "dwOpen"),
        ("Heart", "좋아요", False, None),
        ("User", "마이", False, None),
    ]
    cells = ""
    for ic, label, act, el_id in items:
        attrs = ' id="dwOpen" aria-controls="drawer" aria-expanded="false"' if el_id else ""
        cells += (
            f'<button class="bn-item{" is-active" if act else ""}" type="button"{attrs}>'
            f'{icon(ic, 24)}<span>{esc(label)}</span></button>'
        )
    return f"""<nav class="bottomnav" id="bottomnav">
  <div class="bn-items">{cells}</div>
  <div class="bn-home-indicator"><span></span></div>
</nav>"""


# ---------------------------------------------------------------- CSS
CSS = """
/* =========================================================================
   NOVERA Design System — Storybook 토큰
   develop--693fcc16142e19f5d9fb6f9c.chromatic.com / Foundation/*
   ========================================================================= */
:root{
  /* --- primitive : Foundation/Colors --- */
  --gray-50:#fcfdff; --gray-100:#f9fafd; --gray-150:#f4f6fb; --gray-200:#edf0f5;
  --gray-300:#e3e6ee; --gray-400:#c5c9d3; --gray-500:#a6acb7; --gray-600:#888e9c;
  --gray-700:#697180; --gray-800:#4b5465; --gray-900:#2f3744; --gray-950:#171c24;
  --blue-50:#f9fbff; --blue-100:#eef3ff; --blue-200:#cedbff; --blue-500:#6f94ff;
  --blue-600:#4f7cff; --blue-700:#355fea;
  --red-100:#ffeef1; --red-500:#f9556e; --red-600:#e6374f;
  --green-100:#f1fcf4; --green-500:#3fbe75;
  --yellow-100:#fffaee; --yellow-500:#ffc439;
  --base-white:#fff; --base-black:#000;
  --alpha-black8:rgba(0,0,0,.08); --alpha-black16:rgba(0,0,0,.16);
  --alpha-black40:rgba(0,0,0,.4); --alpha-black64:rgba(0,0,0,.64);
  --alpha-white24:rgba(255,255,255,.24); --alpha-white40:rgba(255,255,255,.4);
  --alpha-white64:rgba(255,255,255,.64);
  --alpha-white80:rgba(255,255,255,.8);

  /* --- semantic : text / icon --- */
  --text-primary:var(--gray-900);   --text-secondary:var(--gray-700);
  --text-tertiary:var(--gray-600);  --text-muted:var(--gray-500);
  --text-disabled:var(--gray-400);  --text-inverse:var(--base-white);
  --text-positive:var(--green-500); --text-warning:var(--yellow-500);
  --text-negative:var(--red-600);
  --icon-primary:var(--gray-800);   --icon-secondary:var(--gray-600);
  --icon-muted:var(--gray-500);     --icon-fill:var(--gray-300);
  --icon-inverse:var(--base-white); --icon-positive:var(--green-500);

  /* --- semantic : bg / border --- */
  --bg-default:var(--base-white); --bg-subtle:var(--gray-100);
  --bg-muted:var(--gray-150);     --bg-gray:var(--gray-150);
  --bg-subtler:var(--gray-50);    --bg-inverse:var(--gray-900);
  --bg-darkgray:var(--gray-900);  --bg-darkgray-soft:var(--gray-700);
  --bg-darkgray-strong:var(--gray-950);
  --bg-positive:var(--green-100); --bg-warning:var(--yellow-100);
  --bg-primary:var(--blue-100);   --bg-negative:var(--red-100);
  --bg-mask:var(--alpha-black40); --bg-dim:var(--alpha-black64);
  --border-default:var(--gray-300); --border-strong:var(--gray-400);
  --border-thumbnail:var(--alpha-black8);

  /* --- brand --- */
  --brand1-default:var(--blue-600); --brand1-strong:var(--blue-700);
  --brand1-subtle:var(--blue-500);  --brand1-soft:var(--blue-100);

  /* --- rounded : Foundation/Rounded --- */
  --rounded-none:0; --rounded-xxs:4px; --rounded-xs:6px; --rounded-sm:8px;
  --rounded-md:12px; --rounded-lg:16px; --rounded-xl:24px; --rounded-full:999px;

  /* --- spacing : Foundation/Spacing --- */
  --spacing-2:2px;  --spacing-4:4px;  --spacing-8:8px;  --spacing-12:12px;
  --spacing-16:16px;--spacing-20:20px;--spacing-24:24px;--spacing-28:28px;
  --spacing-32:32px;--spacing-40:40px;

  /* --- componentSize --- */
  --componentSize-xs-height:26px; --componentSize-xs-iconSize:14px;
  --componentSize-sm-height:32px; --componentSize-sm-iconSize:16px;
  --componentSize-md-height:44px; --componentSize-md-iconSize:20px;
  --componentSize-lg-height:56px; --componentSize-lg-iconSize:24px;

  /* --- 자간 : Figma text style 의 letterSpacing 1 = 1% --- */
  --tracking-1:.01em;

  /* --- 모션 이징 : Figma 모션 키프레임에서 쓰는 두 커브 ---
     ease-out-quint 는 그대로 옮길 수 있고, 스프링은 linear() 를 지원하는
     브라우저에서만 원본 곡선으로 올린다 (아래 @supports) */
  --ease-out-quint:cubic-bezier(.22,1,.36,1);
  --ease-spring:cubic-bezier(.34,1.3,.64,1);

  /* --- 화면 좌우 거터 (Figma Mobile 375 기준) --- */
  --gutter:var(--spacing-20);          /* 본문 좌우 20px */
  --gutter-header:var(--spacing-16);   /* TopNavigation 16px */
  --gutter-tabs:var(--spacing-12);     /* 카테고리 탭바 12px (라벨 좌우 12 → 첫 라벨 24px) */
  --maxw:486px;
}

/* Figma 스프링(감쇠 진동) 곡선 원본 — linear() 이징을 지원하는 브라우저에서만 적용 */
@supports (transition-timing-function:linear(0,1)){
  :root{
    --ease-spring:linear(0, 0.0212, 0.0764, 0.1545, 0.2463, 0.3445, 0.4435, 0.5391,
      0.6282, 0.7091, 0.7805, 0.8421, 0.8939, 0.9365, 0.9704, 0.9967, 1.0162, 1.03,
      1.0389, 1.044, 1.0459, 1.0455, 1.0433, 1.04, 1.0359, 1.0314, 1.0269, 1.0224,
      1.0182, 1.0144, 1.011, 1.008, 1.0055, 1.0034, 1.0018, 1.0005, 0.9995, 0.9988,
      0.9983, 0.998, 0.9979, 0.9979, 0.998, 0.9981, 0.9983, 0.9985, 0.9987, 0.9989,
      0.9991, 0.9993, 0.9995);
  }
}

*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html{background:var(--bg-muted)}
body{
  font-family:'Pretendard Variable',Pretendard,-apple-system,BlinkMacSystemFont,
    'Apple SD Gothic Neo','Malgun Gothic',system-ui,sans-serif;
  color:var(--text-primary);background:var(--bg-muted);
  display:flex;justify-content:center;-webkit-font-smoothing:antialiased;
}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}
.ico{display:block;flex:none}

.app{
  position:relative;width:100%;max-width:var(--maxw);min-height:100vh;
  background:var(--bg-default);overflow-x:hidden;
  box-shadow:0 0 40px rgba(23,28,36,.12);
  padding-bottom:calc(80px + env(safe-area-inset-bottom));
}

/* ---------- 사이드 내비게이션 (Figma Left Sidebar 5443:57347) ---------- */
/* 486px 이하에서는 숨기고 햄버거+드로어를 쓴다 */
.sidenav{display:none}
@media (min-width:487px){
  /* 디자인의 페이지 배경(#fcfdff)과 사이드바 흰 배경. 콘텐츠 컬럼은 배경 위에
     그대로 얹히므로 모바일에서 쓰던 "휴대폰 카드" 그림자는 걷어낸다 */
  body{background:var(--gray-50);justify-content:flex-start}
  .app{margin-inline:auto;box-shadow:none}

  .sidenav{
    position:fixed;left:0;top:0;bottom:0;z-index:40;
    width:280px;display:flex;flex-direction:column;
    background:var(--bg-default);border-right:1px solid var(--gray-200);
    overflow-y:auto;overscroll-behavior:contain;
  }
  /* 사이드바가 차지한 폭만큼 본문 컬럼을 밀어 남는 영역 가운데 정렬 */
  body{padding-left:280px}

  /* 사이드바가 내비게이션을 대신하므로 모바일 하단 탭바는 감춘다.
     (드로어를 여는 "카테고리" 버튼도 하단 탭바 안에 있어 함께 사라진다) */
  .bottomnav{display:none}
  .app{padding-bottom:0}
}
.sn-group{display:flex;flex-direction:column;gap:2px;
  padding:var(--spacing-24) var(--spacing-16)}
/* 이 프로토타입의 --text-secondary 는 gray-700 에 물려 있는데 Figma 사이드바 라벨은
   text/secondary = gray-800(#4b5465) 이다. 전역 토큰을 건드리면 페이지 전반이
   같이 바뀌므로 여기서만 디자인 값에 맞춘다 */
.sn-item{display:flex;align-items:center;gap:var(--spacing-12);
  padding:var(--spacing-12) var(--spacing-16);border-radius:var(--rounded-sm);
  color:var(--gray-800)}
.sn-item:hover{background:var(--bg-gray)}
.sn-item.is-active{background:var(--bg-primary);color:var(--brand1-default)}
/* Figma 아이콘 프레임 실측 20x24 (글리프는 그 안에서 가운데 정렬) */
.sn-ico{flex:none;width:20px;height:24px;color:currentColor}
.sn-label{display:flex;align-items:center;gap:6px;
  font-size:14px;font-weight:600;line-height:1.5;letter-spacing:var(--tracking-1);
  white-space:nowrap}
.sn-n{padding:1px var(--spacing-4);border-radius:var(--rounded-xxs);
  background:var(--bg-negative);color:var(--text-negative);
  font-size:10px;font-weight:600;line-height:1.5}
.sn-divider{height:1px;background:var(--gray-200)}

/* ---------- 상단 고지 배너 (Figma Inline Banner 5439:86728) ---------- */
/* 텍스트는 배너 폭 기준 중앙, 닫기 버튼은 우측 20px 절대배치 -- 텍스트가 길어져도
   중앙 정렬이 닫기 버튼 때문에 밀리지 않는다 */
.noticebar{position:relative;display:flex;align-items:center;justify-content:center;
  min-height:36px;padding:var(--spacing-8) 48px;background:var(--gray-950)}
.noticebar-text{font-size:13px;font-weight:600;line-height:1.4;
  letter-spacing:var(--tracking-1);color:var(--text-inverse);text-align:center}
.noticebar-close{position:absolute;top:50%;right:20px;transform:translateY(-50%);
  display:flex;align-items:center;justify-content:center;padding:var(--spacing-4);
  color:var(--text-inverse);opacity:.7}
.noticebar-close:active{opacity:1}
.noticebar.is-closed{display:none}

/* ---------- TopNavigation ---------- */
.header{
  position:sticky;top:0;z-index:30;background:var(--bg-default);
  display:flex;align-items:center;height:52px;
  padding:var(--spacing-8) var(--gutter-header);
}
.header-inner{flex:1;display:flex;align-items:center;justify-content:space-between}
.logo{display:flex;margin-right:auto}
.logo svg{width:149px;height:18px}
.head-actions{display:flex;align-items:center;gap:var(--spacing-8)}
.head-icons{display:flex;align-items:center}
.touch{position:relative;display:flex;align-items:center;justify-content:center;
  padding:var(--spacing-8);color:var(--icon-primary)}
.push-badge{
  position:absolute;top:2px;right:2px;min-width:16px;height:16px;padding:0 var(--spacing-4);
  display:flex;align-items:center;justify-content:center;border-radius:var(--rounded-full);
  background:var(--brand1-default);color:var(--text-inverse);
  font-size:11px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.4;
}
.lang{
  display:flex;align-items:center;gap:var(--spacing-4);
  height:var(--componentSize-sm-height);padding:0 var(--spacing-12) 0 var(--spacing-8);
  border-radius:var(--rounded-xs);background:var(--bg-gray);
  font-size:12px;font-weight:600;letter-spacing:var(--tracking-1);color:var(--text-secondary);
}
.lang .ico{color:var(--icon-secondary)}

/* ---------- 좌측 사이드 드로어 ---------- */
/* 스크림/드로어는 .app 이 아니라 뷰포트 기준으로 띄운다 -- .app 은 overflow-x:hidden
   이라 그 안에 두면 닫힌 상태(translateX(-100%))가 잘려 애니메이션이 끊긴다 */
.dw-scrim{position:fixed;inset:0;z-index:60;background:rgba(0,0,0,.28);
  opacity:0;transition:opacity .28s ease}
.dw-scrim.is-open{opacity:1}
.drawer{
  position:fixed;left:0;top:0;bottom:0;z-index:61;
  width:min(320px,86vw);display:flex;flex-direction:column;
  background:var(--bg-default);box-shadow:2px 0 24px rgba(23,28,36,.18);
  transform:translateX(-100%);transition:transform .3s cubic-bezier(.32,.72,0,1);
  overflow-y:auto;overscroll-behavior:contain;
  padding-bottom:calc(var(--spacing-16) + env(safe-area-inset-bottom));
}
.drawer.is-open{transform:none}
.dw-head{display:flex;align-items:center;justify-content:space-between;
  height:52px;padding:var(--spacing-8) var(--spacing-16)}
.dw-logo{display:flex}
.dw-logo svg{width:132px;height:16px}
.dw-close{display:flex;align-items:center;justify-content:center;
  padding:var(--spacing-8);margin-right:calc(var(--spacing-8) * -1);color:var(--icon-primary)}
.dw-search{display:flex;align-items:center;gap:var(--spacing-8);
  margin:var(--spacing-8) var(--spacing-16) var(--spacing-12);
  height:40px;padding:0 var(--spacing-12);border-radius:var(--rounded-sm);
  background:var(--bg-gray);color:var(--text-muted);font-size:14px;line-height:1.4}
.dw-search .ico{color:var(--icon-muted)}
.dw-menu{display:flex;flex-direction:column;padding:0 var(--spacing-8)}
.dw-item{display:flex;align-items:center;justify-content:space-between;gap:var(--spacing-8);
  padding:var(--spacing-12) var(--spacing-8);border-radius:var(--rounded-sm)}
.dw-item:active{background:var(--bg-gray)}
.dw-item-label{display:flex;align-items:center;gap:var(--spacing-4);
  font-size:16px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-primary)}
.dw-n{padding:1px var(--spacing-4);border-radius:var(--rounded-xxs);
  background:var(--bg-negative);color:var(--text-negative);
  font-size:10px;font-weight:700;line-height:1.5}
.dw-caret{color:var(--icon-muted)}
.dw-divider{height:1px;margin:var(--spacing-12) var(--spacing-16);background:var(--gray-200)}
.dw-utils{display:flex;flex-direction:column;padding:0 var(--spacing-8)}
.dw-util{display:flex;align-items:center;gap:var(--spacing-12);
  padding:var(--spacing-12) var(--spacing-8);border-radius:var(--rounded-sm);
  font-size:14px;font-weight:600;line-height:1.4;color:var(--text-secondary)}
.dw-util:active{background:var(--bg-gray)}
.dw-util .ico{color:var(--icon-secondary)}
.dw-foot{margin-top:auto;padding:var(--spacing-16) var(--spacing-16) 0}
@media (prefers-reduced-motion:reduce){
  .drawer,.dw-scrim{transition:none}
}

/* ---------- Components/Tabs ---------- */
/* 구분선은 inset shadow — 높이(42px)에 영향 없이 풀블리드로 그림 */
.tabbar{position:relative;box-shadow:inset 0 -1px 0 var(--gray-200)}
.tabs{position:relative;overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tabs-inner{display:flex;align-items:center;width:max-content}
.tab{display:flex;flex-direction:column;align-items:center;justify-content:center}
.tab-label{
  position:relative;display:flex;align-items:center;justify-content:center;gap:var(--spacing-4);
  padding:var(--spacing-8) var(--spacing-12);
  font-size:14px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-muted);white-space:nowrap;
}
.tab.is-active .tab-label{color:var(--text-primary)}
.tab-underline{height:2px;width:100%;background:var(--text-primary);opacity:0;
  transition:opacity .18s ease}
.tab.is-active .tab-underline{opacity:1}
.tab-n{
  position:absolute;top:0;right:-4px;padding:1px var(--spacing-4);
  border-radius:var(--rounded-xxs);
  font-size:10px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;color:var(--text-negative);
}
/* 카테고리 탭바: 좌우 12px, 라벨 좌우 12px → 첫 라벨 텍스트 24px */
.tabbar--category{position:sticky;top:52px;z-index:29;background:var(--bg-default)}
.tabbar--category .tabs{padding:var(--spacing-4) var(--gutter-tabs) 0}
/* 컬렉션 탭바: 탭 박스가 거터(20)에서 시작, 라벨 좌우 16 → 첫 라벨 텍스트 36px (Figma) */
.tabbar--collection .tabs{padding:0 var(--gutter)}
.tabbar--collection .tab-label{padding:var(--spacing-8) var(--spacing-16)}

/* ---------- Main Banner (Figma 5664:102707 + 모션 타임라인) ---------- */
/* 시안 타임라인(16.4s / 4장 루프)을 그대로 옮긴 값 —
   슬라이드 1장당 4100ms = 3500ms 정지 + 600ms 이동.
   텍스트+페이지네이션(Bottom Container)은 이동 200ms 전에 사라지고,
   이동이 끝난 뒤 300ms 에 걸쳐 다시 나타난다. */
:root{
  --mb-slide-dur:600ms;
  --mb-slide-ease:cubic-bezier(.33,0,.1,1);
  --mb-fade-out:200ms;
  --mb-fade-in:300ms;
}
.mainbanner{position:relative;height:320px;overflow:hidden;touch-action:pan-y}
.mb-track{display:flex;height:100%;
  transition:transform var(--mb-slide-dur) var(--mb-slide-ease)}
.mb-slide{position:relative;flex:0 0 100%;height:320px;overflow:hidden}
/* 배너 이미지는 항상 세로 높이(container %) 기준으로 크기를 정하고 width:auto로
   원본 비율을 그대로 유지한다 -- 가로폭에는 절대 맞추지 않는다. 이미지가 컨테이너보다
   넓어지면 좌우는 overflow:hidden 으로 살짝만 잘리고, 좁으면 남는 여백을 각 배너의
   실제 색과 맞춘 배경으로 자연스럽게 채운다. */
/* 바탕 그라디언트는 인라인(각 슬라이드 Background Image 실측값)으로 들어오고,
   사진이 있으면 그 위에 얹힌다. 사진이 아직 없는 슬라이드는 그라디언트만 남는다 */
.mb-bg{position:absolute;inset:0;overflow:hidden;display:flex;align-items:center;justify-content:center}
/* 쿠폰 배너는 Figma Background Image 프레임을 통째로 내보낸 이미지라
   그라디언트·카드·그림자가 이미 들어있다. 좌우 너비에 꽉 맞춰 늘리고,
   원본이 배너와 같은 375:320 비율이라 크롭도 사실상 없다 */
.mb-bg--coupon img{width:100%;height:100%;object-fit:cover}
/* 인물 컷(VARI · BE BOYS)은 시안대로 세로 500/320 비율 커버 — 상단 정렬로
   얼굴이 딤에 묻히지 않게 한다 */
.mb-bg--vari img,.mb-bg--beboys img{width:100%;height:100%;object-fit:cover;object-position:50% 20%}
/* 귀멸 키아트는 배경까지 포함된 풀블리드 이미지라 가로 폭에 꽉 맞추고 위쪽
   정렬해, 아래 남는 어두운 영역으로 마스크가 자연스럽게 떨어지면서
   라벨/타이틀이 얹히게 한다 */
.mb-bg--kimetsu{align-items:flex-start}
.mb-bg--kimetsu img{width:100%;height:auto;object-fit:contain;
  -webkit-mask-image:linear-gradient(180deg,#000 65.27%,transparent 100%);
  mask-image:linear-gradient(180deg,#000 65.27%,transparent 100%)}
.mb-dim{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(0,0,0,0) 0%,var(--alpha-black16) 50%,var(--alpha-black64) 100%)}
/* Figma Bottom Container(5664:102715): 좌우 거터가 아닌 고정 폭 320 중앙 정렬,
   텍스트와 페이지네이션이 한 컨테이너 안에서 gap 24 · 아래 정렬로 나란히 서고
   슬라이드 전환 때 함께 페이드된다 */
.mb-bottom{position:absolute;left:0;right:0;bottom:28px;margin:0 auto;
  width:min(320px,calc(100% - 40px));display:flex;align-items:flex-end;
  gap:var(--spacing-24);
  transition:opacity var(--mb-fade-in) ease-out}
.mb-track.is-fading .mb-bottom{opacity:0;
  transition:opacity var(--mb-fade-out) ease-out}
.mb-text{flex:1;min-width:0;display:flex;flex-direction:column;gap:6px}
.mb-label{font-size:12px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;
  color:var(--alpha-white80)}
/* Title/5 — 20 / Bold 700. <b> 를 쓰면 Pretendard Variable 에서 900 으로 렌더됨 */
.mb-title{font-size:20px;font-weight:700;line-height:1.3;color:var(--text-inverse)}
.mb-title b,.mb-title strong{font-weight:700}
.mb-pagination{flex:none;display:flex;align-items:center;justify-content:center;
  gap:var(--spacing-4);padding:2px;font-size:11px;letter-spacing:var(--tracking-1);line-height:1.4;
  font-variant-numeric:tabular-nums;pointer-events:none}
.mb-page-cur{font-weight:600;color:var(--text-inverse)}
.mb-page-sep,.mb-page-tot{color:var(--alpha-white40)}
@media (prefers-reduced-motion:reduce){
  .mb-track,.mb-bottom{transition:none}
}

/* ---------- Section ---------- */
.sec{padding:var(--spacing-12) 0 var(--spacing-28)}
.sec-head{display:flex;align-items:flex-start;gap:var(--spacing-20);padding:0 var(--gutter)}
.sec-head-text{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.sec-title{font-size:18px;font-weight:600;line-height:1.4;color:var(--text-primary)}
.sec-sub{font-size:12px;font-weight:400;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-tertiary)}
.text-btn{
  display:flex;align-items:center;justify-content:center;gap:var(--spacing-4);
  height:var(--componentSize-sm-height);border-radius:var(--rounded-xs);
  font-size:12px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;
  color:var(--text-muted);white-space:nowrap;
}
.text-btn .ico{color:var(--icon-muted)}

/* ---------- Meet Your Artist Event — Showcase Banner (Figma 5749:63751) ---------- */
.sec--showcase{padding-bottom:var(--spacing-8)}

/* Banner Area(5749:63752) — blue-700→blue-500 바탕 위에 아티스트 컷,
   그 위에 black80 → mask(40%) 오버레이. 시안은 이미지를 163% 높이로 얹어
   윗부분만 보여주므로 cover + 상단 기준 포지션으로 옮겼다 */
.sb-banner{position:relative;overflow:hidden;
  background:linear-gradient(180deg,var(--blue-700) 0%,var(--blue-500) 100%)}
.sb-bg{position:absolute;inset:0}
.sb-bg img{width:100%;height:100%;object-fit:cover;object-position:50% 30%}
.sb-scrim{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(0,0,0,.8) 0%,var(--bg-mask) 100%)}
.sb-inner{position:relative;display:flex;flex-direction:column;align-items:center;
  gap:var(--spacing-24);padding:var(--spacing-20) var(--gutter) 48px}
.sb-head{display:flex;flex-direction:column;gap:var(--spacing-4);width:100%}
.sb-toprow{position:relative;display:flex;align-items:center;justify-content:space-between}
.sb-kind{padding:var(--spacing-2) 6px;border-radius:var(--rounded-xxs);
  background:var(--bg-darkgray-strong);color:var(--text-inverse);
  font-size:12px;font-weight:600;line-height:1.5;letter-spacing:var(--tracking-1)}
.sb-more{position:absolute;top:-4px;right:-4px;display:flex;align-items:center;
  gap:var(--spacing-4);height:26px;padding:var(--spacing-4) 0;border-radius:var(--rounded-xs);
  font-size:11px;font-weight:600;line-height:1.5;letter-spacing:var(--tracking-1);
  color:var(--text-muted)}
.sb-more .ico{color:var(--text-muted)}
.sb-titles{display:flex;flex-direction:column;gap:var(--spacing-4);width:100%;
  color:var(--text-inverse)}
.sb-title{font-size:22px;font-weight:700;line-height:1.3}
.sb-desc{font-size:12px;font-weight:400;line-height:1.4;letter-spacing:var(--tracking-1)}
.sb-meta{display:flex;align-items:flex-start;gap:var(--spacing-28);width:100%}
.sb-cap{font-size:11px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--alpha-white80)}
.sb-artist{flex:none;display:flex;flex-direction:column;gap:6px}
.sb-artist-row{display:flex;align-items:center;gap:6px}
.sb-artist-avatar{flex:none;width:20px;height:20px;border-radius:var(--rounded-full);
  overflow:hidden;border:1px solid var(--border-thumbnail);display:block}
.sb-artist-avatar img{width:100%;height:100%;object-fit:cover}
.sb-artist-name{font-size:16px;font-weight:700;line-height:1.3;color:var(--text-inverse)}
.sb-timer{flex:1;min-width:0;display:flex;flex-direction:column;gap:var(--spacing-2)}
.cd-clock{display:flex;align-items:flex-start;gap:var(--spacing-8)}
.cd-unit{display:flex;flex-direction:column;align-items:center;min-width:30px}
.cd-num{font-size:26px;font-weight:700;line-height:1.3;color:var(--text-inverse);
  font-variant-numeric:tabular-nums}
.cd-cap{font-size:10px;font-weight:400;line-height:1.5;letter-spacing:var(--tracking-1);
  color:var(--alpha-white64)}
.cd-colon{width:8px;text-align:center;font-size:20px;font-weight:700;line-height:1.3;
  color:var(--alpha-white40)}
/* 남은 이벤트가 없을 때 — 숫자는 00 에서 멈추고 라벨만 종료를 알린다 */
.sb-timer.is-ended .cd-num{color:var(--alpha-white40)}

/* Overlapping Cards(5749:63783) — 배너 위로 30px 올라탄다 */
.sb-cards{position:relative;z-index:1;margin-top:-30px;padding:0 var(--gutter);
  display:flex;flex-direction:column;gap:var(--spacing-12)}
.ecard{display:flex;align-items:flex-start;gap:var(--spacing-12);padding:var(--spacing-12);
  border:1px solid var(--gray-200);border-radius:var(--rounded-lg);background:var(--bg-default)}
.ecard-img{position:relative;flex:none;display:block;width:80px;height:80px;
  border-radius:var(--rounded-sm);overflow:hidden;background:var(--bg-subtle)}
.ecard-img img{width:100%;height:100%;object-fit:cover}
.ecard-kind{position:absolute;left:3px;bottom:3px;padding:1px var(--spacing-4);
  border-radius:var(--rounded-xs);background:var(--bg-darkgray-strong);color:var(--text-inverse);
  font-size:10px;font-weight:600;line-height:1.5;letter-spacing:var(--tracking-1)}
.ecard-body{flex:1;min-width:0;display:flex;flex-direction:column;gap:var(--spacing-4)}
.ecard-head{display:flex;flex-direction:column;gap:var(--spacing-4)}
.ecard-brand-row{display:flex;align-items:center;gap:10px}
.ecard-brand{flex:1;min-width:0;font-size:11px;font-weight:400;line-height:1.4;
  letter-spacing:var(--tracking-1);color:var(--text-tertiary);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ecard-chips{flex:none;display:flex;flex-wrap:wrap;gap:var(--spacing-4)}
.ebadge{display:inline-flex;align-items:center;gap:var(--spacing-2);
  padding:1px var(--spacing-4);border-radius:var(--rounded-xs);
  font-size:10px;font-weight:600;line-height:1.5;letter-spacing:var(--tracking-1)}
.ebadge--primary{background:var(--bg-primary);color:var(--brand1-default)}
.ebadge--primary .ico{color:var(--brand1-default)}
.ebadge--warning{background:var(--bg-warning);color:var(--text-warning)}
.ebadge--warning .ico{color:var(--text-warning)}
.ecard-name{font-size:13px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-primary);
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.ecard-price-area{display:flex;flex-direction:column;gap:var(--spacing-4)}
/* 가로형 카드의 가격은 그리드 카드(16 Bold)보다 한 단계 작다 — Subtitle/3 */
.ecard .price-num{font-size:14px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1)}
.ecard-meta{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.em-cell{display:inline-flex;align-items:center;gap:var(--spacing-2);
  font-size:10px;font-weight:400;line-height:1.5;letter-spacing:var(--tracking-1);
  color:var(--text-muted);white-space:nowrap}
.em-cell .ico{color:var(--text-muted)}
.em-sep{flex:none;width:1px;height:10px;background:var(--border-default)}

/* NextArtistPreview(5749:63826) — 가장 임박한 칩만 선명하게 */
.sb-next{display:flex;align-items:flex-start;gap:var(--spacing-12);
  padding:10px var(--gutter) var(--spacing-20);
  overflow-x:auto;scrollbar-width:none}
.sb-next::-webkit-scrollbar{display:none}
.na-item{flex:none;display:flex;align-items:center;gap:var(--spacing-8);
  padding:var(--spacing-8);border-radius:var(--rounded-md);background:var(--bg-muted)}
.na-item:not(:first-child){opacity:.7}
.na-avatar{flex:none;width:32px;height:32px;border-radius:var(--rounded-full);
  overflow:hidden;display:block;background:var(--bg-subtle)}
.na-avatar img{width:100%;height:100%;object-fit:cover}
.na-text{display:flex;flex-direction:column;gap:1px;white-space:nowrap}
.na-name{font-size:10px;font-weight:600;line-height:1.5;letter-spacing:var(--tracking-1);
  color:var(--text-primary)}
.na-time{font-size:10px;font-weight:600;line-height:1.5;letter-spacing:var(--tracking-1);
  color:var(--text-tertiary);font-variant-numeric:tabular-nums}

@media (max-width:359px){
  .sb-meta{flex-direction:column;gap:var(--spacing-12)}
}

/* ---------- Quick Menu (Figma 5612:54901, 이벤트 바로가기) ---------- */
/* 셀 60×73 / 갭 8 / 아이콘 스퀘어 48×48 rounded-12 (좌우 6·상하 4) / 라벨 60×17 */
.sec--quickmenu{padding:var(--spacing-24) 0}
.qm-list{display:flex;align-items:flex-start;justify-content:center;gap:6px 8px;
  padding:0 var(--gutter);
  overflow-x:auto;scrollbar-width:none}
.qm-list::-webkit-scrollbar{display:none}
/* 셀은 시안대로 60px 고정 — 라벨이 그보다 길면(대면 이벤트) 말줄임 대신
   갭 안쪽으로 살짝 넘쳐 흐르게 둔다 (Figma 렌더와 동일) */
.qm-item{display:flex;flex-direction:column;align-items:center;flex:none;width:60px}
/* 스크롤 진입 시 좌 → 우 로 아이콘이 올라오고, 라벨이 뒤따라 뜬다 */
.qm-sq{opacity:0;transform:translateY(14px) scale(.84);
  transition:opacity .34s ease var(--d),
             transform .5s cubic-bezier(.34,1.45,.6,1) var(--d)}
.qm-list.is-in .qm-sq{opacity:1;transform:none}
.qm-label{opacity:0;transform:translateY(6px);
  transition:opacity .3s ease calc(var(--d) + 110ms),
             transform .34s cubic-bezier(.22,1,.36,1) calc(var(--d) + 110ms)}
.qm-list.is-in .qm-label{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  .qm-sq,.qm-label{transition:none;opacity:1;transform:none}
}
.qm-sq{display:flex;align-items:center;justify-content:center;
  width:48px;height:48px;margin:4px 6px;border-radius:var(--rounded-md);
  background:linear-gradient(180deg,var(--bg-gray) 0%,var(--bg-primary) 100%)}
.qm-sq svg{width:36px;height:36px}
.qm-label{
  display:block;width:100%;padding:0 2px;font-size:12px;font-weight:600;
  letter-spacing:var(--tracking-1);line-height:1.4;
  color:var(--text-secondary);text-align:center;white-space:nowrap;overflow:visible;
}
.avatar{display:block;border-radius:var(--rounded-full);overflow:hidden;
  border:1px solid var(--border-thumbnail);background:var(--bg-muted)}
.avatar--48{width:48px;height:48px}
.avatar img{width:100%;height:100%;object-fit:cover}

/* ---------- ProductCard row ---------- */
.prow{display:flex;gap:var(--spacing-12);padding-left:var(--gutter);
  margin-top:var(--spacing-16);overflow-x:auto;
  scroll-snap-type:x proximity;scroll-padding-left:var(--gutter);scrollbar-width:none}
.prow::-webkit-scrollbar{display:none}
.row-end{flex:0 0 var(--gutter);height:1px}
.pcard{flex:0 0 140px;display:flex;flex-direction:column;gap:var(--spacing-12);
  scroll-snap-align:start}
.pcard-img{position:relative;width:140px;height:140px;border-radius:var(--rounded-sm);
  overflow:hidden;background:var(--bg-subtle)}
.pcard-img>img{width:100%;height:100%;object-fit:cover}
.pcard-scrim{position:absolute;left:0;right:0;bottom:0;height:64px;
  background:linear-gradient(180deg,rgba(255,255,255,0) 0%,rgba(0,0,0,.1) 100%)}
.pc-badge{
  position:absolute;top:var(--spacing-8);left:var(--spacing-8);
  padding:2px 6px;border-radius:var(--rounded-xs);
  background:var(--bg-darkgray-strong);color:var(--text-inverse);
  font-size:10px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;
}
.pcard-wish{position:absolute;right:var(--spacing-8);bottom:var(--spacing-8);
  padding:var(--spacing-4);display:flex;color:var(--icon-inverse);
  filter:drop-shadow(0 1px 2px rgba(23,28,36,.28));transition:transform .15s ease}
.pcard-wish:active{transform:scale(.88)}
.pcard-body{display:flex;flex-direction:column;gap:var(--spacing-8)}
.pcard-title{display:flex;flex-direction:column;gap:2px}
.pcard-brand{font-size:12px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.4;
  color:var(--text-tertiary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
/* NDS ProductTitle-atomic 는 1줄/2줄 컴포넌트가 모두 있음 — 잘리지 않도록 2줄까지 허용.
   min-height 로 2줄 자리를 항상 예약해 같은 행에서 1줄/2줄 상품명이 섞여도
   가격 영역의 세로 위치가 흔들리지 않게 함 */
.pcard-name{font-size:14px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-primary);min-height:calc(14px * 1.4 * 2);
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pcard-price-area{display:flex;flex-direction:column;gap:var(--spacing-8)}
.price{display:flex;flex-wrap:wrap;align-items:center;gap:2px}
.price-cur{font-size:10px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;
  color:var(--text-tertiary)}
.price-sym{font-size:14px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-secondary)}
.price-num{font-size:16px;font-weight:700;line-height:1.3;color:var(--text-primary)}

/* ---------- Components/Badge ---------- */
.badges{display:flex;flex-wrap:wrap;gap:var(--spacing-4);min-height:19px}
.badge{display:inline-flex;align-items:center;gap:2px;padding:2px 6px;
  border-radius:var(--rounded-xs);
  font-size:10px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5}
.badge--positive{background:var(--bg-positive);color:var(--text-positive)}
.badge--positive .ico{color:var(--icon-positive)}
.badge--warning{background:var(--bg-warning);color:var(--text-warning)}

/* ---------- Fan's Pick (Artist Ranking) ---------- */
.sec--rank{display:flex;flex-direction:column;gap:var(--spacing-28)}
.podium{display:flex;align-items:flex-end;justify-content:center;gap:var(--spacing-16);
  padding:2px var(--gutter) 0}
.stand{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;
  gap:var(--spacing-12)}
/* ② 콘텐츠(아바타 · 순위 뱃지 · 이름 · 찜 수)는 시안대로 한 덩어리로 움직인다 —
   위에서 8px 내려오며 0.7 → 1 로 커지고 페이드인 */
.stand-top{display:flex;flex-direction:column;align-items:center;gap:var(--spacing-8);width:100%;
  opacity:0;transform:translateY(-8px) scale(.7);
  transition:opacity .3s var(--ease-out-quint) var(--d-content),
             transform .45s var(--ease-spring) var(--d-content)}
.podium.is-in .stand-top{opacity:1;transform:none}
.stand-avatar{position:relative;display:flex;flex-direction:column;align-items:center}
.stand-avatar .avatar{margin:0 0 -4px}
.crown{position:absolute;top:-15px;left:50%;font-size:20px;line-height:1;
  transform:translateX(-50%)}
.rank{padding:2px 6px;border-radius:var(--rounded-full);
  font-size:10px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;
  color:var(--text-inverse);min-width:31px;text-align:center}
.rank--first{background:var(--brand1-default);font-size:12px;padding:2px 8px;min-width:36px}
.rank--second{background:var(--brand1-subtle)}
.rank--third{background:var(--bg-darkgray-soft)}
.stand-meta{display:flex;flex-direction:column;align-items:center;gap:2px;width:100%}
.stand-name{width:100%;font-size:14px;font-weight:600;line-height:1.4;
  letter-spacing:var(--tracking-1);text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stand-count{display:flex;align-items:center;justify-content:center;gap:2px;
  font-size:12px;letter-spacing:var(--tracking-1);line-height:1.4;color:var(--text-tertiary);
  font-variant-numeric:tabular-nums}
.stand-count .ico{color:var(--icon-fill)}
.stand--first .stand-count{font-weight:600;color:var(--brand1-default)}
.stand--first .stand-count .ico{color:var(--brand1-default)}
/* ① 시상대: 3위 → 2위 → 1위 순으로 아래(--bar-from)에서 제자리로 올라오며 페이드인.
   최종 높이를 처음부터 점유하므로 애니메이션 중 아래 콘텐츠가 밀리지 않는다 */
.stand-block-wrap{width:100%;height:var(--h);display:flex;align-items:flex-end}
.stand-block{width:100%;height:100%;border-radius:var(--rounded-lg) var(--rounded-lg) 0 0;
  background:linear-gradient(180deg,var(--bg-gray) 0%,var(--bg-subtler) 100%);
  opacity:0;transform:translateY(var(--bar-from));
  transition:opacity .3s var(--ease-out-quint) var(--d-bar),
             transform .5s var(--ease-spring) var(--d-bar)}
.podium.is-in .stand-block{opacity:1;transform:none}
.stand--second{--h:70px}
.stand--first{--h:120px}
.stand--third{--h:50px}
.stand--first .stand-block{background:linear-gradient(180deg,var(--bg-primary) 0%,var(--blue-50) 100%)}
.stand--third .stand-block{border-radius:var(--rounded-md) var(--rounded-md) 0 0}
@media (prefers-reduced-motion:reduce){
  .stand-top,.stand-block{transition:none;opacity:1;transform:none}
}

.notice-box{margin:0 var(--gutter);padding:var(--spacing-16);border-radius:var(--rounded-md);
  background:var(--bg-gray);display:flex;flex-direction:column;gap:6px}
.notice-head{display:flex;align-items:center;gap:var(--spacing-4);
  font-size:13px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.4;color:var(--text-secondary)}
.notice-head .ico{color:var(--icon-secondary)}
.notice-body{font-size:12px;letter-spacing:var(--tracking-1);line-height:1.4;color:var(--text-tertiary)}
.tooltip-wrap{position:relative;display:inline-flex;align-items:center;margin-left:2px;color:var(--icon-tertiary)}
.tooltip-wrap .tooltip-bubble{position:absolute;bottom:calc(100% + 8px);left:50%;
  transform:translateX(-50%) translateY(4px);width:max-content;max-width:220px;
  padding:var(--spacing-8) var(--spacing-12);border-radius:var(--rounded-xs);
  background:var(--bg-inverse);color:var(--text-inverse);font-size:11px;font-weight:400;
  letter-spacing:var(--tracking-1);line-height:1.4;white-space:nowrap;
  opacity:0;visibility:hidden;pointer-events:none;z-index:5;
  transition:opacity .15s ease,transform .15s ease;box-shadow:0 4px 12px rgba(0,0,0,.18)}
.tooltip-wrap .tooltip-bubble::after{content:"";position:absolute;top:100%;left:50%;
  transform:translateX(-50%);border:5px solid transparent;border-top-color:var(--bg-inverse)}
.tooltip-wrap.is-open .tooltip-bubble{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0);pointer-events:auto}
@media (hover:hover){
  .tooltip-wrap:hover .tooltip-bubble{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}
}

/* ---------- Inline banner (full-bleed) ---------- */
.inline-banner{padding:var(--spacing-24) 0}
.inline-banner .banner-frame{width:100%;height:77px;overflow:hidden;
  display:flex;align-items:center;justify-content:center;background:#000}
/* 기획전 인라인 배너도 좌우 너비에 꽉 맞춰 늘린다 (좌우 레터박스 없음) */
.inline-banner img{width:100%;height:100%;object-fit:cover}

/* ---------- Collection ---------- */
.sec--collection{padding:var(--spacing-24) 0 var(--spacing-28)}
.col-top{padding:0 var(--gutter);margin-bottom:var(--spacing-8)}
.col-panel{display:none}
.col-panel.is-active{display:block}
/* 기획전(컬렉션) 히어로는 좌우 너비에 꽉 맞춰 늘린다. 비율은 유지한 채 넘치는
   위아래만 크롭되고, --col-bg 는 이미지가 뜨기 전 배경으로만 남는다 */
.col-hero{position:relative;height:140px;overflow:hidden;
  display:flex;align-items:center;justify-content:center;background:var(--col-bg,#000)}
.col-hero img{width:100%;height:100%;object-fit:cover}
.col-hero--overlay::after{content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,rgba(6,6,11,.1) 0%,rgba(6,6,11,.75) 52%,rgba(6,6,11,.9) 100%)}
.col-hero-text{position:absolute;right:var(--gutter);top:50%;transform:translateY(-50%);
  z-index:1;display:flex;flex-direction:column;align-items:flex-start;gap:var(--spacing-8)}
.col-hero-badge{padding:2px var(--spacing-8);border-radius:var(--rounded-full);
  background:var(--alpha-white24);color:var(--text-inverse);
  font-size:10px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;backdrop-filter:blur(4px)}
.col-hero-headline{font-size:18px;font-weight:700;line-height:1.3;color:var(--text-inverse)}
.col-body{padding-top:var(--spacing-16)}
.col-head{padding:0 var(--gutter);display:flex;flex-direction:column;gap:2px}
.col-title{font-size:16px;font-weight:700;line-height:1.3;color:var(--text-primary)}
.col-desc{font-size:11px;letter-spacing:var(--tracking-1);line-height:1.4;color:var(--text-tertiary)}

/* ---------- Footer (Figma 5257:59492) ---------- */
/* 바깥 px 12 + 내부 px 8 = 좌우 거터 20 (본문과 동일) */
.footer{background:var(--bg-darkgray-strong);
  margin-top:56px;                       /* 직전 섹션 여백 28 + 56 = 84 (기존의 3배) */
  display:flex;flex-direction:column;align-items:center}
.ft-divider{width:100%;height:1px;background:rgba(255,255,255,.08)}
.ft-contents{width:100%;display:flex;flex-direction:column;gap:var(--spacing-16);
  padding:var(--spacing-32) var(--spacing-12) var(--spacing-8)}
.ft-top{display:flex;flex-direction:column;gap:var(--spacing-12)}
.ft-logo{padding-left:var(--spacing-8)}
.ft-logo svg{width:150px;height:40px;opacity:.9}
.ft-menu{display:flex;flex-wrap:wrap;align-items:center;gap:var(--spacing-16)}
/* Label/3 — 13 / SemiBold 600 / text-tertiary */
.ft-menu-item{padding:var(--spacing-8);font-size:13px;font-weight:600;line-height:1.4;
  letter-spacing:var(--tracking-1);color:var(--text-tertiary)}
/* Action/2 — 14 / SemiBold 600 / text-muted (굵기가 아니라 크기·명도로 강조) */
.ft-menu-item--strong{font-size:14px;font-weight:600;line-height:1.5;color:var(--text-muted)}
.ft-info{display:flex;flex-direction:column;gap:var(--spacing-4);padding:0 var(--spacing-8)}
.ft-info-row{display:flex;flex-wrap:wrap;align-items:center;gap:var(--spacing-8)}
.ft-pair{display:flex;align-items:flex-start;gap:var(--spacing-8);
  font-size:13px;line-height:1.4;color:var(--text-tertiary)}
/* 구분선을 항목 안쪽에 붙여 줄바꿈 시 줄머리에 남지 않도록 */
.ft-pair:not(:last-child)::after{content:'';flex:none;width:1px;height:8px;margin-top:5px;
  background:var(--alpha-white24)}
.ft-key{font-weight:600;letter-spacing:var(--tracking-1);flex:none}   /* Label/3 */
.ft-val{font-weight:400}                                              /* Body/4 */
/* Action/underline/3 — 12 / SemiBold 600 / underline */
.ft-link{padding:2px var(--spacing-4);font-size:12px;font-weight:600;line-height:1.5;
  letter-spacing:var(--tracking-1);color:var(--text-tertiary);text-decoration:underline}
.ft-sns{display:flex;gap:var(--spacing-8);padding:0 var(--spacing-8)}
.ft-sns-item{padding:var(--spacing-4);border-radius:var(--rounded-sm);
  background:var(--bg-inverse);display:flex;align-items:center;justify-content:center;
  color:var(--icon-inverse)}
.ft-sns-item svg{width:24px;height:24px}
.ft-rights{display:flex;flex-direction:column;padding:0 var(--spacing-8)}
/* Caption/2 — 11 / Regular 400 / text-secondary */
.ft-copy{padding:var(--spacing-12) 0;text-align:center;
  font-size:11px;font-weight:400;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-secondary)}

/* ---------- BottomNavigation ---------- */
.bottomnav{
  position:fixed;left:50%;bottom:0;z-index:40;
  width:100%;max-width:var(--maxw);
  background:var(--alpha-white80);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-top:1px solid var(--gray-200);
  padding-bottom:env(safe-area-inset-bottom);
  transform:translateX(-50%) translateY(0);
  transition:transform .28s cubic-bezier(.4,0,.2,1);
  will-change:transform;
}
.bottomnav.is-hidden{transform:translateX(-50%) translateY(115%)}
.bn-items{display:flex;align-items:center;justify-content:center;padding:0 var(--gutter)}
.bn-item{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;gap:2px;
  padding:var(--spacing-8) var(--spacing-12);color:var(--icon-muted)}
.bn-item span{font-size:11px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;
  color:var(--text-tertiary)}
.bn-item.is-active{color:var(--icon-primary)}
.bn-item.is-active span{color:var(--text-primary)}
.bn-home-indicator{display:flex;align-items:center;justify-content:center;padding:var(--spacing-8) 0}
.bn-home-indicator span{width:120px;height:5px;border-radius:100px;background:var(--alpha-black40)}
@media (prefers-reduced-motion:reduce){ .bottomnav{transition:none} }

/* ---------- 어드민 배너 등록 시트 ---------- */
.scrim{position:fixed;inset:0;z-index:50;background:var(--bg-dim);
  opacity:0;transition:opacity .26s ease}
.scrim.is-open{opacity:1}
.sheet{
  position:fixed;left:50%;bottom:0;z-index:51;width:100%;max-width:var(--maxw);
  transform:translateX(-50%) translateY(100%);
  transition:transform .32s cubic-bezier(.32,.72,0,1);
  background:var(--bg-default);border-radius:var(--rounded-lg) var(--rounded-lg) 0 0;
  max-height:92vh;display:flex;flex-direction:column;overflow:hidden;
  box-shadow:0 -8px 32px rgba(23,28,36,.18);
}
.sheet.is-open{transform:translateX(-50%) translateY(0)}
.sheet-grip{width:36px;height:4px;border-radius:var(--rounded-full);
  background:var(--bg-gray-strong,var(--gray-300));margin:var(--spacing-8) auto 0}
.sheet-head{display:flex;align-items:flex-start;gap:var(--spacing-12);
  padding:var(--spacing-12) var(--gutter) var(--spacing-16)}
.sheet-head-text{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.sheet-title{font-size:18px;font-weight:600;line-height:1.4;color:var(--text-primary)}
.sheet-desc{font-size:12px;font-weight:400;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-tertiary)}
.sheet-close{flex:none;padding:var(--spacing-8);margin:-8px -8px 0 0;color:var(--icon-secondary)}
.sheet-body{flex:1;min-height:0;overflow-y:auto;padding:0 var(--gutter) var(--spacing-16);
  display:flex;flex-direction:column;gap:var(--spacing-20)}
.field{display:flex;flex-direction:column;gap:var(--spacing-8)}
.field-label{display:flex;align-items:center;gap:var(--spacing-4);
  font-size:13px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-secondary)}
.field-req{padding:1px var(--spacing-4);border-radius:var(--rounded-xxs);
  background:var(--bg-negative);color:var(--text-negative);
  font-size:10px;font-weight:600;line-height:1.5}
.field-hint{font-size:11px;font-weight:400;color:var(--text-muted)}
.field-count{margin-left:auto;font-size:11px;font-weight:400;font-variant-numeric:tabular-nums;
  color:var(--text-muted)}
.field-count.is-near{color:var(--text-warning)}
.field-count.is-full{color:var(--text-negative)}
.bn-preview{position:relative;width:100%;aspect-ratio:375/320;overflow:hidden;
  border-radius:var(--rounded-sm);background:var(--bg-muted)}
/* 실제 배너와 동일한 .mb-bg--* img 규칙(세로 높이 기준 fill)을 그대로 물려받는다 --
   미리보기만 다른 cover 규칙을 두면 실제 적용 결과와 달라 보이는 문제가 있었음 */
.bn-preview .mb-bottom{bottom:20px}
/* 등록 시트의 미리보기는 실제 배너와 달리 정적 목업이라 텍스트+페이지네이션을
   한 줄(flex)로 같이 둔다 -- 실제 배너 쪽의 "고정 오버레이" 분리와는 무관 */
.mb-bottom--preview{align-items:flex-end;gap:var(--spacing-24)}
.mb-pagination-inline{display:flex;align-items:center;justify-content:center;gap:var(--spacing-4);
  padding:2px;font-size:11px;letter-spacing:var(--tracking-1);line-height:1.4;
  font-variant-numeric:tabular-nums;flex:none}
.upload{display:flex;align-items:center;gap:var(--spacing-12);padding:var(--spacing-12);
  border:1px dashed var(--border-default);border-radius:var(--rounded-sm);
  background:var(--bg-subtler);cursor:pointer}
.upload-thumb{flex:none;width:56px;height:48px;border-radius:var(--rounded-xs);
  overflow:hidden;background:var(--bg-gray)}
.upload-thumb img{width:100%;height:100%;object-fit:cover}
.upload-text{display:flex;flex-direction:column;gap:2px;min-width:0}
.upload-title{font-size:13px;font-weight:600;line-height:1.4;color:var(--text-primary)}
.upload-hint{font-size:11px;font-weight:400;line-height:1.4;color:var(--text-muted)}
/* 업로드 이미지 사이즈 자동 체크 결과 */
.upload-check{display:flex;align-items:center;gap:6px;padding:6px var(--spacing-4) 0;
  font-size:12px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1)}
.upload-check .ico{flex:none}
.upload-check--ok{color:var(--text-positive)}
.upload-check--ok .ico{color:var(--icon-positive)}
.upload-check--warn{color:var(--text-warning)}
.upload-check--warn .ico{color:var(--icon-warning,var(--yellow-500))}
.upload-check-dim{font-weight:400;color:var(--text-muted)}
/* 업로드한 이미지는 배경색 없이 배너 전체를 꽉 채운다 -- 세로 높이 기준으로 커버,
   원본 비율은 유지한 채 넘치는 부분만 크롭 */
.mb-bg--custom img{width:100%;height:100%;object-fit:cover}
.input{width:100%;min-height:var(--componentSize-md-height);
  padding:var(--spacing-12);border:1px solid var(--border-default);
  border-radius:var(--rounded-sm);background:var(--bg-default);
  font-family:inherit;font-size:14px;font-weight:400;line-height:1.4;color:var(--text-primary)}
.input::placeholder{color:var(--text-disabled)}
.input:focus{outline:none;border-color:var(--brand1-default);
  box-shadow:0 0 0 3px var(--brand1-soft)}
.input--area{resize:none;line-height:1.5}
.auto-note{padding:var(--spacing-12);border-radius:var(--rounded-md);background:var(--bg-gray);
  display:flex;flex-direction:column;gap:6px}
.auto-note-title{display:flex;align-items:center;gap:var(--spacing-4);
  font-size:13px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-secondary)}
.auto-note-title .ico{color:var(--icon-secondary)}
.auto-note-list{list-style:none;display:flex;flex-direction:column;gap:2px}
.auto-note-list li{position:relative;padding-left:10px;
  font-size:12px;font-weight:400;line-height:1.5;letter-spacing:var(--tracking-1);
  color:var(--text-tertiary)}
.auto-note-list li::before{content:'';position:absolute;left:2px;top:8px;
  width:3px;height:3px;border-radius:var(--rounded-full);background:var(--text-disabled)}
.sheet-foot{display:flex;gap:var(--spacing-8);padding:var(--spacing-12) var(--gutter);
  padding-bottom:calc(var(--spacing-12) + env(safe-area-inset-bottom));
  border-top:1px solid var(--gray-200);background:var(--bg-default)}
.btn{flex:1;height:var(--componentSize-md-height);border-radius:var(--rounded-sm);
  font-size:14px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1)}
.btn--ghost{background:var(--bg-gray);color:var(--text-secondary)}
.btn--solid{background:var(--brand1-default);color:var(--text-inverse)}
.btn--solid:active{background:var(--brand1-strong)}
.btn--solid:disabled{background:var(--bg-disabled,var(--gray-300));color:var(--text-disabled);
  pointer-events:none}
/* 적용 확인 토스트 */
.bn-toast{position:fixed;left:50%;bottom:28px;z-index:52;transform:translateX(-50%) translateY(8px);
  padding:10px 16px;border-radius:var(--rounded-full);background:var(--bg-darkgray-strong);
  color:var(--text-inverse);font-size:13px;font-weight:600;letter-spacing:var(--tracking-1);
  display:flex;align-items:center;gap:6px;opacity:0;pointer-events:none;
  transition:opacity .22s ease,transform .22s ease;box-shadow:0 8px 24px rgba(23,28,36,.28)}
.bn-toast.is-open{opacity:1;transform:translateX(-50%) translateY(0)}
.bn-toast .ico{color:var(--icon-positive)}
.mb-slide{cursor:pointer}
@media (prefers-reduced-motion:reduce){ .sheet,.scrim{transition:none} }

@media (max-width:374px){
  :root{--gutter:16px}
  .pcard{flex-basis:132px} .pcard-img{width:132px;height:132px}
}

/* =========================================================================
   Desktop 반응형 (1440px 기준 설계, 1200px 캡)
   1440 뷰포트에서 --gutter 가 정확히 120px 이 되어 콘텐츠가 1200px 로 맞춰짐
   (Figma TopNavigation 의 px-120 과 동일한 결과). 1024~1440 사이에서는 최소
   24px 여백을 보장하고, 1440 을 넘는 와이드 모니터에서도 1200px 에서 더 안
   늘어나고 중앙 정렬만 된다.
   ========================================================================= */
"""

# ---------------------------------------------------------------- JS
JS = """
// ----- 가로 스크롤 영역 초기화 -----
// 브라우저가 새로고침 시 중첩 스크롤 컨테이너 위치를 복원하면서
// 첫 카드의 좌측 거터(20px)가 어긋나 보이는 것을 방지
(function(){
  function resetRows(){
    document.querySelectorAll('.prow,.qm-list,.tabs').forEach(function(r){ r.scrollLeft=0; });
  }
  resetRows();
  window.addEventListener('load',resetRows);
})();

// ----- Main banner: Figma 모션 타임라인 그대로 자동 슬라이드 + 스와이프 -----
// Figma 5612:54824 의 16.4s 루프(4장)를 1장 단위로 풀면 4100ms:
//   0 ─ 3300ms 정지 → 3300ms 텍스트/페이지네이션 페이드아웃(200ms, ease-out)
//   → 3500ms 이동(600ms, cubic-bezier(.33,0,.1,1))
//   → 4100ms 새 슬라이드 텍스트 페이드인(300ms, ease-out)
// 이동 구간에는 어느 슬라이드의 텍스트도 보이지 않는 것이 시안의 의도다.
// 되감기 없이 같은 방향으로 계속 흐르도록 앞뒤에 클론 슬라이드를 두고,
// 클론에 도착하면 전환 없이 원본 위치로 옮겨 놓는다.
(function(){
  var track=document.querySelector('.mb-track');
  var box=document.querySelector('.mainbanner');
  if(!track||!box) return;
  var real=[].slice.call(track.children);
  var n=real.length;
  if(n<2) return;

  var HOLD=3500, FADE_OUT=200, SLIDE=600;

  var head=real[n-1].cloneNode(true);   // 맨 앞에 마지막 슬라이드 클론
  var tail=real[0].cloneNode(true);     // 맨 뒤에 첫 슬라이드 클론
  head.setAttribute('aria-hidden','true');
  tail.setAttribute('aria-hidden','true');
  track.insertBefore(head, real[0]);
  track.appendChild(tail);

  var idx=1, moving=false, isPaused=false;
  var guard=null, tHold=null, tFade=null;

  function place(k, animate){
    track.style.transition = animate ? '' : 'none';   // '' → CSS 의 600ms 커브
    track.style.transform = 'translateX(-'+(k*100)+'%)';
    if(!animate) void track.offsetWidth;   // reflow 를 강제해 다음 전환이 살아나게
  }
  function sync(){
    track.dataset.active = String(((idx-1)%n+n)%n);
  }
  function clearTimers(){
    [guard,tHold,tFade].forEach(function(t){ if(t) clearTimeout(t); });
    guard=tHold=tFade=null;
  }
  function schedule(){
    clearTimers();
    if(isPaused) return;
    tFade=setTimeout(function(){ track.classList.add('is-fading'); }, HOLD-FADE_OUT);
    tHold=setTimeout(function(){ go(1); }, HOLD);
  }
  function settle(){
    if(!moving) return;                              // transitionend + guard 중복 방지
    moving=false;
    if(idx===n+1){ idx=1; place(idx,false); }        // 마지막 클론 → 첫 원본
    else if(idx===0){ idx=n; place(idx,false); }     // 첫 클론 → 마지막 원본
    sync();
    track.classList.remove('is-fading');             // 새 슬라이드 텍스트가 300ms 동안 떠오른다
    schedule();
  }
  function go(d){
    if(moving) return;
    clearTimers();
    moving=true;
    track.classList.add('is-fading');                // 이동 중에는 텍스트를 감춘다
    idx+=d; place(idx,true);
    guard=setTimeout(settle, SLIDE+120);             // transitionend 미발생 대비
  }
  track.addEventListener('transitionend',function(e){
    if(e.target===track && e.propertyName==='transform') settle();
  });

  // 시트가 열려 있는 등 명시적으로 일시정지된 상태에서는 절대 자동재생을 되살리지 않는다
  function play(){ if(isPaused) return; schedule(); }
  function stop(){ clearTimers(); }

  var x0=null,dx=0,swiped=false;
  box.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; dx=0; swiped=false; stop(); },{passive:true});
  box.addEventListener('touchmove',function(e){ if(x0!==null){ dx=e.touches[0].clientX-x0; if(Math.abs(dx)>10) swiped=true; } },{passive:true});
  box.addEventListener('touchend',function(){
    if(Math.abs(dx)>40){ go(dx<0?1:-1); } else { play(); }
    x0=null;
  });
  // hover 로는 멈추지 않는다 -- 486px 고정폭 프로토타입이라 데스크탑에서 커서가
  // 배너 위에 얹혀 있는 시간이 길고, 그동안 배너가 완전히 멈춰 고장난 것처럼 보였다
  document.addEventListener('visibilitychange',function(){ document.hidden?stop():play(); });

  // 스와이프로 끝난 제스처는 클릭으로 취급하지 않는다
  window.NoveraBanner={
    active:function(){ return parseInt(track.dataset.active,10)||0; },
    swiped:function(){ return swiped; },
    pause:function(){ isPaused=true; stop(); },
    resume:function(){ isPaused=false; track.classList.remove('is-fading'); play(); },
    slidesFor:function(k){ return track.querySelectorAll('.mb-slide[data-slide="'+k+'"]'); }
  };

  place(idx,false); sync();
  play();
})();

// ----- Meet Your Artist Event: 상품 일시(event_at)와 동기화된 카운트다운 -----
// data.json 의 event_at 을 전부 넘겨받아, 볼 때마다 그중 "가장 가까운 미래" 를
// 골라 남은 시간을 센다. 남은 이벤트가 없으면 00 에서 멈추고 종료 상태가 된다.
// 다음 아티스트 칩의 "오늘 오후 8:00" 같은 문구도 같은 시각에서 만들어진다.
(function(){
  var box=document.getElementById('eventCountdown');
  var next=document.getElementById('nextArtists');
  if(!box && !next) return;

  function parseList(el,attr){
    try{
      return (JSON.parse(el.getAttribute(attr)||'[]')||[])
        .map(function(s){ return Date.parse(s); })
        .filter(function(t){ return !isNaN(t); })
        .sort(function(a,b){ return a-b; });
    }catch(e){ return []; }
  }

  var stamps = box ? parseList(box,'data-deadlines') : [];
  var label  = document.getElementById('cdLabelText');
  var cells={};
  if(box) box.querySelectorAll('.cd-num').forEach(function(el){
    cells[el.getAttribute('data-cd')]=el;
  });
  function set(k,v){ if(cells[k]) cells[k].textContent=(v<10?'0':'')+v; }

  // "오늘 오후 8:00" / "내일 오후 8:00" / "9.30 오후 8:00" — 보는 사람의 로컬 시각 기준
  function whenText(ts){
    var d=new Date(ts), now=new Date();
    var a=new Date(now.getFullYear(),now.getMonth(),now.getDate());
    var b=new Date(d.getFullYear(),d.getMonth(),d.getDate());
    var days=Math.round((b-a)/86400000);
    var h=d.getHours();
    var t=(h<12?'오전':'오후')+' '+(h%12||12)+':'+('0'+d.getMinutes()).slice(-2);
    if(days===0) return '오늘 '+t;
    if(days===1) return '내일 '+t;
    return (d.getMonth()+1)+'.'+d.getDate()+' '+t;
  }

  if(next){
    next.querySelectorAll('.na-item').forEach(function(el){
      var ts=Date.parse(el.getAttribute('data-at'));
      var out=el.querySelector('.na-time');
      if(out) out.textContent = isNaN(ts) ? '' : whenText(ts);
    });
  }

  function paint(){
    if(!box) return;
    var now=Date.now(), target=null;
    for(var i=0;i<stamps.length;i++){ if(stamps[i]>now){ target=stamps[i]; break; } }
    if(target===null){
      box.classList.add('is-ended');
      if(label) label.textContent='예정된 이벤트가 없어요';
      set('d',0); set('h',0); set('m',0); set('s',0);
      return;
    }
    box.classList.remove('is-ended');
    if(label) label.textContent='구매 종료까지';
    var left=Math.max(0, Math.floor((target-now)/1000));
    set('d', Math.floor(left/86400));
    set('h', Math.floor(left%86400/3600));
    set('m', Math.floor(left%3600/60));
    set('s', left%60);
  }

  paint();
  setInterval(paint, 1000);
})();

// ----- BottomNavigation: 스크롤 다운 → 내려가며 사라짐 / 스크롤 업 → 다시 나타남 -----
(function(){
  var nav=document.getElementById('bottomnav');
  if(!nav) return;
  var last=window.scrollY, acc=0, ticking=false;
  var THRESHOLD=10;   // 미세한 흔들림 무시
  var TOP_SAFE=80;    // 최상단 근처에서는 항상 노출
  function update(){
    var y=Math.max(0, window.scrollY);
    var d=y-last;
    if(d===0){ ticking=false; return; }
    acc = ((d>0) === (acc>0)) ? acc+d : d;   // 방향이 바뀌면 누적값 리셋
    var atBottom = y + window.innerHeight >= document.body.scrollHeight - 4;
    if(y<=TOP_SAFE || atBottom)      nav.classList.remove('is-hidden');
    else if(acc >  THRESHOLD)        nav.classList.add('is-hidden');
    else if(acc < -THRESHOLD)        nav.classList.remove('is-hidden');
    last=y; ticking=false;
  }
  window.addEventListener('scroll',function(){
    if(!ticking){ ticking=true; requestAnimationFrame(update); }
  },{passive:true});
})();

// ----- 메인 배너 클릭 → 어드민 배너 등록 시트 -----
// 배경 이미지 + 라벨/타이틀만 입력하면 딤·타이포·페이지네이션은 자동 합성된다.
(function(){
  var sheet=document.getElementById('bnSheet'), scrim=document.getElementById('bnScrim');
  if(!sheet||!scrim) return;
  var elFile=document.getElementById('bnFile'), elThumb=document.getElementById('bnThumb'),
      elCheck=document.getElementById('bnCheck'),
      elLabel=document.getElementById('bnLabel'), elTitle=document.getElementById('bnTitle'),
      elLink=document.getElementById('bnLink'),
      elLabelCount=document.getElementById('bnLabelCount'), elTitleCount=document.getElementById('bnTitleCount'),
      pvImg=document.getElementById('bnPvImg'), pvLabel=document.getElementById('bnPvLabel'),
      pvTitle=document.getElementById('bnPvTitle'), pvPage=document.getElementById('bnPvPage'),
      preview=document.getElementById('bnPreview'),
      toast=document.getElementById('bnToast'), toastMsg=document.getElementById('bnToastMsg');
  var target=0, uploaded=null, lastFocus=null, toastTimer=null;

  // Foundation/Icon — CircleCheckFill / CircleInfoFill (14px)
  var ICON_OK='<svg class="ico" width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path fill="currentColor" d="M12 2C17.52 2 22 6.48 22 12C22 17.52 17.52 22 12 22C6.48 22 2 17.52 2 12C2 6.48 6.48 2 12 2ZM16.53 8.86C16.24 8.56 15.76 8.56 15.47 8.86L10.66 13.65L8.53 11.52C8.24 11.23 7.76 11.23 7.47 11.52C7.18 11.81 7.18 12.29 7.47 12.58L10.13 15.24C10.43 15.54 10.9 15.54 11.19 15.24L16.53 9.92C16.82 9.63 16.82 9.15 16.53 8.86Z"/></svg>';
  var ICON_WARN='<svg class="ico" width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path fill="currentColor" d="M12 2C17.52 2 22 6.48 22 12C22 17.52 17.52 22 12 22C6.48 22 2 17.52 2 12C2 6.48 6.48 2 12 2ZM12 10.25C11.59 10.25 11.25 10.59 11.25 11V16C11.25 16.41 11.59 16.75 12 16.75C12.42 16.75 12.75 16.41 12.75 16V11C12.75 10.59 12.42 10.25 12 10.25ZM12 7.25C11.58 7.25 11.25 7.59 11.25 8C11.25 8.41 11.58 8.75 12 8.75H12C12.42 8.75 12.75 8.41 12.75 8C12.75 7.59 12.42 7.25 12 7.25H12Z"/></svg>';

  var REC_W=750, REC_H=640, REC_RATIO=REC_W/REC_H;   // Main Banner @2x 권장 사이즈

  function esc(t){ var d=document.createElement('div'); d.textContent=t; return d.innerHTML; }
  var NL=String.fromCharCode(10), BR=new RegExp('<br\\s*/?>','gi');
  function titleHtml(v){ return esc(v).split(NL).slice(0,2).join('<br>'); }
  // 배너의 innerHTML("ZO&amp;FRIENDS<br>...")을 그대로 읽으면 엔티티가 풀리지 않은 채
  // textarea 값에 들어가 "ZO&amp;FRIENDS" 처럼 깨져 보인다. 임시 노드에 파싱시켜
  // textContent 로 꺼내면 엔티티 디코딩과 태그 제거가 한 번에 된다.
  function htmlToText(html){
    var d=document.createElement('div');
    d.innerHTML=html.replace(BR,NL);
    return (d.textContent||'');
  }

  function paint(){
    pvLabel.textContent = elLabel.value;
    pvTitle.innerHTML = titleHtml(elTitle.value);
    pvPage.textContent = String(target+1).padStart(2,'0');
  }

  function formatBytes(n){
    if(n<1024) return n+'B';
    if(n<1024*1024) return Math.round(n/1024)+'KB';
    return (n/1024/1024).toFixed(1)+'MB';
  }

  // 업로드된 이미지의 실제 해상도·비율·용량을 읽어 배너 권장 규격과 비교
  function checkImage(file){
    var url=URL.createObjectURL(file);
    var img=new Image();
    img.onload=function(){
      var w=img.naturalWidth, h=img.naturalHeight;
      var sizeTxt=w+'×'+h+'px · '+formatBytes(file.size);
      var lowRes=(w<REC_W||h<REC_H);
      var offRatio=Math.abs((w/h)-REC_RATIO)/REC_RATIO>0.12;
      var icon,label,cls;
      if(lowRes){
        cls='upload-check upload-check--warn';
        icon=ICON_WARN; label='해상도가 낮아요 · 권장 '+REC_W+'×'+REC_H+'px 이상';
      }else if(offRatio){
        cls='upload-check upload-check--warn';
        icon=ICON_WARN; label='비율이 달라요 · 배너를 꽉 채우며 넘치는 부분이 크롭돼요';
      }else{
        cls='upload-check upload-check--ok';
        icon=ICON_OK; label='적합한 이미지예요';
      }
      elCheck.className=cls;
      elCheck.innerHTML=icon+'<span>'+label+' · <span class="upload-check-dim">'+sizeTxt+'</span></span>';
      elCheck.hidden=false;
      URL.revokeObjectURL(url);
    };
    img.src=url;
  }

  function updateCount(el,counter,max){
    var n=el.value.length;
    counter.textContent=n+'/'+max;
    counter.classList.toggle('is-near', n>=Math.round(max*0.85)&&n<max);
    counter.classList.toggle('is-full', n>=max);
  }

  function showToast(msg){
    toastMsg.textContent=msg;
    toast.classList.add('is-open');
    clearTimeout(toastTimer);
    toastTimer=setTimeout(function(){ toast.classList.remove('is-open'); },1800);
  }

  function open(k){
    target=k;
    var src=window.NoveraBanner.slidesFor(k)[0];
    if(!src) return;
    // 현재 배너 값으로 폼 프리필
    var bg=src.querySelector('.mb-bg');
    var img=bg.querySelector('img');
    elLabel.value=(src.querySelector('.mb-label').textContent||'').trim();
    elTitle.value=htmlToText(src.querySelector('.mb-title').innerHTML||'').trim();
    elLink.value=src.getAttribute('data-href')||'';
    uploaded=null;
    elCheck.hidden=true;
    updateCount(elLabel, elLabelCount, 24);
    updateCount(elTitle, elTitleCount, 60);
    var pvBg=preview.querySelector('.mb-bg');
    pvBg.className='mb-bg '+[].filter.call(bg.classList,function(c){return c!=='mb-bg'}).join(' ');
    pvBg.style.cssText=bg.style.cssText;
    pvImg.src=img?img.src:''; elThumb.src=img?img.src:'';
    pvImg.style.cssText=img?img.style.cssText:'';
    paint();

    lastFocus=document.activeElement;
    scrim.hidden=false; sheet.hidden=false;
    void sheet.offsetWidth;
    scrim.classList.add('is-open'); sheet.classList.add('is-open');
    document.body.style.overflow='hidden';
    window.NoveraBanner.pause();
    elLabel.focus({preventScroll:true});
  }
  function close(){
    scrim.classList.remove('is-open'); sheet.classList.remove('is-open');
    document.body.style.overflow='';
    window.NoveraBanner.resume();
    setTimeout(function(){ scrim.hidden=true; sheet.hidden=true; },320);
    if(lastFocus&&lastFocus.focus) lastFocus.focus({preventScroll:true});
  }
  function apply(){
    var slides=window.NoveraBanner.slidesFor(target);   // 원본 + 클론 함께 갱신
    [].forEach.call(slides,function(sl){
      sl.querySelector('.mb-label').textContent=elLabel.value;
      sl.querySelector('.mb-title').innerHTML=titleHtml(elTitle.value);
      if(elLink.value) sl.setAttribute('data-href',elLink.value);
      var bg=sl.querySelector('.mb-bg');
      if(uploaded){
        bg.classList.add('mb-bg--custom');              // 배경색 없이 이미지가 배너 전체를 커버
        bg.style.background='';
        var im=bg.querySelector('img');
        if(!im){ im=document.createElement('img'); im.alt=''; bg.appendChild(im); }
        im.src=uploaded; im.style.cssText='';
      }
    });
    showToast('배너가 적용되었어요');
    close();
  }

  elFile.addEventListener('change',function(){
    var f=elFile.files&&elFile.files[0];
    if(!f) return;
    checkImage(f);
    var r=new FileReader();
    r.onload=function(){
      uploaded=r.result;
      elThumb.src=uploaded;
      var pvBg=preview.querySelector('.mb-bg');
      pvBg.classList.add('mb-bg--custom');
      pvBg.style.background='';
      pvImg.src=uploaded; pvImg.style.cssText='';
    };
    r.readAsDataURL(f);
  });
  elLabel.addEventListener('input',function(){ paint(); updateCount(elLabel, elLabelCount, 24); });
  elTitle.addEventListener('input',function(){ paint(); updateCount(elTitle, elTitleCount, 60); });

  document.getElementById('bnClose').addEventListener('click',close);
  document.getElementById('bnCancel').addEventListener('click',close);
  document.getElementById('bnApply').addEventListener('click',apply);
  scrim.addEventListener('click',close);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!sheet.hidden) close(); });

  document.querySelectorAll('.mb-slide').forEach(function(sl){
    sl.addEventListener('click',function(){
      if(window.NoveraBanner.swiped()) return;        // 스와이프 제스처는 무시
      open(parseInt(sl.getAttribute('data-slide'),10)||0);
    });
    sl.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){ e.preventDefault(); open(parseInt(sl.getAttribute('data-slide'),10)||0); }
    });
  });
})();

// ----- Quick Menu: 아이콘 → 라벨 순으로 좌에서 우로 등장 -----
(function(){
  var list=document.getElementById('quickmenu-list');
  if(!list) return;
  if(!('IntersectionObserver' in window)){ list.classList.add('is-in'); return; }
  new IntersectionObserver(function(entries,obs){
    entries.forEach(function(en){
      if(!en.isIntersecting) return;
      list.classList.add('is-in');
      obs.disconnect();                 // 한 번만 재생
    });
  },{threshold:.3}).observe(list);
})();

// ----- Fan's Pick: 순위가 순차적으로 차오르는 인터랙션 -----
(function(){
  var podium=document.getElementById('podium');
  if(!podium) return;
  var stands=[].slice.call(podium.querySelectorAll('.stand'));
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var timers=[];
  function countUp(stand){
    var el=stand.querySelector('.count');
    var to=parseInt(el.getAttribute('data-to'),10)||0;
    var delay=parseInt(stand.getAttribute('data-delay'),10)||0;
    if(reduce){ el.textContent=to.toLocaleString(); return; }
    var dur=900, t0=null;
    function step(ts){
      if(t0===null) t0=ts;
      var p=Math.min(1,(ts-t0)/dur);
      el.textContent=Math.round(to*(1-Math.pow(1-p,3))).toLocaleString();  // easeOutCubic
      if(p<1) requestAnimationFrame(step);
    }
    timers.push(setTimeout(function(){ requestAnimationFrame(step); }, delay));
  }
  function run(){
    if(podium.classList.contains('is-in')) return;
    podium.classList.add('is-in');
    stands.forEach(countUp);
  }
  function reset(){
    podium.classList.remove('is-in');
    timers.forEach(clearTimeout); timers=[];
    stands.forEach(function(s){ s.querySelector('.count').textContent='0'; });
  }
  if(!('IntersectionObserver' in window)){ run(); return; }
  new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting) run();
      else if(en.boundingClientRect.top > 0) reset();  // 아래로 벗어나면 리셋 → 재진입 시 재생
    });
  },{threshold:.35}).observe(podium);
})();

// ----- Collection 탭 -----
(function(){
  var tabs=document.querySelectorAll('.tabbar--collection .tab');
  var panels=document.querySelectorAll('.col-panel');
  tabs.forEach(function(t){
    t.addEventListener('click',function(){
      var key=t.getAttribute('data-col');
      tabs.forEach(function(x){ x.classList.toggle('is-active', x===t); });
      panels.forEach(function(p){ p.classList.toggle('is-active', p.getAttribute('data-col')===key); });
      t.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'});
    });
  });
})();

// ----- 상단 카테고리 탭 -----
document.querySelectorAll('.tabbar--category .tab').forEach(function(t){
  t.addEventListener('click',function(){
    document.querySelectorAll('.tabbar--category .tab').forEach(function(x){
      x.classList.toggle('is-active', x===t);
    });
    t.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'});
  });
});

// ----- 상단 고지 배너 닫기 -----
(function(){
  var bar=document.getElementById('noticeBar'), btn=document.getElementById('noticeClose');
  if(!bar||!btn) return;
  btn.addEventListener('click',function(){ bar.classList.add('is-closed'); });
})();

// ----- 좌측 사이드 드로어 -----
(function(){
  var drawer=document.getElementById('drawer'), scrim=document.getElementById('dwScrim'),
      openBtn=document.getElementById('dwOpen'), closeBtn=document.getElementById('dwClose');
  if(!drawer||!scrim||!openBtn) return;
  var lastFocus=null;

  function open(){
    lastFocus=document.activeElement;
    scrim.hidden=false; drawer.hidden=false;
    void drawer.offsetWidth;                       // 트랜지션 시작점 확정
    scrim.classList.add('is-open'); drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden','false');
    openBtn.setAttribute('aria-expanded','true');
    document.body.style.overflow='hidden';
    closeBtn.focus({preventScroll:true});
  }
  function close(){
    scrim.classList.remove('is-open'); drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden','true');
    openBtn.setAttribute('aria-expanded','false');
    document.body.style.overflow='';
    setTimeout(function(){ scrim.hidden=true; drawer.hidden=true; },300);
    if(lastFocus&&lastFocus.focus) lastFocus.focus({preventScroll:true});
  }

  openBtn.addEventListener('click',open);
  closeBtn.addEventListener('click',close);
  scrim.addEventListener('click',close);
  drawer.querySelectorAll('a').forEach(function(a){ a.addEventListener('click',close); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!drawer.hidden) close(); });
})();

// ----- 툴팁 (탭으로 열고 닫기) -----
(function(){
  var wraps=document.querySelectorAll('.tooltip-wrap');
  wraps.forEach(function(w){
    w.addEventListener('click',function(e){
      e.stopPropagation();
      var open=w.classList.contains('is-open');
      wraps.forEach(function(x){ x.classList.remove('is-open'); });
      if(!open) w.classList.add('is-open');
    });
  });
  document.addEventListener('click',function(){
    wraps.forEach(function(x){ x.classList.remove('is-open'); });
  });
})();

// ----- 찜 토글 -----
document.querySelectorAll('.pcard-wish').forEach(function(b){
  b.addEventListener('click',function(e){
    e.preventDefault(); e.stopPropagation();
    var on=b.classList.toggle('is-on');
    b.style.color = on ? 'var(--red-500)' : 'var(--icon-inverse)';
  });
});
"""


# ---------------------------------------------------------------- 조립
def build() -> str:
    inline_banner = datauri(ASSETS / "banner" / "inline.jpg")

    body = f"""<div class="app">
  {build_notice_bar()}
  <header class="header">
    <div class="header-inner">
      <a class="logo" href="https://shop.novera.town/" target="_blank" rel="noreferrer">{brand_svg('logo-novera-shop')}</a>
      <div class="head-actions">
        <div class="head-icons">
          <button class="touch" type="button" aria-label="검색">{icon('Search', 20)}</button>
          <button class="touch" type="button" aria-label="장바구니">{icon('Bag', 20)}<span class="push-badge">2</span></button>
        </div>
        <button class="lang" type="button">{icon('Globe', 16)}KO</button>
      </div>
    </div>
  </header>

  {build_cat_tabs()}

  <section class="mainbanner">
    <div class="mb-track">{build_banners()}</div>
  </section>

  <section class="sec sec--quickmenu">
    {build_quickmenu()}
  </section>

  {build_event_showcase()}

  <section class="sec sec--rank">
    {section_header("Fan's Pick!", "팬들이 선택한 최애 TOP 3를 확인해 보세요", "찜하러 가기")}
    {build_podium()}
    <div class="notice-box">
      <p class="notice-head">아티스트 랭킹 정보
        <span class="tooltip-wrap" tabindex="0">
          {icon('CircleInfoFill', 14)}
          <span class="tooltip-bubble" role="tooltip">Last update 2026.08.18 14:00 (KST)</span>
        </span>
      </p>
      <p class="notice-body">팬들이 직접 참여한 찜하기 수치 기준 데이터예요.<br>좋아하는 최애에 아낌없이 찜해보세요!</p>
    </div>
  </section>

  <section class="sec">
    {section_header("Now Trending", "지금 이 순간, 핫한 인기 상품들만 모았어요")}
    {product_row(S['trend'])}
  </section>

  <section class="sec">
    {section_header("New Arrival", "따끈따끈 새로운 상품을 만나보세요!")}
    {product_row(S['new'])}
  </section>

  <div class="inline-banner">
    <a class="banner-frame" href="#"><img src="{inline_banner}" alt="&lt;귀멸의 칼날: 전집중展&gt; 전시 2026년 6월 27일 ~ 9월 27일"></a>
  </div>

  {build_collections()}

  {build_footer()}
  {build_bottom_nav()}
  {build_banner_sheet()}
</div>
{build_sidenav()}
{build_drawer()}"""

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>NOVERA shop · 홈 개편 프로토타입 (Mobile)</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>{CSS}</style>
</head>
<body>
{body}
<script>{JS}</script>
</body>
</html>"""


if __name__ == "__main__":
    out = ROOT / "NOVERA_shop_home_mobile.html"
    doc = build()
    out.write_text(doc, encoding="utf-8")
    print("wrote", out, f"({len(doc.encode('utf-8')) / 1024:.0f} KB)")
