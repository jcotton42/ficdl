using AngleSharp;
using AngleSharp.Dom;
using AngleSharp.Io;
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace FicDl.Scrapers {
    public class FfnScraper : IScraper {
        private static readonly Regex CenterStyle = new Regex(@"text-align\s*:\s*center", RegexOptions.IgnoreCase);
        private static readonly Regex UnderlineStyle = new Regex(@"text-decoration\s*:\s*underline", RegexOptions.IgnoreCase);

        private readonly IBrowsingContext _context;
        private readonly string _baseUrl;
        private readonly string _titleFromUrl;
        private IDocument? _firstChapter;

        public FfnScraper(IBrowsingContext context, Uri uri) {
            _context = context;
            _titleFromUrl = uri.Segments[^1];
            _baseUrl = $"https://{uri.Host}/{uri.Segments[1]}{uri.Segments[2]}".TrimEnd('/');
        }

        public async Task<StoryMetadata> GetMetadataAsync(CancellationToken cancellationToken) {
            IDocument page;
            if(_firstChapter is null) {
                var url = $"{_baseUrl}/1/{_titleFromUrl}";
                page = await _context.OpenAsync(url, cancellationToken).ConfigureAwait(false);
                _context.NavigateTo(page);
                _firstChapter = page;
            } else {
                page = _firstChapter;
            }

            var title = ExtractTitle(page);
            var author = ExtractAuthor(page);
            var hasCover = ExtractCoverUri(page) is not null;
            var chapterNames = ExtractChapterNames(page) ?? new[]{title};
            var description = ExtractDescription(page);
            var updateDate = ExtractUpdateDate(page);

            return new StoryMetadata(
                title,
                author,
                hasCover,
                chapterNames,
                description,
                updateDate
            );
        }

        public async Task<IDocument> GetChapterTextAsync(int number, CancellationToken cancellationToken) {
            if(number == 1 && _firstChapter is not null) {
                return await ExtractTextAsync(_firstChapter).ConfigureAwait(false);
            }

            var page = await _context.OpenAsync($"{_baseUrl}/{number}/{_titleFromUrl}", cancellationToken).ConfigureAwait(false);
            _context.NavigateTo(page);
            return await ExtractTextAsync(page).ConfigureAwait(false);
        }

        public async Task<IResponse> GetCoverAsync(CancellationToken cancellationToken) {
            var resourceLoader = _context.GetService<IResourceLoader>()
                ?? throw new InvalidOperationException("Browsing context was not configured with a resource loader.");

            var (coverUri, coverElem) = ExtractCoverUri(_firstChapter)
                ?? throw new InvalidOperationException("Attempted cover download for story with no cover.");

            var download = resourceLoader.FetchAsync(new ResourceRequest(coverElem, new Url(coverUri)));
            using var cancelRegistration = cancellationToken.Register(download.Cancel);
            return await download.Task.ConfigureAwait(false);
        }

        private async Task<IDocument> ExtractTextAsync(IDocument page) {
            var text = await _context.OpenNewAsync().ConfigureAwait(false);

            var body = text.QuerySelector("body");
            foreach(var child in page.QuerySelector("#storytext").ChildNodes) {
                if(child is IElement elem) {
                    if(elem.TagName == "P") {
                        body.AppendChild(ProcessParagraph(elem));
                    } else {
                        body.AppendChild(elem.Clone());
                    }
                } else {
                    body.AppendChild(child.Clone());
                }
            }

            return text;

            IElement ProcessParagraph(IElement p) {
                var newP = text.CreateElement("p");

                foreach(var child in p.ChildNodes) {
                    newP.AppendChild(child.Clone());
                }

                foreach(var span in newP.QuerySelectorAll("span")) {
                    if(span.HasAttribute("style") && UnderlineStyle.IsMatch(span.GetAttribute("style"))) {
                        span.ClassList.Add("underline");
                        span.RemoveAttribute("style");
                    }
                }

                if(p.HasAttribute("style") && CenterStyle.IsMatch(p.GetAttribute("style"))) {
                    var div = text.CreateElement("div");
                    div.ClassList.Add("center");
                    div.AppendChild(newP);

                    return div;
                } else {
                    return newP;
                }
            }
        }

        private string ExtractTitle(IDocument page) {
            return page.QuerySelector("#profile_top > b").Text();
        }

        private string ExtractAuthor(IDocument page) {
            return page.QuerySelector("#profile_top > a").Text();
        }

        private IReadOnlyList<string>? ExtractChapterNames(IDocument page) {
            var dropdown = page.QuerySelector("#chap_select");
            if(dropdown is null) {
                // single-chapter story
                return null;
            }
            var chapters = new List<string>();

            foreach(var chapter in dropdown.Children) {
                var title = chapter.Text().Split(". ", 2)[1];
                chapters.Add(title);
            }

            return chapters.AsReadOnly();
        }

        private (string, IElement)? ExtractCoverUri(IDocument page) {
            var coverElem = page.QuerySelector(".cimage[data-original]");
            if(coverElem is null) {
                return null;
            }

            var uri = coverElem.GetAttribute("data-original");
            if(uri.StartsWith("//")) {
                return ("https:" + uri, coverElem);
            }
            return (uri, coverElem);
        }

        private string ExtractDescription(IDocument page) {
            return page.QuerySelector("#profile_top > div").Text();
        }

        private DateTimeOffset ExtractUpdateDate(IDocument page) {
            return DateTimeOffset.FromUnixTimeSeconds(
                long.Parse(page.QuerySelector("#profile_top span[data-xutime]").GetAttribute("data-xutime"))
            );
        }

        public void Dispose() {
            _context.Dispose();
        }

        public override string ToString() {
            return $"FfnScraper({_baseUrl}/1/{_titleFromUrl})";
        }
    }
}
