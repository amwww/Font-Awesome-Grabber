import requests, re, json
from tqdm import tqdm

print('Downloading CSS...', end='')
css = requests.get('https://site-assets.fontawesome.com/releases/v6.6.0/css/all.css').text
print(' | Done')

print('Preparing CSS...', end='')
with open('all.css', 'w') as f:
    f.write(css)
with open('icons.json', 'w') as f:
    f.write('{\n\n}')
print(' | Done')

print('Parsing CSS...', end='')
chars = re.findall(r'(?<={content:")[a-z0-9\\]+(?="})', css)
print(' | Done')

print('Extracting Icons...')
for char in tqdm(chars):
    reg = re.compile('[.a-z-0-9,:]+(?=:(after|before){content:\"' + char.replace('\\', '\\\\') + '\")')
    group = reg.findall(css)[0]
    reg = re.compile('[.a-z-0-9,:]+(?=:' + group + '{content:\"' + char.replace('\\', '\\\\') + '\")')
    classes = reg.findall(css)[0].replace(f':{group}', '').split(',')
    with open('icons.json', 'r') as f:
        db = json.load(f)
        for cl in classes:
            db[cl] = char.replace('\\', '')
    with open('icons.json', 'w') as f:
        json.dump(db, f, indent=4)
print('Finished.')