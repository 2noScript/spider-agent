import os


def parse_netscape_cookie_file(text: str):
    cookies = []

    if text.startswith("\ufeff"):
        text = text[1:]

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("#") and not line.startswith("#HttpOnly_"):
            continue

        http_only = False
        working = line

        if working.startswith("#HttpOnly_"):
            http_only = True
            working = working.replace("#HttpOnly_", "", 1)

        parts = working.split("\t")
        if len(parts) < 7:
            continue

        domain = parts[0]
        cookie_path = parts[2]
        secure = parts[3].upper() == "TRUE"
        expires = int(parts[4]) if parts[4].isdigit() else 0
        name = parts[5]
        value = "\t".join(parts[6:])

        cookies.append(
            {
                "name": name,
                "value": value,
                "domain": domain,
                "path": cookie_path,
                "expires": expires,
                "httpOnly": http_only,
                "secure": secure,
            }
        )

    return cookies


async def read_cookie_file(
    cookies_dir: str,
    cookies_path: str,
    domain_suffix: str = None,
    max_bytes: int = 5 * 1024 * 1024,
):
    resolved = os.path.abspath(os.path.join(cookies_dir, cookies_path))

    if not resolved.startswith(os.path.abspath(cookies_dir) + os.sep):
        raise ValueError("cookies_path must be a relative path within the cookies directory")

    stat = os.stat(resolved)
    if stat.st_size > max_bytes:
        raise ValueError("Cookie file too large (max 5MB)")

    with open(resolved, "r", encoding="utf-8") as f:
        text = f.read()

    cookies = parse_netscape_cookie_file(text)

    if domain_suffix:
        cookies = [c for c in cookies if c["domain"].endswith(domain_suffix)]

    return [
        {
            "name": c["name"],
            "value": c["value"],
            "domain": c["domain"],
            "path": c["path"],
            "expires": c["expires"],
            "httpOnly": bool(c["httpOnly"]),
            "secure": bool(c["secure"]),
        }
        for c in cookies
    ]

