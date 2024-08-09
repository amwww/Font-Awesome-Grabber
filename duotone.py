import os, shutil, json, re
from tqdm import tqdm

print('Preparing Duotone...', end='')
shutil.rmtree('fa-duotone-combined-900', ignore_errors=True)
os.mkdir('fa-duotone-combined-900')
with open('fa-duotone-combined-900.json', 'w') as f:
    f.write('{\n\n}')
print(' | Done')

print('Building Duotone...')
with open('fa-duotone-900.json', 'r') as f:
    db = json.load(f)
    svgidxtb = {}
    for key in db:
        if key.startswith('10'):
            continue
        svgidxtb[db[key][0]] = key
    for idx in tqdm(svgidxtb):
        if svgidxtb[idx].startswith('10'):
            continue
        with open(f'fa-duotone-combined-900.json', 'r') as f:
            comb = json.load(f)
            comb[svgidxtb[idx]] = [idx]
        with open(f'fa-duotone-combined-900.json', 'w') as f:
            json.dump(comb, f, indent=4)
        with open(f'fa-duotone-900/{idx}.svg', 'r') as s:
            svg1 = s.read()
        try:
            with open(f'fa-duotone-900/{db[f"10{svgidxtb[idx]}"][0]}.svg', 'r') as s:
                svg2 = s.read()
        except Exception:
            svg2 = svg1
        innerSvg = re.findall(r'<symbol[ a-z="_0-9-.A-Z><\/#(,)]*<\/symbol><use[ a-z="_0-9-.A-Z><\/#(,)]*(?=<\/svg>)', svg1)
        wrapper1 = re.findall(r'<svg[ a-zA-Z0-9=".:\/-]*>', svg1)
        wrapper2 = re.findall(r'<svg[ a-zA-Z0-9=".:\/-]*>', svg2)
        if len(wrapper1) < 1:
            wrapper1 = wrapper2
        with open(f'fa-duotone-combined-900/{idx}.svg', 'w') as f:
            f.write(svg2.replace('</svg>', innerSvg[0] + '</svg>').replace(wrapper2[0], wrapper1[0]) if innerSvg else svg2)
print('Finished.')