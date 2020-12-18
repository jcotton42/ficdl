using System;
using System.IO;

namespace FicDl {
    /// <summary>
    /// Creates a temporary directory, deletes it when disposed.
    /// </summary>
    public sealed class TemporaryDirectory : IDisposable {
        private bool _disposed;
        private readonly string _path;

        /// <summary>
        /// The path to the temporary directory.
        /// </summary>
        /// <exception cref="ObjectDisposedException">
        /// When this instance has been disposed, and the directory deleted.
        /// </exception>
        public string Path {
            get {
                if(_disposed) {
                    throw new ObjectDisposedException("this");
                }
                return _path;
            }
        }

        public TemporaryDirectory() {
            _path = System.IO.Path.Combine(System.IO.Path.GetTempPath(), System.IO.Path.GetRandomFileName());
            Directory.CreateDirectory(Path);
        }

        /// <summary>
        /// Deletes the temporary directory.
        /// </summary>
        public void Dispose() {
            if(!_disposed) {
                _disposed = true;
                Directory.Delete(_path, recursive: true);
            }
        }
    }
}
