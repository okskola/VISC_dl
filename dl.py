import requests
import os

BASE = "https://www.visc.gov.lv/lv/media/{}/download"
CHECKPOINT = "last_id.txt"
DOWNLOAD_DIR = "files"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# resume from checkpoint
if os.path.exists(CHECKPOINT):
    with open(CHECKPOINT, "r") as f:
        i = int(f.read().strip()) + 1
else:
    i = 1

try:
    while True:
        url = BASE.format(i)
        try:
            r = requests.get(url, allow_redirects=True, timeout=10)
            ctype = r.headers.get("Content-Type", "").lower()

            if "html" not in ctype:
                disp = r.headers.get("Content-Disposition", "")
                if "filename=" in disp:
                    fname = disp.split("filename=")[-1].strip('"')
                else:
                    fname = f"file_{i}"

                path = os.path.join(DOWNLOAD_DIR, fname)
                with open(path, "wb") as f:
                    f.write(r.content)
                print(f"Downloaded {i} → {path}")

                with open(CHECKPOINT, "w") as f:
                    f.write(str(i))
            else:
                print(f"Skipped {i}")

        except Exception as e:
            print(f"Error at {i}: {e}")

        i += 1

except KeyboardInterrupt:
    print("\nStopped by user. Progress saved.")
