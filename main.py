from flask import Flask, request, jsonify
import logging, sys, os

app = Flask(__name__)
app.url_map.strict_slashes = False 

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
app.logger.handlers.clear()
app.logger.addHandler(handler)

app.logger.setLevel(logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.Error)
VERBOSE = os.getenv("WEBHOOK_VERBOSE", "0") == "1"

def github_webhook():
    payload = request.get_json(silent=True) or {}
    repo = (payload.get("repository") or {}).get("full_name", "?")
    ref = payload.get("ref", "?")
    branch = ref.split("/")[-1] if ref else "?"
    pusher = (payload.get("pusher") or {}).get("name", "?")
    head = (payload.get("head_commit") or {}).get("id", "")[:7]
    msg = (payload.get("head_commit") or {}).get("message", "").splitlines()[0]
    
    app.logger.info("Github push: repo=%s branch=%s by=%s head=%s msg=%r",
                    repo, branch, pusher, head, msg)
    
    if VERBOSE:
        app.logger.info("Header: %r", dict(request.headers))
        
    return jsonify({"ok": True}), 200

if __name__  == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"
    app.loger.info("== Flask webhook-server iniciado ==")
    app.run(host="0.0.0.0", port=5000) 
