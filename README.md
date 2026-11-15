# FFXIV Plugins UNIversal
Consolidated plugins list for FFXIV Dalamud

![uni](img/uni.png)

`https://raw.githubusercontent.com/cBachoo/ffxiv-plugins-uni/main/repo.json`

## Updating
`repo.json` is regenerated every 6 hours by a GitHub Action. To run it locally with [uv](https://docs.astral.sh/uv/):

```sh
uv run update
```

(`python3 update.py` also works; there are no dependencies.)

To add a source, append its URL to `REPOS` in `update.py`.

## Penumbra
Recommended to include separately otherwise it will throw a fit that it was not downloaded from the original repo.

Add Penumbra alongside this repo to Dalamud's custom plugin repositories list.

`https://raw.githubusercontent.com/xivdev/Penumbra/master/repo.json`
