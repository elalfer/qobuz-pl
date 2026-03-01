# qobuz_pl

A command‑line utility that lets you download Qobuz playlist as XSPF file supported
by various media players. Especially usefull with Strawberry player support.

## Installation

### Clone the repo

```
git clone https://github.com/elalfer/qobuz_pl.git
cd qobuz_pl
```

### (Optional but recommended) create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

`pip install qobuz_dl`

## Quick start

```Bash
# Download a playlist
qobuz_pl.py download -e user@example.com -u https://www.qobuz.com/en-pl/playlist/123456

# List all user's playlists (not implemented)
qobuz_pl.py list -e user@example.com
```

## Usage

```Bash
Run
qobuz_pl.py <action> -e <email> -p <password> -u <playlist_url>

action:
 - download – fetch all tracks
 - list – show playlist metadata

Options:
  -h, --help            show this help message and exit
  -e EMAIL, --email=EMAIL
                        Qobuz email
  -p PASSWORD, --password=PASSWORD
                        Qobuz password
  -u URL, --url=URL     Playlist URL
  --id=ID               Playlist id
```

## Contributing

 - Fork the repo
 - Create a branch (git checkout -b feature/foo)
 - Commit your changes
 - Submit a pull request

## License

MIT
