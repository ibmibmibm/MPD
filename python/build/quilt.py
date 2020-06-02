import subprocess
from shlex import quote

def msys_check_call(command, **kwargs):
    quoted = ' '.join(map(lambda x: quote(x), command))
    command = ['C:\\tools\\msys64\\msys2_shell.cmd', '-msys2', '-defterm', '-no-start', '-use-full-path', '-here', '-c', quoted]
    subprocess.check_call(command, **kwargs)

def run_quilt(toolchain, cwd, patches_path, *args):
    env = dict(toolchain.env)
    env['QUILT_PATCHES'] = patches_path
    if toolchain.is_windows and toolchain.native:
        msys_check_call(['quilt'] + list(args), cwd=cwd, env=env)
    else:
        subprocess.check_call(['quilt'] + list(args), cwd=cwd, env=env)

def push_all(toolchain, src_path, patches_path):
    run_quilt(toolchain, src_path, patches_path, 'push', '-a')
