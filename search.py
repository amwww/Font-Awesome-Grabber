import json
from rich import print as print_rich
from rich_menu import Menu

folders = ['fa-solid-900', 'fa-regular-400', 'fa-light-300', 'fa-thin-100', 'fa-duotone-900', 'fa-duotone-combined-900', 'fa-sharp-solid-900', 'fa-sharp-regular-400', 'fa-sharp-light-300', 'fa-sharp-thin-100']

def search():
    while True:
        mode = Menu(
            'Search Exact Unicode',
            'Search Exact Class',
            'Browse Classes',
            'Exit',
            title='[bold yellow]Select a Search Mode[/bold yellow]',
            align='left',
            highlight_color='italic blue',
            panel_title='Search Mode',
        ).ask(screen=True)
        if mode == 'Search Exact Unicode':
            print_rich('[bold yellow]Searching Exact Unicode[/bold yellow] | [bold green]Enter Unicode >[/bold green]', end=' ')
            search = input('').upper()
            for folder in folders:
                with open(f'{folder}.json', 'r') as f:
                    db = json.load(f)
                    try:
                        result = db[search]
                        print_rich(f'[bold green]Found[/bold green] | [bold yellow]{folder}[/bold yellow]/[bold blue]{result[0]}.svg[/bold blue]')
                    except Exception as e:
                        print_rich(f'[bold red]Not Found[/bold red] | [bold yellow]{folder}[/bold yellow]')
        elif mode == 'Search Exact Class':
            print_rich('[bold yellow]Searching Exact Class[/bold yellow] | [bold green]Enter Class >[/bold green]', end=' .fa-')
            search = f".fa-{input('').lower()}"
            with open('icons.json', 'r') as f:
                db = json.load(f)
                try:
                    result = db[search]
                    print_rich(f'[bold green]Found[/bold green] | [bold yellow]Unicode[/bold yellow] | [bold blue]{result}[/bold blue]')
                    continuemenu = Menu(
                        f'Search Unicode for {search}',
                        'Continue',
                        title='[bold yellow]Search Results[/bold yellow]',
                        align='left',
                        highlight_color='italic blue',
                        panel_title='',
                    ).ask(screen=False)
                    if continuemenu == f'Search Unicode for {search}':
                        for folder in folders:
                            with open(f'{folder}.json', 'r') as f:
                                db = json.load(f)
                                try:
                                    idx = db[result.upper()]
                                    print_rich(f'[bold green]Found[/bold green] | [bold yellow]{folder}[/bold yellow]/[bold blue]{idx[0]}.svg[/bold blue]')
                                except Exception as e:
                                    print_rich(f'[bold red]Not Found[/bold red] | [bold yellow]{folder}[/bold yellow]')
                    else:
                        continue
                except Exception as e:
                    print_rich(f'[bold red]Not Found[/bold red]')
        elif mode == 'Browse Classes':
            print_rich('[bold yellow]Browse Classes[/bold yellow] | [bold green]Enter Class >[/bold green]', end=' .fa-')
            search = input('').lower()
            results = []
            with open('icons.json', 'r') as f:
                db = json.load(f)
                for key in db:
                    if search in key:
                        results.append(f'{key} | {db[key]}')
            browsemenu = Menu('Exit', *results, title='[bold yellow]Search Results[/bold yellow]', align='left', highlight_color='italic blue', panel_title='Search Results')
            result = browsemenu.ask(screen=False)
            if result == 'Exit':
                break
            continuemenu = Menu(
                f'Search Unicode for {result.split(" | ")[1]}',
                'Continue',
                title='[bold yellow]Search Results[/bold yellow]',
                align='left',
                highlight_color='italic blue',
                panel_title='',
            ).ask(screen=False)
            if continuemenu == f'Search Unicode for {result.split(" | ")[1]}':
                for folder in folders:
                    with open(f'{folder}.json', 'r') as f:
                        db = json.load(f)
                        try:
                            idx = db[result.split(" | ")[1].upper()]
                            print_rich(f'[bold green]Found[/bold green] | [bold yellow]{folder}[/bold yellow]/[bold blue]{idx[0]}.svg[/bold blue]')
                        except Exception as e:
                            print_rich(f'[bold red]Not Found[/bold red] | [bold yellow]{folder}[/bold yellow]')
            else:
                continue
        elif mode == 'Exit':
            break
        continuemenu = Menu(
            'Continue',
            'Exit',
            title='[bold yellow]Search Results[/bold yellow]',
            align='left',
            highlight_color='italic blue',
            panel_title='',
        ).ask(screen=False)
        if continuemenu == 'Exit':
            break