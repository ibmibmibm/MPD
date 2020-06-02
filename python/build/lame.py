import os, subprocess
import shutil
from build.autotools import AutotoolsProject


def generate_edits(arch):
    def edits(data):
        data = data \
            .replace('CC = cl', 'CC = clang-cl') \
            .replace(' /GAy ', ' ') \
            .replace('T_LIB_DYNAMIC = libmp3lame.lib', 'T_LIB_DYNAMIC = mp3lame.lib') \
            .replace('T_LIB_STATIC = libmp3lame-static.lib', 'T_LIB_STATIC = mp3lame-static.lib')
        if 'x86_64' in arch:
            data = data.replace('MACHINE = /machine:I386', 'MACHINE =/machine:X64')
        return data
    return edits


class LameProject(AutotoolsProject):
    def __init__(self, *args, **kwargs):
        super(LameProject, self).__init__(*args, **kwargs)

    def configure(self, toolchain):
        if not toolchain.msvc:
            return super(LameProject, self).configure(toolchain)
        else:
            if not self.edits:
                self.edits = {}
            self.edits['Makefile.MSVC'] = generate_edits(toolchain.arch)
            return self.unpack(toolchain, out_of_tree=False)

    def build(self, toolchain):
        if not toolchain.msvc:
            return super(LameProject, self).build(toolchain)
        else:
            build = self.configure(toolchain)
            shutil.copy(os.path.join(build, 'configMS.h'), os.path.join(build, 'config.h'))
            args = ['comp=msvc', 'asm=yes']
            if 'x86_64' in toolchain.arch:
                args += ['MSVCVER=Win64']

            subprocess.check_call(['nmake', '-f', 'Makefile.MSVC', 'all'] + args, cwd=build)
            include_lame = os.path.join(toolchain.install_prefix, 'include', 'lame')
            bin = os.path.join(toolchain.install_prefix, 'bin')
            lib = os.path.join(toolchain.install_prefix, 'lib')
            os.makedirs(include_lame, exist_ok=True)
            shutil.copy(os.path.join(build, 'include', 'lame.h'), include_lame)
            shutil.copy(os.path.join(build, 'output', 'mp3lame.lib'), lib)
            shutil.copy(os.path.join(build, 'output', 'mp3lame.dll'), bin)