pcre2_dep = dependency('libpcre2-8', required: get_option('pcre2'))
conf.set('HAVE_PCRE2', pcre2_dep.found())
if not pcre2_dep.found()
  subdir_done()
endif

pcre2 = static_library(
  'pcre2',
  'UniqueRegex.cxx',
  include_directories: inc,
  dependencies: [
    pcre2_dep,
  ],
)

pcre2_dep = declare_dependency(
  link_with: pcre2,
  dependencies: [
    pcre2_dep,
  ],
)
