# sndid
`sndid` identifies sounds.

At present only birds are identified.


# Install
Install thusly.

Using Debian Stable (12/Bookworm).

Install thine dependencies:
```
sudo apt update
sudo apt install git ffmpeg python3-pip python3-venv python-is-python3 \
  netcat-traditional sox alsa-utils portaudio19-dev
```

Install this repo. Adapt to local Python setup, ala:

```
git clone --recursive https://spacecruft.org/deepcrayon/sndid
cd sndid/
pyenv local 3.11 # For example, if pyenv is used
python -m venv venv
source venv/bin/activate
pip install -U pip poetry
poetry install
```

# Usage
Note, BirdNet tensorflow works fine with just the CPU, no GPU required to use the model.

## Command line
As such:

```
sndid
```

Help:
```
$ sndid -h
usage: sndid.py [-h] [-i INPUT] [-t LATITUDE] [-n LONGITUDE] [-y YEAR] [-m MONTH] [-d DAY] [-c CONFIDENCE] [-l | --list | --no-list]

Run sndid

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input filename to process (default samples/sample.wav)
  -t LATITUDE, --latitude LATITUDE
                        Latitude (default 40.57)
  -n LONGITUDE, --longitude LONGITUDE
                        Longitude (default -105.23)
  -y YEAR, --year YEAR  Year (default today)
  -m MONTH, --month MONTH
                        Month (default today)
  -d DAY, --day DAY     Day (default today)
  -c CONFIDENCE, --confidence CONFIDENCE
                        Minimum Confidence (default 0.50)
  -l, --list, --no-list
                        Output as human readable list not terse (default True)
```

Sample output:

```
$ sndid
Hairy Woodpecker, Dryobates villosus, 15.0, 18.0, 0.8371534943580627
Hairy Woodpecker, Dryobates villosus, 18.0, 21.0, 0.8111729025840759
Hairy Woodpecker, Dryobates villosus, 30.0, 33.0, 0.50068598985672
Hairy Woodpecker, Dryobates villosus, 33.0, 36.0, 0.7170186042785645
Hairy Woodpecker, Dryobates villosus, 39.0, 42.0, 0.6576249003410339
Hairy Woodpecker, Dryobates villosus, 48.0, 51.0, 0.8048814535140991
Hairy Woodpecker, Dryobates villosus, 51.0, 54.0, 0.9604988694190979
Hairy Woodpecker, Dryobates villosus, 54.0, 57.0, 0.8156641125679016
Hairy Woodpecker, Dryobates villosus, 57.0, 60.0, 0.8230038285255432
```


## Server
The sndid-server waits for connections to feed it wav file segments,
then processes the sound.

It prints to the terminal and also logs to `sndid.log`.

Run thusly:

```
sndid-server
```

Help:
```
$ sndid-server -h
usage: sndid-server.py [-h] [-i IP] [-p PORT] [-t LATITUDE] [-n LONGITUDE] [-y YEAR] [-m MONTH] [-d DAY] [-c CONFIDENCE]

Run sndid-server

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Server IP address (default 127.0.0.1)
  -p PORT, --port PORT  Server network port (default 9988)
  -t LATITUDE, --latitude LATITUDE
                        Latitude (default 40.57)
  -n LONGITUDE, --longitude LONGITUDE
                        Longitude (default -105.23)
  -y YEAR, --year YEAR  Year (default 2023)
  -m MONTH, --month MONTH
                        Month (default 9)
  -d DAY, --day DAY     Day (default 19)
  -c CONFIDENCE, --confidence CONFIDENCE
                        Minimum Confidence (default 0.25)
```

Sample output on startup:

```
$ sndid-server
2023-10-03 10:45:47.343270-06:00 sndid-server started 127.0.0.1:9988
```

After client connects and sends mono wav:

```
$ sndid-server 
2023-10-03 10:45:47.343270-06:00 sndid-server started 127.0.0.1:9988
2023-10-03 10:46:34.060983-06:00 Hairy Woodpecker, Dryobates villosus, 0.3896884322166443
2023-10-03 10:46:34.061248-06:00 Hairy Woodpecker, Dryobates villosus, 0.47060683369636536
2023-10-03 10:46:34.061312-06:00 Hairy Woodpecker, Dryobates villosus, 0.5013241171836853
2023-10-03 10:46:34.061377-06:00 Hairy Woodpecker, Dryobates villosus, 0.6557420492172241
2023-10-03 10:46:34.061429-06:00 Hairy Woodpecker, Dryobates villosus, 0.7146830558776855
2023-10-03 10:46:34.061498-06:00 Hairy Woodpecker, Dryobates villosus, 0.806126594543457
2023-10-03 10:46:34.061553-06:00 Hairy Woodpecker, Dryobates villosus, 0.8105885982513428
2023-10-03 10:46:34.061628-06:00 Hairy Woodpecker, Dryobates villosus, 0.8147749900817871
2023-10-03 10:46:34.061678-06:00 Hairy Woodpecker, Dryobates villosus, 0.8241879343986511
2023-10-03 10:46:34.061725-06:00 Hairy Woodpecker, Dryobates villosus, 0.837184488773346
2023-10-03 10:46:34.061771-06:00 Hairy Woodpecker, Dryobates villosus, 0.9604253768920898
```

Sample server output from a realtime stream:

```
$ sndid-server
2023-10-03 10:38:52.975515-06:00 sndid-server started 127.0.0.1:9988
2023-10-03 10:41:27.162509-06:00 Northern Flicker, Colaptes auratus, 0.2552548944950104
2023-10-03 10:41:27.162775-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.3168713450431824
2023-10-03 10:41:27.172693-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.3708573877811432
2023-10-03 10:41:27.172858-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.4243549406528473
2023-10-03 10:41:38.446815-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.2577541172504425
2023-10-03 10:41:49.688914-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.3252100646495819
2023-10-03 10:42:45.590852-06:00 Rock Wren, Salpinctes obsoletus, 0.34000715613365173
2023-10-03 10:43:52.545070-06:00 Spotted Towhee, Pipilo maculatus, 0.31051698327064514
2023-10-03 10:44:15.007297-06:00 Clark's Nutcracker, Nucifraga columbiana, 0.6180582642555237
2023-10-03 10:44:15.007515-06:00 Northern Flicker, Colaptes auratus, 0.35758695006370544
2023-10-03 10:44:26.109497-06:00 Clark's Nutcracker, Nucifraga columbiana, 0.27328306436538696
2023-10-03 10:44:26.109734-06:00 Clark's Nutcracker, Nucifraga columbiana, 0.32902488112449646
2023-10-03 10:44:26.109799-06:00 Clark's Nutcracker, Nucifraga columbiana, 0.6783570647239685
```

## Client
Requires mono wav file.

To convert stereo to mono with sox:

```
sox -c 2 stereo.wav -c 1 mono.wav
```


Run client to submit file to server thusly:

```
sndid-client
```

Help:
```
$ sndid-client -h
usage: sndid-client [-h] [-i IP] [-p PORT] [-f FILE]

Run sndid-client

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Server IP address (default 127.0.0.1)
  -p PORT, --port PORT  Server network port (default 9988)
  -f FILE, --file FILE  Input filename to process (default samples/mono.wav)
```

Sample output:

```
$ sndid-client
Sending samples/mono.wav to 127.0.0.1:9988
```

## ALSA Client
Use this script to stream from the microphone to the server,
using ALSA.

```
sndid-alsa
```


Help:

```
$ sndid-alsa -h
usage: sndid-alsa [-h] [-i IP] [-p PORT] [-r RATE] [-t TIME]

Run sndid-alsa

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Server IP address (default 127.0.0.1)
  -p PORT, --port PORT  Server network port (default 9988)
  -r RATE, --rate RATE  Rate in Hertz (default 48000)
  -t TIME, --time TIME  Length of segments in seconds (default 10)
```

Sample output:

```
$ sndid-alsa 
Streaming ALSA in to 127.0.0.1:9988
Recording WAVE 'stdin' : Float 32 bit Little Endian, Rate 48000 Hz, Mono
```

Exit with `CTRL-C`.

## Stream
`sndid-stream` streams *from* a URL to the `sndid-server`.
Input URL can be anything ffmpeg can read (everything).


Help:
```
$ sndid-stream -h
usage: sndid-stream [-h] [-i IP] [-p PORT] [-t TIME] -u URL

Run sndid-stream

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Server IP address (default 127.0.0.1)
  -p PORT, --port PORT  Server network port (default 9988)
  -t TIME, --time TIME  Length of segments in seconds (default 60)
  -u URL, --url URL     Input url
```

Exit with `CTRL-Z` and `kill %1`  :) por ahora.


## List
`sndid-list` lists sounds available to be identified at a particular
time and location.

XXX This script is foobar at the moment, as it uses a different
model than the other scripts.

Use:

```
sndid-list
```

Help:
```
$ sndid-list -h
usage: sndid-list.py [-h] [-t LATITUDE] [-n LONGITUDE] [-y YEAR] [-m MONTH] [-d DAY] [-g | --geo | --no-geo] [-c | --cal | --no-cal]

Run sndid-list

options:
  -h, --help            show this help message and exit
  -t LATITUDE, --latitude LATITUDE
                        Latitude (default 40.57)
  -n LONGITUDE, --longitude LONGITUDE
                        Longitude (default -105.23)
  -y YEAR, --year YEAR  Year (default today)
  -m MONTH, --month MONTH
                        Month (default today)
  -d DAY, --day DAY     Day (default today)
  -g, --geo, --no-geo   Limit list by geocoordinates (default False)
  -c, --cal, --no-cal   Limit list by calendar date (default False, use with --geo)
```

Sample output:

```
$ sndid-list -c -g
American Robin, Turdus migratorius
Black-billed Magpie, Pica hudsonia
Black-capped Chickadee, Poecile atricapillus
Blue Jay, Cyanocitta cristata
Canada Goose, Branta canadensis
Common Raven, Corvus corax
Eurasian Collared-Dove, Streptopelia decaocto
European Starling, Sturnus vulgaris
House Finch, Haemorhous mexicanus
Mallard, Anas platyrhynchos
Mountain Bluebird, Sialia currucoides
Mountain Chickadee, Poecile gambeli
Mourning Dove, Zenaida macroura
Northern Flicker, Colaptes auratus
Red-tailed Hawk, Buteo jamaicensis
Turkey Vulture, Cathartes aura
Western Meadowlark, Sturnella neglecta
White-crowned Sparrow, Zonotrichia leucophrys
Wilson's Warbler, Cardellina pusilla
Yellow-rumped Warbler, Setophaga coronata
```

The current count of all species in model:

```
$ sndid-list |& wc -l
6522
```


## JACK
`sndid-jack` reads audio from JACK ports, Ardour Master Out 1/2 by default,
and identifies birds in the stream.

It logs the identification in a text file.

It saves the identification to an audio file.

```
$ sndid-jack --help
usage: sndid-jack [-h] [--config_file CONFIG_FILE] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--n-inputs N_INPUTS] [--segment-length SEGMENT_LENGTH]
                  [--min-confidence MIN_CONFIDENCE] [--lat LAT] [--lon LON] [--output-dir OUTPUT_DIR] [--version]

sndid-jack - AI processing JACK Audio Connection Kit.

options:
  -h, --help            show this help message and exit
  --config_file CONFIG_FILE, -c CONFIG_FILE
                        Configuration File name
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}, -L {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level.
  --n-inputs N_INPUTS, -n N_INPUTS
                        Number of inputs
  --segment-length SEGMENT_LENGTH, -l SEGMENT_LENGTH
                        Segment length
  --min-confidence MIN_CONFIDENCE, -m MIN_CONFIDENCE
                        Minimum confidence
  --lat LAT, -y LAT     Latitude
  --lon LON, -x LON     Longitude
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory for detections
  --version, -v         show program's version number and exit
```


# Development
To "develop", install the requirements:

Run black on the Python files for nice formatting:

```
black sndid/*.py
```


# Upstream
## Birds
### BirdNet
BirdNet is the bird model used.
The model is under a non-libre CC NC license.

* https://birdnet.cornell.edu/

The source code is available here:

* https://github.com/kahst/BirdNET-Analyzer


### birdnetlib
birdnetlib is based on BirdNet, but with a different codebase and author.
birdnetlib uses BirdNet's non-libre NC model files.
birdnetlib has a dependency on the non-free BirdNet-Analyzer Python code
just for testing.

The source code to birdnetlib itself is under the Apache 2.0 license.
birdnetlib is Free Software / Open Source Software, with non-libre dependency
for testing.

* https://github.com/joeweiss/birdnetlib

In sum, AFAICT, building upon birdnetlib, then creating a libre model,
would be a fully libre system without any non-libre dependencies.


# Status
Alpha, initial development.

* The system ran from October, 2023 to May, 2024
and generated 671,080 identifications.

* Analyzing files works.

* Using `sndid-server` then `sndid-stream` works best now for "realtime",
but is kludgy.

* `sndid-jack` works well with few xruns.


# Disclaimer
I'm not a programmer and I know less about birds.

## AI
Currently using Codestral v0.1 and Qwen2 Instruct models with Parrot.


# Copyright
Unofficial project, not related to upstream projects.

Upstream sources under their respective copyrights.


# License
Apache 2.0.

*Copyright &copy; 2023, 2024 Jeff Moe.*
