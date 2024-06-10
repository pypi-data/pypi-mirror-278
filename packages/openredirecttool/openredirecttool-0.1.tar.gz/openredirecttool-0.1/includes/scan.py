import re
from urllib.parse import urlparse, parse_qs

def is_open_redirect(url):
    """
    Check if the given URL contains an open redirect vulnerability.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    for param, values in query_params.items():
        for value in values:
            if is_external_url(value):
                return True
    return False

def is_external_url(url):
    """
    Check if the given URL is an external URL.
    """
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)

def cvescan(url, output_file):
    """
    Scan the given URL for potential open redirect vulnerabilities
    and write the result to the specified output file.
    """
    vulnerability_found = is_open_redirect(url)
    result = (
        f"Potential open redirect vulnerability found at {url}."
        if vulnerability_found else
        f"No vulnerability found at {url}."
    )
    
    with open(output_file, 'w') as file:
        file.write(result)
    
    print(f"Scan result written to '{output_file}'.")

if __name__ == "__main__":
    # Example usage
    example_url = 'http://example.com?redirect=http://malicious.com'
    output_file = 'scan_result.txt'
    cvescan(example_url, output_file)