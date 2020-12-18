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
        private string? _coverPath;
        private int _currentChapterNumber = 2;
        private int _chapterCount = 3;
        private bool _canDownload = true;
        private readonly IWindowManager _windowManager;

        public string? Url { get; set; }
        public string? CoverPath {
            get => _coverPath;
            set => SetAndNotify(ref _coverPath, value);
        }
        public int CurrentChapterNumber {
            get => _currentChapterNumber;
            set => SetAndNotify(ref _currentChapterNumber, value);
        }
        public int ChapterCount {
            get => _chapterCount;
            set => SetAndNotify(ref _chapterCount, value);
        }

        public DownloadViewModel(IWindowManager windowManager) {
            _windowManager = windowManager;
        }

        public void BrowseForCover() {
            var dlg = new OpenFileDialog() {
                DereferenceLinks = true,
                Filter = "JPG and PNG Images|*.jpg;*.jpeg;*.png",
                Multiselect = false,
                Title = "Choose cover"
            };

            if(dlg.ShowDialog() == true) {
                CoverPath = dlg.FileName;
            }
        }

        public bool CanDownload {
            get => _canDownload;
            set => SetAndNotify(ref _canDownload, value);
        }
        public void Download() {
            var downloader = new DownloadProgressViewModel(Url);
            _windowManager.ShowDialog(downloader);
        }
    }
}
