import os.path, subprocess
from shlex import quote

from build.project import Project


def msys_check_call(command, **kwargs):
    quoted = ' '.join(map(lambda x: quote(x), command))
    command = ['C:\\tools\\msys64\\msys2_shell.cmd', '-msys2', '-defterm', '-no-start', '-use-full-path', '-here', '-c', quoted]
    subprocess.check_call(command, **kwargs)


class FfmpegProject(Project):
    def __init__(self, url, md5, installed, configure_args=[],
                 cppflags='',
                 **kwargs):
        Project.__init__(self, url, md5, installed, **kwargs)
        self.configure_args = configure_args
        self.cppflags = cppflags

    def _filter_cflags(self, flags):
        # FFmpeg expects the GNU as syntax
        flags = flags.replace(' -integrated-as ', ' -no-integrated-as ')
        return flags

    def build(self, toolchain):
        if not self.edits:
            self.edits = {}
        if toolchain.is_windows and toolchain.native:
            self.edits['configure'] = lambda data: data.replace('check_cppflags -D_FILE_OFFSET_BITS=64\n', '').replace('check_cppflags -D_LARGEFILE_SOURCE\n', '')

        src = self.unpack(toolchain)
        build = self.make_build_path(toolchain)

        if toolchain.is_arm:
            arch = 'arm'
        elif toolchain.is_aarch64:
            arch = 'aarch64'
        else:
            arch = 'x86'

        if toolchain.is_windows:
            if toolchain.native:
                target_os = 'win64' if 'x86_64' in toolchain.arch else 'win32'
            else:
                target_os = 'mingw32'
        else:
            target_os = 'linux'

        configure = [
            os.path.join(os.path.relpath(src, start=build), 'configure'),
            '--cc=' + toolchain.cc,
            '--cxx=' + toolchain.cxx,
            '--nm=' + toolchain.nm,
            '--extra-cflags=' + self._filter_cflags(toolchain.cflags) + ' ' + toolchain.cppflags + ' ' + self.cppflags,
            '--extra-cxxflags=' + self._filter_cflags(toolchain.cxxflags) + ' ' + toolchain.cppflags + ' ' + self.cppflags,
            '--extra-ldflags=' + toolchain.ldflags,
            '--extra-libs=' + toolchain.libs,
            '--ar=' + toolchain.ar,
            '--ranlib=' + toolchain.ranlib,
            '--arch=' + arch,
            '--target-os=' + target_os,
            '--prefix=' + toolchain.install_prefix,
        ] + self.configure_args

        if toolchain.is_armv7:
            configure.append('--cpu=cortex-a8')

        if toolchain.is_windows and toolchain.native:
            configure.append('--toolchain=msvc')
            configure[0] = configure[0].replace('\\', '/')
            msys_check_call(configure, cwd=build, env=toolchain.env)
            msys_check_call(['/usr/bin/make', 'V=1', '-j12'], cwd=build, env=toolchain.env)
            msys_check_call(['/usr/bin/make', 'install'], cwd=build, env=toolchain.env)
        else:
            configure.append('--enable-cross-compile')

            subprocess.check_call(configure, cwd=build, env=toolchain.env)
            subprocess.check_call(['/usr/bin/make', '--quiet', '-j12'], cwd=build, env=toolchain.env)
            subprocess.check_call(['/usr/bin/make', '--quiet', 'install'], cwd=build, env=toolchain.env)
