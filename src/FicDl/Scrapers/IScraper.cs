using System;
using System.Collections.Generic;

namespace FicDl.Scrapers {
    public record StoryMetadata(
        string Title,
        string Author,
        bool HasCover,
        IReadOnlyList<string> ChapterNames,
        string Description,
        DateTimeOffset UpdateDateUtc
    );
}
