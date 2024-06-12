# Download videos from ixigua.com

### Installation

```bash
python3 -m pip install ixigua
```

### Usage

```bash
ixigua --help
```

### Examples

1. download a single video

```bash
# item_url, item_id or pseries_url+item_id
ixigua https://www.ixigua.com/7359024563227656714
ixigua https://www.ixigua.com/7034201007231861256?id=7359024563227656714
ixigua 7359024563227656714
```

2. download all videos in a playlist

```bash
# pseries_url, pseries_id or pseries_url+item_id
ixigua https://www.ixigua.com/7034201007231861256?id=7359024563227656714 --playlist
ixigua https://www.ixigua.com/7034201007231861256 --playlist
ixigua 7034201007231861256 --playlist
```

3. more options

```bash
# dryrun mode
ixigua 7359024563227656714 --dryrun
ixigua 7359024563227656714 --dryrun --playlist

# download part of the playlist
ixigua 7359024563227656714 --playlist --playlist-start 10 --playlist-end 15

# prefix with rank number
ixigua 7359024563227656714 --playlist --rank-prefix

# prefix with index number
ixigua 7359024563227656714 --playlist --playlist-start 10  --index-prefix 11

# specify the output directory
ixigua 7359024563227656714 -O out

# specify a definition
ixigua 7359024563227656714 --definition 480p
```
