using System;
using System.Collections.Generic;

namespace FicDl.Scrapers {
    public record StroyMetadata(
        string Title,
        string Author,
        Uri? CoverUri,
        Uri? CoverThumbnailUri,
        IReadOnlyList<string> ChapterNames,
        string Description,
        DateTimeOffset UpdateDateUtc
    );
}
