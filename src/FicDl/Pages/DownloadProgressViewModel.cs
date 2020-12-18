using AngleSharp;
using AngleSharp.Io;
using AngleSharp.Io.Network;
using FicDl.Scrapers;
using FicDl.Writers;
using Stylet;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace FicDl.Pages {
    public class DownloadProgressViewModel : Screen {
        private readonly CancellationTokenSource cancelSource;
        private readonly string uri;
        private string storyTitle;
        private string storyAuthor;
        private int currentChapterNumber;
        private int chapterCount;
        private string currentChapterTitle;
        private bool isIndeterminate;

        public string StoryTitle {
            get => this.storyTitle;
            set => this.SetAndNotify(ref this.storyTitle, value);
        }
        public string StoryAuthor {
            get => this.storyAuthor;
            set => this.SetAndNotify(ref this.storyAuthor, value);
        }
        public int CurrentChapterNumber {
            get => this.currentChapterNumber;
            set => this.SetAndNotify(ref this.currentChapterNumber, value);
        }
        public int ChapterCount {
            get => this.chapterCount;
            set => this.SetAndNotify(ref this.chapterCount, value);
        }
        public string CurrentChapterTitle {
            get => this.currentChapterTitle;
            set => this.SetAndNotify(ref this.currentChapterTitle, value);
        }
        public bool IsIndeterminate {
            get => this.isIndeterminate;
            set => this.SetAndNotify(ref this.isIndeterminate, value);
        }

        public DownloadProgressViewModel(string uri) {
            this.cancelSource = new CancellationTokenSource();
            this.uri = uri;
        }

        public void CancelDownload() {
            this.cancelSource.Cancel();
        }

        private async void DownloadStory() {
            var httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55");
            var config = AngleSharp.Configuration.Default
                .WithRequester(new HttpClientRequester(httpClient))
                .WithDefaultLoader(new LoaderOptions {
                    IsResourceLoadingEnabled = true
                });

            var scraper = new FfnScraper(BrowsingContext.New(config), new Uri(uri));
            var metadata = await scraper.GetMetadataAsync(this.cancelSource.Token);

            StoryTitle = metadata.Title;
            StoryAuthor = metadata.Author;
            ChapterCount = metadata.ChapterNames.Count;

            Debug.WriteLine(metadata);
            var rand = new Random();
            foreach(var chapterName in metadata.ChapterNames) {
                CurrentChapterNumber++;
                CurrentChapterTitle = chapterName;
                await Task.Delay(TimeSpan.FromMilliseconds(rand.Next(500, 1250)), this.cancelSource.Token);
                using var text = await scraper.GetChapterTextAsync(CurrentChapterNumber, this.cancelSource.Token);
                await using var file = File.CreateText(
                    Path.Combine("C:/Users/Joshua/apptest", $"{CurrentChapterNumber} - {chapterName}.html")
                );
                text.ToHtml(file);
            }

            if(metadata.HasCover) {
                Debug.WriteLine("Story has a cover.");
                using var response = await scraper.GetCoverAsync(this.cancelSource.Token);
                Debug.WriteLine("Content type: {0}", response.GetContentType());
                await using var file = File.Create(
                    $"C:/Users/Joshua/apptest/cover{response.GetContentType().Suffix}",
                    4096,
                    FileOptions.Asynchronous
                );
                await response.Content.CopyToAsync(file);
            }
            
            this.RequestClose(true);
        }

        protected override void OnInitialActivate() {
            this.DownloadStory();
        }
    }
}
