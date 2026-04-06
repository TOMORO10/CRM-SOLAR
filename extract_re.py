import re

try:
    with open('fenoge_crm.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the last script tag content
    match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
    if match:
        script_content = match.group(1)
        with open('temp_script.js', 'w', encoding='utf-8') as f:
            f.write(script_content)
        print("Script successfully extracted")
    else:
        print("Script tag not found")
except Exception as e:
    print("Error:", e)
