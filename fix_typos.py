with open('fenoge_crm.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('/\\n/\\g', '/\\n/g')
text = text.replace('/\\r/\\g', '/\\r/g')
text = text.replace('/;/\\g', '/;/g')

with open('fenoge_crm.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Typos fixed!")
