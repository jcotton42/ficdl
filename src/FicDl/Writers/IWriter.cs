using AngleSharp.Dom;
using FicDl.Scrapers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FicDl.Writers {
    public interface IWriter {
    }

    public record WriterOptions(
        List<(string ChapterTitle, IDocument Chapter)> Chapters,
        StoryMetadata Metadata,
        string OutputPath,
        string? CoverPath,
        string FontFamily,
        string FontSize,
        string LineHeight,
        string PageSize
    );
}
