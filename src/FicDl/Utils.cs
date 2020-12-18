using System;
using System.IO;

namespace FicDl {
    /// <summary>
    /// Creates a temporary directory, deletes it when disposed.
    /// </summary>
    public sealed class TemporaryDirectory : IDisposable {
        private bool disposed;
        private readonly string path;

        /// <summary>
        /// The path to the temporary directory.
        /// </summary>
        /// <exception cref="ObjectDisposedException">
        /// When this instance has been disposed, and the directory deleted.
        /// </exception>
        public string Path {
            get {
                if(this.disposed) {
                    throw new ObjectDisposedException("this");
                }
                return this.path;
            }
        }

        public TemporaryDirectory() {
            this.path = System.IO.Path.Combine(System.IO.Path.GetTempPath(), System.IO.Path.GetRandomFileName());
            Directory.CreateDirectory(this.Path);
        }

        /// <summary>
        /// Deletes the temporary directory.
        /// </summary>
        public void Dispose() {
            if(!this.disposed) {
                this.disposed = true;
                Directory.Delete(this.path, recursive: true);
            }
        }
    }
}
