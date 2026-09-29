import os
import openai

ADVICE_TEMPLATES = {
    'Missing CSP Header': {
        'impact': 'Increases risk of XSS and data injection attacks.',
        'recommendation': 'Add a Content-Security-Policy header to restrict sources of scripts and styles.'
    },
    'Missing HSTS Header': {
        'impact': 'Allows insecure HTTP connections, enabling man-in-the-middle attacks.',
        'recommendation': 'Add Strict-Transport-Security header to enforce HTTPS.'
    },
    'Missing X-Frame-Options Header': {
        'impact': 'Your site can be embedded in iframes, leading to clickjacking attacks.',
        'recommendation': 'Set X-Frame-Options to DENY or SAMEORIGIN.'
    },
    'Missing X-Content-Type-Options Header': {
        'impact': 'Browsers may MIME-sniff content, leading to code execution.',
        'recommendation': 'Add X-Content-Type-Options: nosniff.'
    },
    'Missing Referrer-Policy Header': {
        'impact': 'Referrer information may leak to third parties.',
        'recommendation': 'Set a Referrer-Policy to control referrer information.'
    },
    'Expired SSL Certificate': {
        'impact': 'Users will see security warnings and may leave the site.',
        'recommendation': 'Renew the SSL certificate immediately.'
    },
    'SSL Certificate Expiring Soon': {
        'impact': 'The certificate will expire soon, causing future issues.',
        'recommendation': 'Renew the certificate before it expires.'
    },
    'Insecure TLS Version': {
        'impact': 'Older TLS versions are vulnerable to attacks like BEAST and POODLE.',
        'recommendation': 'Disable TLS 1.0 and 1.1, use TLS 1.2 or 1.3.'
    },
    'VirusTotal Malicious Detections': {
        'impact': 'Your domain may be associated with malware or phishing.',
        'recommendation': 'Investigate and clean the domain, request re-evaluation.'
    },
    'IP Reported for Abuse': {
        'impact': 'Your IP may be blacklisted, affecting email deliverability and reputation.',
        'recommendation': 'Check for compromised services and request removal from blacklists.'
    },
    'Open Ports Detected': {
        'impact': 'Open ports increase attack surface.',
        'recommendation': 'Close unnecessary ports or restrict access via firewall.'
    },
    'Missing SPF Record': {
        'impact': 'Email spoofing is possible.',
        'recommendation': 'Add an SPF TXT record to authorize mail servers.'
    },
    'Missing DKIM Record': {
        'impact': 'Emails may be flagged as spam or forged.',
        'recommendation': 'Configure DKIM signing for your domain.'
    },
    'Missing DMARC Record': {
        'impact': 'No policy for handling failed authentication, increasing spoofing risk.',
        'recommendation': 'Publish a DMARC record to prevent email spoofing.'
    },
    'WordPress Vulnerabilities Found': {
        'impact': 'Known vulnerabilities can be exploited to compromise the site.',
        'recommendation': 'Update WordPress core, themes, and plugins immediately.'
    },
    # Add more as needed
}

def enrich_findings(findings, use_llm=None):
    """Enrich findings with impact/recommendation.
    If use_llm is True and OpenAI key exists, use LLM; otherwise fallback to templates.
    """
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    if use_llm is None:
        use_llm = bool(openai.api_key)

    for f in findings:
        if f.get('recommendation') and f.get('description'):
            continue  # already detailed
        template = ADVICE_TEMPLATES.get(f['issue_name'])
        if use_llm and openai.api_key:
            try:
                prompt = f"Given the cybersecurity finding '{f['issue_name']}' with severity {f['severity']} and category {f.get('category','general')}, provide a brief impact and recommendation. Format: Impact: ... Recommendation: ..."
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                text = resp.choices[0].message.content.strip()
                if 'Impact:' in text and 'Recommendation:' in text:
                    impact = text.split('Impact:')[1].split('Recommendation:')[0].strip()
                    recommendation = text.split('Recommendation:')[1].strip()
                    f['description'] = impact
                    f['recommendation'] = recommendation
                else:
                    # Fallback to template
                    if template:
                        f['description'] = template['impact']
                        f['recommendation'] = template['recommendation']
            except:
                if template:
                    f['description'] = template['impact']
                    f['recommendation'] = template['recommendation']
        else:
            if template:
                f['description'] = template['impact']
                f['recommendation'] = template['recommendation']
    return findings