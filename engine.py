import math
def scan(markets,tickers,capital=1000,fee=.001,minimum=.005,steps=6,width=2500):
    graph={}
    for symbol,m in markets.items():
        if not m.get("spot") or m.get("active") is False: continue
        t=tickers.get(symbol,{})
        b,a=t.get("bid"),t.get("ask")
        if not b or not a or not (0<b<=a): continue
        base,quote=m["base"],m["quote"]
        graph.setdefault(base,[]).append((quote,b*(1-fee)))
        graph.setdefault(quote,[]).append((base,(1-fee)/a))
    frontier=[(capital,("USDT",))]
    results=[]
    for i in range(steps):
        nxt=[]
        for amount,path in frontier:
            for coin,rate in graph.get(path[-1],[]):
                value=amount*rate
                if coin=="USDT":
                    if i>=1 and value/capital-1>=minimum:
                        results.append((value/capital-1,path+(coin,)))
                elif coin not in path and i+1<steps:
                    nxt.append((value,path+(coin,)))
        # Rank by estimated USDT equivalent, not raw token quantity.
        def score(item):
            amount,path=item
            return amount*max((r for c,r in graph.get(path[-1],[]) if c=="USDT"),default=0)
        frontier=sorted(nxt,key=score,reverse=True)[:width]
    return sorted(results,reverse=True)[:100]
