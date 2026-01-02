import fire
import subprocess

from log import Log


class ToolsInstaller:
    def __init__(self):
        try:
            subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            Log.error("Git is not installed. Please install Git first.")
            exit(1)

    def install(self, *args, **kwargs):
        remote_server_ssh_key = kwargs.get(
            "remote_server_ssh_key", kwargs.get("ssh_key", "")
        )
        remote_server_user = kwargs.get("remote_server_user", kwargs.get("user", ""))
        remote_server_host = kwargs.get("remote_server_host", kwargs.get("host", ""))
        if not remote_server_ssh_key:
            Log.error(
                "Remote server SSH key is required: --remote_server_ssh_key or --ssh_key"
            )
            exit(1)
        if not remote_server_user:
            Log.error("Remote server user is required: --remote_server_user or --user")
            exit(1)
        if not remote_server_host:
            Log.error("Remote server host is required: --remote_server_host or --host")
            exit(1)

        Log.info("Will installing tools:", args)
        for tool in args:
            if tool == "pyenv":
                from pyenv import PyenvInstaller

                Log.info("Installing pyenv...")
                installer = PyenvInstaller(
                    remote_server_ssh_key=remote_server_ssh_key,
                    remote_server_user=remote_server_user,
                    remote_server_host=remote_server_host,
                )
                installer.install()
            elif tool == "nodenv":
                from nodenv import NodenvInstaller

                Log.info("Installing nodenv...")
                installer = NodenvInstaller(
                    remote_server_ssh_key=remote_server_ssh_key,
                    remote_server_user=remote_server_user,
                    remote_server_host=remote_server_host,
                )
                installer.install()
            else:
                Log.error(f"Unknown tool: {tool}")


if __name__ == "__main__":
    fire.Fire(ToolsInstaller)
