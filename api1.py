from flask import Flask,jsonify,request
import requests
app=Flask(__name__)
@app.route("/test_api",methods=["GET"])
def test_func():
    u=request.args.get("user")
    res = requests.get("http://codeforces.com/api/user.status?",params={"handle":u})
    jdata=res.json()
    jres=jdata["result"]
    n=0
    for i in range(len(jres)):
        if(jres[i]["verdict"]=="CHALLENGED"): n+=1
    req=requests.get("https://codeforces.com/contests/with/"+u)
    wp=str(req.content)
    st='<a href="/contest/'
    ans=[]
    for i in range(len(wp)-20):
        if wp[i:i+18]==st:
            temp=""
            for j in range(4):
                if wp[i+18+j].isdigit():temp+=wp[i+j+18]    
                else:break
            if temp!="":
                ans.append(int(temp))
    ans=list(set(ans))
    tc=sc=0
    for ci in ans:
        res = requests.get("http://codeforces.com/api/contest.hacks?",params={"contestId":str(ci)})
        jdata=res.json()
        jres=jdata["result"]
        for i in range(len(jres)):
            if(jres[i]["hacker"]["members"][0]["handle"]=="user"):
                tc+=1
                if(jres[i]["judgeProtocol"]["verdict"]=="Successful hacking attempt"): sc+=1
    ret={"n":n,"tc":tc,"sc":sc}
    return (jsonify(ret))
if __name__=="__main__":
    app.run()