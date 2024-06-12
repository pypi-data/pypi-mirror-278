from uniws import *


def software() -> 'Software':
    return Software(
        app_fetch=SoftwareFetch(),
        app_build=SoftwareBuild(),
        app_install=SoftwareInstall(),
        app_test=SoftwareTest(),
        app_clean=SoftwareClean(),
        app_action=SoftwareAction(),
    )


def script_list(cmd: 'str') -> 'dict[str, str]':
    lines = sh(
        cmd=f'cd {DIR_UNI} && ./{cmd}.sh \'?\'',
        cap=True,
    ).out.splitlines()
    choices = {}
    for x in lines:
        pair = x.split(' ', 1)
        pair.append('')
        choices[pair[0].strip()] = pair[1].strip()
    return choices


def script_run(cmd: 'str', args: 'list[str]') -> 'list[str]':
    sh(f'cd {DIR_UNI} && ./{cmd}.sh \'!\' ' + ' '.join(args))


class SoftwareFetch(AppSoftwareFetch):
    def __init__(self) -> 'None':
        super().__init__(script_list('swf'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('swf', args.get(self.arg_sw, []))


class SoftwareBuild(AppSoftwareBuild):
    def __init__(self) -> 'None':
        super().__init__(script_list('swb'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('swb', args.get(self.arg_sw, []))


class SoftwareInstall(AppSoftwareInstall):
    def __init__(self) -> 'None':
        super().__init__(script_list('swi'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('swi', args.get(self.arg_sw, []))


class SoftwareTest(AppSoftwareTest):
    def __init__(self) -> 'None':
        super().__init__(script_list('swt'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('swt', args.get(self.arg_sw, []))


class SoftwareClean(AppSoftwareClean):
    def __init__(self) -> 'None':
        super().__init__(script_list('swc'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('swc', args.get(self.arg_sw, []))


class SoftwareAction(AppSoftwareAction):
    def __init__(self) -> 'None':
        super().__init__(script_list('swa'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('swa', args.get(self.arg_sw, []))
