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

#include "DumpDecoderClient.hxx"
#include "decoder/DecoderAPI.hxx"
#include "input/InputStream.hxx"
#include "util/StringBuffer.hxx"
#include "util/Compiler.h"

#include "win32/unistd.hxx"

#include <cstdio>

void
DumpDecoderClient::Ready(const AudioFormat audio_format,
			 bool seekable,
			 SignedSongTime duration) noexcept
{
	assert(!initialized);
	assert(audio_format.IsValid());

	std::fprintf(stderr, "audio_format=%s duration=%f seekable=%d\n",
		ToString(audio_format).c_str(),
		duration.ToDoubleS(), seekable);

	initialized = true;
}

DecoderCommand
DumpDecoderClient::GetCommand() noexcept
{
	return DecoderCommand::NONE;
}

void
DumpDecoderClient::CommandFinished() noexcept
{
}

SongTime
DumpDecoderClient::GetSeekTime() noexcept
{
	return SongTime();
}

uint64_t
DumpDecoderClient::GetSeekFrame() noexcept
{
	return 1;
}

void
DumpDecoderClient::SeekError() noexcept
{
}

InputStreamPtr
DumpDecoderClient::OpenUri(const char *uri)
{
	return InputStream::OpenReady(uri, mutex);
}

size_t
DumpDecoderClient::Read(InputStream &is, void *buffer, size_t length) noexcept
{
	try {
		return is.LockRead(buffer, length);
	} catch (...) {
		return 0;
	}
}

void
DumpDecoderClient::SubmitTimestamp([[maybe_unused]] FloatDuration t) noexcept
{
}

DecoderCommand
DumpDecoderClient::SubmitData([[maybe_unused]] InputStream *is,
			      const void *data, size_t datalen,
			      [[maybe_unused]] uint16_t kbit_rate) noexcept
{
	if (kbit_rate != prev_kbit_rate) {
		prev_kbit_rate = kbit_rate;
		std::fprintf(stderr, "%u kbit/s\n", kbit_rate);
	}

	[[maybe_unused]] size_t nbytes = std::fwrite(data, datalen, 1, stdout);
	return GetCommand();
}

DecoderCommand
DumpDecoderClient::SubmitTag([[maybe_unused]] InputStream *is,
			     Tag &&tag) noexcept
{
	std::fprintf(stderr, "TAG: duration=%f\n", tag.duration.ToDoubleS());

	for (const auto &i : tag)
		std::fprintf(stderr, "  %s=%s\n", tag_item_names[i.type], i.value);

	return GetCommand();
}

static void
DumpReplayGainTuple(const char *name, const ReplayGainTuple &tuple) noexcept
{
	if (tuple.IsDefined())
		std::fprintf(stderr, "replay_gain[%s]: gain=%f peak=%f\n",
			name, (double)tuple.gain, (double)tuple.peak);
}

static void
DumpReplayGainInfo(const ReplayGainInfo &info) noexcept
{
	DumpReplayGainTuple("album", info.album);
	DumpReplayGainTuple("track", info.track);
}

void
DumpDecoderClient::SubmitReplayGain(const ReplayGainInfo *rgi) noexcept
{
	if (rgi != nullptr)
		DumpReplayGainInfo(*rgi);
}

void
DumpDecoderClient::SubmitMixRamp([[maybe_unused]] MixRampInfo &&mix_ramp) noexcept
{
	std::fprintf(stderr, "MixRamp: start='%s' end='%s'\n",
		mix_ramp.GetStart(), mix_ramp.GetEnd());
}
