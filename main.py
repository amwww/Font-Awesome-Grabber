import ziafont
import brotli, os, requests, json, shutil
from fontTools.ttLib import woff2
from tqdm import tqdm

def convert(infilename, outfilename):
    with open(infilename , mode='rb') as infile:
        with open(outfilename, mode='wb') as outfile:
            woff2.decompress(infile, outfile)

fonts = [
    'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-solid-900.woff2',
    'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-regular-400.woff2',
    'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-light-300.woff2',
    'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-thin-100.woff2',
    'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-duotone-900.woff2'
]
print('Processing Fonts...')
for font in tqdm(fonts):
    response = requests.get(font)
    with open(font.split('/')[-1], 'wb') as f:
        f.write(response.content)
    convert(font.split('/')[-1], font.split('/')[-1].replace('.woff2', '.ttf'))
    os.remove(font.split('/')[-1])
    fontloc = font.split('/')[-1].replace('.woff2', '.ttf')
    zfont = ziafont.Font(fontloc)
    glyphid = 0
    shutil.rmtree(fontloc.replace(".ttf", ""), ignore_errors=True)
    os.makedirs(fontloc.replace(".ttf", ""), exist_ok=True)
    with open(f'{fontloc.replace(".ttf", "")}.json', 'w') as f:
        f.write('{\n\n}')
    while True:
        try:
            glyph = zfont.glyph_fromid(glyphid)
            with open(f'{fontloc.replace(".ttf", "")}/{glyphid}.svg', 'w+') as f:
                f.write(glyph.svg())
            with open(f'{fontloc.replace(".ttf", "")}.json', 'r') as f:
                db = json.load(f)
                for char in glyph.char:
                    if f'{ord(char):X}' in db:
                        db[f'{ord(char):X}'].append(glyphid)
                    else:
                        db[f'{ord(char):X}'] = [glyphid]
            with open(f'{fontloc.replace(".ttf", "")}.json', 'w+') as f:
                json.dump(db, f, indent=4)
            glyphid += 1
        except Exception as e:
            break
if input('Press Enter to Continue with CSS or press Q to Quit...').lower() != 'q':
    import css