// unset

using AngleSharp;
using System;

namespace FicDl.Scrapers {
    public class ScraperFactory {
        private readonly Func<IBrowsingContext> _browsingContextFactory;

        public ScraperFactory(Func<IBrowsingContext> browsingContextFactory) {
            _browsingContextFactory = browsingContextFactory;
        }

        public IScraper CreateScraper(Uri uri) {
            if(uri.Host.EndsWith("fanfiction.net", StringComparison.OrdinalIgnoreCase)) {
                return new FfnScraper(_browsingContextFactory(), uri);
            } else {
                throw new ArgumentException($"No scraper for {uri} exists.", nameof(uri));
            }
        }
    }
}
