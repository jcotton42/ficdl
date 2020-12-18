using AngleSharp;
using Serilog;
using System;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace FicDl.Writers {
    public class EpubWriter {
        private readonly IBrowsingContext _context;
        private readonly ILogger _logger;

        public string Extension => ".epub";
        public string Description => "ePub";

        public EpubWriter(IBrowsingContext context, ILogger logger) {
            _context = context;
            _logger = logger;
        }

        //public string? GetToolPath() {
            // should be in the parent abstract class
            // that impl will check env vars and PATH
            // on Windows PathFindOnPathW will help here
        //}

        public async Task WriteAsync(WriterOptions options, CancellationToken cancellationToken) {
            var doc = await _context.OpenNewAsync(cancellation: cancellationToken);
            var body = doc.GetElementsByTagName("body")[0];

            foreach(var (title, text) in options.Chapters) {
                var h1 = doc.CreateElement("h1");
                h1.TextContent = title;
                body.AppendChild(h1);
                foreach(var node in text.GetElementsByName("body")[0].ChildNodes) {
                    body.AppendChild(node);
                }
            }

            var startInfo = new ProcessStartInfo {
                FileName = "pandoc",
                ArgumentList = {
                    "--from=html",
                    "--to=epub",
                    "--metadata=lang:en-US",
                    $"--metadata=title:{options.Metadata.Title}",
                    $"--metadata=creator:{options.Metadata.Author}",
                    $"--metadata=date:{options.Metadata.UpdateDateUtc:yyyy-MM-dd}",
                    $"--metadata=description:{options.Metadata.Description}",
                    "--toc",
                    $"--output={options.OutputPath}"
                },
                UseShellExecute = false,
                RedirectStandardError = true,
                RedirectStandardInput = true,
                RedirectStandardOutput = false,
                StandardErrorEncoding = Encoding.UTF8,
                StandardInputEncoding = Encoding.UTF8,
                CreateNoWindow = true
            };
            if(options.CoverPath is not null) {
                startInfo.ArgumentList.Add($"--epub-cover-image={options.CoverPath}");
            }

            var process = new Process {
                StartInfo = startInfo
            };

            process.ErrorDataReceived += (_, args) => _logger.Information(args.Data);

            process.Start();
            process.BeginErrorReadLine();
            
            using(var stdinStream = process.StandardInput) {
                doc.ToHtml(stdinStream);
            }
            
            try {
                await process.WaitForExitAsync(cancellationToken).ConfigureAwait(false);
            } catch(TaskCanceledException) {
                process.CancelErrorRead();
                try {
                    process.Kill();
                } catch(InvalidOperationException) {
                    // process already exited, just ignore it
                }
                File.Delete(options.OutputPath);
                _logger.Information("Write to {OutputPath} canceled.", options.OutputPath);
                throw;
            }
        }
    }
}
