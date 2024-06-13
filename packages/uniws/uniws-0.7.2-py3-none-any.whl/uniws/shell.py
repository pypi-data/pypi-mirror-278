import subprocess
import argapp


class ShellResult:
    def __init__(
        self,
        cmd: 'str',
        out: 'str',
        code: 'int',
    ) -> 'None':
        self.cmd = cmd
        self.out = out
        self.code = code


class ShellError(argapp.CallError):
    def __init__(self, result: 'ShellResult') -> 'None':
        super().__init__(
            text=str(
                f'The command failed (code {result.code}):\n'
                f'{result.cmd}'
            ),
            code=result.code,
        )
        self.cmd = result.cmd
        self.out = result.out


def sh(
    cmd: 'str',
    cap: 'bool' = False,
    chk: 'bool' = True,
) -> 'ShellResult':
    '''
    Execute a shell command, note that:
     * `/bin/bash` is used as the shell.
     * `expand_aliases` is enabled prior to execution.

    Parameters:
     * `cmd` - a shell command to execute. The original value is never
       modified, but extra commands are prepended (see above).
     * `cap` - whether to capture the output (both stdout and stderr).
     * `chk` - whether to raise a `ShellError` if the return code is not zero.

    Exceptions:
     * `ShellError`, if `chk` is `True` and `cmd` returns a non-zero code.

    Returns:
     * `ShellResult`, with the fields properly set.
    '''
    args = [f'shopt -s expand_aliases;\n{cmd}']
    kwds = {
        'shell': True,
        'universal_newlines': True,
        'executable': '/bin/bash',
    }
    if cap:
        kwds['stdout'] = subprocess.PIPE
        kwds['stderr'] = subprocess.STDOUT
    proc = subprocess.Popen(*args, **kwds)
    proc.wait()
    result = ShellResult(
        cmd=cmd,
        out=('' if not cap else proc.stdout.read()),
        code=proc.returncode,
    )
    if chk and result.code != 0:
        raise ShellError(result)
    return result
