ASSISTANT_MAP = {
    "demo-site-rosy.vercel.app": "asst_zZE4Nr5XBwdulUANBvHexdEZ",
    "client2.vercel.app": "asst_abc123456789",
    "localhost": "asst_localdev123"
}

def get_assistant_id_from_request(req):
    origin = req.headers.get("Origin", "")
    hostname = origin.replace("https://", "").replace("http://", "").split(":")[0].strip()
    return ASSISTANT_MAP.get(hostname)
