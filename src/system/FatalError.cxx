/*
 * Copyright 2003-2020 The Music Player Daemon Project
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

#include "FatalError.hxx"
#include "util/Domain.hxx"
#include "LogV.hxx"

#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#ifdef _WIN32
#include <windows.h>
#else
#include <cerrno>
#endif

static constexpr Domain fatal_error_domain("fatal_error");

[[noreturn]]
static void
Abort()
{
	std::_Exit(EXIT_FAILURE);
}

void
FatalError(const char *msg)
{
	LogError(fatal_error_domain, msg);
	Abort();
}

void
FormatFatalError(const char *fmt, ...)
{
	std::va_list ap;
	va_start(ap, fmt);
	LogFormatV(LogLevel::ERROR, fatal_error_domain, fmt, ap);
	va_end(ap);

	Abort();
}

#ifdef _WIN32

void
FatalSystemError(const char *msg, DWORD code)
{
	char buffer[512];
	buffer[0] = '\0';
	{
		wchar_t w_msg[128];
		DWORD w_msg_length = FormatMessageW(
			FORMAT_MESSAGE_FROM_SYSTEM |
		       FORMAT_MESSAGE_IGNORE_INSERTS,
		       nullptr, code, 0,
		       w_msg, 128, nullptr);
		if (w_msg_length > 0) {
			int len = WideCharToMultiByte(
				CP_UTF8, 0, w_msg, w_msg_length,
				buffer, 512 - 1, nullptr, nullptr);
			while (len > 0) {
				switch (buffer[len - 1]) {
					case '\r':
					case '\n':
					case '\t':
					case '\0':
						--len;
						continue;
					default:
						;
				}
				break;
			}
			if (len >= 0) {
				buffer[len] = '\0';
			}
		}
	}

	FormatFatalError("%s: %s", msg, buffer);
}

#endif

void
FatalSystemError(const char *msg)
{
#ifdef _WIN32
	FatalSystemError(msg, GetLastError());
#else
	auto system_error = std::strerror(errno);
	FormatError(fatal_error_domain, "%s: %s", msg, system_error);
	Abort();
#endif
}

void
FormatFatalSystemError(const char *fmt, ...)
{
	char buffer[1024];
	std::va_list ap;
	va_start(ap, fmt);
	std::vsnprintf(buffer, sizeof(buffer), fmt, ap);
	va_end(ap);

	FatalSystemError(buffer);
}
