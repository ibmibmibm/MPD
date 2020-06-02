#!/usr/bin/env python3

import os, os.path
import sys, subprocess
import shutil

configure_args = sys.argv[1:]

x64 = True
native = (os.name == 'nt')

while len(configure_args) > 0:
    arg = configure_args[0]
    if arg == '--64':
        x64 = True
    elif arg == '--32':
        x64 = False
    else:
        break
    configure_args.pop(0)

if x64:
    host_arch = 'x86_64-w64-mingw32'
else:
    host_arch = 'i686-w64-mingw32'

# the path to the MPD sources
mpd_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]) or '.', '..'))
sys.path[0] = os.path.join(mpd_path, 'python')

# output directories
from build.dirs import lib_path, tarball_path, src_path

arch_path = os.path.join(lib_path, host_arch)
build_path = os.path.join(arch_path, 'build')
root_path = os.path.join(arch_path, 'root')

class CrossGccToolchain:
    def __init__(self, toolchain_path, arch,
                 tarball_path, src_path, build_path, install_prefix):
        self.native = False
        self.msvc = False
        self.arch = arch
        self.tarball_path = tarball_path
        self.src_path = src_path
        self.build_path = build_path
        self.install_prefix = install_prefix

        toolchain_bin = os.path.join(toolchain_path, 'bin')
        self.cc = os.path.join(toolchain_bin, arch + '-gcc')
        self.cxx = os.path.join(toolchain_bin, arch + '-g++')
        self.ar = os.path.join(toolchain_bin, arch + '-gcc-ar')
        self.ranlib = os.path.join(toolchain_bin, arch + '-gcc-ranlib')
        self.nm = os.path.join(toolchain_bin, arch + '-nm')
        self.strip = os.path.join(toolchain_bin, arch + '-strip')
        self.windres = os.path.join(toolchain_bin, arch + '-windres')

        common_flags = '-O3 -g -D_FORTIFY_SOURCES=2 -fstack-protector -flto'

        if not x64:
            # enable SSE support which is required for LAME
            common_flags += ' -march=pentium3'

        self.cflags = common_flags
        self.cxxflags = common_flags
        self.cppflags = '-isystem ' + os.path.join(install_prefix, 'include') + \
                        ' -DWINVER=0x0600 -D_WIN32_WINNT=0x0600'
        self.ldflags = '-L' + os.path.join(install_prefix, 'lib') + \
                       ' -static-libstdc++ -static-libgcc ' + common_flags
        self.libs = ''

        self.is_arm = arch.startswith('arm')
        self.is_armv7 = self.is_arm and 'armv7' in self.cflags
        self.is_aarch64 = arch == 'aarch64'
        self.is_windows = 'mingw32' in arch

        self.env = dict(os.environ)

        # redirect pkg-config to use our root directory instead of the
        # default one on the build host
        import shutil
        bin_dir = os.path.join(install_prefix, 'bin')
        try:
            os.makedirs(bin_dir)
        except:
            pass
        self.pkg_config = shutil.copy(os.path.join(mpd_path, 'build', 'pkg-config.sh'),
                                      os.path.join(bin_dir, 'pkg-config'))
        self.env['PKG_CONFIG'] = self.pkg_config

class ClangClToolchain:
    def __init__(self, arch,
                 tarball_path, src_path, build_path, install_prefix):
        self.native = True
        self.msvc = True
        self.arch = arch
        self.tarball_path = tarball_path
        self.src_path = src_path
        self.build_path = build_path
        self.install_prefix = install_prefix

        self.cc = 'clang-cl'
        self.cxx = 'clang-cl'
        self.ld = 'lld-link'
        self.ar = 'llvm-ar'
        self.ranlib = 'llvm-ranlib'
        self.nm = 'llvm-nm'
        self.strip = 'llvm-strip'
        self.windres = 'rc'

        common_flags = '-O2'

        if not x64:
            # enable SSE support which is required for LAME
            common_flags += ' -arch:SSE2'
        else:
            common_flags += ' -arch:AVX2'

        warning_flags = ' '.join((
            '-Wno-nonportable-system-include-path',
            '-Wno-documentation',
            '-Wno-documentation-unknown-command',
            '-Wno-unused-command-line-argument',
            '-Wno-unused-macros',
            '-Wno-unused-parameter',
            '-Wno-reserved-id-macro',
            '-Wno-format-nonliteral',
            '-Wno-assign-enum',
            '-Wno-sign-conversion',
            '-Wno-double-promotion',
            '-Wno-shorten-64-to-32',
            '-Wno-implicit-int-conversion',
            '-Wno-implicit-float-conversion',
            '-Wno-float-conversion',
            '-Wno-old-style-cast',
        ))

        self.cflags = common_flags + ' -std:c17'
        self.cxxflags = common_flags + ' -std:c++17'
        self.cppflags = '-I' + os.path.join(install_prefix, 'include').replace('\\', '/') + \
                        ' -DWIN32 -DWINVER=0x0600 -D_WIN32_WINNT=0x0600 -MD ' + warning_flags
        self.ldflags = '/libpath:' + os.path.join(install_prefix, 'lib').replace('\\', '/')
        self.libs = ''

        self.is_arm = False
        self.is_armv7 = False
        self.is_aarch64 = False
        self.is_windows = True

        self.env = dict(os.environ)

        self.env['PKG_CONFIG_PATH'] = os.path.join(install_prefix, 'lib', 'pkgconfig')

        self.env['BOOST_ROOT'] = install_prefix
        self.env['CMAKE_PREFIX_PATH'] = install_prefix

    def msys_check_call(command, **kwargs):
        quoted = ' '.join(map(lambda x: quote(x), command))
        command = ['C:\\tools\\msys64\\msys2_shell.cmd', '-msys2', '-defterm', '-no-start', '-use-full-path', '-here', '-c', quoted]
        subprocess.check_call(command, **kwargs)

# a list of third-party libraries to be used by MPD on Android
from build.libs import *
thirdparty_libs = [
    libmpdclient,
    libogg,
    libvorbis,
    opus,
    flac,
    zlib,
    libid3tag,
    liblame,
    libmodplug,
    wildmidi,
    ffmpeg,
    curl,
    libexpat,
    libnfs,
    boost,
]

if not native:
    # build the third-party libraries
    toolchain = CrossGccToolchain('/usr', host_arch,
                                  tarball_path, src_path, build_path, root_path)
else:
    # build the third-party libraries
    toolchain = ClangClToolchain(host_arch, tarball_path, src_path, build_path, root_path)

for x in thirdparty_libs:
    if not x.is_installed(toolchain):
        x.build(toolchain)

# configure and build MPD

from build.meson import configure as run_meson
run_meson(toolchain, mpd_path, '.', configure_args)
subprocess.check_call(['ninja'], env=toolchain.env)
