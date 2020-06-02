import re
from os.path import abspath

from build.project import Project
from build.mad import MadProject
from build.lame import LameProject
from build.zlib import ZlibProject
from build.meson import MesonProject
from build.cmake import CmakeProject
from build.autotools import AutotoolsProject
from build.ffmpeg import FfmpegProject
from build.boost import BoostProject

libmpdclient = MesonProject(
    'https://www.musicpd.org/download/libmpdclient/2/libmpdclient-2.18.tar.xz',
    '4cb01e1f567e0169aca94875fb6e1200e7f5ce35b63a4df768ec1591fb1081fa',
    'lib/libmpdclient.a',
)

libogg = CmakeProject(
    'https://github.com/xiph/ogg/archive/v1.3.4.tar.gz',
    '3da31a4eb31534b6f878914b7379b873c280e610649fe5c07935b3d137a828bc',
    ('lib/libogg.a', 'lib/ogg.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
        '-DINSTALL_DOCS=OFF',
    ],
    base='ogg-1.3.4',
    name='libogg',
    version='1.3.4',
)

libvorbis = CmakeProject(
    'https://github.com/xiph/vorbis/archive/v1.3.6.tar.gz',
    '43fc4bc34f13da15b8acfa72fd594678e214d1cab35fc51d3a54969a725464eb',
    ('lib/libvorbis.a', 'lib/vorbis.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
    ],
    base='vorbis-1.3.6',
    name='libvorbis',
    version='1.3.6',
)

opus = CmakeProject(
    'https://archive.mozilla.org/pub/opus/opus-1.3.1.tar.gz',
    '65b58e1e25b2a114157014736a3d9dfeaad8d41be1c8179866f144a2fb44ff9d',
    ('lib/libopus.a', 'lib/opus.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
        '-DOPUS_FIXED_POINT=ON',
    ],
    base='opus-1.3.1',
    name='libopus',
    version='1.3.1',
    edits={
        'CMakeLists.txt': lambda data: data.replace('include(opus_buildtype.cmake)', ''),
    }
)

flac = CmakeProject(
    'https://github.com/xiph/flac/archive/1.3.3.tar.gz',
    '668cdeab898a7dd43cf84739f7e1f3ed6b35ece2ef9968a5c7079fe9adfe1689',
    ('lib/libFLAC.a', 'lib/FLAC.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
        '-DBUILD_EXAMPLES=ON',
    ],
    base='flac-1.3.3',
    name='libflac',
    version='1.3.3',
)

zlib = CmakeProject(
    'http://zlib.net/zlib-1.2.11.tar.xz',
    '4ff941449631ace0d4d203e3483be9dbc9da454084111f97ea0a2114e19bf066',
    ('lib/libz.a', 'lib/zlib.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
    ],
    base='zlib-1.2.11',
    name='zlib',
    version='1.2.11',
    edits={
        # https://github.com/madler/zlib/issues/268
        'gzguts.h': lambda data: data.replace('#if defined(_WIN32) || defined(__CYGWIN__)', '#if defined(_WIN32) || defined(__MINGW32__)'),
        'zconf.h.cmakein': lambda data: data.replace('#ifdef HAVE_UNISTD_H', '#if defined(HAVE_UNISTD_H) && HAVE_UNISTD_H').replace('#ifdef HAVE_STDARG_H', '#if defined(HAVE_STDARG_H) && HAVE_STDARG_H')
    }
)

libid3tag = MadProject(
    'ftp://ftp.mars.org/pub/mpeg/libid3tag-0.15.1b.tar.gz',
    'e5808ad997ba32c498803822078748c3',
    ('lib/libid3tag.a', 'lib/libid3tag.lib'),
    [
        '--enable-shared', '--disable-static',

        # without this, libid3tag's configure.ac ignores -O* and -f*
        '--disable-debugging',
    ],
    dsp_file='libid3tag.dsp',
    autogen=True,

    edits={
        # fix bug in libid3tag's configure.ac which discards all but the last optimization flag
        'configure.ac': lambda data: re.sub(r'optimize="\$1"', r'optimize="$optimize $1"', data, count=1),
    }
)

libmad = MadProject(
    'ftp://ftp.mars.org/pub/mpeg/libmad-0.15.1b.tar.gz',
    '1be543bc30c56fb6bea1d7bf6a64e66c',
    ('lib/libmad.a', 'lib/libmad.lib'),
    [
        '--enable-shared', '--disable-static',

        # without this, libmad's configure.ac ignores -O* and -f*
        '--disable-debugging',
    ],
    dsp_file='libmad.dsp',
    autogen=True,
)

liblame = LameProject(
    'http://downloads.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz',
    'ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e',
    ('lib/libmp3lame.a', 'lib/mp3lame.lib'),
    [
        '--enable-shared', '--disable-static',
        '--disable-gtktest', '--disable-analyzer-hooks',
        '--disable-decoder', '--disable-frontend',
    ],
)

libmodplug = CmakeProject(
    'https://github.com/Konstanty/libmodplug/archive/5a39f5913d07ba3e61d8d5afdba00b70165da81d.tar.gz',
    '7d472134fce267e3407caed1247b91c3dab24d7956b439027eabf2832c63845d',
    ('lib/libmodplug.a', 'lib/modplug.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
    ],
    base='libmodplug-5a39f5913d07ba3e61d8d5afdba00b70165da81d',
    name='libmodplug',
    version='1.3.3',
    edits={
        'src/fastmix.cpp': lambda data: data.replace('register MODCHANNEL * const pChn = pChannel', 'MODCHANNEL * const pChn = pChannel')
    },
)

wildmidi = CmakeProject(
    'https://codeload.github.com/Mindwerks/wildmidi/tar.gz/wildmidi-0.4.3',
    '498e5a96455bb4b91b37188ad6dcb070824e92c44f5ed452b90adbaec8eef3c5',
    ('lib/libWildMidi.a', 'lib/wildmidi.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
        '-DWANT_PLAYER=OFF',
        '-DWANT_STATIC=ON',
    ],
    base='wildmidi-wildmidi-0.4.3',
    name='wildmidi',
    version='0.4.3',
    edits={
        # fix bug in libid3tag's configure.ac which discards all but the last optimization flag
        'src/CMakeLists.txt': lambda data: data \
            .replace('IF (WIN32 AND CMAKE_COMPILER_IS_MINGW)', 'IF (WIN32)') \
            .replace('IF (WIN32 AND MSVC)', 'IF (WIN32 AND FALSE)') \
            .replace('SET(LIBRARY_DYN_NAME "wildmidi_dynamic")', 'SET(LIBRARY_DYN_NAME "wildmidi")') \
            .replace('${CMAKE_BINARY_DIR}\\\\${CMAKE_BUILD_TYPE}\\\\', '${CMAKE_BINARY_DIR}/'),
    }
)

ffmpeg = FfmpegProject(
    'http://ffmpeg.org/releases/ffmpeg-4.2.3.tar.xz',
    '9df6c90aed1337634c1fb026fb01c154c29c82a64ea71291ff2da9aacb9aad31',
    ('lib/libavcodec.a', 'lib/avcodec.lib'),
    [
        '--enable-shared', '--disable-static',
        '--enable-gpl',
        '--enable-small',
        '--disable-pthreads',
        '--disable-programs',
        '--disable-doc',
        '--disable-avdevice',
        '--disable-swresample',
        '--disable-swscale',
        '--disable-postproc',
        '--disable-avfilter',
        '--disable-lzo',
        '--disable-faan',
        '--disable-pixelutils',
        '--disable-network',
        '--disable-encoders',
        '--disable-muxers',
        '--disable-protocols',
        '--disable-devices',
        '--disable-filters',
        '--disable-v4l2_m2m',

        '--disable-parser=bmp',
        '--disable-parser=cavsvideo',
        '--disable-parser=dvbsub',
        '--disable-parser=dvdsub',
        '--disable-parser=dvd_nav',
        '--disable-parser=flac',
        '--disable-parser=g729',
        '--disable-parser=gsm',
        '--disable-parser=h261',
        '--disable-parser=h263',
        '--disable-parser=h264',
        '--disable-parser=hevc',
        '--disable-parser=mjpeg',
        '--disable-parser=mlp',
        '--disable-parser=mpeg4video',
        '--disable-parser=mpegvideo',
        '--disable-parser=opus',
        '--disable-parser=vc1',
        '--disable-parser=vp3',
        '--disable-parser=vp8',
        '--disable-parser=vp9',
        '--disable-parser=png',
        '--disable-parser=pnm',
        '--disable-parser=xma',

        '--disable-demuxer=aqtitle',
        '--disable-demuxer=ass',
        '--disable-demuxer=bethsoftvid',
        '--disable-demuxer=bink',
        '--disable-demuxer=cavsvideo',
        '--disable-demuxer=cdxl',
        '--disable-demuxer=dvbsub',
        '--disable-demuxer=dvbtxt',
        '--disable-demuxer=h261',
        '--disable-demuxer=h263',
        '--disable-demuxer=h264',
        '--disable-demuxer=ico',
        '--disable-demuxer=image2',
        '--disable-demuxer=jacosub',
        '--disable-demuxer=lrc',
        '--disable-demuxer=microdvd',
        '--disable-demuxer=mjpeg',
        '--disable-demuxer=mjpeg_2000',
        '--disable-demuxer=mpegps',
        '--disable-demuxer=mpegvideo',
        '--disable-demuxer=mpl2',
        '--disable-demuxer=mpsub',
        '--disable-demuxer=pjs',
        '--disable-demuxer=rawvideo',
        '--disable-demuxer=realtext',
        '--disable-demuxer=sami',
        '--disable-demuxer=scc',
        '--disable-demuxer=srt',
        '--disable-demuxer=stl',
        '--disable-demuxer=subviewer',
        '--disable-demuxer=subviewer1',
        '--disable-demuxer=swf',
        '--disable-demuxer=tedcaptions',
        '--disable-demuxer=vobsub',
        '--disable-demuxer=vplayer',
        '--disable-demuxer=webvtt',
        '--disable-demuxer=yuv4mpegpipe',

        # we don't need these decoders, because we have the dedicated
        # libraries
        '--disable-decoder=flac',
        '--disable-decoder=opus',
        '--disable-decoder=vorbis',

        # audio codecs nobody uses
        '--disable-decoder=atrac1',
        '--disable-decoder=atrac3',
        '--disable-decoder=atrac3al',
        '--disable-decoder=atrac3p',
        '--disable-decoder=atrac3pal',
        '--disable-decoder=binkaudio_dct',
        '--disable-decoder=binkaudio_rdft',
        '--disable-decoder=bmv_audio',
        '--disable-decoder=dsicinaudio',
        '--disable-decoder=dvaudio',
        '--disable-decoder=metasound',
        '--disable-decoder=paf_audio',
        '--disable-decoder=ra_144',
        '--disable-decoder=ra_288',
        '--disable-decoder=ralf',
        '--disable-decoder=qdm2',
        '--disable-decoder=qdmc',

        # disable lots of image and video codecs
        '--disable-decoder=ass',
        '--disable-decoder=asv1',
        '--disable-decoder=asv2',
        '--disable-decoder=apng',
        '--disable-decoder=avrn',
        '--disable-decoder=avrp',
        '--disable-decoder=bethsoftvid',
        '--disable-decoder=bink',
        '--disable-decoder=bmp',
        '--disable-decoder=bmv_video',
        '--disable-decoder=cavs',
        '--disable-decoder=ccaption',
        '--disable-decoder=cdgraphics',
        '--disable-decoder=clearvideo',
        '--disable-decoder=dirac',
        '--disable-decoder=dsicinvideo',
        '--disable-decoder=dvbsub',
        '--disable-decoder=dvdsub',
        '--disable-decoder=dvvideo',
        '--disable-decoder=exr',
        '--disable-decoder=ffv1',
        '--disable-decoder=ffvhuff',
        '--disable-decoder=ffwavesynth',
        '--disable-decoder=flic',
        '--disable-decoder=flv',
        '--disable-decoder=fraps',
        '--disable-decoder=gif',
        '--disable-decoder=h261',
        '--disable-decoder=h263',
        '--disable-decoder=h263i',
        '--disable-decoder=h263p',
        '--disable-decoder=h264',
        '--disable-decoder=hevc',
        '--disable-decoder=hnm4_video',
        '--disable-decoder=hq_hqa',
        '--disable-decoder=hqx',
        '--disable-decoder=idcin',
        '--disable-decoder=iff_ilbm',
        '--disable-decoder=indeo2',
        '--disable-decoder=indeo3',
        '--disable-decoder=indeo4',
        '--disable-decoder=indeo5',
        '--disable-decoder=interplay_video',
        '--disable-decoder=jacosub',
        '--disable-decoder=jpeg2000',
        '--disable-decoder=jpegls',
        '--disable-decoder=microdvd',
        '--disable-decoder=mimic',
        '--disable-decoder=mjpeg',
        '--disable-decoder=mmvideo',
        '--disable-decoder=mpl2',
        '--disable-decoder=motionpixels',
        '--disable-decoder=mpeg1video',
        '--disable-decoder=mpeg2video',
        '--disable-decoder=mpeg4',
        '--disable-decoder=mpegvideo',
        '--disable-decoder=mscc',
        '--disable-decoder=msmpeg4_crystalhd',
        '--disable-decoder=msmpeg4v1',
        '--disable-decoder=msmpeg4v2',
        '--disable-decoder=msmpeg4v3',
        '--disable-decoder=msvideo1',
        '--disable-decoder=mszh',
        '--disable-decoder=mvc1',
        '--disable-decoder=mvc2',
        '--disable-decoder=on2avc',
        '--disable-decoder=paf_video',
        '--disable-decoder=png',
        '--disable-decoder=qdraw',
        '--disable-decoder=qpeg',
        '--disable-decoder=rawvideo',
        '--disable-decoder=realtext',
        '--disable-decoder=roq',
        '--disable-decoder=roq_dpcm',
        '--disable-decoder=rscc',
        '--disable-decoder=rv10',
        '--disable-decoder=rv20',
        '--disable-decoder=rv30',
        '--disable-decoder=rv40',
        '--disable-decoder=sami',
        '--disable-decoder=sheervideo',
        '--disable-decoder=snow',
        '--disable-decoder=srt',
        '--disable-decoder=stl',
        '--disable-decoder=subrip',
        '--disable-decoder=subviewer',
        '--disable-decoder=subviewer1',
        '--disable-decoder=svq1',
        '--disable-decoder=svq3',
        '--disable-decoder=tiff',
        '--disable-decoder=tiertexseqvideo',
        '--disable-decoder=truemotion1',
        '--disable-decoder=truemotion2',
        '--disable-decoder=truemotion2rt',
        '--disable-decoder=twinvq',
        '--disable-decoder=utvideo',
        '--disable-decoder=vc1',
        '--disable-decoder=vmdvideo',
        '--disable-decoder=vp3',
        '--disable-decoder=vp5',
        '--disable-decoder=vp6',
        '--disable-decoder=vp7',
        '--disable-decoder=vp8',
        '--disable-decoder=vp9',
        '--disable-decoder=vqa',
        '--disable-decoder=webvtt',
        '--disable-decoder=wmv1',
        '--disable-decoder=wmv2',
        '--disable-decoder=wmv3',
        '--disable-decoder=yuv4',
    ],
)

curl = CmakeProject(
    'http://curl.haxx.se/download/curl-7.70.0.tar.xz',
    '032f43f2674008c761af19bf536374128c16241fb234699a55f9fb603fcfbae7',
    ('lib/libcurl.a', 'lib/libcurl.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
        '-DCURL_LTO=ON',
        '-DENABLE_THREADED_RESOLVER=OFF',
        '-DHTTP_ONLY=ON',
        '-DCURL_DISABLE_VERBOSE_STRINGS=ON',
        '-DENABLE_IPV6=ON',
        '-DCMAKE_USE_LIBSSH2=OFF',
        '-DCMAKE_USE_WINSSL=ON',
        '-DENABLE_UNIX_SOCKETS=OFF',
    ],
    base='curl-7.70.0',
    name='curl',
    version='7.70.0',
    edits={
        'CMakeLists.txt': lambda data: data.replace('/MANIFEST:NO', '-MANIFEST:NO')
    },
    patches='src/lib/curl/patches',
)

libexpat = CmakeProject(
    'https://github.com/libexpat/libexpat/releases/download/R_2_2_9/expat-2.2.9.tar.bz2',
    'f1063084dc4302a427dabcca499c8312b3a32a29b7d2506653ecc8f950a9a237',
    ('lib/libexpat.a', 'lib/libexpat.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
        '-DEXPAT_BUILD_DOCS=OFF',
    ],
    base='expat-2.2.9',
    name='expat',
    version='2.2.9',
)

libnfs = CmakeProject(
    'https://github.com/sahlberg/libnfs/archive/46c8a3006a084c05336ea56fc7957b2dad9342e7.tar.gz',
    '16ba5c8e85b188c51d3713dfba156ac8ef5b20b51cd0a516a6e6a3bc4bea3052',
    ('lib/libnfs.a', 'lib/nfs.lib'),
    [
        '-DBUILD_SHARED_LIBS=ON',
    ],
    base='libnfs-46c8a3006a084c05336ea56fc7957b2dad9342e7',
    name='libnfs',
    version='4.0.0',
    patches='src/lib/nfs/patches',
)

boost = BoostProject(
    'https://dl.bintray.com/boostorg/release/1.73.0/source/boost_1_73_0.tar.bz2',
    '4eb3b8d442b426dc35346235c8733b5ae35ba431690e38c6a8263dce9fcbb402',
    'include/boost/version.hpp',
)
