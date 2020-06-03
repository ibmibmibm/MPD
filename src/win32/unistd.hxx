/*
 * Copyright 2020 The Music Player Daemon Project
 * http://www.musicpd.org
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#ifndef MPD_WIN32_UNISTD_H
#define MPD_WIN32_UNISTD_H

#if !defined(_WIN32) || defined(__MINGW32__)

#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#else // defined(_WIN32) && !defined(__MINGW32__)

#include <cstdint>
#include <cwchar>
#include <type_traits>
#include <winsock2.h>

#ifndef STDIN_FILENO
#define STDIN_FILENO 0
#endif

#ifndef STDOUT_FILENO
#define STDOUT_FILENO 1
#endif

#ifndef STDERR_FILENO
#define STDERR_FILENO 2
#endif

#ifndef R_OK
#define R_OK 04
#endif

#if !defined(S_ISREG) && defined(S_IFMT) && defined(S_IFREG)
#define S_ISREG(m) (((m) & S_IFMT) == S_IFREG)
#endif

#if !defined(S_ISDIR) && defined(S_IFMT) && defined(S_IFDIR)
#define S_ISDIR(m) (((m) & S_IFMT) == S_IFDIR)
#endif

using ssize_t = std::make_signed<size_t>::type;
using mode_t = int32_t;

#endif // !defined(_WIN32) || defined(__MINGW32__)

#if defined(_WIN32)
#include <windows.h>
#include <io.h>
#endif // defined(_WIN32)

#endif
