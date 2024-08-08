import json


folders = ['fa-solid-900', 'fa-regular-400', 'fa-light-300', 'fa-thin-100', 'fa-duotone-900']
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
                        print(f'Foreground: {folder}/{match[0]}.svg')
                        print(f'Background: {folder}/{db[f"10{unicode.upper()}"][0]}.svg')
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