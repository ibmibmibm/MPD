/*
 * Copyright 2007-2018 Content Management AG
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

#include "UniqueRegex.hxx"
#include "util/RuntimeError.hxx"

void UniqueRegex::Compile(std::string_view pattern, bool anchored, bool capture,
			  bool caseless) {
	constexpr uint32_t default_options =
		PCRE2_DOTALL | PCRE2_NO_AUTO_CAPTURE | PCRE2_UTF;

	uint32_t options = default_options;
	if (anchored)
		options |= PCRE2_ANCHORED;
	if (capture)
		options &= ~PCRE2_NO_AUTO_CAPTURE;
	if (caseless)
		options |= PCRE2_CASELESS;

	int error_code;
	size_t error_offset;
	re = pcre2_compile(reinterpret_cast<const uint8_t *>(pattern.data()),
			   pattern.size(), options, &error_code, &error_offset, nullptr);
	if (re == nullptr) {
		unsigned char error_string[256];
		pcre2_get_error_message(error_code, error_string, sizeof(error_string));
		throw FormatRuntimeError("Error in regex at offset %d: %s", error_offset,
					 error_string);
	}

	pcre2_jit_compile(re, PCRE2_JIT_COMPLETE);
	pcre2_jit_free_unused_memory(nullptr);
}
