# README

Media Player Broker (mpb) is an application that helps you play and track media you have watched over disparet locations. mpb keeps track of what you have played at Location A so when you are at Location B you can see what you have watched from either location to avoid digging through history command output over SSH.

mpb is not a player itself but it can be configured to launch your player of choice to view media.


## Latest Changes

- cleaned up version and config's usage of importlib.metadata and/or pkg_resources (removed pkg_resources)
- cleaned up `info` to be more concise and to show more 'about' info
- update copyright date
- package updates: idna, pydantic, typer, package
- change python version requirement from 3.8+ to 3.11+ (for speed and to leverage internal tomllib)


### NOTICE

- version 1.0.0 requires python 3.11+ (for internal toml processing capabilities and its fast)
- version 0.14.0 corrected the spelling error (injest ─⏵ ingest) which requires a change to your `user_config.toml` file (change `[injest]` to `[ingest]`)


### The Need

Rather than living in the cloud I have my videos duplicated at various locations. I needed something that remembers what episode of MacGyver I had watched in one location so when I was in another location I could continue watching the next episode without digging through `history` output or keeping track of what was played where.

mpb consists of a CLI application (the client) and a database (couchdb). From the client you `ingest` your media metadata. This extracts the file names from file paths and stores the data in the database. After ingesting, you can `list` your media which shows you the media Item, whether it has been watched or not along with a Rating, Notes, and the Sources the item is available at. You can then use the `play` command along with the Item to watch the Item. After playback is completed you are prompted to mark the item as played/watched, Rate it and add Notes - all of which are used in the `list` command to show what you have already watched and what is new.

mpb can also be used by multiple 'users' - you can share a 'user' so your wife can see what you have watched or you can keep separate users so your wife sees what she has watched and you know what you have watched.


### Install

We recommend using [pipx](https://github.com/pypa/pipx) to install mpbroker: `pipx install mpbroker`. You can also install via pip: `pip install --user mpbroker`.

mpbroker uses a config file to store your setup. This file contains information such as your media player, the database url, and types of data to ingest. You can grab the sample config file from  [mpbroker/example/user_config.toml](https://gitlab.com/drad/mpbroker/-/blob/master/mpbroker/example/user_config.toml) and place it in a config location. mpbroker searches the following locations for the config file (in order of precedence):

- $MPB_CONFIG_HOME: set this environment variable to any path you like and place the mpbroker `user_config.toml` file in this location
- $XDG_CONFIG_HOME/mpbroker
- $APPDATA/mpbroker
- $HOME/.config/mpbroker


### Configure

#### Notices

- an example `user_config.toml` file can be found in the [project example directory](https://gitlab.com/drad/mpbroker/-/tree/master/mpbroker/example)
- if you do not want to use the standard locations and do not want to set a `MPB_CONFIG_HOME` envvar you can set `MPB_CONFIG_HOME` on the command line before calling mpb such as `MPB_CONFIG_HOME=/opt/tmp mpb list 'The_Matrix'`

To set up MPB you need to:
- create your `user_config.toml` file (see above for locations of this file)
- configure your user_config.toml file (at a minimum you will need to set/change the `database.db_uri` value)
- ensure your mpb database is available
  + use the `db-init` command to initialize your db if it is a new instance!

If you are testing mpb or do not have a database you can use docker-compose to start a local database with `docker-compose up` from the [project's docker-compose.yml file](https://gitlab.com/drad/mpbroker). If you use the local database your `database.db_uri` would be: `http://localhost:5984` (add your username and password if needed).


### Using MPB

mpb has built in help (`mpb --help`) which should give you enough info to get going.

A Quick Start:

- you will likely want to `ingest` some media
- next you can use `list` to view/find an item to play
- finally you can `play` an item

#### Paging Output

mpb has pager support, to enable it set the 'use_pager' config option in the user_config.toml file. By default this is not enabled as most pagers drop color support. If you would like pager support and want color to remain in the output you can set the following in your `~/.bashrc` (or equivalent) file:

```
export LESS='--quit-if-one-screen --ignore-case --status-column --LONG-PROMPT --RAW-CONTROL-CHARS --HILITE-UNREAD --tabs=4 --no-init --window=-4'
```

Tip: using a pager allows showing one 'page' (screen) of results at a time; however, most pagers (less) also allow searching within the results easily and quickly. We recommend setting the `--RAW-CONTROL-CHARS` and using `less` with mpbroker.


### Ingestion

Ingestion is the process of loading media metadata into your mpbroker database.

#### Extract Metadata

Extracting metadata on ingestion increases the ingestion time but adds the following data to each ingested media item:

    file_size: # filesize in human readable format (569 MiB, 1.1 GiB)
    file_type: # file type (video/H265)
    file_format: # file format (Matroska)
    encoding: # encoding (x265)
    duration: # duration in human readable format (1 h 52 min, 2 h 48 min)
    resolution: # resulution in width x height format (720 x 480)
    aspect_ratio: # display aspect ratio (16:9)
    audio_format:  audio format (AAC)
    audio_sampling: audio sample rate (48000)

To extract metadata you will need to install [MediaInfo](https://mediaarea.net/en/MediaInfo) which should be available in the repo of most distributions:

- arch: `mediainfo`
- debian: `mediainfo`

#### Ingestion Time Details

- ~500 videos
    + with metadata extraction: 6.05s
    + without metadata extraction: 99.05s
- 2785 videos
    + with metadata extraction: 596.53s
    + without metadata extraction: 72.75s
