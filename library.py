folders = ['fa-solid-900', 'fa-regular-400', 'fa-light-300', 'fa-thin-100', 'fa-duotone-900']
import json, shutil, os
shutil.rmtree('library', ignore_errors=True)
os.mkdir('library')
for folder in folders:
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FAG - Library""" + f" | {folder} " + """</title>
        <style>
            .icon-wrapper {
                display: flex;
                align-items: center;
                flex-direction: column;
                width: min-content;
            }
            .ttf-icon::before {
                font-family: 'FontAwesome';
            }
            body {
                display: grid;
                grid-template-columns: repeat(auto-fill, 60px);
                font-family: Arial, Helvetica, sans-serif;
            }
            @font-face{
                font-family:"FontAwesome";
                font-display:block;
                src:url(../../""" + f'{folder}' + """.ttf) format("truetype")}
        </style>
        
    </head>
    <body>

    """
    with open(f'library/{folder}.html', 'w') as f:
        f.write(template)
    with open(f'library/{folder}.html', 'a') as f:
        svgidx = 0
        svgs = []
        while True:
            try:
                with open(f'{folder}/{svgidx}.svg', 'r') as s:
                    svgs.append(s.read())
            except Exception:
                break
            svgidx += 1
        iconidxtb = {}
        with open(f'{folder}.json', 'r') as j:
            idxs = json.load(j)
            for key in idxs:
                iconidxtb[idxs[key][0]] = key
        print(iconidxtb)
        for idx, svg in enumerate(svgs):
            f.write('<div class="icon-wrapper">')
            f.write(svg)
            try:
                f.write(f'<style>#ttf-icon-{idx}::before' + '{' + f'content:"\{iconidxtb[idx].lower()}"' + '}</style>')
                f.write(f'<p id="ttf-icon-{idx}" class="ttf-icon"></p>')
                f.write(f'<a href="../../{folder}/{idx}.svg">{iconidxtb[idx]}</a>')
            except KeyError as e:
                print(e)
            f.write('</div>')
        f.write("\n</body>\n</html>")