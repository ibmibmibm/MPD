#include "fs/LookupFile.hxx"
#include "util/Compiler.h"

#include <gtest/gtest.h>

#include <cstdlib>
#include <cstring>

#ifdef _WIN32
#define L(x) L##x
#else
#define L(x) x
#endif

TEST(ArchiveTest, Lookup)
{
	EXPECT_THROW(LookupFile(Path::FromFS(L(""))), std::system_error);

	EXPECT_FALSE(LookupFile(Path::FromFS(L("."))));

	EXPECT_FALSE(LookupFile(Path::FromFS(L("config.h"))));

	EXPECT_THROW(LookupFile(Path::FromFS(L("src/foo/bar"))), std::system_error);

	std::fclose(std::fopen("dummy", "w"));

	auto result = LookupFile(Path::FromFS(L("dummy/foo/bar")));
	EXPECT_TRUE(result);
	EXPECT_STREQ(result.archive.c_str(), L("dummy"));
	EXPECT_STREQ(result.inside.c_str(), L("foo/bar"));

	result = LookupFile(Path::FromFS(L("config.h/foo/bar")));
	EXPECT_TRUE(result);
	EXPECT_STREQ(result.archive.c_str(), L("config.h"));
	EXPECT_STREQ(result.inside.c_str(), L("foo/bar"));
}
