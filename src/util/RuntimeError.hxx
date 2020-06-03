/*
 * Copyright 2013-2017 Max Kellermann <max.kellermann@gmail.com>
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

#ifndef RUNTIME_ERROR_HXX
#define RUNTIME_ERROR_HXX

#include "util/Compiler.h"

#include <cassert>
#include <cstdarg>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <utility>

gcc_printf(1, 2) static inline std::runtime_error
	FormatRuntimeError(const char *fmt, ...) noexcept {
	std::va_list args1, args2;
	va_start(args1, fmt);
	va_copy(args2, args1);

	const int size = std::vsnprintf(nullptr, 0, fmt, args1);
	va_end(args1);
	assert(size >= 0);

	auto buffer = std::make_unique<char[]>(size + 1);
	std::vsprintf(buffer.get(), fmt, args2);
	va_end(args2);

	return std::runtime_error(std::string(buffer.get(), size));
}

gcc_printf(1, 2) static inline std::invalid_argument
	FormatInvalidArgument(const char *fmt, ...) noexcept {
	std::va_list args1, args2;
	va_start(args1, fmt);
	va_copy(args2, args1);

	const int size = std::vsnprintf(nullptr, 0, fmt, args1);
	va_end(args1);
	assert(size >= 0);

	auto buffer = std::make_unique<char[]>(size + 1);
	std::vsprintf(buffer.get(), fmt, args2);
	va_end(args2);

	return std::invalid_argument(std::string(buffer.get(), size));
}

#endif
