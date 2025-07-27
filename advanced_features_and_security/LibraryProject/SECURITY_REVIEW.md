# Security Review

## HTTPS & SSL
- Enforced HTTPS via `SECURE_SSL_REDIRECT=True`
- Configured HSTS (1 year) with preload and subdomains

## Cookies
- Secure cookies enabled (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)

## Headers
- X-Frame-Options set to DENY (clickjacking protection)
- Content-Type sniffing disabled
- Browser XSS filter enabled

## Recommendation
- Periodically renew SSL certificates.
- Use CSP headers for advanced XSS protection.
