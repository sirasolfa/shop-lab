import json, sys, urllib.request, concurrent.futures as cf
from PIL import ImageFile
A="https://shop-api.novera.town/v1/files/"
def dims(fid):
    for rng in ("bytes=0-131071", None):
        try:
            req=urllib.request.Request(A+fid, headers={"Range":rng} if rng else {})
            with urllib.request.urlopen(req, timeout=60) as r:
                data=r.read(); ct=r.headers.get("Content-Type"); cr=r.headers.get("Content-Range")
                total=int(cr.split("/")[-1]) if cr and "/" in cr else len(data)
            p=ImageFile.Parser(); p.feed(data)
            if p.image: return fid, p.image.size[0], p.image.size[1], ct, total
        except Exception as e: err=str(e)
    return fid, None, None, None, None
ids=list(json.load(open(sys.argv[1])).keys())
out={}
with cf.ThreadPoolExecutor(16) as ex:
    for fid,w,h,ct,sz in ex.map(dims, ids): out[fid]=dict(w=w,h=h,ct=ct,size=sz)
json.dump(out, open(sys.argv[2],"w"))
print("failed", sum(1 for v in out.values() if v["w"] is None))
