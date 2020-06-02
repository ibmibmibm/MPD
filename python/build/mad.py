import os, subprocess
import shutil
from build.autotools import AutotoolsProject


def generate_edits(include, arch):
    def edits(data):
        data = data.replace('CPP=cl.exe', 'CPP=clang-cl.exe') \
                   .replace('/I "..\..\libz" /I "..\..\libz-1.1.4"', '/I ' + include)
        if 'x86_64' in arch:
            data = data.replace('Win32', 'x64')
        return data
    return edits


class MadProject(AutotoolsProject):
    def __init__(self, *args, dsp_file, **kwargs):
        super(MadProject, self).__init__(*args, **kwargs)
        self.dsp_file = dsp_file

    def configure(self, toolchain):
        if not toolchain.msvc:
            return super(MadProject, self).configure(toolchain)
        else:
            include = os.path.join(toolchain.install_prefix, 'include')
            arch = toolchain.arch
            self.edits[os.path.join('msvc++', self.dsp_file)] = generate_edits(include, arch)
            return self.unpack(toolchain, out_of_tree=False)

    def build(self, toolchain):
        if not toolchain.msvc:
            return super(MadProject, self).build(toolchain)
        else:
            build = self.configure(toolchain)
            msvc = os.path.join(build, 'msvc++')
            if 'x86_64' in toolchain.arch:
                arch = 'x64'
            else:
                arch = 'Win32'
            subprocess.check_call(['devenv', self.dsp_file, '/upgrade'], cwd=msvc)
            subprocess.check_call(['msbuild', '/p:PlatformToolset=ClangCl', '/p:Configuration=Release', '/p:Platform=' + arch], cwd=msvc)
            shutil.copy(os.path.join(build, 'id3tag.h'), os.path.join(toolchain.install_prefix, 'include'))
            shutil.copy(os.path.join(msvc, 'Release', 'libid3tag.lib'), os.path.join(toolchain.install_prefix, 'lib'))
