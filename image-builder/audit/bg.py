import json,sys,io,urllib.request,concurrent.futures as cf,collections
from PIL import Image
s=json.load(open('slots.json')); d=json.load(open('dims.json'))
ids=[f for f,v in s.items() if any(x[0]=='product_main' for x in v)]
def corner(fid):
    try:
        data=urllib.request.urlopen("https://shop-api.novera.town/v1/files/"+fid,timeout=60).read()
        im=Image.open(io.BytesIO(data)).convert('RGBA'); w,h=im.size
        px=[im.getpixel((x,y)) for x,y in [(2,2),(w-3,2),(2,h-3),(w-3,h-3)]]
        return fid,px
    except Exception as e: return fid,None
res={}
with cf.ThreadPoolExecutor(16) as ex:
    for fid,px in ex.map(corner,ids): res[fid]=px
def cls(px):
    if not px: return 'err'
    if any(p[3]<250 for p in px): return 'transparent'
    def near(p,c,t=4): return all(abs(p[i]-c[i])<=t for i in range(3))
    if all(near(p,(243,243,246)) for p in px): return 'F3F3F6'
    if all(near(p,(255,255,255)) for p in px): return 'white'
    if all(near(p,px[0],6) for p in px): return 'other_solid'
    return 'photo/mixed'
c=collections.Counter(); both=0
for fid,px in res.items():
    k=cls(px); c[k]+=1
    if k=='F3F3F6' and d[fid]['w']==1000 and d[fid]['h']==1000: both+=1
print(c, 'guide(1000²+F3F3F6)=',both,'/',len(res))
sz=collections.Counter(f"{d[f]['w']}x{d[f]['h']}" for f,px in res.items() if cls(px)=='F3F3F6'); print('F3F3F6 sizes',sz.most_common(6))
