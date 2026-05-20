
import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "http://127.0.0.1:8000"

def check_load():
    print("Checking Load Schedules...")
    try:
        url = f"{BASE_URL}/load-schedules/"
        resp = urllib.request.urlopen(url, context=ctx)
        data = json.load(resp)
        print(f"✅ Loaded {len(data)} staff schedules.")
        if len(data) > 0:
            sample = data[0]
            print(f"Sample: {sample}")
            if "shift_start" in sample and "work_days" in sample:
                return sample["name"]
        return None
    except Exception as e:
        print(f"❌ Load Failed: {e}")
        return None

def check_edit(name):
    print(f"Checking Edit Schedule for {name}...")
    try:
        url = f"{BASE_URL}/edit-schedule/"
        params = {
            "role": "Doctor", # Assuming sample was a doctor, but resilient if not exact
            "name": name,
            "shift_start": "10:00",
            "shift_end": "18:00",
            "work_days": "Mon,Wed,Fri"
        }
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data)
        resp = urllib.request.urlopen(req, context=ctx)
        res_json = json.load(resp)
        print(f"Edit Response: {res_json}")
        
        if res_json.get("status") == "ok":
             print("✅ Edit successful.")
        else:
             print("❌ Edit reported failure.")

    except Exception as e:
        print(f"❌ Edit Failed: {e}")

if __name__ == "__main__":
    name = check_load()
    if name:
        check_edit(name)
