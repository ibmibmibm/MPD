/*
 * Copyright 2007-2019 Content Management AG
 * All rights reserved.
 *
 * author: Max Kellermann <mk@cm4all.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * - Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the
 * distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
 * FOUNDATION OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "Convert.hxx"

#include <chrono>
#include <ctime>
#include <stdexcept>

#ifndef _WIN32
#include <sys/time.h> /* for struct timeval */
#else
#include <winsock.h>
#endif

std::tm
GmTime(std::chrono::system_clock::time_point tp)
{
	const std::time_t t = std::chrono::system_clock::to_time_t(tp);
#ifdef _WIN32
	const std::tm *tm = std::gmtime(&t);
#else
	struct std::tm buffer, *tm = gmtime_r(&t, &buffer);
#endif
	if (tm == nullptr)
		throw std::runtime_error("gmtime_r() failed");

	return *tm;
}

std::tm
LocalTime(std::chrono::system_clock::time_point tp)
{
	const std::time_t t = std::chrono::system_clock::to_time_t(tp);
#ifdef _WIN32
	const std::tm *tm = localtime(&t);
#else
	std::tm buffer, *tm = localtime_r(&t, &buffer);
#endif
	if (tm == nullptr)
		throw std::runtime_error("localtime_r() failed");

	return *tm;
}

#ifndef __GLIBC__

/**
 * Determine the time zone offset in a portable way.
 */
gcc_const
static std::time_t
GetTimeZoneOffset() noexcept
{
	std::time_t t = 1234567890;
#ifdef _WIN32
	std::tm *p = std::gmtime(&t);
#else
	std::tm tm;
	tm.tm_isdst = 0;
	std::tm *p = &tm;
	gmtime_r(&t, p);
#endif
	return t - mktime(p);
}

#endif /* !__GLIBC__ */

std::chrono::system_clock::time_point
TimeGm(std::tm &tm) noexcept
{
#if defined(__GLIBC__)
	/* timegm() is a GNU extension */
	const auto t = timegm(&tm);
#elif defined(_WIN32)
	const auto t = _mkgmtime(&tm);
#else
	tm.tm_isdst = 0;
	const auto t = mktime(&tm) + GetTimeZoneOffset();
#endif /* !__GLIBC__ */

	return std::chrono::system_clock::from_time_t(t);
}

std::chrono::system_clock::time_point
MakeTime(std::tm &tm) noexcept
{
	return std::chrono::system_clock::from_time_t(mktime(&tm));
}

std::chrono::steady_clock::duration
ToSteadyClockDuration(const struct timeval &tv) noexcept
{
	return std::chrono::steady_clock::duration(std::chrono::seconds(tv.tv_sec)) +
		std::chrono::steady_clock::duration(std::chrono::microseconds(tv.tv_usec));
}
