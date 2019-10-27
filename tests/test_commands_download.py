import hashlib
import os

from click.testing import CliRunner

from mmemoji.cli import cli

from .utils import EMOJIS, emoji_inventory, user_env


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["create", "--help"])
    assert result.exit_code == 0


def test_download_emoji(cli_runner, tmp_path):
    # Setup
    destination = tmp_path
    emoji_name = "emoji_1"
    emoji_filename = "{}.png".format(emoji_name)
    emoji_sha1 = EMOJIS[emoji_name]["sha1"]
    user = "user-1"
    # Test
    with user_env(user), emoji_inventory([emoji_name], user):
        result = cli_runner.invoke(
            cli, ["download", emoji_name, str(destination)]
        )
    paths = result.stdout.rstrip().split("\n")
    assert result.exit_code == 0
    assert len(paths) == 1
    assert os.path.basename(paths[0]) == emoji_filename
    with (destination / emoji_filename).open("rb") as f:
        assert hashlib.sha1(f.read()).hexdigest() == emoji_sha1
