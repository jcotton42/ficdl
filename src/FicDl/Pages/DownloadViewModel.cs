using FicDl.Scrapers;
using Microsoft.Win32;
using Stylet;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace FicDl.Pages {
    public class DownloadViewModel : Screen {
        private string? coverPath;
        private int currentChapterNumber = 2;
        private int chapterCount = 3;
        private bool canDownload = true;
        private readonly IWindowManager windowManager;

        public string? Url { get; set; }
        public string? CoverPath {
            get => this.coverPath;
            set => this.SetAndNotify(ref this.coverPath, value);
        }
        public int CurrentChapterNumber {
            get => this.currentChapterNumber;
            set => this.SetAndNotify(ref this.currentChapterNumber, value);
        }
        public int ChapterCount {
            get => this.chapterCount;
            set => this.SetAndNotify(ref this.chapterCount, value);
        }

        public DownloadViewModel(IWindowManager windowManager) {
            this.windowManager = windowManager;
        }

        public void BrowseForCover() {
            var dlg = new OpenFileDialog() {
                DereferenceLinks = true,
                Filter = "JPG and PNG Images|*.jpg;*.jpeg;*.png",
                Multiselect = false,
                Title = "Choose cover"
            };

            if(dlg.ShowDialog() == true) {
                this.CoverPath = dlg.FileName;
            }
        }

        public bool CanDownload {
            get => this.canDownload;
            set => this.SetAndNotify(ref this.canDownload, value);
        }
        public async void Download() {
            var downloader = new DownloadProgressViewModel(this.Url);
            this.windowManager.ShowDialog(downloader);
        }
    }
}
