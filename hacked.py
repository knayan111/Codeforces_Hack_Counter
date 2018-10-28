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
    ret={"n",n}
    return (jsonify(ret))
if __name__=="__main__":
    app.run()