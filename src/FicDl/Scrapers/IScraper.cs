using AngleSharp.Dom;
using AngleSharp.Io;
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace FicDl.Scrapers {
    public record StoryMetadata(
        string Title,
        string Author,
        bool HasCover,
        IReadOnlyList<string> ChapterNames,
        string Description,
        DateTimeOffset UpdateDateUtc
    );

    public interface IScraper : IDisposable {
        Task<StoryMetadata> GetMetadataAsync(CancellationToken cancellationToken);
        Task<IDocument> GetChapterTextAsync(int number, CancellationToken cancellationToken);
        Task<IResponse> GetCoverAsync(CancellationToken cancellationToken);
    }
}
