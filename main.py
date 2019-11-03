from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route("/test_api", methods = ["GET"])
def test_func():
  u = request.args.get("user")
  res = requests.get("https://codeforces.com/api/user.status?", params={"handle": u})
  jdata = res.json()
  jres = jdata["result"]
  n = 0
  for i in jres:
    if(i["verdict"] == "CHALLENGED"):
      n += 1
  res = requests.get("https://codeforces.com/api/user.rating?", params={"handle": u})
  jdata = res.json()
  jres = jdata["result"]
  us = sc = 0
  for i in jres:
    res2 = requests.get("https://codeforces.com/api/contest.standings?", params = {"contestId": i["contestId"], "handles": u})
    jdata2 = res2.json()
    jres2 = jdata2["result"]["rows"]
    if jres2:
      sc += jres2[0]["successfulHackCount"]
      us += jres2[0]["unsuccessfulHackCount"]  
  ret = {"n": n, "us": us, "sc": sc}
  return jsonify(ret)

if __name__=="__main__":
    app.run(debug = True)