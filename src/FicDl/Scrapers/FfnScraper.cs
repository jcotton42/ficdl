using AngleSharp;
using AngleSharp.Dom;
using AngleSharp.Io;
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace FicDl.Scrapers {
    public class FfnScraper {
        private static readonly Regex CenterStyle = new Regex(@"text-align\s*:\s*center", RegexOptions.IgnoreCase);
        private static readonly Regex UnderlineStyle = new Regex(@"text-decoration\s*:\s*underline", RegexOptions.IgnoreCase);
        private readonly IBrowsingContext context;
        private string baseUrl;
        private string titleFromUrl;
        private IDocument? firstChapter;

        public FfnScraper(IBrowsingContext context, Uri uri) {
            this.context = context;
            this.titleFromUrl = uri.Segments[^1];
            this.baseUrl = $"https://{uri.Host}/{uri.Segments[1]}{uri.Segments[2]}".TrimEnd('/');
        }

        public async Task<StroyMetadata> GetMetadataAsync(CancellationToken cancellationToken) {
            var url = $"{this.baseUrl}/1/{this.titleFromUrl}";
            var page = await context.OpenAsync(CreateGetRequest(url), cancellationToken);
            this.firstChapter = page;

            var title = this.ExtractTitle(page);
            var author = this.ExtractAuthor(page);
            var coverUri = this.ExtractCoverUri(page);
            var coverThumbnailUri = this.ExtractCoverThumbnailUri(page);
            var chapterNames = this.ExtractChapterNames(page) ?? new[]{title};
            var description = this.ExtractDescription(page);
            var updateDate = this.ExtractUpdateDate(page);

            return new StroyMetadata(
                title,
                author,
                coverUri,
                coverThumbnailUri,
                chapterNames,
                description,
                updateDate
            );
        }

        // DownloadCoverAsync
        // necessary b/c e.g. FFN needs Referer headers, otherwise the scrape is blocked
        // AngleSharp can't set that header right now, might need to use HttpClient directly

        public async Task<IDocument> GetChapterTextAsync(int number, CancellationToken cancellationToken) {
            if(number == 1 && this.firstChapter is not null) {
                return await this.ExtractTextAsync(this.firstChapter);
            }

            var page = await this.context.OpenAsync(CreateGetRequest($"{this.baseUrl}/{number}/{this.titleFromUrl}"), cancellationToken);
            return await this.ExtractTextAsync(page);
        }

        /// Workaround for AngleSharp bug (https://github.com/AngleSharp/AngleSharp/issues/920)
        /// where setting Referer on the DefaultRequester isn't passed through
        private static DocumentRequest CreateGetRequest(string uri) {
            return DocumentRequest.Get(new Url(uri), referer: "https://www.fanfiction.net/");
        }

        private async Task<IDocument> ExtractTextAsync(IDocument page) {
            var text = await context.OpenNewAsync();

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

        private Uri? ExtractCoverUri(IDocument page) {
            var cover = page.QuerySelector(".cimage[data-original]");
            if(cover is null) {
                return null;
            }

            var uri = cover.GetAttribute("data-original");
            if(uri.StartsWith("//")) {
                return new Uri("https:" + uri);
            }
            return new Uri(uri);
        }

        private Uri? ExtractCoverThumbnailUri(IDocument page) {
            var cover = page.QuerySelector(".cimage:not([data-original])");
            if(cover is null) {
                return null;
            }

            var uri = cover.GetAttribute("src");
            if(uri.StartsWith("//")) {
                return new Uri("http:" + uri);
            }
            return new Uri(uri);
        }

        private string ExtractDescription(IDocument page) {
            return page.QuerySelector("#profile_top > div").Text();
        }

        private DateTimeOffset ExtractUpdateDate(IDocument page) {
            return DateTimeOffset.FromUnixTimeSeconds(
                long.Parse(page.QuerySelector("#profile_top span[data-xutime]").GetAttribute("data-xutime"))
            );
        }

        public override string ToString() {
            return $"FfnScraper({this.baseUrl}/1/{this.titleFromUrl})";
        }
    }
}
