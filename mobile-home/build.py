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

    return f"""<a class="pcard" href="https://shop.novera.town/products/{p['id']}" target="_blank" rel="noreferrer">
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
    ("demon", "귀멸의 칼날"),
    ("zo", "조앤프렌즈"),
    ("nct", "엔시티"),
    ("junsu", "김준수"),
    ("kep", "케플러"),
]

# Fan's Pick TOP3 — 실제 아티스트 + Figma 시안의 찜 수치(실 데이터 미제공)
PODIUM = [
    dict(key="zo", name="조앤프렌즈", count=9820, rank="2nd", place="second"),
    dict(key="demon", name="귀멸의 칼날", count=12456, rank="1st", place="first"),
    dict(key="nct", name="엔시티", count=8120, rank="3rd", place="third"),
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
         title="회원가입만 해도<br>전상품 <b>1,000원</b> 즉시 할인!", img="main1"),
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
            f"""<div class="mb-slide">
  {bg}
  <div class="mb-dim"></div>
  <div class="mb-bottom">
    <div class="mb-text"><p class="mb-label">{b['label']}</p><p class="mb-title">{b['title']}</p></div>
    <div class="mb-page"><span class="mb-page-cur">{i + 1:02d}</span><span class="mb-page-sep">|</span><span class="mb-page-tot">{len(MAIN_BANNERS):02d}</span></div>
  </div>
</div>"""
        )
    return "".join(out)


def build_artists() -> str:
    cells = []
    for key, name in ARTISTS:
        img = datauri(ASSETS / "artist" / f"{key}.jpg")
        cells.append(
            f"""<button class="artist" type="button">
  <span class="avatar avatar--48"><img src="{img}" alt="{esc(name)}"></span>
  <span class="artist-label">{esc(name)}</span>
</button>"""
        )
    cells.append(
        '<span class="artist artist--add"><span class="avatar-add" role="button" '
        'aria-label="아티스트 더보기">' + icon("Plus", 24) + "</span></span>"
    )
    return f'<div class="artist-list">{"".join(cells)}<i class="row-end"></i></div>'


def build_podium() -> str:
    stands = []
    order = {"third": 0, "second": 1, "first": 2}  # 3위 → 2위 → 1위 순으로 차오름
    for p in PODIUM:
        img = datauri(ASSETS / "artist" / f"{p['key']}.jpg")
        crown = '<span class="crown">👑</span>' if p["place"] == "first" else ""
        delay = order[p["place"]] * 180
        stands.append(
            f"""<div class="stand stand--{p['place']}" style="--d:{delay}ms" data-delay="{delay}">
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
    rows = [
        ("상호", "(주)다날엔터테인먼트"),
        ("대표이사", "현능호"),
        ("주소", "(13595) 경기도 성남시 분당구 백현로 93, 11층(수내동, 후너스빌딩)"),
        ("사업자등록번호", "129-86-70437"),
        ("통신판매업신고번호", '2012-경기성남-0116 <a href="#">정보확인</a>'),
        ("개인정보보호관리책임자", "현능호"),
        ("호스팅 제공자", "아마존웹서비스(AWS)"),
        ("CS센터/문의", '<a href="mailto:cs@novera.town">cs@novera.town</a>'),
    ]
    info = "".join(
        f'<div class="ft-row"><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in rows
    )
    return f"""<footer class="footer">
  <div class="ft-logo">{brand_svg('danal')}</div>
  <nav class="ft-links">
    <a href="#">공지사항</a><a href="#">FAQ</a><a href="#">이용약관</a><a href="#"><b>개인정보처리방침</b></a>
  </nav>
  <dl class="ft-info">{info}</dl>
  <div class="ft-sns"><a href="#" aria-label="X">{brand_svg('x')}</a><a href="#" aria-label="Instagram">{brand_svg('insta')}</a></div>
  <p class="ft-copy">ⓒ 2026. 다날엔터테인먼트. all rights reserved.</p>
</footer>"""


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
  font-size:11px;font-weight:600;letter-spacing:1px;line-height:1.4;
}
.lang{
  display:flex;align-items:center;gap:var(--spacing-4);
  height:var(--componentSize-sm-height);padding:0 var(--spacing-12) 0 var(--spacing-8);
  border-radius:var(--rounded-xs);background:var(--bg-gray);
  font-size:12px;font-weight:600;letter-spacing:1px;color:var(--text-secondary);
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
  font-size:14px;font-weight:600;line-height:1.4;letter-spacing:1px;
  color:var(--text-muted);white-space:nowrap;
}
.tab.is-active .tab-label{color:var(--text-primary)}
.tab-underline{height:2px;width:100%;background:var(--text-primary);opacity:0;
  transition:opacity .18s ease}
.tab.is-active .tab-underline{opacity:1}
.tab-n{
  position:absolute;top:0;right:-4px;padding:1px var(--spacing-4);
  border-radius:var(--rounded-xxs);
  font-size:10px;font-weight:600;letter-spacing:1px;line-height:1.5;color:var(--text-negative);
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
.mb-label{font-size:12px;font-weight:600;letter-spacing:1px;line-height:1.5;
  color:var(--alpha-white80)}
.mb-title{font-size:20px;font-weight:700;line-height:1.3;color:var(--text-inverse)}
.mb-page{display:flex;align-items:center;justify-content:center;gap:var(--spacing-4);
  padding:2px;font-size:11px;letter-spacing:1px;line-height:1.4;
  font-variant-numeric:tabular-nums}
.mb-page-cur{font-weight:600;color:var(--text-inverse)}
.mb-page-sep,.mb-page-tot{color:var(--alpha-white40)}

/* ---------- Section ---------- */
.sec{padding:var(--spacing-12) 0 var(--spacing-28)}
.sec--bias{padding:var(--spacing-24) 0 var(--spacing-20)}
.sec-head{display:flex;align-items:flex-start;gap:var(--spacing-20);padding:0 var(--gutter)}
.sec-head-text{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.sec-title{font-size:18px;font-weight:600;line-height:1.4;color:var(--text-primary)}
.sec-sub{font-size:12px;font-weight:400;line-height:1.4;letter-spacing:1px;
  color:var(--text-tertiary)}
.text-btn{
  display:flex;align-items:center;justify-content:center;gap:var(--spacing-4);
  height:var(--componentSize-sm-height);border-radius:var(--rounded-xs);
  font-size:12px;font-weight:600;letter-spacing:1px;line-height:1.5;
  color:var(--text-muted);white-space:nowrap;
}
.text-btn .ico{color:var(--icon-muted)}

/* ---------- Artist list (Who's Your Bias?) ---------- */
.artist-list{display:flex;align-items:flex-start;gap:2px;margin-top:var(--spacing-12);
  padding-left:calc(var(--gutter) - var(--avatar-inset));
  overflow-x:auto;scrollbar-width:none}
.artist-list::-webkit-scrollbar{display:none}
.artist{display:flex;flex-direction:column;align-items:center;flex:none;width:60px}
.avatar{display:block;border-radius:var(--rounded-full);overflow:hidden;
  border:1px solid var(--border-thumbnail);background:var(--bg-muted)}
.avatar--48{width:48px;height:48px}
.avatar img{width:100%;height:100%;object-fit:cover}
.artist>.avatar{margin:var(--spacing-8) var(--avatar-inset)}
.artist-label{
  display:block;width:100%;padding:0 2px;font-size:11px;letter-spacing:1px;line-height:1.4;
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
  font-size:10px;font-weight:600;letter-spacing:1px;line-height:1.5;
}
.pcard-wish{position:absolute;right:var(--spacing-8);bottom:var(--spacing-8);
  padding:var(--spacing-4);display:flex;color:var(--icon-inverse);
  filter:drop-shadow(0 1px 2px rgba(23,28,36,.28));transition:transform .15s ease}
.pcard-wish:active{transform:scale(.88)}
.pcard-body{display:flex;flex-direction:column;gap:var(--spacing-8)}
.pcard-title{display:flex;flex-direction:column;gap:2px}
.pcard-brand{font-size:12px;font-weight:600;letter-spacing:1px;line-height:1.4;
  color:var(--text-tertiary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pcard-name{font-size:14px;font-weight:600;line-height:1.4;color:var(--text-primary);
  display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}
.pcard-price-area{display:flex;flex-direction:column;gap:var(--spacing-8)}
.price{display:flex;flex-wrap:wrap;align-items:center;gap:2px}
.price-cur{font-size:10px;font-weight:600;letter-spacing:1px;line-height:1.5;
  color:var(--text-tertiary)}
.price-sym{font-size:14px;font-weight:600;line-height:1.4;color:var(--text-secondary)}
.price-num{font-size:16px;font-weight:700;line-height:1.4;color:var(--text-primary)}

/* ---------- Components/Badge ---------- */
.badges{display:flex;flex-wrap:wrap;gap:var(--spacing-4);min-height:19px}
.badge{display:inline-flex;align-items:center;gap:2px;padding:2px 6px;
  border-radius:var(--rounded-xs);
  font-size:10px;font-weight:600;letter-spacing:1px;line-height:1.5}
.badge--positive{background:var(--bg-positive);color:var(--text-positive)}
.badge--positive .ico{color:var(--icon-positive)}
.badge--warning{background:var(--bg-warning);color:var(--text-warning)}

/* ---------- Fan's Pick (Artist Ranking) ---------- */
.sec--rank{display:flex;flex-direction:column;gap:var(--spacing-28)}
.podium{display:flex;align-items:flex-end;justify-content:center;gap:var(--spacing-16);
  padding:2px var(--gutter) 0}
.stand{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;
  gap:var(--spacing-12)}
.stand-top{display:flex;flex-direction:column;align-items:center;gap:var(--spacing-8);
  width:100%;opacity:0;transform:translateY(12px);
  transition:opacity .45s ease var(--d),transform .5s cubic-bezier(.34,1.15,.64,1) var(--d)}
.podium.is-in .stand-top{opacity:1;transform:none}
.stand-avatar{position:relative;display:flex;flex-direction:column;align-items:center}
.stand-avatar .avatar{margin:0 0 -4px}
.crown{position:absolute;top:-15px;left:50%;font-size:20px;line-height:1;
  opacity:0;transform:translate(-50%,6px) scale(.6);
  transition:opacity .3s ease calc(var(--d) + 430ms),
             transform .45s cubic-bezier(.34,1.6,.64,1) calc(var(--d) + 430ms)}
.podium.is-in .crown{opacity:1;transform:translate(-50%,0) scale(1)}
.rank{padding:2px 6px;border-radius:var(--rounded-full);
  font-size:10px;font-weight:600;letter-spacing:1px;line-height:1.5;
  color:var(--text-inverse);min-width:31px;text-align:center}
.rank--first{background:var(--brand1-default);font-size:12px;padding:2px 8px;min-width:36px}
.rank--second{background:var(--brand1-subtle)}
.rank--third{background:var(--bg-darkgray-soft)}
.stand-meta{display:flex;flex-direction:column;align-items:center;gap:2px;width:100%}
.stand-name{width:100%;font-size:14px;font-weight:600;line-height:1.4;
  text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stand-count{display:flex;align-items:center;justify-content:center;gap:2px;
  font-size:12px;letter-spacing:1px;line-height:1.4;color:var(--text-tertiary);
  font-variant-numeric:tabular-nums}
.stand-count .ico{color:var(--icon-fill)}
.stand--first .stand-count{font-weight:600;color:var(--brand1-default)}
.stand--first .stand-count .ico{color:var(--brand1-default)}
/* 시상대: 3위 → 2위 → 1위 순으로 아래에서 위로 차오름.
   래퍼가 최종 높이를 미리 점유하므로 애니메이션 중 아래 콘텐츠가 밀리지 않음 */
.stand-block-wrap{width:100%;height:var(--h);display:flex;align-items:flex-end}
.stand-block{width:100%;height:0;border-radius:var(--rounded-lg) var(--rounded-lg) 0 0;
  background:linear-gradient(180deg,var(--bg-gray) 0%,var(--bg-subtler) 100%);
  transition:height .75s cubic-bezier(.22,1,.36,1) var(--d)}
.podium.is-in .stand-block{height:100%}
.stand--second{--h:70px}
.stand--first{--h:120px}
.stand--third{--h:50px}
.stand--first .stand-block{background:linear-gradient(180deg,var(--bg-primary) 0%,var(--blue-50) 100%)}
.stand--third .stand-block{border-radius:var(--rounded-md) var(--rounded-md) 0 0}
@media (prefers-reduced-motion:reduce){
  .stand-top,.stand-block,.crown{transition:none}
  .podium .stand-top{opacity:1;transform:none}
  .podium .crown{opacity:1;transform:translate(-50%,0) scale(1)}
  .podium .stand-block{height:100%}
}

.notice-box{margin:0 var(--gutter);padding:var(--spacing-16);border-radius:var(--rounded-md);
  background:var(--bg-gray);display:flex;flex-direction:column;gap:6px}
.notice-head{display:flex;align-items:center;gap:var(--spacing-4);
  font-size:13px;font-weight:600;letter-spacing:1px;line-height:1.4;color:var(--text-secondary)}
.notice-head .ico{color:var(--icon-secondary)}
.notice-body{font-size:12px;letter-spacing:1px;line-height:1.4;color:var(--text-tertiary)}
.notice-time{font-size:10px;letter-spacing:1px;line-height:1.5;color:var(--text-disabled)}

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
  font-size:10px;font-weight:600;letter-spacing:1px;line-height:1.5;backdrop-filter:blur(4px)}
.col-hero-headline{font-size:18px;font-weight:700;line-height:1.3;color:var(--text-inverse)}
.col-body{padding-top:var(--spacing-16)}
.col-head{padding:0 var(--gutter);display:flex;flex-direction:column;gap:2px}
.col-title{font-size:16px;font-weight:700;line-height:1.4;color:var(--text-primary)}
.col-desc{font-size:11px;letter-spacing:1px;line-height:1.4;color:var(--text-tertiary)}

/* ---------- Footer ---------- */
.footer{background:var(--bg-darkgray-strong);color:var(--text-muted);
  padding:var(--spacing-32) var(--gutter) var(--spacing-40);
  display:flex;flex-direction:column;gap:var(--spacing-20)}
.ft-logo svg{width:150px;height:auto;opacity:.9}
.ft-links{display:flex;flex-wrap:wrap;gap:var(--spacing-20);
  font-size:13px;font-weight:600;color:var(--gray-300)}
.ft-info{display:flex;flex-direction:column;gap:var(--spacing-8)}
.ft-row{display:flex;gap:var(--spacing-8);font-size:11px;line-height:1.5}
.ft-row dt{font-weight:600;color:var(--gray-400);flex:none}
.ft-row dd{color:var(--gray-600)}
.ft-row a{text-decoration:underline}
.ft-sns{display:flex;gap:var(--spacing-8)}
.ft-sns a{width:36px;height:36px;border-radius:var(--rounded-sm);
  background:rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center}
.ft-sns svg{width:20px;height:20px}
.ft-copy{font-size:10px;line-height:1.5;color:var(--gray-700)}

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
.bn-item span{font-size:11px;font-weight:600;letter-spacing:1px;line-height:1.5;
  color:var(--text-tertiary)}
.bn-item.is-active{color:var(--icon-primary)}
.bn-item.is-active span{color:var(--text-primary)}
.bn-home-indicator{display:flex;align-items:center;justify-content:center;padding:var(--spacing-8) 0}
.bn-home-indicator span{width:120px;height:5px;border-radius:100px;background:var(--alpha-black40)}
@media (prefers-reduced-motion:reduce){ .bottomnav{transition:none} }

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

// ----- Main banner: 자동 슬라이드 (4s) + 스와이프 -----
(function(){
  var track=document.querySelector('.mb-track');
  if(!track) return;
  var n=track.children.length, i=0, timer=null;
  function go(k){ i=(k+n)%n; track.style.transform='translateX(-'+(i*100)+'%)'; }
  function play(){ stop(); timer=setInterval(function(){ go(i+1); }, 4000); }
  function stop(){ if(timer) clearInterval(timer); timer=null; }
  var x0=null,dx=0, box=document.querySelector('.mainbanner');
  box.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; dx=0; stop(); },{passive:true});
  box.addEventListener('touchmove',function(e){ if(x0!==null) dx=e.touches[0].clientX-x0; },{passive:true});
  box.addEventListener('touchend',function(){ if(Math.abs(dx)>40) go(i+(dx<0?1:-1)); x0=null; play(); });
  box.addEventListener('mouseenter',stop);
  box.addEventListener('mouseleave',play);
  document.addEventListener('visibilitychange',function(){ document.hidden?stop():play(); });
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
    timers.push(setTimeout(function(){ requestAnimationFrame(step); }, delay+150));
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
    {section_header("New Arrival", "따끈따끈 새로운 상품을 만나보세요!")}
    {product_row(S['new'])}
  </section>

  <section class="sec">
    {section_header("Now Trending", "지금 이 순간, 핫한 인기 상품들만 모았어요")}
    {product_row(S['trend'])}
  </section>

  <div class="inline-banner">
    <a href="#"><img src="{inline_banner}" alt="&lt;귀멸의 칼날: 전집중展&gt; 전시 2026년 6월 27일 ~ 9월 27일"></a>
  </div>

  {build_collections()}

  <section class="sec">
    {section_header("무료배송 상품", "배송비 부담 없이 바로 담아보세요")}
    {product_row(S['free'])}
  </section>

  {build_footer()}
  {build_bottom_nav()}
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
