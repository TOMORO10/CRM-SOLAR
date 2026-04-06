from bs4 import BeautifulSoup
import json
import re

try:
    with open('fenoge_crm.html', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')
    script_content = scripts[len(scripts)-1].string if scripts else ""
    
    with open('temp_script.js', 'w', encoding='utf-8') as f:
        f.write(script_content)
    print("Script extracted to temp_script.js")
except Exception as e:
    print("Error:", e)
