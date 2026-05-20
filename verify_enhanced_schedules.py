import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "http://127.0.0.1:8000"

def get_schedules():
    url = f"{BASE_URL}/load-schedules/"
    resp = urllib.request.urlopen(url, context=ctx)
    return json.load(resp)

def verify_fields():
    print("Checking new fields in load-schedules...")
    data = get_schedules()
    if not data:
        print("❌ No data returned")
        return None
    
    sample = data[0]
    print(f"Sample Record: {sample}")
    
    required = ["shift_type", "work_days"]
    if sample["role"] == "Doctor":
        required += ["slot_duration"]
        
    missing = [f for f in required if f not in sample]
    if missing:
        print(f"❌ Missing fields: {missing}")
    else:
        print("✅ New fields present.")
    return sample["name"], sample["role"]

def test_edit(name, role):
    print(f"Testing Edit for {role} ({name})...")
    url = f"{BASE_URL}/edit-schedule/"
    
    params = {
        "role": role,
        "name": name,
        "shift_start": "08:00",
        "shift_end": "16:00",
        "work_days": "Mon,Wed,Fri",
        "shift_type": "Morning"
    }
    
    if role == "Doctor":
        params["slot_duration"] = "30"
        params["max_patients"] = "25"
        
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data)
    resp = urllib.request.urlopen(req, context=ctx)
    res_json = json.load(resp)
    
    if res_json.get("status") == "ok":
        print(f"✅ Edit successful for {role}")
        
        # Verify persistence
        all_data = get_schedules()
        record = next((r for r in all_data if r["name"] == name), None)
        if record:
            if record["work_days"] == "Mon,Wed,Fri":
                print("   - Work days persisted")
            else:
                print(f"   ❌ Work days mismatch: {record['work_days']}")

            if role == "Doctor":
                if record["slot_duration"] == "30":
                     print("   - Slot duration persisted")
                else:
                     print(f"   ❌ Slot duration mismatch: {record['slot_duration']}")
    else:
        print(f"❌ Edit failed: {res_json}")

if __name__ == "__main__":
    name, role = verify_fields()
    if name:
        test_edit(name, role)
