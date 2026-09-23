/* Build a WoW 3.3.5a patch MPQ containing one or more files.
 *
 * Usage: makepatch <out.mpq> <local-file>:<archive\path> [...]
 *
 * Contains no game data of its own -- it packs files you supply. */
#include <StormLib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv)
{
    if (argc < 3) { fprintf(stderr, "usage: %s <out.mpq> <file>:<archive\\path> ...\n", argv[0]); return 2; }

    HANDLE mpq = NULL;
    /* MPQ v1 with enough slots; v1 is what a 3.3.5 client reads. */
    if (!SFileCreateArchive(argv[1], MPQ_CREATE_ARCHIVE_V1 | MPQ_CREATE_LISTFILE, 16, &mpq))
    { fprintf(stderr, "cannot create %s (err %u)\n", argv[1], SErrGetLastError()); return 1; }

    for (int i = 2; i < argc; ++i)
    {
        char spec[1024]; strncpy(spec, argv[i], sizeof(spec) - 1); spec[sizeof(spec)-1] = 0;
        char* colon = strchr(spec, ':');
        if (!colon) { fprintf(stderr, "bad spec %s\n", argv[i]); SFileCloseArchive(mpq); return 2; }
        *colon = 0;
        char const* local = spec;
        char const* inside = colon + 1;

        if (!SFileAddFileEx(mpq, local, inside, MPQ_FILE_COMPRESS | MPQ_FILE_REPLACEEXISTING,
                            MPQ_COMPRESSION_ZLIB, MPQ_COMPRESSION_NEXT_SAME))
        { fprintf(stderr, "cannot add %s as %s (err %u)\n", local, inside, SErrGetLastError());
          SFileCloseArchive(mpq); return 1; }

        printf("  added %s as %s\n", local, inside);
    }

    SFileCloseArchive(mpq);
    printf("wrote %s\n", argv[1]);
    return 0;
}
