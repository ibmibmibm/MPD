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

/*
 * This program is a command line interface to MPD's software volume
 * library (pcm_volume.c).
 *
 */

#include "pcm/Volume.hxx"
#include "pcm/AudioParser.hxx"
#include "pcm/AudioFormat.hxx"
#include "util/ConstBuffer.hxx"
#include "util/PrintException.hxx"

#include "win32/unistd.hxx"

#include <cstddef>
#include <cstdio>
#include <cstdlib>

int
main(int argc, char **argv)
try {
	static char buffer[4096];
	size_t nbytes;

	if (argc > 2) {
		std::fprintf(stderr, "Usage: software_volume [FORMAT] <IN >OUT\n");
		return EXIT_FAILURE;
	}

	AudioFormat audio_format(48000, SampleFormat::S16, 2);
	if (argc > 1)
		audio_format = ParseAudioFormat(argv[1], false);

	PcmVolume pv;
	const auto out_sample_format = pv.Open(audio_format.format, false);

	if (out_sample_format != audio_format.format)
		std::fprintf(stderr, "Converting to %s\n",
			sample_format_to_string(out_sample_format));

	while ((nbytes = std::fread(buffer, sizeof(buffer), 1, stdin)) > 0) {
		auto dest = pv.Apply({buffer, size_t(nbytes)});
		[[maybe_unused]] size_t ignored = fwrite(dest.data, dest.size, 1, stdout);
	}

	pv.Close();
} catch (...) {
	PrintException(std::current_exception());
	return EXIT_FAILURE;
}
