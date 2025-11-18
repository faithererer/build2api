def convert_cookie_editor_to_playwright(cookies_from_editor, logger=None):
    """
    将从 Cookie-Editor 插件导出的 cookie 列表转换为 Playwright 兼容的格式。
    """
    playwright_cookies = []
    allowed_keys = {'name', 'value', 'domain', 'path', 'expires', 'httpOnly', 'secure', 'sameSite'}

    for cookie in cookies_from_editor:
        pw_cookie = {}
        for key in ['name', 'value', 'domain', 'path', 'httpOnly', 'secure']:
            if key in cookie:
                pw_cookie[key] = cookie[key]
        if cookie.get('session', False):
            pw_cookie['expires'] = -1
        elif 'expirationDate' in cookie:
            if cookie['expirationDate'] is not None:
                pw_cookie['expires'] = int(cookie['expirationDate'])
            else:
                pw_cookie['expires'] = -1
        
        if 'sameSite' in cookie:
            same_site_value = str(cookie['sameSite']).lower()
            if same_site_value == 'no_restriction':
                pw_cookie['sameSite'] = 'None'
            elif same_site_value in ['lax', 'strict']:
                pw_cookie['sameSite'] = same_site_value.capitalize()
            elif same_site_value == 'unspecified':
                pw_cookie['sameSite'] = 'Lax'

        if all(key in pw_cookie for key in ['name', 'value', 'domain', 'path']):
            playwright_cookies.append(pw_cookie)
        else:
            if logger:
                logger.warning(f"跳过一个格式不完整的 cookie: {cookie}")
            
    return playwright_cookies