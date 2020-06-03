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

#include "fs/io/GzipOutputStream.hxx"
#include "fs/io/StdioOutputStream.hxx"
#include "system/Error.hxx"
#include "util/PrintException.hxx"

#include "win32/unistd.hxx"

#include <cstdio>
#include <cstdlib>

static void
Copy(OutputStream &dest, std::FILE *src)
{
	while (true) {
		char buffer[4096];
		size_t nbytes = std::fread(buffer, sizeof(buffer), 1, src);
		if (nbytes == 0) {
			if (ferror(src))
				throw MakeErrno("fread() failed");

			return;
		}

		dest.Write(buffer, nbytes);
	}
}

static void
CopyGzip(OutputStream &_dest, std::FILE *src)
{
	GzipOutputStream dest(_dest);
	Copy(dest, src);
	dest.Flush();
}

static void
CopyGzip(std::FILE *_dest, std::FILE * src)
{
	StdioOutputStream dest(_dest);
	CopyGzip(dest, src);
}

int
main(int argc, [[maybe_unused]] char **argv)
try {
	if (argc != 1) {
		std::fprintf(stderr, "Usage: run_gzip\n");
		return EXIT_FAILURE;
	}

	CopyGzip(stdout, stdin);
	return EXIT_SUCCESS;
} catch (...) {
	PrintException(std::current_exception());
	return EXIT_FAILURE;
}
