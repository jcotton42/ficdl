using AngleSharp;
using AngleSharp.Io;
using AngleSharp.Io.Network;
using FicDl.Scrapers;
using Stylet;
using System;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace FicDl.Pages {
    public class DownloadProgressViewModel : Screen {
        private CancellationTokenSource? _cancelSource;
        private string _uri;
        private string? _storyTitle;
        private string? _storyAuthor;
        private int _currentChapterNumber;
        private int _chapterCount;
        private string? _currentChapterTitle;
        private bool _isIndeterminate;

        public string? StoryTitle {
            get => _storyTitle;
            set => SetAndNotify(ref _storyTitle, value);
        }
        public string? StoryAuthor {
            get => _storyAuthor;
            set => SetAndNotify(ref _storyAuthor, value);
        }
        public int CurrentChapterNumber {
            get => _currentChapterNumber;
            set => SetAndNotify(ref _currentChapterNumber, value);
        }
        public int ChapterCount {
            get => _chapterCount;
            set => SetAndNotify(ref _chapterCount, value);
        }
        public string? CurrentChapterTitle {
            get => _currentChapterTitle;
            set => SetAndNotify(ref _currentChapterTitle, value);
        }
        public bool IsIndeterminate {
            get => _isIndeterminate;
            set => SetAndNotify(ref _isIndeterminate, value);
        }

        public void CancelDownload() {
            _cancelSource.Cancel();
        }

        public void PrepareForDownload(string uri) {
            ChapterCount = int.MaxValue;
            CurrentChapterNumber = 0;
            StoryTitle = null;
            StoryAuthor = null;
            CurrentChapterTitle = null;
            IsIndeterminate = false;

            _uri = uri;
            _cancelSource?.Dispose();
            _cancelSource = new CancellationTokenSource();
        }

        private async void DownloadStory() {
            var httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55");
            var config = AngleSharp.Configuration.Default
                .WithRequester(new HttpClientRequester(httpClient))
                .WithDefaultLoader(new LoaderOptions {
                    IsResourceLoadingEnabled = true
                });

            var scraper = new FfnScraper(BrowsingContext.New(config), new Uri(_uri));
            var metadata = await scraper.GetMetadataAsync(_cancelSource.Token);

            StoryTitle = metadata.Title;
            StoryAuthor = metadata.Author;
            ChapterCount = metadata.ChapterNames.Count;

            Debug.WriteLine(metadata);
            var rand = new Random();
            foreach(var chapterName in metadata.ChapterNames) {
                CurrentChapterNumber++;
                CurrentChapterTitle = chapterName;
                await Task.Delay(TimeSpan.FromMilliseconds(rand.Next(500, 1250)), _cancelSource.Token);
                using var text = await scraper.GetChapterTextAsync(CurrentChapterNumber, _cancelSource.Token);
                await using var file = File.CreateText(
                    Path.Combine("C:/Users/Joshua/apptest", $"{CurrentChapterNumber} - {chapterName}.html")
                );
                text.ToHtml(file);
            }

            if(metadata.HasCover) {
                Debug.WriteLine("Story has a cover.");
                using var response = await scraper.GetCoverAsync(_cancelSource.Token);
                Debug.WriteLine("Content type: {0}", response.GetContentType());
                await using var file = File.Create(
                    $"C:/Users/Joshua/apptest/cover{response.GetContentType().Suffix}",
                    4096,
                    FileOptions.Asynchronous
                );
                await response.Content.CopyToAsync(file);
            }
            
            RequestClose(true);
        }

        protected override void OnActivate() {
            DownloadStory();
        }
    }
}
