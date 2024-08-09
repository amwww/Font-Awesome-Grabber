import json, shutil, os
from tqdm import tqdm

folders = ['fa-solid-900', 'fa-regular-400', 'fa-light-300', 'fa-thin-100', 'fa-duotone-900', 'fa-duotone-combined-900', 'fa-sharp-solid-900', 'fa-sharp-regular-400', 'fa-sharp-light-300', 'fa-sharp-thin-100']

def library():
    print('Cleaning Library...', end='')
    shutil.rmtree('library', ignore_errors=True)
    os.mkdir('library')
    print(' | Done')
    print('Building Library...')
    for idx, folder in enumerate(folders):
        print(f'Building {folder}... {idx+1}/{len(folders)}')
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
                main {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, 80px);
                    font-family: Arial, Helvetica, sans-serif;
                }
                @font-face{
                    font-family:"FontAwesome";
                    font-display:block;
                    src:url(../""" + f'{folder}' + """.ttf) format("truetype")
                }
                h1, a, p {
                    font-family:Arial;
                }
                .class-name{
                    font-size: 10px;
                }
            </style>
            
        </head>
        <body>
        <h1>Font Awesome Grabber by amwww</h1>
        <a href="https://github.com/amwww/Font-Awesome-Grabber">View on Github</a>
        <p>Font """ + f"{folder}" + """ </p>
        """ + " ".join([f'<a href="{fname}.html">{fname}</a>' for fname in folders]) + """
        <hr>
        <main>
        """
        with open(f'library/{folder}.html', 'w') as f:
            f.write(template)
        with open(f'library/{folder}.html', 'a') as f:
            svgidx = 0
            startidx = 0
            try:
                with open(f'{folder}/0.svg', 'r') as s:
                    pass
            except Exception as e:
                svgidx = 1
                startidx = 1
            svgs = []
            while True:
                try:
                    with open(f'{folder}/{svgidx}.svg', 'r') as s:
                        svgs.append(s.read())
                except Exception as e:
                    break
                svgidx += 1
            iconidxtb = {}
            with open(f'{folder}.json', 'r') as j:
                idxs = json.load(j)
                for key in idxs:
                    if idxs[key][0] in iconidxtb:
                        iconidxtb[idxs[key][0]].append(key)
                        continue
                    iconidxtb[idxs[key][0]] = [key]
            uniclass = {}
            with open(f'icons.json', 'r') as i:
                icons = json.load(i)
                for classname in icons:
                    uniclass[icons[classname]] = classname
            for idx, svg in enumerate(svgs):
                f.write('<div class="icon-wrapper">')
                f.write(svg)
                try:
                    for fidx in iconidxtb[idx]:
                        f.write(f'<a href="../{folder}/{idx}.svg">{fidx}</a>')
                        try:

                            f.write(f'<p class="class-name">{uniclass[fidx.lower()]}</p>')
                        except KeyError:
                            pass
                    f.write(f'<style>#ttf-icon-{idx}::before' + '{' + f'content:"\{iconidxtb[idx][0].lower()}"' + '}</style>')
                    f.write(f'<p id="ttf-icon-{idx}" class="ttf-icon"></p>')
                except KeyError:
                    pass
                f.write('</div>')
            f.write("\n</main>\n</body>\n</html>")
    print('Finished.')

if __name__ == '__main__':
    library()