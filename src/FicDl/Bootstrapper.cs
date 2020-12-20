using AngleSharp;
using AngleSharp.Io;
using AngleSharp.Io.Network;
using FicDl.Pages;
using Stylet;
using StyletIoC;
using System.Net.Http;

namespace FicDl {
    public class Bootstrapper : Bootstrapper<ShellViewModel> {
        protected override void ConfigureIoC(IStyletIoCBuilder builder) {
            builder.Bind<HttpClient>().ToFactory(_ => {
                var client = new HttpClient();
                client.DefaultRequestHeaders.UserAgent.ParseAdd(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    + " (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55");
                return client;
            }).InSingletonScope();

            builder.Bind<IBrowsingContext>().ToFactory(container => {
                var config = AngleSharp.Configuration.Default
                    .WithRequester(new HttpClientRequester(container.Get<HttpClient>()))
                    .WithDefaultLoader(new LoaderOptions {IsResourceLoadingEnabled = true});
                return BrowsingContext.New(config);
            });
        }

        protected override void Configure() {
            // Perform any other configuration before the application starts
        }
    }
}
