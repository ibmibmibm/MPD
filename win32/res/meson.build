windows_conf = configuration_data()
windows_conf.set('VERSION', meson.project_version())

splitted_version = meson.project_version().split('~')[0].split('.')
windows_conf.set('VERSION_MAJOR', splitted_version[0])
windows_conf.set('VERSION_MINOR', splitted_version.get(1, '0'))
windows_conf.set('VERSION_REVISION', splitted_version.get(2, '0'))
windows_conf.set('VERSION_EXTRA', splitted_version.get(3, '0'))

mpd_rc = configure_file(
  input: 'mpd.rc.in',
  output: 'mpd.rc',
  configuration: windows_conf,
)
mpd_ico = configure_file(
  input: 'mpd.ico',
  output: 'mpd.ico',
  copy: true,
)

windows_mod = import('windows')
windows_resources = windows_mod.compile_resources(mpd_rc)
