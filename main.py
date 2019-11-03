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
  FAILED = 0
  OK = 0
  PARTIAL = 0
  COMPILATION_ERROR = 0
  RUNTIME_ERROR = 0
  WRONG_ANSWER = 0
  PRESENTATION_ERROR = 0
  TIME_LIMIT_EXCEEDED = 0
  MEMORY_LIMIT_EXCEEDED = 0
  IDLENESS_LIMIT_EXCEEDED = 0
  SECURITY_VIOLATED = 0
  CRASHED = 0
  INPUT_PREPARATION_CRASHED = 0
  CHALLENGED = 0
  SKIPPED = 0
  TESTING = 0
  REJECTED = 0
  ABSENT = 0
  for i in jres:
    try:
      if (i["verdict"] == "FAILED"):
        FAILED += 1
      elif (i["verdict"] == "OK"):
        OK += 1
      elif (i["verdict"] == "PARTIAL"):
        PARTIAL += 1
      elif (i["verdict"] == "COMPILATION_ERROR"):
        COMPILATION_ERROR += 1
      elif (i["verdict"] == "RUNTIME_ERROR"):
        RUNTIME_ERROR += 1
      elif (i["verdict"] == "WRONG_ANSWER"):
        WRONG_ANSWER += 1
      elif (i["verdict"] == "PRESENTATION_ERROR"):
        PRESENTATION_ERROR += 1
      elif (i["verdict"] == "TIME_LIMIT_EXCEEDED"):
        TIME_LIMIT_EXCEEDED += 1
      elif (i["verdict"] == "MEMORY_LIMIT_EXCEEDED"):
        MEMORY_LIMIT_EXCEEDED += 1
      elif (i["verdict"] == "IDLENESS_LIMIT_EXCEEDED"):
        IDLENESS_LIMIT_EXCEEDED += 1
      elif (i["verdict"] == "SECURITY_VIOLATED"):
        SECURITY_VIOLATED += 1
      elif (i["verdict"] == "CRASHED"):
        CRASHED += 1
      elif (i["verdict"] == "INPUT_PREPARATION_CRASHED"):
        INPUT_PREPARATION_CRASHED += 1
      elif (i["verdict"] == "CHALLENGED"):
        CHALLENGED += 1
      elif (i["verdict"] == "SKIPPED"):
        SKIPPED += 1
      elif (i["verdict"] == "TESTING"):
        TESTING += 1
      else:
        REJECTED += 1
    except IndexError:
      ABSENT += 1
  res = requests.get("https://codeforces.com/api/user.rating?", params={"handle": u})
  jdata = res.json()
  jres = jdata["result"]
  successfulHackCount = 0
  unsuccessfulHackCount = 0
  for i in jres:
    res2 = requests.get("https://codeforces.com/api/contest.standings?", params = {"contestId": i["contestId"], "handles": u})
    jdata2 = res2.json()
    jres2 = jdata2["result"]["rows"]
    if jres2:
      successfulHackCount += jres2[0]["successfulHackCount"]
      unsuccessfulHackCount += jres2[0]["unsuccessfulHackCount"]  
  ret = {"FAILED": FAILED, "OK": OK, "PARTIAL": PARTIAL, "COMPILATION_ERROR": COMPILATION_ERROR, "RUNTIME_ERROR": RUNTIME_ERROR, "WRONG_ANSWER": WRONG_ANSWER, "PRESENTATION_ERROR": PRESENTATION_ERROR, "TIME_LIMIT_EXCEEDED": TIME_LIMIT_EXCEEDED, "MEMORY_LIMIT_EXCEEDED": MEMORY_LIMIT_EXCEEDED, "IDLENESS_LIMIT_EXCEEDED": IDLENESS_LIMIT_EXCEEDED, "SECURITY_VIOLATED": SECURITY_VIOLATED, "CRASHED": CRASHED, "INPUT_PREPARATION_CRASHED": INPUT_PREPARATION_CRASHED, "CHALLENGED": CHALLENGED, "SKIPPED": SKIPPED, "TESTING": TESTING, "REJECTED": REJECTED, "ABSENT": ABSENT, "successfulHackCount": successfulHackCount, "unsuccessfulHackCount": unsuccessfulHackCount}
  return jsonify(ret)

if __name__=="__main__":
    app.run(debug = True)