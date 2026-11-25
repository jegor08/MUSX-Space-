import tkinter as tk
from tkinter import ttk
import threading, queue, time
import ccxt
from engine import scan
root=tk.Tk()
root.title("MusX Space — prototype")
root.geometry("1050x650")
root.configure(bg="#17191e")
style=ttk.Style(); style.theme_use("clam")
style.configure(".",background="#22262d",foreground="#eeeeee",fieldbackground="#22262d")
style.configure("Treeview",background="#17191e",foreground="white",fieldbackground="#17191e",rowheight=30)
top=ttk.Frame(root,padding=12); top.pack(fill="x")
ttk.Label(top,text="MusX Space | Spot scanner",font=("Segoe UI",20)).pack(anchor="w")
names=["mexc","bingx","bitget","bybit","binance"]
flags={n:tk.BooleanVar(value=n=="bybit") for n in names}
bar=ttk.Frame(top); bar.pack(fill="x")
for n,v in flags.items(): ttk.Checkbutton(bar,text=n.upper(),variable=v).pack(side="left")
params=[]
for label,default in [("USDT","1000"),("Min %","0.5"),("Fee % per leg","0.1"),("Max legs","6")]:
    ttk.Label(bar,text=label).pack(side="left",padx=4)
    v=tk.StringVar(value=default); params.append(v)
    ttk.Entry(bar,textvariable=v,width=7).pack(side="left")
status=tk.StringVar(value="Ready. Indicative quotes only; depth not verified.")
ttk.Label(root,textvariable=status).pack(fill="x")
tree=ttk.Treeview(root,columns=("exchange","route","spread","status"),show="headings")
for c,w in zip(("exchange","route","spread","status"),(100,480,120,180)):
    tree.heading(c,text=c); tree.column(c,width=w)
tree.tag_configure("active",foreground="#39ff88")
tree.tag_configure("inactive",foreground="#ff5252")
tree.pack(fill="both",expand=True,padx=12,pady=12)
q=queue.Queue(); tracked=set(); rows={}; busy=False
def worker(selected,capital,minimum,fee,steps):
    for name in selected:
        try:
            ex=getattr(ccxt,name)({"enableRateLimit":True,"options":{"defaultType":"spot"},"timeout":15000})
            markets=ex.load_markets(); tickers=ex.fetch_tickers()
            found=scan(markets,tickers,capital,fee,minimum,steps)
            q.put((name,found,None))
        except Exception as e: q.put((name,[],str(e)))
    q.put(None)
def start():
    global busy
    if busy:return
    try:
        capital,minimum,fee=map(float,[v.get() for v in params[:3]])
        steps=int(params[3].get())
        assert capital>0 and minimum>=0 and 0<=fee<100 and 2<=steps<=6
        selected=[n for n,v in flags.items() if v.get()]
        assert selected
    except Exception:
        status.set("Check settings and select an exchange.");return
    busy=True; status.set("Scanning public quotes...")
    threading.Thread(target=worker,args=(selected,capital,minimum/100,fee/100,steps),daemon=True).start()
def track():
    for item in tree.selection():
        tracked.add(item)
        vals=list(tree.item(item,"values")); vals[3]="TRACKING / "+vals[3]; tree.item(item,values=vals)
def poll():
    global busy
    while not q.empty():
        result=q.get()
        if result is None: busy=False; continue
        name,found,error=result
        fresh=set()
        for spread,path in found:
            key=name+":"+"-".join(path); fresh.add(key)
            vals=(name.upper()," → ".join(path),f"{spread*100:.3f}%","TRACKING / ACTIVE" if key in tracked else "ACTIVE")
            if key in rows: tree.item(key,values=vals,tags=("active",))
            else: tree.insert("", "end",iid=key,values=vals,tags=("active",)); rows[key]=name
        for key,n in list(rows.items()):
            if n==name and key not in fresh:
                if key in tracked:
                    old=list(tree.item(key,"values")); old[2]="—"; old[3]="UNKNOWN" if error else "NOT FOUND"
                    tree.item(key,values=old,tags=("inactive",)); root.bell()
                else: tree.delete(key); del rows[key]
        status.set(name.upper()+": "+(error or f"{len(found)} indicative routes"))
    root.after(300,poll)
def repeat():
    start(); root.after(20000,repeat)
ttk.Button(top,text="Scan now",command=start).pack(side="left")
ttk.Button(top,text="Track selected",command=track).pack(side="left")
root.after(300,poll); root.after(1000,repeat); root.mainloop()
