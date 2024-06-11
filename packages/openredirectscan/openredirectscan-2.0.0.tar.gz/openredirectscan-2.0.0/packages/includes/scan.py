from urllib.parse import urlparse, parse_qs, urlunparse

def process_url(url):
    def check_for_open_redirect(url):
        parsed_url = urlparse(url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

        query_params = parse_qs(parsed_url.query)
        
        redirect_params = [
            'page', 'url', 'ret', 'r2', 'img', 'u', 'return', 'r', 'URL', 'next', 
            'redirect', 'redirectBack', 'AuthState', 'referer', 'redir', 'aspxerrorpath',
            'link', 'q', 'location', 'uri', 'forward', 'file', 'rb', 'urlact', 'from', 'goto',
            'call_back', 'redirect_url', 'redirect_to', 'back', 'view', 'back_url', 'data', 
            'out', 'path', 'ref', 'uri', 'retour', 'cu_url', 'href', 'linkurl', 'media', 'list',
            'redirect_uri', 'returnTo', 'post_logout_redirect_uri', 'destination', 'continue',
            'context', 'logout?'
        ]

        for param in query_params:
            if param.lower() in redirect_params:
                redirect_url = query_params[param][0]
                redirect_url_parsed = urlparse(redirect_url)
                redirect_base_url = urlunparse((redirect_url_parsed.scheme, redirect_url_parsed.netloc, '', '', '', ''))

                # Check if the redirect URL is different from the base URL
                if redirect_base_url and redirect_base_url != base_url:
                    print("\nParsed URL components:")
                    print("Scheme:", parsed_url.scheme)
                    print("Netloc:", parsed_url.netloc)
                    print("Path:", parsed_url.path)
                    print("Params:", parsed_url.params)
                    print("Query:", parsed_url.query)
                    print("Fragment:", parsed_url.fragment)

                    return True

        return False

    if check_for_open_redirect(url):
        return f"URL {url} is vulnerable to open redirects."
    else:
        return f"URL {url} is not vulnerable to open redirects."