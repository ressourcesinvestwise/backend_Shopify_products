import re

def extract_product_id(url):
    match = re.search(r'/item/(\d+)\.html', url)
    return match.group(1) if match else None