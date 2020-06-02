import os.path, subprocess

from build.cmake import CmakeProject

class ZlibProject(CmakeProject):
    def __init__(self, *args, **kwargs):
        super(ZlibProject, self).__init__(*args, **kwargs)

    def build(self, toolchain):
        super(ZlibProject, self).build(toolchain)

        static_zlib = os.path.join(toolchain.install_prefix, 'lib', 'zlibstatic.lib')
        dynamic_zlib = os.path.join(toolchain.install_prefix, 'lib', 'zlib.lib')
        if os.path.exists(static_zlib):
            os.unlink(dynamic_zlib)
            os.rename(static_zlib, dynamic_zlib)
