using Stylet;

namespace FicDl.Pages {
    public class ShellViewModel : Screen {
        public DownloadViewModel DownloadView { get; }

        public ShellViewModel(DownloadViewModel downloadViewModel) {
            DownloadView = downloadViewModel;
        }
    }
}
