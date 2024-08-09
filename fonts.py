import ziafont
import brotli, os, requests, json, shutil
from fontTools.ttLib import woff2
from tqdm import tqdm

def convert(infilename, outfilename):
    with open(infilename , mode='rb') as infile:
        with open(outfilename, mode='wb') as outfile:
            woff2.decompress(infile, outfile)

def fonts():
    fonts = [
        'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-solid-900.woff2',
        'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-regular-400.woff2',
        'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-light-300.woff2',
        'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-thin-100.woff2',
        'https://site-assets.fontawesome.com/releases/v6.6.0/webfonts/fa-duotone-900.woff2'
    ]
    print('Processing Fonts...')
    for idx, font in enumerate(fonts):
        print(f'Proccessing {idx+1}/{len(fonts)}...')
        print('Downloading Font...', end='')
        response = requests.get(font)
        print(' | Done')
        print('Converting Font...', end='')
        with open(font.split('/')[-1], 'wb') as f:
            f.write(response.content)
        convert(font.split('/')[-1], font.split('/')[-1].replace('.woff2', '.ttf'))
        os.remove(font.split('/')[-1])
        fontloc = font.split('/')[-1].replace('.woff2', '.ttf')
        print(' | Done')
        print('Loading Font...', end='')
        zfont = ziafont.Font(fontloc)
        print(' | Done')
        print('Cleaning Font Directory...', end='')
        shutil.rmtree(fontloc.replace(".ttf", ""), ignore_errors=True)
        os.makedirs(fontloc.replace(".ttf", ""), exist_ok=True)
        with open(f'{fontloc.replace(".ttf", "")}.json', 'w') as f:
            f.write('{\n\n}')
        print(' | Done')
        print('Counting Glyphs...', end='')
        glyphid = 0
        while True:
            try:
                glyph = zfont.glyph_fromid(glyphid)
                glyphid += 1
            except Exception as e:
                break
        print(' | Done')
        total = glyphid
        glyphid = 0
        for glyphid in tqdm(range(total)):
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
            except Exception as e:
                break

if __name__ == '__main__':
    fonts()