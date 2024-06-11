import sys

from typing import Any
from argapp import App, AppHelper, Arg
from .shell import *
from .lib import *

if DIR_UWS:
    sys.path.insert(0, DIR_UNI)
    from hardware import hardware
    from software import software
else:
    def hardware() -> 'Hardware':
        return Hardware()

    def software() -> 'Software':
        return Software()


ABBRS = {
    'hwc': "connect",
    'hwp': "power",
    'hws': "shell",
    'hwd': "download",
    'hwu': "upload",
    'hwa': "action",
    'swf': "fetch",
    'swb': "build",
    'swi': "install",
    'swt': "test",
    'swc': "clean",
    'swa': "action",
}


class Uniws(App):
    def __init__(self) -> 'None':
        super().__init__(
            name='uniws',
            help='Uniform workspace CLI.',
        )
        self.apps.append(UniwsSetup())
        self.apps.append(UniwsReset())
        self.apps.append(UniwsInit())
        self.apps.append(UniwsWare(
            name='sw',
            help='Work with the software.',
            apps={
                'fetch': AppSoftwareFetch({}),
                'build': AppSoftwareBuild({}),
                'install': AppSoftwareInstall({}),
                'test': AppSoftwareTest({}),
                'clean': AppSoftwareClean({}),
                'action': AppSoftwareAction({}),
            },
            ware=software(),
        ))
        self.apps.append(UniwsWare(
            name='hw',
            help='Work with the hardware.',
            apps={
                'connect': AppHardwareConnect('', {}, {}),
                'power': AppHardwarePower('', {}, {}),
                'shell': AppHardwareShell({}),
                'download': AppHardwareDownload({}),
                'upload': AppHardwareUpload({}),
                'action': AppHardwareAction({}),
            },
            ware=hardware(),
        ))


class UniwsSetup(App):
    def __init__(self) -> 'None':
        super().__init__(
            name='setup',
            help='Manage app. Add shortcuts and completion.'
        )

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        path_uniws = sh('which uniws', cap=True).out.strip()
        # Do not append PYTHON_ARGCOMPLETE_OK if it is already there.
        if sh(
            cmd=f'grep "PYTHON_ARGCOMPLETE_OK" {path_uniws}',
            cap=True,
            chk=False,
        ).code:
            print(f'Modify: {path_uniws}')
            sh(f'echo "# PYTHON_ARGCOMPLETE_OK" >> {path_uniws}')
        # Create shortcut commands.
        for abbr in ABBRS:
            path_abbr = f'{os.path.dirname(path_uniws)}/{abbr}'
            # Do not overwrite the existing ones.
            if os.path.exists(path_abbr):
                print(f'Ignore: {path_abbr}')
                continue
            print(f'Create: {path_abbr}')
            # Generate the file on-the-fly.
            text_abbr = (
                f'#!/usr/bin/env python3\n'
                f'# PYTHON_ARGCOMPLETE_OK\n'
                f'import sys\n'
                f'from uniws.app import Uniws\n'
                f'from argapp import main\n'
                f'\n'
                f'argv = sys.argv[1:]\n'
                f'argv.insert(0, \"{ABBRS[abbr]}\")\n'
                f'argv.insert(0, \"{abbr[:2]}\")\n'
                f'argv.insert(0, \"uniws\")\n'
                f'main(Uniws(), argv)'
            )
            sh(f'true'
               f' && echo \'{text_abbr}\' > {path_abbr}'
               f' && chmod 755 {path_abbr}'
               f';')


class UniwsReset(App):
    def __init__(self) -> 'None':
        super().__init__(
            name='reset',
            help='Manage app. Remove shortcuts and revert changes.'
        )

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        path_uniws = sh('which uniws', cap=True).out.strip()
        # Delete PYTHON_ARGCOMPLETE_OK.
        if not sh(
            cmd=f'grep "PYTHON_ARGCOMPLETE_OK" {path_uniws}',
            cap=True,
            chk=False,
        ).code:
            print(f'Modify: {path_uniws}')
            sh(f'sed -i \'/^# PYTHON_ARGCOMPLETE_OK$/d\' {path_uniws}')
        # Remove shortcut commands.
        for abbr in ABBRS:
            path_abbr = f'{os.path.dirname(path_uniws)}/{abbr}'
            # Do not remove what sumply has the same name.
            if sh(f'grep "Uniws()" {path_abbr}', True, False).code:
                print(f'Ignore: {path_abbr}')
            else:
                print(f'Remove: {path_abbr}')
                sh(f'rm {path_abbr}')


class UniwsInit(App):
    def __init__(self) -> 'None':
        super().__init__(
            name='init',
            help='Initialize a new workspace.'
        )
        self.arg_dir = Arg(
            name='DIR',
            help='Empty or non-existent directory. Defaults to current.',
            count='?',
        )
        self.args.append(self.arg_dir)

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        dir = os.path.abspath(args[self.arg_dir] or os.getcwd())
        if os.path.exists(dir):
            if os.path.isdir(dir):
                if len(os.listdir(dir)) != 0:
                    raise CallError(f'The directory is not empty: {dir}')
            else:
                raise CallError(f'Not a directory: {dir}')
        else:
            os.makedirs(dir, 0o755)
        sh(f'cp -RaT {os.path.dirname(__file__)}/template {dir}')
        sh(f'rm -rf {dir}/.uniws/__pycache__')


class UniwsWare(App):
    def __init__(
        self,
        name: 'str',
        help: 'str',
        apps: 'dict[str, AppWareCommand]',
        ware: 'Hardware | Software',
    ) -> 'None':
        super().__init__(name, help)
        for x in apps:
            app = getattr(ware, f'app_{x}') or apps[x]
            self.apps.append(app)
