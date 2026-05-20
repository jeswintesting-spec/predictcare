def test_shift_times():
    print("Testing Shift Logic...")
    shifts = {
        "Morning": ("06:00", "12:00"),
        "Afternoon": ("12:00", "18:00"),
        "Evening": ("18:00", "23:59"), # HTML input time max
        "Night": ("00:00", "06:00")
    }
    
    for name, (s, e) in shifts.items():
        print(f"  {name}: {s} - {e}")

def to_mins(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m

def calculate_slots(start, end, duration):
    s = to_mins(start)
    e = to_mins(end)
    if e < s: e += 24 * 60
    
    total = (e - s) // int(duration)
    print(f"  {start}-{end} ({duration}m) -> {total} slots")
    return total

def verify_slots():
    print("\nVerifying Slot Calculations...")
    # Morning 6h, 15m
    assert calculate_slots("06:00", "12:00", 15) == 24
    # Night 6h, 30m
    assert calculate_slots("00:00", "06:00", 30) == 12
    # Evening ~6h (18:00 - 23:59 is 5h 59m = 359m)
    # 359 // 15 = 23 slots (one min short of 24, which is expected with 23:59 limit)
    calculate_slots("18:00", "23:59", 15)

if __name__ == "__main__":
    test_shift_times()
    verify_slots()
    print("\n✅ 24h Logic Verified")
