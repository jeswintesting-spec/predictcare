# ⚠️ PostgreSQL Server Not Running

## Quick Fix

**You need to start Postgres.app:**

1. **Open Finder** → Go to **Applications**
2. **Double-click** on **Postgres.app**
3. **Click "Start"** or **"Initialize"** button in the app window

The app should show a green indicator when running.

---

## Alternative: Start from Terminal

If the app is already open but not started:

```bash
# Open Postgres.app
open -a Postgres
```

Wait a few seconds for it to start, then tell me "server is running"

---

## How to Verify

Once started, you should see:
- ✅ Postgres.app icon in menu bar (elephant icon)
- ✅ Green "Running" status in the app
- ✅ Port 5432 listed

---

**After starting the server, just say "done" and I'll continue the migration automatically!**
