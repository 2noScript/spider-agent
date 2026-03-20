import re

proxy_regex = re.compile(r"^(http|https|socks5):\/\/((\w+:\w+)@)?([\w.-]+):(\d{2,5})$")

