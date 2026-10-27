import json, re, sys, urllib.request, concurrent.futures as cf
A="https://shop-api.novera.town"
def get(p):
    with urllib.request.urlopen(A+p, timeout=30) as r: return json.load(r)
slots={}  # file_id -> list of (slot, label)
def add(fid, slot, label):
    if fid: slots.setdefault(int(fid), []).append((slot, label))
for t in ["BNRTP_001","BNRTP_002","BNRTP_003","BNRTP_004","BNRTP_005"]:
    for b in get(f"/v1/banners/{t}"):
        add(b.get("imagePcFileId"), f"banner_{t}_PC", b["title"]); add(b.get("imageMoFileId"), f"banner_{t}_MO", b["title"])
for p in get("/v1/popups"):
    add(p.get("image",{}).get("imagePcFileId"),"popup_PC",p.get("title")); add(p.get("image",{}).get("imageMoFileId"),"popup_MO",p.get("title"))
ev=get("/v1/events/specials?limit=100")["datas"]
for e in ev:
    add(e.get("thumbnailPcFileId"),"exhibition_thumb_PC",e["title"]); add(e.get("thumbnailMoFileId"),"exhibition_thumb_MO",e["title"])
    for html in (e.get("contents") or "", e.get("notice") or ""):
        for fid in re.findall(r"/files/(\d+)", html): add(fid,"exhibition_contents",e["title"])
# brands
cur=None; seen=0
while True:
    q="/v1/brands?limit=100&sortType=NAME_ASC"+(f"&lastCursor={cur}" if cur is not None else "")
    d=get(q)
    for b in d["datas"]: add(b.get("imageId"),"brand",b["name"])
    seen+=len(d["datas"])
    if not d.get("isNext") or d.get("lastCursor")==cur: break
    cur=d["lastCursor"]
print("brands",seen, file=sys.stderr)
# products
page=1; pids=[]
while True:
    d=get(f"/v1/products?limit=100&page={page}&sortType=LATEST")
    for p in d["datas"]:
        pids.append(p["id"]); add(p.get("mainImageId"),"product_main",p["name"][:40])
    if not d.get("isNext"): break
    page+=1
print("products",len(pids), file=sys.stderr)
def det(pid):
    try: return get(f"/v1/products/{pid}")
    except Exception as e: return None
with cf.ThreadPoolExecutor(12) as ex:
    for d in ex.map(det,pids):
        if not d: continue
        for s in d.get("subImageIds") or []: add(s,"product_sub",d["name"][:40])
        for k in ("productDescription","noticeText"):
            v=d.get(k)
            if isinstance(v,str):
                for fid in re.findall(r"/files/(\d+)", v): add(fid,"product_detail",d["name"][:40])
json.dump({str(k):v for k,v in slots.items()}, open(sys.argv[1],"w"), ensure_ascii=False)
print("files",len(slots), file=sys.stderr)
