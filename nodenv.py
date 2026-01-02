"""
Install nodenv, node-build on a remote server via SSH.
And set NODE_BUILD_MIRROR_URL to Tsinghua Tuna mirror.
"""

import subprocess
import os
import shutil

from log import Log


class NodenvInstaller:
    def __init__(
        self,
        /,
        remote_server_ssh_key: str,
        remote_server_user: str,
        remote_server_host: str,
        remote_server_dist_path: str = "~/.nodenv",
        git_base_url: str = "https://github.com",
    ):
        if git_base_url.endswith("/"):
            git_base_url = git_base_url[:-1]
        self.git_base_url = git_base_url

        # https://github.com/nodenv/nodenv
        self.nodenv_git_url = f"{self.git_base_url}/nodenv/nodenv.git"
        self.node_build_git_url = f"{self.git_base_url}/nodenv/node-build.git"
        self.cache_dir = ".cache/nodenv"
        self.version = "main"

        self.remote_server_ssh_key = remote_server_ssh_key
        self.remote_server_user = remote_server_user
        self.remote_server_host = remote_server_host
        self.remote_server_dist_path = remote_server_dist_path

    def _make_cache_dir(self):
        """
        Create cache dir CWD/.cache/nodenv for saving downloaded files.
        """
        Log.info("Creating cache directory for nodenv...")
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        Log.info(f"Created cache directory at {self.cache_dir}")

    def _clone_repo(self, repo_url: str, dest_dir: str):
        Log.info(f"Cloning {repo_url} into {dest_dir}...")
        subprocess.run(
            [
                "git",
                "clone",
                "--branch",
                self.version,
                "--depth",
                "1",
                repo_url,
                dest_dir,
            ],
            check=True,
        )
        Log.info(f"Cloned {repo_url} into {dest_dir}")

    def _download(self):
        self._clone_repo(self.nodenv_git_url, os.path.join(self.cache_dir, "nodenv"))
        self._clone_repo(
            self.node_build_git_url,
            os.path.join(self.cache_dir, "nodenv", "plugins", "node-build"),
        )

    def _gzip_cache(self):
        Log.info("Compressing downloaded nodenv...")

        tarball_path = os.path.join(self.cache_dir, "nodenv.tar.gz")
        if os.path.exists(tarball_path):
            os.remove(tarball_path)

        subprocess.run(
            [
                "tar",
                "-czf",
                tarball_path,
                "-C",
                os.path.join(self.cache_dir, "nodenv"),
                ".",
            ],
            check=True,
        )
        Log.info(f"Compressed nodenv to {tarball_path}")
        return tarball_path

    def _get_remote_gzip_path(self):
        return "~/tools-installer/nodenv.tar.gz"

    def _makesure_remote_dir(self):
        Log.info("Ensuring remote directory exists...")
        subprocess.run(
            [
                "ssh",
                "-i",
                self.remote_server_ssh_key,
                f"{self.remote_server_user}@{self.remote_server_host}",
                "mkdir -p ~/tools-installer",
            ],
            check=True,
        )
        Log.info("Remote directory ensured.")

    def _upload_to_remote(self):
        Log.info("Uploading nodenv.tar.gz to remote server...")
        local_gzip_path = self._gzip_cache()
        remote_gzip_path = self._get_remote_gzip_path()

        subprocess.run(
            [
                "scp",
                "-i",
                self.remote_server_ssh_key,
                local_gzip_path,
                f"{self.remote_server_user}@{self.remote_server_host}:{remote_gzip_path}",
            ],
            check=True,
        )
        Log.info("Uploaded nodenv.tar.gz to remote server.")

    def _unpack_on_remote(self):
        Log.info("Unpacking nodenv on remote server...")
        remote_gzip_path = self._get_remote_gzip_path()
        subprocess.run(
            [
                "ssh",
                "-i",
                self.remote_server_ssh_key,
                f"{self.remote_server_user}@{self.remote_server_host}",
                f"mkdir -p {self.remote_server_dist_path} && tar -xzf {remote_gzip_path} -C {self.remote_server_dist_path}",
            ],
            check=True,
        )
        Log.info("Unpacked nodenv on remote server.")

    def install(self):
        self._make_cache_dir()
        self._download()
        self._makesure_remote_dir()
        self._upload_to_remote()
        self._unpack_on_remote()
        Log.info("nodenv installation completed.")
        print(
            "\nPlease ssh into the remote server and add run following commands to add nodenv to your PATH:",
            "\n  ~/.nodenv/bin/nodenv init\n",
        )
        print(
            "Also, to use Tsinghua Tuna mirror for node-build, add the following line to your shell profile (~/.bashrc, ~/.zshrc, etc.):",
            '\n  export NODE_BUILD_MIRROR_URL="https://mirrors.tuna.tsinghua.edu.cn/nodejs-release"',
        )
