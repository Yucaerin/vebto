# 🚨 Authenticated Arbitrary File Upload - Vebto Platform Suite

This repository contains a proof-of-concept exploit for an **Authenticated Arbitrary File Upload** vulnerability affecting several SaaS platforms developed by **Vebto** on CodeCanyon.

🧠 **Developer Page:**  
[CodeCanyon – Vebto](https://codecanyon.net/user/vebto)

---

## 🆔 Vulnerability Metadata

- **CWE-ID:** [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
- **Severity:** High
- **Exploit Type:** Remote Code Execution (via Authenticated File Upload)
- **Authentication Required:** ✅ Yes (register + login)
- **User Interaction Required:** ❌ No
- **Public Exploit Available:** ✅ Yes (this repository)
- **Patched:** ❌ Not confirmed
- **Researcher:** Yucaerin

---

## 🧨 Vulnerability Summary

Multiple SaaS applications developed by **Vebto** expose a file upload endpoint at:

```
POST /api/v1/file-entries
```

Once a user registers and logs in, this endpoint allows uploading files with no sufficient checks on:

- MIME type
- File extension
- Actual content validation

This enables an attacker to upload **malicious PHP files disguised as images**, and gain code execution if the file is accessible via public URL.

---

## 🧬 Affected Products

Confirmed or potentially affected platforms built by Vebto:

- **BeLink** - Bio Link & URL Shortener Platform  
- **BeDesk** - Customer Support Software & Helpdesk Ticketing System  
- **BeMusic** - Music Streaming Engine  
- **BeDrive** - File Sharing and Cloud Storage  
- **Architect** - HTML and Site Builder  
- **MTDb** - Ultimate Movie & TV Database  

---

## ✅ Features

- 🔁 Mass exploitation with domain list (`list.txt`)
- 🔐 Auto XSRF token extraction
- 📝 Auto registration + login
- 🧠 Smart handling of email verification (manual link input)
- 🐚 Uploads `bq.php` shell as `image/jpeg`
- 📁 Saves successful shell URLs to `result_upload.txt`

---

## ⚙️ Requirements

- Python 3.x
- Modules:
  - `requests`

Install module:

```bash
pip install requests
```

---

## 📁 Structure

```
mass_uploader.py        # Main exploit script
list.txt                # Target domains
bq.jpg                  # Payload disguised as JPEG
result_upload.txt       # Shell URLs on success
result_needs_verification.txt  # Targets requiring manual email verification
```

---

## 🚀 Usage

1. Put target domains in `list.txt`:
    ```
    site1.com
    site2.net
    ```

2. Ensure `bq.jpg` is a valid JPEG with PHP payload:
    ```php
    ÿØÿà

    <?php
    // your payload
    ?>
    ```

3. Run the script:
    ```bash
    python3 mass_uploader.py
    ```

4. If target requires email verification:
    - Script will prompt:
      ```
      Enter the email verification link:
      ```
    - Paste the link received by email (can be from temp email).

5. On success, shell URL will be saved to `result_upload.txt`.

---

## 🔒 Recommendations for Developers

To mitigate this vulnerability:

- ✅ Enforce authentication with access control for uploads
- ✅ Sanitize and validate file MIME type and extensions
- ✅ Use server-side file type inspection (e.g., finfo)
- ✅ Store uploaded files outside the public webroot
- ✅ Prevent access to scriptable file types (`.php`, `.phtml`, etc.)

---

## ⚠️ Legal Disclaimer

This project is for **educational and authorized testing purposes only**.  
Using it on systems without explicit permission is **illegal and unethical**.
