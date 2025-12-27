# Chromatographic Playlist

Many years ago I heard about a moving picture about people in a record shop. Perhaps it was _High Fidelity_. For some reason I understood that one of the 
characters sorted his music albums chromatographically, so thought that was a novel idea. I have since learned that this was not the case in that movie, but then again, why not?

So here it is, a tool to sort your playlists chromotographically by album cover art.

## Quick Start

```bash
uv run python -m chromalist get-playlist 1o5JatfgL3F34icBqTynSk # Top Hits 1980-1990
uv run python -m chromalist process-images
uv run python -m chromalist generate-sorted-playlist
```

Run tests:

```bash
uv run pytest
```

## How it works

- fetch a playlist from Spotify (note: API token required)
- get the album cover art for each song
- use the _k-means clustering_ algorithm to extract the dominant _k_ colours from the cover image
- map the top colour to HSV colour space, and use the Hue component as a unidimensional scalar we can sort by
- emit the chromatographically sorted playlist

## Implementation

- Python: we use Python as the implementation language, because it has very good image processing libraries.
- Sci-Py: we use the _k-means algorithm_ from there
- Astral `uv`: a quick way to manage the Python packages (https://docs.astral.sh/uv/)
- Astral `ty`: the type-checker (see https://docs.astral.sh/ty/)
- Typer: for parsing the CLI (see https://typer.tiangolo.com/)
- Docker: This project runs in a Docker container

### Source Layout

```
project_root/
├── pyproject.toml       # Configuration for uv, deps, and tool settings
├── src/
│   └── chromalist/      
│       ├── __init__.py          # Empty, no exports
│       ├── __main__.py          # Allows `python -m chromalist`
│       ├── cli.py               # Command-line interface logic (click/typer)
│       ├── spotify_client.py    # Spotify client for downloading the playlists and album art
│       ├── image_processing.py  # Image processing logic
│       └── models.py            # A bit overkill, but this is the domain model
└── tests/                       # Tests code for the various files above
```

### Command Line Interface
By default, all intermediate data (playlists, images _etc._) is stored in the `tmp/` directory.

#### Setting the Output Directory
You can use the `--output-dir {dir-name}` to specify the output directory for intermediate files. The default is `tmp/`.

#### Download a Playlist from Spotify
Download a playlist with a given ID and its album cover images to the output directory.

The playlist is called `playlist.json`, the images are named from their Spotify track IDs, `{track-id}.jpg`.

```bash
uv run python -m chromalist get-playlist {playlist-id}
```

#### Process Images
Run the image processing on the images in the output directory, writing a `image-colours.json` file there with the result.

```bash
uv run python -m chromalist process-images
```

#### Sort Playlist
Generate a chromatically sorted playlist from the `playlist.json` and the `image-colours.json` in the output directory 
writing a file `sorted-playlist.json` with the result.

```bash
uv run python -m chromalist generate-sorted-playlist
```

### Spotify API Tokens

You have to sign up for the Spotify Developer programme.
After that "Create an app" to get a client ID and client secret to sign in via the API.

Note: For some reason you may get 404 errors when requesting Spotify-owned playlists like the Global Top 50.
I read somewhere that perhaps this is just for newly created developer accounts, but if you try with
someone else's playlist it works fine.


## Examples

### Top Hits  1980-1990
https://open.spotify.com/playlist/1o5JatfgL3F34icBqTynSk

So, if we let run Top Hits 1980-1990, playlist ID `1o5JatfgL3F34icBqTynSk` it sorts it into this: 

<img src="https://i.scdn.co/image/ab67616d0000b273eb11e2abccdca41f39ad3b89" alt="I'm Still Standing (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273499c6d2eaeb941d76acdfe41" alt="It's a Sin (Pet Shop Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273499c6d2eaeb941d76acdfe41" alt="Always on My Mind (Pet Shop Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273499c6d2eaeb941d76acdfe41" alt="Domino Dancing (Pet Shop Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273499c6d2eaeb941d76acdfe41" alt="West End Girls (Pet Shop Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b83db319caf59b07c8055f71" alt="D.I.S.C.O. - English Maxi Version (Ottawan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b83db319caf59b07c8055f71" alt="Hands Up (Ottawan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734d0418c998ee5879cce6a91f" alt="One Night In Bangkok - Radio Edit / From “Chess” / Remastered 2016 (Murray Head)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273605223665713cdf285ee0c81" alt="Smooth Criminal - 2012 Remaster (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6954c1f074f66907a8c5483" alt="In The Air Tonight - 2015 Remastered (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dc77e9fda68572f218233a87" alt="What A Feeling (Irene Cara)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c208d60c83e8611195875e13" alt="La Bamba (Los Lobos)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273af5437d890d1a41486e0a322" alt="Young Turks - 2008 Remaster (Rod Stewart)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735334fdec11d3cee1ba545a56" alt="Upside Down (Diana Ross)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732e0cd1330748a5b7764dd562" alt="Smooth Criminal - 2012 Remaster (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732e0cd1330748a5b7764dd562" alt="The Way You Make Me Feel - 2012 Remaster (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732e0cd1330748a5b7764dd562" alt="Bad - 2012 Remaster (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c500e7ab2ab870a9fed56e8f" alt="St. Elmos Fire (Man in Motion) (John Parr)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27396a1909790d3b6a986e2b971" alt="Moonlight Shadow (Mike Oldfield)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cfe4163cbb6d12f3ec15898e" alt="Maneater (Daryl Hall & John Oates)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734500e13175a66153e053eacc" alt="Just Like Heaven - Remastered 2006 (The Cure)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27388ffe8c41647856e6fa5e1ab" alt="Just Can't Get Enough (Depeche Mode)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7a9a6a2bf311630d3fc6956" alt="Faith - Remastered (George Michael)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7a9a6a2bf311630d3fc6956" alt="Father Figure - Remastered (George Michael)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ae9574ae6ef79308324579dc" alt="Seven Tears (Goombay Dance Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e1661e05970bbafcf9339e43" alt="Love in the First Degree (Bananarama)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273920f421260033ee54865d673" alt="We Are The World (U.S.A. For Africa)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739824c6e084b02d24b2e22e94" alt="Break My Stride (Matthew Wilder)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27399d424b0873a9a714279a9f3" alt="Like a Virgin (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739015296f9afabfc102989521" alt="How Will I Know (Whitney Houston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273be1421122cef4940f500ac06" alt="Brother Louie (Modern Talking)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273be1421122cef4940f500ac06" alt="Atlantis Is Calling (S.O.S. for Love) (Modern Talking)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273edbbd1e4dde99597ce850c54" alt="True Colors (Cyndi Lauper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732ff76b4da68f018b4735ee59" alt="Flashdance...What a Feeling - Radio Edit (Irene Cara)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bd0c47e4cfb4ee327e53bc73" alt="You Spin Me Round (Like a Record) (Dead Or Alive)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fb2daafa0993f39d87a84385" alt="Another Day in Paradise - 2016 Remaster (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730a043c8c45330aa972c46339" alt="99 Luftballons (Nena)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ed1e6f4480313f95ac380159" alt="Give It Up (KC & The Sunshine Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f82ae34da3139fbd2a88332b" alt="What's Love Got to Do with It - 2015 Remaster (Tina Turner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f82ae34da3139fbd2a88332b" alt="Private Dancer - 2015 Remaster (Tina Turner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27343cd140ef706ad2eec17d514" alt="Pedro (Raffaella Carrà)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27349c982dae436bac27c336f45" alt="Tainted Love (Soft Cell)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cb3cea7439a97660b3aedb8c" alt="Straight Up (Paula Abdul)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731b83255ef342451b977987aa" alt="Hit Me With Your Best Shot (Pat Benatar)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27319db9ac54c80a898a179f0f1" alt="Footloose (Kenny Loggins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27319db9ac54c80a898a179f0f1" alt="Danger Zone - From "Top Gun" Original Soundtrack (Kenny Loggins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734f3004f43ea41a8ee1510035" alt="Gloria (Laura Branigan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27328fc1c4ca395c4a2ffa31a47" alt="Kingston Town (UB40)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d1e7c0e1bf0980298428a1ae" alt="I Want To Break Free - Single Remix (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d1e7c0e1bf0980298428a1ae" alt="Radio Ga Ga - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a0473825f51aed3fac5fd187" alt="It's a Heartache (Bonnie Tyler)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27399aab0b95eb4bb1e7e24c795" alt="You're My Heart, You're My Soul (Modern Talking)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27399aab0b95eb4bb1e7e24c795" alt="You Can Win If You Want (Modern Talking)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737d32e463de3d8d8b39dcac2c" alt="Listen To Your Heart (Roxette)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737d32e463de3d8d8b39dcac2c" alt="The Look (Roxette)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737d32e463de3d8d8b39dcac2c" alt="Dressed For Success (Roxette)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b9c4979446c4d39bc08e9503" alt="Forever Young (Alphaville)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27364c19b24ce947ffa363f8f96" alt="Faith (George Michael)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27349cb2d53994caada391cf39e" alt="9 to 5 (Dolly Parton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273784f3d22b1b28313311acd2a" alt="Karma Chameleon (Culture Club)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c7d7cdad0c2ffa5620129ee8" alt="Karma Chameleon - Remastered 2002 (Culture Club)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734121faee8df82c526cbab2be" alt="Billie Jean (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734121faee8df82c526cbab2be" alt="Beat It (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734121faee8df82c526cbab2be" alt="Thriller (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27390b8a540137ee2a718a369f9" alt="Fast Car (Tracy Chapman)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734650ca0a8f88129d4667acc5" alt="I'm So Excited (The Pointer Sisters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27388d9f988d7b80763afa0ed20" alt="You Drive Me Crazy (Shakin' Stevens)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273404ce2160a2d568946709926" alt="Costa Blanca (Fantastique)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734742af6d5c9eae5f7f63ee5e" alt="Words - Original Version 1983 (F.R. David)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732ec4aea38b44eba9756767fa" alt="Smalltown Boy (Bronski Beat)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27307d3de253ec02c26c04b95f1" alt="Venus (Bananarama)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ab243ed96c6518acc60f9b1b" alt="Islands in the Stream (Dolly Parton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273255e131abc1410833be95673" alt="Never Gonna Give You Up (Rick Astley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273255e131abc1410833be95673" alt="Together Forever (Rick Astley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f8996a3f97e80d9d700635c3" alt="I Still Haven't Found What I'm Looking For - Remastered 2007 (U2)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f56fd6d98d947df0faa32be6" alt="The Road to Hell Part 2 (Chris Rea)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bd4d1a9adfb6d6fe515a8118" alt="When the Rain Begins to Fall (Jermaine Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cd7c557f88ea2f827f91ff85" alt="Oh Julie (Shakin' Stevens)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e9d575a198f3f79e362c72d0" alt="Boys - Summertime Love (Sabrina)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736b44fa8f5415cc4c945117be" alt="Material Girl (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ec057272ce74dadb7f9870bf" alt="Leave a Light On (7" Version) (Belinda Carlisle)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ec057272ce74dadb7f9870bf" alt="La Luna (7" Version) (Belinda Carlisle)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ec057272ce74dadb7f9870bf" alt="Heaven Is A Place On Earth (Promo 7" Edit) (Belinda Carlisle)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ec057272ce74dadb7f9870bf" alt="Circle in the Sand (7" Version) (Belinda Carlisle)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273927530e44371f0bc1bb296d4" alt="(I've Had) The Time of My Life - From "Dirty Dancing" Soundtrack (Bill Medley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bcf214aa282a19326c295e31" alt="Baby Jane - 2008 Remaster (Rod Stewart)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c5c6cddc4cdce692d2c9c630" alt="Big in Japan - 2019 Remaster (Alphaville)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e5855edffddef46b7feff49b" alt="You Can Call Me Al (Paul Simon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a6299e1e5c220b5b132d2a0b" alt="Gimme Hope Jo'Anna (Eddy Grant)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27370a92681f8aff88714cb0296" alt="Lambada - Original Version 1989 (Kaoma)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27354fc938a153a1adb6461e20f" alt="I'm So Excited (The Pointer Sisters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e54b27a25383c0e8e10e6778" alt="The Loco-Motion (Kylie Minogue)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273da6790936a48b6719083dcac" alt="We Built This City (Starship)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a2fc41b0dd6ce4f0d16a4c46" alt="Wake Me Up Before You Go-Go (Wham!)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a2fc41b0dd6ce4f0d16a4c46" alt="Everything She Wants (Wham!)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a29ca418b2a64e80002a86e3" alt="Here Comes the Rain Again - Remastered Version (Eurythmics)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273275774501f737e10d92adaca" alt="Relax (Come Fighting) (Frankie Goes To Hollywood)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273515b863931c7c056796cf177" alt="The Riddle (Nik Kershaw)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735579d8a505c727349a203074" alt="Don't You Want Me (The Human League)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d0c7c131a979c9e5436f89ce" alt="Englishman In New York (Sting)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d3e56dcd0f042784a8b145f4" alt="Gloria (Umberto Tozzi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732deb62442d38d6e6fff5efa8" alt="Black Velvet (Alannah Myles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735a0fca95bfacb33ca3580a29" alt="Sacrifice (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273af1bb86907b4457c4e83390f" alt="Woman in Love (Barbra Streisand)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b5aaa0790028feff586033f3" alt="Dolce Vita (Ryan Paris)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735a51a3d944b6a2891abf7607" alt="Senza Una Donna - Remastered 2007 (Zucchero)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737b436d31c5ae44b334736619" alt="Maniac (Michael Sembello)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273db56ceff816b668b7b6f04ff" alt="The Lion Sleeps Tonight (Tight Fit)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e8dd4db47e7177c63b0b7d53" alt="Take on Me (a-ha)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a3bc94f95c99c3ad2f40740a" alt="Enola Gay - Remastered 2003 (Orchestral Manoeuvres In The Dark)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732fcad2af6e3d43006c6f42c4" alt="I Want It All - Single Version (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aedd9728f5cc4b13ee49e061" alt="Cheri Cheri Lady (Modern Talking)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730225711dc520d382bf0d0b45" alt="Higher Love - Single Version (Steve Winwood)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737a1e0215c41f0ce411623301" alt="If I Could Turn Back Time (Cher)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27329c68eb2726f08eca5ba8613" alt="Uptown Girl (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf1fee2a55e98e22bf358512" alt="Heaven (Bryan Adams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273680c56a0f621a43edf19046a" alt="Live Is Life (Digitally Remastered) - Single Version (Opus)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c1d3679959ec78f671658952" alt="You Win Again (Bee Gees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273681265e351fc75e60d0fa50b" alt="Girls Just Want to Have Fun (Cyndi Lauper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aaba065944cd82a6f15c86b6" alt="Everywhere - 2017 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aaba065944cd82a6f15c86b6" alt="Little Lies - 2017 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738a667825eb276f019e61be41" alt="Don't Answer Me (The Alan Parsons Project)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b3994c94dfb241923664bb4d" alt="Sweet Dreams (Are Made of This) - 2005 Remaster (Eurythmics)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fb2faa3ed46d1d0124ca325e" alt="(I Just) Died In Your Arms (Cutting Crew)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cebdf1f7660ace8c2a80585c" alt="I'm on My Way (The Proclaimers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8e97cafeb2acb85b21a777e" alt="Every Breath You Take (The Police)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273995239a0e35a898037ec4b29" alt="Walk Of Life (Dire Straits)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27322463d6939fec9e17b2a6235" alt="Everybody Wants To Rule The World (Tears For Fears)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731336b31b6a1799f0de5807ac" alt="Livin' On A Prayer (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731336b31b6a1799f0de5807ac" alt="You Give Love A Bad Name (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c5653f9038e42efad2f8a266" alt="Don't Stop Believin' (Journey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273026c97edb4b984cccdc91204" alt="Crash (The Primitives)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ef89c52c42eaf1f89347a16c" alt="You Got It (Roy Orbison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273056e90910cbaf5c5b892aeba" alt="Another One Bites The Dust - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273056e90910cbaf5c5b892aeba" alt="Crazy Little Thing Called Love - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737993518ee7b6756f3f9eb27f" alt="Athos (Cusco)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ff191d7fbdb5a13eaf84132b" alt="Back In Black (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fffb0cd86567da0cd03baa5e" alt="Hands Up - Single Version (Ottawan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce023ce7dfdd5199bcdfd5a1" alt="Time After Time (Cyndi Lauper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce023ce7dfdd5199bcdfd5a1" alt="Girls Just Want to Have Fun (Cyndi Lauper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273705698f9c5e04d08ee33aaa8" alt="Sexy Sexy Lover - Vocal Version (Modern Talking)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a04b4373fd72bf81c8784adf" alt="The Best (Tina Turner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b414c63fb435b622238c15ed" alt="Jump - 2015 Remaster (Van Halen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27332a7d87248d1b75463483df5" alt="Thriller (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27332a7d87248d1b75463483df5" alt="Beat It (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27332a7d87248d1b75463483df5" alt="Billie Jean (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733c73b2e0a6aa490736f19751" alt="I Love Rock 'N Roll (Joan Jett & the Blackhearts)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d794da71193896da66166ef1" alt="Hold On Tight (Electric Light Orchestra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738cf86a9be38868f1d73cdb58" alt="Heart Of Glass - Special Mix (Blondie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738cefe8e2f2cfd63ce073fa96" alt="Total Eclipse of the Heart (Bonnie Tyler)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730f6ce5c138493ac768d9afc8" alt="Don't Stop Believin' (Journey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a641b32019d779543f24f39d" alt="Crockett's Theme (Jan Hammer)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739bfc30d5173d5cddab44e5c1" alt="Geronimo's Cadillac (Modern Talking)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f5e30500f0eec7d92b159eae" alt="The Final Countdown (Europe)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733b43ef752e5af1d00c1fc213" alt="In The Army Now (Status Quo)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738f9281135c8a343ac36ab44d" alt="Eternal Flame (The Bangles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733e030a7e606959674643d274" alt="I Want to Know What Love Is - 1999 Remaster (Foreigner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732c33399e119cec9b0fcde564" alt="Say You, Say Me (Lionel Richie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273142d0705dc9bc174ef1d7c10" alt="Cause You Are Young - Maxi-Version (C.C. Catch)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273142d0705dc9bc174ef1d7c10" alt="I Can Lose My Heart Tonight - Maxi-Version (C.C. Catch)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273142d0705dc9bc174ef1d7c10" alt="Heartbreak Hotel (C.C. Catch)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273142d0705dc9bc174ef1d7c10" alt="Heaven and Hell (C.C. Catch)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273142d0705dc9bc174ef1d7c10" alt="Soul Survivor - Single Version (C.C. Catch)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273142d0705dc9bc174ef1d7c10" alt="Strangers by Night - Maxi-Version (C.C. Catch)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ab0a92e5cd20c2224c44a8a6" alt="You Can't Hurry Love - 2016 Remaster (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730bcbe6f61bcd984b8116709a" alt="You Spin Me Round (Like a Record) - Rip It Up Version (Dead Or Alive)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a69b2f779d3e76c1c2ac8df8" alt="Never Ending Story (Limahl)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731310670cbb82f06474372cfd" alt="Self Control (Laura Branigan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273de3094d98b62340d3268c7bc" alt="La Isla Bonita (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273de3094d98b62340d3268c7bc" alt="True Blue (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738bd8adbdc4727d9080240905" alt="Come On Eileen (Dexys Midnight Runners)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738fe438c0dce2d985ba65197c" alt="I Will Survive - 1981 Re-recording (Gloria Gaynor)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cddc25435cb94483d4b7bb45" alt="Celebration - Single Version (Kool & The Gang)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cddc25435cb94483d4b7bb45" alt="Get Down On It - Single Version (Kool & The Gang)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d2675cb6847d1b1da9fc28a3" alt="Holding Out for a Hero - From "Footloose" Soundtrack (Bonnie Tyler)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d2675cb6847d1b1da9fc28a3" alt="If You Were a Woman (And I Was a Man) (Bonnie Tyler)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a40e4b29bfacc9ef505b86d2" alt="Wonderful Life (Black)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738f5813c842cb115f3cf1fecd" alt="Voyage voyage (Desireless)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731ade47900d03a0276737982b" alt="(I'll Never Be) Maria Magdalena - Single Verison (Sandra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731ade47900d03a0276737982b" alt="Everlasting Love (Sandra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ebc918cfb51e9ced7349f436" alt="Call Me (Blondie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273314bb5b3c472f6f0b6887b57" alt="Party All the Time (Eddie Murphy)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273377198e5b790b5ebf137bd83" alt="Nothing's Gonna Stop Us Now (Starship)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f662f46fe0fe1ba5931af4fd" alt="Got My Mind Set on You (George Harrison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b80d7868e6e0275d12102508" alt="Abracadabra (Steve Miller Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273518f91224cff0d2e9b6d56ef" alt="Sailing On The Seven Seas (Orchestral Manoeuvres In The Dark)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6f713a49f98ec228d7f9883" alt="D.I.S.C.O. - Single Version (Ottawan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e831397f320e6eca72c5ff71" alt="Sun of Jamaica (Goombay Dance Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e0c3e555afcd70597d605b8e" alt="Don't Go (Yazoo)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b4a878f008a0eda552446701" alt="Beat It (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a520a167a62d5548cdb53101" alt="I Wanna Dance with Somebody (Who Loves Me) (Whitney Houston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce5ad5ce2b582aa56ca59022" alt="Our House (Madness)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273eafaf556eda644a745d0144d" alt="Walking On Sunshine (Katrina & The Waves)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733ce3e2272e25916844f10d86" alt="Don't Dream It's Over (Crowded House)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e0f0aa947770fe74049dbba3" alt="Heaven Is A Place On Earth (Belinda Carlisle)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273472fbc1d5743c7d3c75b9ec0" alt="Just the Two of Us (feat. Bill Withers) (Grover Washington, Jr.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b9b09b7eabe5274035553f98" alt="Orinoco Flow - 2009 Remaster (Enya)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273944ecffd87319c90a971b72b" alt="If You Leave - Remastered 2019 (Orchestral Manoeuvres In The Dark)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273592124b134716cc5896c6422" alt="Hot Together (The Pointer Sisters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273015c484a7aca592df1a77828" alt="House of the Rising Sun (The Animals)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a43a6482e327d623bb0c0f77" alt="Dancing In the Dark (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a43a6482e327d623bb0c0f77" alt="Born in the U.S.A. (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a43a6482e327d623bb0c0f77" alt="Glory Days (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273de82204a5baa683ce85d57cb" alt="Tarzan Boy (Baltimora)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ebd6d20c0082524244ef83df" alt="Africa (TOTO)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734f7420eec423c20556744d7d" alt="Tell It to My Heart (Taylor Dayne)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27354c5b44fb18030a3385c7b88" alt="Say Say Say (Paul McCartney)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce32b2f1b4b9e2f1c68f84cc" alt="We Didn't Start the Fire (Billy Joel)" width="64" height="64">

### BRITPOP: 100 best songs
https://open.spotify.com/playlist/0O31LAgwwraj2CExjqqZSx

Playlist ID `0O31LAgwwraj2CExjqqZSx`

<img src="https://i.scdn.co/image/ab67616d0000b2739164bafe9aaa168d93f4816a" alt="Yellow (Coldplay)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27310d91fae4e9d2b0a2d758060" alt="Can You Dig It? (The Mock Turtles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bd8d27544ccf850e5b0d6f0b" alt="This Is How It Feels (Inspiral Carpets)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b898b548c5c60cfe1206a772" alt="Three Lions (Football's Coming Home) (Baddiel, Skinner & Lightning Seeds)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273009e277693241201a82ed486" alt="Sparky's Dream (Teenage Fanclub)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739c68d6c16a9121a08a0c28e9" alt="Blinded By The Sun (The Seahorses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733594e35c6b023eb82e235953" alt="Sometimes (James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b1ec5185789c1629351de33d" alt="Just Another Rainbow (Liam Gallagher)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730e47adf6052f3a1b05c958c1" alt="Gravity (Embrace)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e4162b6b6cb0b24ec845018a" alt="The Only One I Know (The Charlatans)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739c72b249fcaa04d074c1dfcd" alt="Friday I'm In Love (The Cure)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731b5c06982d105c8b6b08d041" alt="For Love (Lush)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cbea7e7a20a9df4b22dc5148" alt="Love Is All Around - From "Four Weddings And A Funeral" (Wet Wet Wet)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b67dbb84e0c1f82be886c8ea" alt="Laid (James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ece7df13dbc6f1ba88c5a1ad" alt="Animal Nitrate (Suede)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ece7df13dbc6f1ba88c5a1ad" alt="Metal Mickey (Suede)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a85e2d460874afa804b07807" alt="Chasing Rainbows (Shed Seven)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a85e2d460874afa804b07807" alt="Chasing Rainbows (Shed Seven)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b6aeeb6414c5d3ddac43be2a" alt="Leave Them All Behind - 2001 Remaster (Ride)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27350fadb5f91ef4accf5d96544" alt="Govinda (Kula Shaker)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273593b4d24c3b4eb501279bbc6" alt="Patio Song (Gorky's Zygotic Mynci)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27394983882a5effd77742a9f52" alt="Tender (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739293c743fa542094336c5e12" alt="Fake Plastic Trees (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27398d2b5f9e0c3d00e6bc423da" alt="Walkaway (Cast)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27372d481a5999197ef5f42f796" alt="Zombie (The Cranberries)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a5ef992caf2355282a9d4c6b" alt="National Express (The Divine Comedy)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732951c50b6cfcf7e0e26279aa" alt="Why Does It Always Rain On Me? (Travis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736d7b8671cfcf7f914c741a72" alt="Lenny Valentino (The Auteurs)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732951c50b6cfcf7e0e26279aa" alt="Driftwood (Travis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736d7b8671cfcf7f914c741a72" alt="New French Girlfriend (The Auteurs)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273de114203356c1f7b136960b6" alt="Beetlebum - 2012 Remaster (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737f04eef099ddb5c34a1f3afc" alt="Parklife - 2012 Remaster (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d86a1e021e7acc7c07c7d668" alt="Live Forever - Remastered (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d86a1e021e7acc7c07c7d668" alt="Supersonic - Remastered (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730a7d1e9face30d0357e21dcd" alt="Do You Remember The First Time? (Pulp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730a7d1e9face30d0357e21dcd" alt="Lipgloss (Pulp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ec548c00d3ac2f10be73366d" alt="Creep (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cd17a643be6e98617af3d87a" alt="Hush (Kula Shaker)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c038b03e66fb6de76a5b3904" alt="The Drugs Don't Work (The Verve)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c038b03e66fb6de76a5b3904" alt="Lucky Man (The Verve)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27312d78ae76a8b2d7a1c2f593d" alt="Good Enough (Dodgy)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27343563ea094f0ea99f5d84583" alt="Whatever (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27361c4e50faedd1482b89de850" alt="Staying Out For The Summer (Dodgy)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27354a78359ef17a590ab24256c" alt="Beautiful Ones (Suede)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27354a78359ef17a590ab24256c" alt="Trash (Suede)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273093f37d1e0d111c33096d3e9" alt="Kelly's Heroes (Black Grape)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738609a2ac949cf0bf0f183def" alt="The Last of the Famous International Playboys - 2010 Remaster (Morrissey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fa15f99bdd335ddc8f588242" alt="Girl From Mars (Ash)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b5f24b5004d008f05b0cb148" alt="Motorcycle Emptiness (Manic Street Preachers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273707d13d3f87652e737e94d45" alt="Bitter Sweet Symphony - Remastered 2016 (The Verve)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273707d13d3f87652e737e94d45" alt="Sonnet (The Verve)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce0e813b2e3c71fcaa5005b7" alt="Tubthumping (Chumbawamba)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf1f6466a493eb73d6d9d280" alt="I Wanna Be Adored - Remastered 2009 (The Stone Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf1f6466a493eb73d6d9d280" alt="She Bangs the Drums - Remastered 2009 (The Stone Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273671c709e025a3ed8c956d115" alt="Have A Nice Day (Stereophonics)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738b88d0f28103db8071d67191" alt="Slight Return (The Bluetones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27357b41d7e2ef3e9903aa21b75" alt="Moving (Supergrass)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27357b41d7e2ef3e9903aa21b75" alt="Pumping On Your Stereo (Supergrass)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a9b827f16c08362301d332fc" alt="The Boy With the Arab Strap (Belle and Sebastian)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739b643c1d962bfdb276598876" alt="One to Another (The Charlatans)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c313153da427c8d0f3cf9179" alt="Spaceman (Babylon Zoo)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273326f28b8d0099329cecb01c8" alt="If You Tolerate This Your Children Will Be Next (Manic Street Preachers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273326f28b8d0099329cecb01c8" alt="You Stole the Sun from My Heart (Manic Street Preachers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ecdb914ea9cbbb31c5a6b71b" alt="Dakota (Stereophonics)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732f2eeee9b405f4d00428d84c" alt="Don't Look Back In Anger (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732f2eeee9b405f4d00428d84c" alt="Wonderwall (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732f2eeee9b405f4d00428d84c" alt="Champagne Supernova (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6d0dd7232e493681a4dd230" alt="Perfect 10 (The Beautiful South)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732f2eeee9b405f4d00428d84c" alt="Some Might Say (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738a9c1b058c215b14983e0725" alt="There She Goes (The La's)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734464fd26a7b4be42675876ac" alt="Road Rage (Catatonia)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b3fb824e9730591fe4e5b17e" alt="Rotterdam (Or Anywhere) (The Beautiful South)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fd952bece8f049dbcd7df93f" alt="Common People - Full Length Version (Pulp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fd952bece8f049dbcd7df93f" alt="Disco 2000 (Pulp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fd952bece8f049dbcd7df93f" alt="Mis-Shapes (Pulp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738f384040b0e29681ce396fcc" alt="Juxtapozed with U (Super Furry Animals)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736e2977bd512137598b5e00fc" alt="Nancy Boy (Placebo)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733d577eba3860affba2f2d334" alt="Ready to Go (Republica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27334cbf7013afccc7df67fa43f" alt="Country House (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27334cbf7013afccc7df67fa43f" alt="Girls & Boys (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27334cbf7013afccc7df67fa43f" alt="Song 2 (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a4ec4c922ae55defc4668afa" alt="Wake up Boo! (The Boo Radleys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c51308138d3d02b0ef0c0a1f" alt="King of the Kerb (Echobelly)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8b444df094279e70d0ed856" alt="Paranoid Android (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731eddfa59f1758ab46ad19ce1" alt="Saturn 5 (Inspiral Carpets)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c9ab72e50682b061dd318604" alt="Lucky You (The Lightning Seeds)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d6edad0d4fc3448ccc61c13c" alt="The Universal - 2012 Remaster (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731ba99b34edfc33fb4a9ea5a1" alt="Getting Away With It (All Messed Up) (James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d1b2fdf89b885ee6d07cef13" alt="Inbetweener (Sleeper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734934e5682e4444406294ab0c" alt="Brimful of Asha - Norman Cook Remix Single Version (Cornershop)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273020eeb90bc55f4a0415eefde" alt="You're Gorgeous (Babybird)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730b13316f2c7d7c916dc675db" alt="Something 4 the Weekend (Super Furry Animals)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736e6832759078e93b8aff1cdd" alt="Daydreamer (Menswear)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738f8e24262ca7ef631e62c5f6" alt="A Design for Life - Remastered (Manic Street Preachers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730d8a62430369b60b0edbc2d1" alt="Olympian (Gene)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737d2fd2378160e40c96bc61ff" alt="Alright (Supergrass)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a9f25500062b93a4f36d51be" alt="She Said (Longpigs)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735ac670b8c48b7446c8aade5e" alt="Connection (Elastica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735ac670b8c48b7446c8aade5e" alt="Waking Up (Elastica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6e31941d10e4819d290af41" alt="When the Sun Hits (Slowdive)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6325f361d7803ad0d908451" alt="Linger (The Cranberries)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27318f632fef2f6c380c8ba43f5" alt="High (Lighthouse Family)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733f43a6ff38258274802d6d6a" alt="Ladykillers (Lush)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27334ff27034756cba57c5d19a3" alt="Pure (The Lightning Seeds)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733521f8507d464f82ac50551d" alt="Ladykillers (Lush)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27351d999a5abe49d96ffd7280b" alt="The Riverboat Song (Ocean Colour Scene)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27351d999a5abe49d96ffd7280b" alt="The Day We Caught The Train (Ocean Colour Scene)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf94c56a92750b354c76b437" alt="The Concept (Teenage Fanclub)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273781ecbc78e1a5f7680eac5d9" alt="All You Good Good People (Embrace)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730137f8e79dc60001c2dc5b79" alt="Sit Down (James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27339180b45808493a1f687c91d" alt="Movin' on Up (Primal Scream)" width="64" height="64">

