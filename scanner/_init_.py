from urllib.parse import urlparse
from .headers import check_security_headers
from .ssl_tls import check_ssl_tls
from .dns_analysis import check_dns
from .virustotal import check_virustotal
from .abuseipdb import check_abuseipdb
from .subdomains import enumerate_subdomains
from .ports import check_open_ports
from .email_security import check_email_security
from .cms_detect import detect_cms
from .vulnerabilities import check_vulnerabilities
from .whois import check_whois
from .shodan import check_shodan
from risk_engine import calculate_risk_score

def get_domain_from_url(url):
    parsed = urlparse(url)
    return parsed.netloc or parsed.path

def run_scan(target_url, user_api_keys=None):
    """Run all scan modules and return findings, risk_score, risk_level.
    user_api_keys: optional dict with user-specific API keys to override globals.
    """
    domain = get_domain_from_url(target_url)
    findings = []

    # Security Headers
    findings.extend(check_security_headers(target_url))

    # SSL/TLS
    findings.extend(check_ssl_tls(domain))

    # DNS
    findings.extend(check_dns(domain))

    # VirusTotal
    findings.extend(check_virustotal(domain, user_api_keys))

    # AbuseIPDB
    findings.extend(check_abuseipdb(domain, user_api_keys))

    # Subdomain Enumeration
    findings.extend(enumerate_subdomains(domain))

    # Port Scanning
    findings.extend(check_open_ports(domain))

    # Email Security
    findings.extend(check_email_security(domain))

    # CMS Detection
    findings.extend(detect_cms(target_url))

    # Vulnerability Checks (if CMS detected, maybe run specific)
    findings.extend(check_vulnerabilities(target_url, domain, user_api_keys))

    # WHOIS
    findings.extend(check_whois(domain))

    # Shodan (optional)
    findings.extend(check_shodan(domain, user_api_keys))

    # Calculate risk score
    risk_score, risk_level = calculate_risk_score(findings)

    return findings, risk_score, risk_level
