from rich import print as print_rich
from rich_menu import Menu
import json, os, datetime, shutil
from tqdm import tqdm

with open('version.txt', 'r') as f:
    version = f.read()

print_rich(f'[bold blue]Welcome To FontAwesome Grabber[/bold blue][bold magenta] Installer [/bold magenta][bold green]by amwww [/bold green][bold italic green](v{version})[/bold italic green]\nhttps://github.com/amwww/Font-Awesome-Grabber\n')

installer = Menu(
    "Download & Proccess Fonts",
    "Download & Proccess CSS",
    "Install Library",
    "Duotone Builder",
    "Search Icons",
    "Reset All",
    "Backup All",
    "Restore Backup",
    "Exit",
    title='[bold yellow]Installer Menu[/bold yellow]',
    align='left',
    highlight_color='italic blue',
    panel_title="Select an Option",
    rule=True
)

def hasdone(proccess) -> bool|dict:
    with open('installer.json', 'r') as f:
        db = json.load(f)
        if proccess in db:
            return db[proccess]
        else:
            return False
        
def setdone(proccess):
    with open('installer.json', 'r') as f:
        db = json.load(f)
        db[proccess] = {
            'done': True,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    with open('installer.json', 'w') as f:
        json.dump(db, f, indent=4)
    return True

if not os.path.isfile('installer.json'):
    print_rich('[bold red]! Installer Config Not Found ![/bold red]')
    print_rich('[bold yellow]> Creating Installer Config[/bold yellow]')
    with open('installer.json', 'w') as f:
        json.dump({}, f, indent=4)
    print_rich('[bold green]Done.[/bold green]')

with open('installer.json', 'r') as f:
    try:
        json.load(f)
    except Exception as e:
        print_rich('[bold red]In[/bold red]')
        with open('installer.json', 'w') as f:
            json.dump({}, f, indent=4)
files = ['fa-solid-900.json', 'fa-regular-400.json', 'fa-light-300.json', 'fa-thin-100.json', 'fa-duotone-900.json', 'fa-duotone-combined-900.json', 'icons.json', 'fa-thin-100.ttf', 'fa-light-300.ttf', 'fa-regular-400.ttf', 'fa-solid-900.ttf', 'fa-duotone-900.ttf', 'installer.json']
folders = ['libary', 'fa-solid-900', 'fa-regular-400', 'fa-light-300', 'fa-thin-100', 'fa-duotone-900', 'fa-duotone-combined-900', 'fa-sharp-solid-900', 'fa-sharp-regular-400', 'fa-sharp-light-300', 'fa-sharp-thin-100']
while True:
    match installer.ask(screen=False):
        case "Backup All":
            print_rich('[bold yellow]Backing Up Files...[/bold yellow]')
            if not os.path.isdir('backups'):
                os.mkdir('backups')
            backupfolder = f'backup-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
            os.mkdir(backupfolder)
            for file in tqdm(files):
                if os.path.isfile(file):
                    os.rename(file, f'backups/{backupfolder}/{file}')
                    shutil.copy(f'backups/{backupfolder}/{file}', file)
            for folder in tqdm(folders):
                if os.path.isdir(folder):
                    os.rename(folder, f'backups/{backupfolder}/{folder}')
                    shutil.copytree(f'backups/{backupfolder}/{folder}', folder)
            print_rich(f'[bold green]Done. Backed up as /{backupfolder}.[/bold green]')
        case "Restore Backup":
            backups = []
            for folder in os.listdir('backups'):
                if folder.startswith('backup-'):
                    backups.append(folder)
            backupmenu = Menu(*backups, 'Exit', title='[bold yellow]Select a Backup[/bold yellow]', align='left', highlight_color='italic blue', panel_title='Select a Backup')
            backup = backupmenu.ask(screen=False)
            print(backup)
            if backup == 'Exit':
                continue
            print_rich(f'[bold yellow]Restoring Backup {backup}...[/bold yellow]')
            dir = os.getcwd()
            for file in tqdm(os.listdir(backup)):
                if os.path.isfile(f'backups/{backup}/{file}'):
                    os.rename(f'backups/{backup}/{file}', f'{file}')
                    shutil.copy(f'{file}', f'backups/{backup}/{file}')
                if os.path.isdir(f'backups/{backup}/{file}'):
                    os.rename(f'backups/{backup}/{file}', f'{file}')
                    shutil.copytree(f'{file}', f'backups/{backup}/{file}')
        case "Reset All":
            confirm_menu = Menu('Yes', 'No', title='[bold yellow]Are you sure?[/bold yellow]', align='left', highlight_color='italic blue', panel_title='Confirm Reset')
            confirm = confirm_menu.ask(screen=False)
            if confirm == 'No':
                continue
            print_rich('[bold yellow]Resetting All...[/bold yellow]')
            for file in tqdm(files):
                if os.path.isfile(file):
                    os.remove(file)
            for folder in tqdm(folders):
                if os.path.isdir(folder):
                    shutil.rmtree(folder)
            print_rich('[bold green]Done.[/bold green]')
            print_rich('[bold green]Please Rerun Installer.[/bold green]')
            exit()
        case "Download & Proccess Fonts":
            from fonts import fonts
            if hasdone('fonts'):
                reinstall_menu = Menu('Yes', 'No', title='[bold yellow]Fonts Already Installed. Reinstall?[/bold yellow]', align='left', highlight_color='italic blue', panel_title='Reinstall Fonts')
                reinstall = reinstall_menu.ask(screen=False)
                if reinstall == 'No':
                    continue
            print_rich('[bold yellow]Downloading & Proccessing Fonts...[/bold yellow]')
            fonts()
            setdone('fonts')
            print_rich('[bold green]Done.[/bold green]')
        case "Download & Proccess CSS":
            if not hasdone('fonts'):
                print_rich('[bold red]! Please Download & Proccess Fonts First ![/bold red]')
                continue
            from css import css
            if hasdone('css'):
                reinstall_menu = Menu('Yes', 'No', title='[bold yellow]CSS Already Processed. Reproccess?[/bold yellow]', align='left', highlight_color='italic blue', panel_title='Reinstall CSS')
                reinstall = reinstall_menu.ask(screen=False)
                if reinstall == 'No':
                    continue
            print_rich('[bold yellow]Downloading & Proccessing CSS...[/bold yellow]')
            css()
            setdone('css')
            print_rich('[bold green]Done.[/bold green]')
        case "Install Library":
            if not hasdone('fonts'):
                print_rich('[bold red]! Please Download & Proccess Fonts First ![/bold red]')
                continue
            if not hasdone('css'):
                print_rich('[bold red]! Please Download & Proccess CSS First ![/bold red]')
                continue
            if not hasdone('duotone'):
                print_rich('[bold red]! Please Build Duotone First ![/bold red]')
                continue
            from library import library
            if hasdone('library'):
                reinstall_menu = Menu('Yes', 'No', title='[bold yellow]Library Already Installed. Reinstall?[/bold yellow]', align='left', highlight_color='italic blue', panel_title='Reinstall Library')
                reinstall = reinstall_menu.ask(screen=False)
                if reinstall == 'No':
                    continue
            print_rich('[bold yellow]Installing Library...[/bold yellow]')
            library()
            setdone('library')
            print_rich('[bold green]Done.[/bold green]')
        case "Duotone Builder":
            if not hasdone('fonts'):
                print_rich('[bold red]! Please Download & Proccess Fonts First ![/bold red]')
                continue
            if not hasdone('css'):
                print_rich('[bold red]! Please Download & Proccess CSS First ![/bold red]')
                continue
            from duotone import duotone
            print_rich('[bold yellow]Building Duotone...[/bold yellow]')
            duotone()
            setdone('duotone')
            print_rich('[bold green]Done.[/bold green]')
        case "Search Icons":
            if not hasdone('fonts'):
                print_rich('[bold red]! Please Download & Proccess Fonts First ![/bold red]')
                continue
            if not hasdone('css'):
                print_rich('[bold red]! Please Download & Proccess CSS First ![/bold red]')
                continue
            if not hasdone('duotone'):
                print_rich('[bold red]! Please Build Duotone First ![/bold red]')
                continue
            from search import search
            search()
        case "Exit":
            exit()