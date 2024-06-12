import os
from typing import Any
from argapp import *


def __cwd() -> 'str':
    return os.path.abspath(os.getenv('PWD', ''))


def __root() -> 'str':
    result = __cwd()
    while result != '/':
        if os.path.exists(f'{result}/.uniws'):
            return result
        result = os.path.dirname(result)
    return ''


DIR_CWD = __cwd()
DIR_UWS = __root()
DIR_UNI = f'{DIR_UWS}/.uniws'


class Hardware:
    def __init__(
        self,
        app_connect: 'App' = None,
        app_power: 'App' = None,
        app_shell: 'App' = None,
        app_download: 'App' = None,
        app_upload: 'App' = None,
        app_action: 'App' = None,
    ) -> 'None':
        self.app_connect: 'App' = app_connect
        self.app_power: 'App' = app_power
        self.app_shell: 'App' = app_shell
        self.app_download: 'App' = app_download
        self.app_upload: 'App' = app_upload
        self.app_action: 'App' = app_action


class Software:
    def __init__(
        self,
        app_fetch: 'App' = None,
        app_build: 'App' = None,
        app_install: 'App' = None,
        app_test: 'App' = None,
        app_clean: 'App' = None,
        app_action: 'App' = None,
    ) -> 'None':
        self.app_fetch: 'App' = app_fetch
        self.app_build: 'App' = app_build
        self.app_install: 'App' = app_install
        self.app_test: 'App' = app_test
        self.app_clean: 'App' = app_clean
        self.app_action: 'App' = app_action


class AppWareCommand(App):
    def __init__(
        self,
        name: 'str',
        help: 'str',
    ) -> 'None':
        super().__init__(name, help)

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        if not DIR_UWS:
            raise CallError('This command must be run inside a workspace.')
        else:
            raise CallError('Not supported by this workspace.')


class AppHardwareCommand(AppWareCommand):
    def __init__(
        self,
        name: 'str',
        help: 'str',
        choices: 'dict[str, str]',
    ) -> 'None':
        super().__init__(name, help)
        self.arg_hw = None
        if not choices:
            return
        self.arg_hw = Arg(
            name='HW',
            help='A hardware to use.',
            choices=choices,
        )
        self.args.append(self.arg_hw)


class AppHardwareConnect(AppHardwareCommand):
    def __init__(
        self,
        state: 'str',
        states: 'dict[str, str]',
        choices: 'dict[str, str]',
        help: 'str' = 'Manage the connection to hardware.',
    ) -> 'None':
        super().__init__('connect', help, choices)
        self.arg_state = Arg(
            name='STATE',
            help='The state to set.',
            count='?',
            default=state or None,
            choices=states or None,
        )
        self.args.append(self.arg_state)


class AppHardwarePower(AppHardwareCommand):
    def __init__(
        self,
        state: 'str',
        states: 'dict[str, str]',
        choices: 'dict[str, str]',
        help: 'str' = 'Manage the power state of hardware.',
    ) -> 'None':
        super().__init__('power', help, choices)
        self.arg_state = Arg(
            name='STATE',
            help='The state to set.',
            count='?',
            default=state or None,
            choices=states or None,
        )
        self.args.append(self.arg_state)


class AppHardwareShell(AppHardwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Execute a command or start a session.',
    ) -> 'None':
        super().__init__('shell', help, choices)
        self.arg_cmd = Arg(
            name='CMD',
            help=('The command to execute as separate tokens.\n'
                  'If empty, start an interactive session.'),
            count='~',
        )
        self.args.append(self.arg_cmd)


class AppHardwareDownload(AppHardwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Download from the hardware.',
    ) -> 'None':
        super().__init__('download', help, choices)
        self.arg_src = Arg(
            name='SRC',
            help='Path to the remote source.',
        )
        self.args.append(self.arg_src)
        self.arg_dst = Arg(
            name='DST',
            help='Path to the local destination.',
        )
        self.args.append(self.arg_dst)


class AppHardwareUpload(AppHardwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Upload to the hardware.',
    ) -> 'None':
        super().__init__('upload', help, choices)
        self.arg_src = Arg(
            name='SRC',
            help='Path to the local source.',
        )
        self.args.append(self.arg_src)
        self.arg_dst = Arg(
            name='DST',
            help='Path to the remote destination.',
        )
        self.args.append(self.arg_dst)


class AppHardwareAction(AppHardwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Perform a workspace-specific action.',
    ) -> 'None':
        super().__init__('action', help, choices)


class AppSoftwareCommand(AppWareCommand):
    def __init__(
        self,
        name: 'str',
        help: 'str',
        choices: 'dict[str, str]',
    ) -> 'None':
        super().__init__(name, help)
        self.arg_sw = None
        if not choices:
            return
        self.arg_sw = Arg(
            name='SW',
            help=('A list of components to work with.\n'
                  'If not specified, the entire workspace is assumed'),
            count='*',
            choices=choices,
        )
        self.args.append(self.arg_sw)


class AppSoftwareFetch(AppSoftwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Fetch the software.',
    ) -> 'None':
        super().__init__('fetch', help, choices)


class AppSoftwareBuild(AppSoftwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Build the software.',
    ) -> 'None':
        super().__init__('build', help, choices)


class AppSoftwareInstall(AppSoftwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Install the software.',
    ) -> 'None':
        super().__init__('install', help, choices)


class AppSoftwareTest(AppSoftwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Test the software.',
    ) -> 'None':
        super().__init__('test', help, choices)


class AppSoftwareClean(AppSoftwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Clean the software.',
    ) -> 'None':
        super().__init__('clean', help, choices)


class AppSoftwareAction(AppSoftwareCommand):
    def __init__(
        self,
        choices: 'dict[str, str]',
        help: 'str' = 'Perform a workspace-specific action.',
    ) -> 'None':
        super().__init__('action', help, choices)
