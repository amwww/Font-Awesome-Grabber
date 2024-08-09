import json

folders = ['fa-solid-900', 'fa-regular-400', 'fa-light-300', 'fa-thin-100', 'fa-duotone-900', 'fa-duotone-combined-900', 'fa-sharp-solid-900', 'fa-sharp-regular-400', 'fa-sharp-light-300', 'fa-sharp-thin-100']
while True:
    mode = input('Welcome to the FA Class Search Engine. Please Select a Mode:\n1. Search by Unicode\n2. Search by FA Class Name\n')
    if mode == '1':
        unicode = input('Enter Unicode to Search: ')
        for folder in folders:
            with open(f'{folder}.json', 'r') as f:
                db = json.load(f)
                try:
                    match = db[unicode.upper()]
                    if folder.split("-")[1] == 'duotone':
                        if folder != 'fa-duotone-combined-900':
                            print(f'Found type duotone (primary). Located in {folder}/{match[0]}.svg')
                            print(f'Found type duotone (secondary). Located in {folder}/{db[f"10{unicode.upper()}"][0]}.svg')
                        else:
                            print(f'Found type duotone (combined). Located in fa-duotone-combined-900/{match[0]}.svg')
                    else:
                        print(f'Found type {folder.split("-")[1]}. Located in {folder}/{match[0]}.svg')
                except KeyError:
                    print(f'No Matches Found type {folder}.')
    elif mode == '2':
        name = input('Enter FA Class Name to Search: ')
        with open('icons.json') as f:
            db = json.load(f)
            try:
                match = db[name]
                print(f'Found Unicode {match}.')
            except KeyError:
                print('No Matches Found.')