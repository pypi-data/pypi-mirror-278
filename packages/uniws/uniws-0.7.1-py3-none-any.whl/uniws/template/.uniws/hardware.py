from uniws import *


def hardware() -> 'Hardware':
    return Hardware(
        app_connect=HardwareConnect(),
        app_power=HardwarePower(),
        app_shell=HardwareShell(),
        app_download=HardwareDownload(),
        app_upload=HardwareUpload(),
        app_action=HardwareAction(),
    )


def script_list(cmd: 'str', request: 'str' = '?') -> 'dict[str, str]':
    lines = sh(
        cmd=f'cd {DIR_UNI} && ./{cmd}.sh \'{request}\'',
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


class HardwareConnect(AppHardwareConnect):
    def __init__(self) -> 'None':
        states = script_list('hwc', '@')
        super().__init__(
            state=('' if not states else next(iter(states))),
            states=states,
            choices=script_list('hwc'),
        )

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('hwc', [
            args.get(self.arg_hw, '""'),
            args.get(self.arg_state, '""'),
        ])


class HardwarePower(AppHardwarePower):
    def __init__(self) -> 'None':
        states = script_list('hwp', '@')
        super().__init__(
            state=('' if not states else next(iter(states))),
            states=states,
            choices=script_list('hwp'),
        )

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('hwp', [
            args.get(self.arg_hw, '""'),
            args.get(self.arg_state, '""'),
        ])


class HardwareShell(AppHardwareShell):
    def __init__(self) -> 'None':
        super().__init__(script_list('hws'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        tokens: 'list[str]' = args[self.arg_cmd]
        for i in range(len(tokens)):
            tokens[i] = tokens[i].replace('"', '\\\"')
            tokens[i] = f'"{tokens[i]}"'
        tokens.insert(0, args.get(self.arg_hw, '""'))
        script_run('hws', tokens)


class HardwareDownload(AppHardwareDownload):
    def __init__(self) -> 'None':
        super().__init__(script_list('hwd'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('hwd', [
            args.get(self.arg_hw, '""'),
            args[self.arg_src],
            args[self.arg_dst],
        ])


class HardwareUpload(AppHardwareUpload):
    def __init__(self) -> 'None':
        super().__init__(script_list('hwu'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('hwu', [
            args.get(self.arg_hw, '""'),
            args[self.arg_src],
            args[self.arg_dst],
        ])


class HardwareAction(AppHardwareAction):
    def __init__(self) -> 'None':
        super().__init__(script_list('hwa'))

    def __call__(self, args: 'dict[Arg, Any]', apps: 'list[App]') -> 'None':
        script_run('hwa', [args.get(self.arg_hw, '""')])
