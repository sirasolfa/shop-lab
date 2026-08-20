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

    # 카드 전체가 상품 상세로 이동 (실제 서비스와 동일 경로)
    return f"""<a class="pcard" href="https://shop.novera.town/products/{p['id']}">
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
            + icon("ChevronRight", 16)
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

ARTISTS = [
    ("tws", "투어스"),
    ("kep1er", "케플러"),
    ("babymonster", "베이비몬스터"),
    ("illit", "아일릿"),
    ("cortis", "코르티스"),
]

# Fan's Pick TOP3 — 실제 아티스트 + Figma 시안의 찜 수치(실 데이터 미제공)
PODIUM = [
    dict(key="kep1er", name="케플러", count=9820, rank="2nd", place="second"),
    dict(key="tws", name="투어스", count=12456, rank="1st", place="first"),
    dict(key="babymonster", name="베이비몬스터", count=8120, rank="3rd", place="third"),
]

COLLECTIONS = [
    dict(key="zo", tab="ZO&FRIENDS", hero="col_zo", overlay=False,
         title="ZO&FRIENDS Collection",
         desc="사랑스러운 조앤프렌즈를 NOVERA shop에서 만나보세요",
         items=S["col_zo"]),
    dict(key="km", tab="귀멸의 칼날", hero="col_km", overlay=True,
         badge="New release", headline="귀멸의 칼날<br>COLLECTION",
         title="귀멸의 칼날 Collection",
         desc="전집중! 귀살대 굿즈를 NOVERA shop에서 만나보세요",
         items=S["col_km"]),
    dict(key="doy", tab="도영", hero="col_doy", overlay=False,
         title="도영 [ Yours ] Collection",
         desc="2025 DOYOUNG ENCORE CONCERT 공식 MD",
         items=S["col_doy"]),
    dict(key="yjs", tab="윤종신", hero="col_yjs", overlay=False,
         title="〈윤종신 그리고 나〉 Collection",
         desc="윤종신의 행보 시리즈를 NOVERA shop에서 만나보세요",
         items=S["col_yjs"]),
    dict(key="kep", tab="Kep1asia", hero="col_kep", overlay=False,
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

MAIN_BANNERS = [
    dict(kind="coupon", label="WELCOME COUPON",
         title="회원가입만 해도<br>전상품 1,000원 즉시 할인!", img="main1"),
    dict(kind="zo", label="서툴러서 더 완벽한 친구들",
         title="ZO&FRIENDS<br>LUCKY COLLECTION", img="main2"),
    dict(kind="km", label="전집중, 귀살대 주목!",
         title="귀멸의 칼날 굿즈<br>COLLECTION Open!", img="main3"),
]


def build_banners() -> str:
    out = []
    for i, b in enumerate(MAIN_BANNERS):
        ext = ".webp" if b["img"] == "main2" else ".jpg"
        src = datauri(ASSETS / "banner" / f"{b['img']}{ext}")
        bg = f'<div class="mb-bg mb-bg--{b["kind"]}"><img src="{src}" alt=""></div>'
        out.append(
            f"""<div class="mb-slide" data-slide="{i}" role="button" tabindex="0"
     aria-label="메인 배너 {i + 1} — 눌러서 배너 등록 화면 열기">
  {bg}
  <div class="mb-dim"></div>
  <div class="mb-bottom">
    <div class="mb-text"><p class="mb-label">{b['label']}</p><p class="mb-title">{b['title']}</p></div>
    <div class="mb-page"><span class="mb-page-cur">{i + 1:02d}</span><span class="mb-page-sep">|</span><span class="mb-page-tot">{len(MAIN_BANNERS):02d}</span></div>
  </div>
</div>"""
        )
    return "".join(out)


ARTIST_STAGGER = 70  # 셀당 등장 간격(ms) — 좌 → 우


def build_artists() -> str:
    cells = []
    for i, (key, name) in enumerate(ARTISTS):
        img = datauri(ASSETS / "artist" / f"{key}.jpg")
        cells.append(
            f"""<button class="artist" type="button" style="--d:{i * ARTIST_STAGGER}ms">
  <span class="avatar avatar--48"><img src="{img}" alt="{esc(name)}"></span>
  <span class="artist-label">{esc(name)}</span>
</button>"""
        )
    cells.append(
        f'<span class="artist artist--add" style="--d:{len(ARTISTS) * ARTIST_STAGGER}ms">'
        '<span class="avatar-add" role="button" aria-label="아티스트 더보기">'
        + icon("Plus", 24) + "</span></span>"
    )
    return f'<div class="artist-list" id="artist-list">{"".join(cells)}<i class="row-end"></i></div>'


# Fan's Pick 등장 타임라인 (스탠드별 오프셋 D 에 더해지는 값)
AVATAR_IN = 0     # ① 아바타 + 순위 뱃지가 아래에서 올라옴
GRAPH_IN = 260    # ② 그래프(시상대) 차오름
META_IN = 300     # ③ 이름 + 하트 카운트 텍스트, 카운팅 시작
CROWN_IN = 560    # ④ 1위 왕관


def build_podium() -> str:
    stands = []
    order = {"third": 0, "second": 1, "first": 2}  # 3위 → 2위 → 1위 순으로 진행
    for p in PODIUM:
        img = datauri(ASSETS / "artist" / f"{p['key']}.jpg")
        crown = '<span class="crown">👑</span>' if p["place"] == "first" else ""
        d = order[p["place"]] * 180
        style = (
            f"--d-avatar:{d + AVATAR_IN}ms;"
            f"--d-graph:{d + GRAPH_IN}ms;"
            f"--d-meta:{d + META_IN}ms;"
            f"--d-crown:{d + CROWN_IN}ms"
        )
        stands.append(
            f"""<div class="stand stand--{p['place']}" style="{style}" data-delay="{d + META_IN}">
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
  <div class="col-hero{' col-hero--overlay' if c.get('overlay') else ''}">
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
        <div class="mb-bottom">
          <div class="mb-text">
            <p class="mb-label" id="bnPvLabel"></p>
            <p class="mb-title" id="bnPvTitle"></p>
          </div>
          <div class="mb-page"><span class="mb-page-cur" id="bnPvPage">01</span><span class="mb-page-sep">|</span><span class="mb-page-tot">{len(MAIN_BANNERS):02d}</span></div>
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


def build_bottom_nav() -> str:
    items = [
        ("HomeFill", "홈", True),
        ("Category", "카테고리", False),
        ("Heart", "좋아요", False),
        ("User", "마이", False),
    ]
    cells = "".join(
        f'<button class="bn-item{" is-active" if act else ""}" type="button">'
        f'{icon(ic, 24)}<span>{esc(label)}</span></button>'
        for ic, label, act in items
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

  /* --- 화면 좌우 거터 (Figma Mobile 375 기준) --- */
  --gutter:var(--spacing-20);          /* 본문 좌우 20px */
  --gutter-header:var(--spacing-16);   /* TopNavigation 16px */
  --gutter-tabs:var(--spacing-12);     /* 카테고리 탭바 12px (라벨 좌우 12 → 첫 라벨 24px) */
  --avatar-inset:6px;                  /* Avatar 좌우 여백 — 원 시작점을 거터에 맞추기 위한 상쇄값 */
  --maxw:430px;
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

/* ---------- TopNavigation ---------- */
.header{
  position:sticky;top:0;z-index:30;background:var(--bg-default);
  display:flex;align-items:center;height:52px;
  padding:var(--spacing-8) var(--gutter-header);
}
.header-inner{flex:1;display:flex;align-items:center;justify-content:space-between}
.logo{display:flex}
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

/* ---------- Main Banner ---------- */
.mainbanner{position:relative;height:320px;overflow:hidden;touch-action:pan-y}
.mb-track{display:flex;height:100%;transition:transform .5s cubic-bezier(.4,0,.2,1)}
.mb-slide{position:relative;flex:0 0 100%;height:320px;overflow:hidden}
.mb-bg{position:absolute;inset:0;overflow:hidden}
.mb-bg--coupon img{width:100%;height:100%;object-fit:cover}
.mb-bg--zo{background:linear-gradient(180deg,#6ac3f0 42.57%,#0072e4 100%);
  display:flex;align-items:flex-start;justify-content:center}
.mb-bg--zo img{width:261px;height:208px;object-fit:contain;margin-top:36px}
.mb-bg--km{background:#06060b}
.mb-bg--km img{width:100%;height:216px;object-fit:cover;
  -webkit-mask-image:linear-gradient(180deg,#000 65.27%,transparent 100%);
  mask-image:linear-gradient(180deg,#000 65.27%,transparent 100%)}
.mb-dim{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(0,0,0,0) 0%,var(--alpha-black16) 50%,var(--alpha-black64) 100%)}
/* Figma: Bottom Container 는 좌우 거터가 아닌 고정 폭 320 중앙 정렬 */
.mb-bottom{
  position:absolute;left:0;right:0;bottom:28px;margin:0 auto;width:min(320px,calc(100% - 40px));
  display:flex;align-items:flex-end;gap:var(--spacing-24);
}
.mb-text{flex:1;min-width:0;display:flex;flex-direction:column;gap:6px}
.mb-label{font-size:12px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;
  color:var(--alpha-white80)}
/* Title/5 — 20 / Bold 700. <b> 를 쓰면 Pretendard Variable 에서 900 으로 렌더됨 */
.mb-title{font-size:20px;font-weight:700;line-height:1.3;color:var(--text-inverse)}
.mb-title b,.mb-title strong{font-weight:700}
.mb-page{display:flex;align-items:center;justify-content:center;gap:var(--spacing-4);
  padding:2px;font-size:11px;letter-spacing:var(--tracking-1);line-height:1.4;
  font-variant-numeric:tabular-nums}
.mb-page-cur{font-weight:600;color:var(--text-inverse)}
.mb-page-sep,.mb-page-tot{color:var(--alpha-white40)}

/* ---------- Section ---------- */
.sec{padding:var(--spacing-12) 0 var(--spacing-28)}
.sec--bias{padding:var(--spacing-24) 0 var(--spacing-20)}
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

/* ---------- Artist list (Who's Your Bias?) ---------- */
.artist-list{display:flex;align-items:flex-start;gap:2px;margin-top:var(--spacing-12);
  padding-left:calc(var(--gutter) - var(--avatar-inset));
  overflow-x:auto;scrollbar-width:none}
.artist-list::-webkit-scrollbar{display:none}
/* Figma: 셀 60×79 / 갭 2 / 아바타 48(좌우 6·상하 8) / 라벨 60×15 */
.artist{display:flex;flex-direction:column;align-items:center;flex:none;width:60px}
/* 스크롤 진입 시 좌 → 우 로 아바타가 올라오고, 라벨이 뒤따라 뜬다 */
.artist>.avatar,.avatar-add{opacity:0;transform:translateY(14px) scale(.84);
  transition:opacity .34s ease var(--d),
             transform .5s cubic-bezier(.34,1.45,.6,1) var(--d)}
.artist-list.is-in .artist>.avatar,.artist-list.is-in .avatar-add{opacity:1;transform:none}
.artist-label{opacity:0;transform:translateY(6px);
  transition:opacity .3s ease calc(var(--d) + 110ms),
             transform .34s cubic-bezier(.22,1,.36,1) calc(var(--d) + 110ms)}
.artist-list.is-in .artist-label{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  .artist>.avatar,.avatar-add,.artist-label{transition:none;opacity:1;transform:none}
}
.avatar{display:block;border-radius:var(--rounded-full);overflow:hidden;
  border:1px solid var(--border-thumbnail);background:var(--bg-muted)}
.avatar--48{width:48px;height:48px}
.avatar img{width:100%;height:100%;object-fit:cover}
.artist>.avatar{margin:var(--spacing-8) var(--avatar-inset)}
.artist-label{
  display:block;width:100%;padding:0 2px;font-size:11px;letter-spacing:var(--tracking-1);line-height:1.4;
  color:var(--text-primary);text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.artist--add{width:60px}
.avatar-add{
  width:48px;height:48px;margin:var(--spacing-8) var(--avatar-inset);
  display:flex;align-items:center;justify-content:center;
  border-radius:var(--rounded-full);background:var(--bg-gray);
  border:1px dashed var(--border-default);color:var(--icon-muted);cursor:pointer;
}

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
.pcard-name{font-size:14px;font-weight:600;line-height:1.4;letter-spacing:var(--tracking-1);
  color:var(--text-primary);
  display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}
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
.stand-top{display:flex;flex-direction:column;align-items:center;gap:var(--spacing-8);width:100%}
/* ① 아바타 + 순위 뱃지 : 아래에서 위로 */
.stand-avatar{position:relative;display:flex;flex-direction:column;align-items:center;
  opacity:0;transform:translateY(18px);
  transition:opacity .36s ease var(--d-avatar),
             transform .46s cubic-bezier(.34,1.3,.64,1) var(--d-avatar)}
.podium.is-in .stand-avatar{opacity:1;transform:none}
.stand-avatar .avatar{margin:0 0 -4px}
/* ④ 1위 왕관 */
.crown{position:absolute;top:-15px;left:50%;font-size:20px;line-height:1;
  opacity:0;transform:translate(-50%,6px) scale(.6);
  transition:opacity .3s ease var(--d-crown),
             transform .45s cubic-bezier(.34,1.6,.64,1) var(--d-crown)}
.podium.is-in .crown{opacity:1;transform:translate(-50%,0) scale(1)}
.rank{padding:2px 6px;border-radius:var(--rounded-full);
  font-size:10px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.5;
  color:var(--text-inverse);min-width:31px;text-align:center}
.rank--first{background:var(--brand1-default);font-size:12px;padding:2px 8px;min-width:36px}
.rank--second{background:var(--brand1-subtle)}
.rank--third{background:var(--bg-darkgray-soft)}
.stand-meta{display:flex;flex-direction:column;align-items:center;gap:2px;width:100%;
  opacity:0;transform:translateY(8px);
  transition:opacity .4s ease var(--d-meta),
             transform .4s cubic-bezier(.22,1,.36,1) var(--d-meta)}
.podium.is-in .stand-meta{opacity:1;transform:none}
.stand-name{width:100%;font-size:14px;font-weight:600;line-height:1.4;
  letter-spacing:var(--tracking-1);text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stand-count{display:flex;align-items:center;justify-content:center;gap:2px;
  font-size:12px;letter-spacing:var(--tracking-1);line-height:1.4;color:var(--text-tertiary);
  font-variant-numeric:tabular-nums}
.stand-count .ico{color:var(--icon-fill)}
.stand--first .stand-count{font-weight:600;color:var(--brand1-default)}
.stand--first .stand-count .ico{color:var(--brand1-default)}
/* 시상대: 3위 → 2위 → 1위 순으로 아래에서 위로 차오름.
   래퍼가 최종 높이를 미리 점유하므로 애니메이션 중 아래 콘텐츠가 밀리지 않음 */
.stand-block-wrap{width:100%;height:var(--h);display:flex;align-items:flex-end}
.stand-block{width:100%;height:0;border-radius:var(--rounded-lg) var(--rounded-lg) 0 0;
  background:linear-gradient(180deg,var(--bg-gray) 0%,var(--bg-subtler) 100%);
  transition:height .75s cubic-bezier(.22,1,.36,1) var(--d-graph)}
.podium.is-in .stand-block{height:100%}
.stand--second{--h:70px}
.stand--first{--h:120px}
.stand--third{--h:50px}
.stand--first .stand-block{background:linear-gradient(180deg,var(--bg-primary) 0%,var(--blue-50) 100%)}
.stand--third .stand-block{border-radius:var(--rounded-md) var(--rounded-md) 0 0}
@media (prefers-reduced-motion:reduce){
  .stand-avatar,.stand-meta,.stand-block,.crown{transition:none}
  .podium .stand-avatar,.podium .stand-meta{opacity:1;transform:none}
  .podium .crown{opacity:1;transform:translate(-50%,0) scale(1)}
  .podium .stand-block{height:100%}
}

.notice-box{margin:0 var(--gutter);padding:var(--spacing-16);border-radius:var(--rounded-md);
  background:var(--bg-gray);display:flex;flex-direction:column;gap:6px}
.notice-head{display:flex;align-items:center;gap:var(--spacing-4);
  font-size:13px;font-weight:600;letter-spacing:var(--tracking-1);line-height:1.4;color:var(--text-secondary)}
.notice-head .ico{color:var(--icon-secondary)}
.notice-body{font-size:12px;letter-spacing:var(--tracking-1);line-height:1.4;color:var(--text-tertiary)}
.notice-time{font-size:10px;letter-spacing:var(--tracking-1);line-height:1.5;color:var(--text-disabled)}

/* ---------- Inline banner (full-bleed) ---------- */
.inline-banner{padding:var(--spacing-24) 0}
.inline-banner img{width:100%;height:77px;object-fit:cover}

/* ---------- Collection ---------- */
.sec--collection{padding:var(--spacing-24) 0 var(--spacing-28)}
.col-top{padding:0 var(--gutter);margin-bottom:var(--spacing-8)}
.col-panel{display:none}
.col-panel.is-active{display:block}
.col-hero{position:relative;height:140px;overflow:hidden}
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
.bn-preview .mb-bg img{width:100%;height:100%;object-fit:cover}
.bn-preview .mb-bottom{bottom:20px}
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
"""

# ---------------------------------------------------------------- JS
JS = """
// ----- 가로 스크롤 영역 초기화 -----
// 브라우저가 새로고침 시 중첩 스크롤 컨테이너 위치를 복원하면서
// 첫 카드의 좌측 거터(20px)가 어긋나 보이는 것을 방지
(function(){
  function resetRows(){
    document.querySelectorAll('.prow,.artist-list,.tabs').forEach(function(r){ r.scrollLeft=0; });
  }
  resetRows();
  window.addEventListener('load',resetRows);
})();

// ----- Main banner: 무한 루프 자동 슬라이드 (4s) + 스와이프 -----
// 3 → 1 로 되감지 않고 같은 방향으로 계속 흐르도록, 앞뒤에 클론 슬라이드를 두고
// 클론에 도착하면 전환 없이 원본 위치로 옮겨 놓는다. (1-2-3-1-2-3 …)
(function(){
  var track=document.querySelector('.mb-track');
  var box=document.querySelector('.mainbanner');
  if(!track||!box) return;
  var real=[].slice.call(track.children);
  var n=real.length;
  if(n<2) return;

  var head=real[n-1].cloneNode(true);   // 맨 앞에 마지막 슬라이드 클론
  var tail=real[0].cloneNode(true);     // 맨 뒤에 첫 슬라이드 클론
  head.setAttribute('aria-hidden','true');
  tail.setAttribute('aria-hidden','true');
  track.insertBefore(head, real[0]);
  track.appendChild(tail);

  var TR='transform .5s cubic-bezier(.4,0,.2,1)';
  var idx=1, moving=false, timer=null, guard=null;

  function place(k, animate){
    track.style.transition = animate ? TR : 'none';
    track.style.transform = 'translateX(-'+(k*100)+'%)';
    if(!animate) void track.offsetWidth;   // reflow 를 강제해 다음 전환이 살아나게
  }
  function sync(){ track.dataset.active = String(((idx-1)%n+n)%n); }
  function settle(){
    if(idx===n+1){ idx=1; place(idx,false); }        // 마지막 클론 → 첫 원본
    else if(idx===0){ idx=n; place(idx,false); }     // 첫 클론 → 마지막 원본
    sync();
    moving=false;
    if(guard){ clearTimeout(guard); guard=null; }
  }
  function go(d){
    if(moving) return;
    moving=true; idx+=d; place(idx,true); sync();
    guard=setTimeout(settle, 700);                   // transitionend 미발생 대비
  }
  track.addEventListener('transitionend',function(e){
    if(e.target===track && e.propertyName==='transform') settle();
  });

  function play(){ stop(); timer=setInterval(function(){ go(1); }, 4000); }
  function stop(){ if(timer) clearInterval(timer); timer=null; }

  var x0=null,dx=0,swiped=false;
  box.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; dx=0; swiped=false; stop(); },{passive:true});
  box.addEventListener('touchmove',function(e){ if(x0!==null){ dx=e.touches[0].clientX-x0; if(Math.abs(dx)>10) swiped=true; } },{passive:true});
  box.addEventListener('touchend',function(){ if(Math.abs(dx)>40) go(dx<0?1:-1); x0=null; play(); });
  box.addEventListener('mouseenter',stop);
  box.addEventListener('mouseleave',play);
  document.addEventListener('visibilitychange',function(){ document.hidden?stop():isPaused||play(); });

  var isPaused=false;
  // 스와이프로 끝난 제스처는 클릭으로 취급하지 않는다
  window.NoveraBanner={
    active:function(){ return parseInt(track.dataset.active,10)||0; },
    swiped:function(){ return swiped; },
    pause:function(){ isPaused=true; stop(); },
    resume:function(){ isPaused=false; play(); },
    slidesFor:function(k){ return track.querySelectorAll('.mb-slide[data-slide="'+k+'"]'); }
  };

  place(idx,false); sync();
  play();
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
        icon=ICON_WARN; label='비율이 달라요 · 가운데 기준으로 잘려 보여요';
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
      if(uploaded){
        var bg=sl.querySelector('.mb-bg');
        bg.className='mb-bg mb-bg--coupon';            // 업로드 이미지는 전체 채움 규칙
        bg.style.cssText='';
        var im=bg.querySelector('img');
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
      pvBg.className='mb-bg mb-bg--coupon'; pvBg.style.cssText='';
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

// ----- Who's Your Bias: 아바타 → 라벨 순으로 좌에서 우로 등장 -----
(function(){
  var list=document.getElementById('artist-list');
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

  <section class="sec sec--bias">
    {section_header("Who's Your Bias?", "당신의 최애를 찜해보세요!", "찜하러 가기")}
    {build_artists()}
  </section>

  <section class="sec">
    {section_header("Meet Your Artist Event!", "최애 아티스트를 만날 수 있는 특별한 이벤트", "전체보기")}
    {product_row(S['event'], badge="EVENT")}
  </section>

  <section class="sec sec--rank">
    {section_header("Fan's Pick!", "팬들이 선택한 최애 TOP 3를 확인해 보세요", "찜하러 가기")}
    {build_podium()}
    <div class="notice-box">
      <p class="notice-head">{icon('Notice', 16)}아티스트 랭킹 정보</p>
      <p class="notice-body">팬들이 직접 참여한 찜하기 수치 기준 데이터예요.<br>좋아하는 최애에 아낌없이 찜해보세요!</p>
      <p class="notice-time">Last update 2026.08.18 14:00 (KST)</p>
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
    <a href="#"><img src="{inline_banner}" alt="&lt;귀멸의 칼날: 전집중展&gt; 전시 2026년 6월 27일 ~ 9월 27일"></a>
  </div>

  {build_collections()}

  <section class="sec">
    {section_header("Free Shipping", "배송비 부담 없이 바로 담아보세요")}
    {product_row(S['free'])}
  </section>

  {build_footer()}
  {build_bottom_nav()}
  {build_banner_sheet()}
</div>"""

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
