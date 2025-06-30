# This file will grow as you add new customers

def get_assistant_id(origin_hostname):
    if "solarco" in origin_hostname:
        return "asst_zZE4Nr5XBwdulUANBvHexdEZ"
    elif "legalfirm" in origin_hostname:
        return "asst_abc123456789"
    elif "demo" in origin_hostname:
        return "asst_demo123456789"
    else:
        return "asst_default_fallback_id"
