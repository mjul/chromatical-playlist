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

### Top 1000 Greatest Songs of All Time
This playlist, https://open.spotify.com/playlist/7epfU4cGVZ1xHWQbQJl7km
Playlist ID: `7epfU4cGVZ1xHWQbQJl7km`

<img src="https://i.scdn.co/image/ab67616d0000b27321ebf49b3292c3f0f575f0f5" alt="Sweet Child O' Mine (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273eb11e2abccdca41f39ad3b89" alt="I'm Still Standing (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737c39dd133836c2c1c87e34d6" alt="Don't Stop Me Now - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27321ebf49b3292c3f0f575f0f5" alt="Welcome To The Jungle (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b694e89ba937dd2631ff584c" alt="Another Brick in the Wall, Pt. 2 (Pink Floyd)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27321ebf49b3292c3f0f575f0f5" alt="Paradise City (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735e25e034e25258b356774c79" alt="Smooth Operator - Single Version (Sade)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27363facc42e4a35eb3aa182b59" alt="Wannabe (Spice Girls)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730f51e29700232d57fe8a0830" alt="Big Poppa - 2005 Remaster (The Notorious B.I.G.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736ce61113662ecf693b605ee5" alt="She's Always a Woman (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732043dd3544a339547d04b436" alt="Roxanne (The Police)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b694e89ba937dd2631ff584c" alt="Comfortably Numb (Pink Floyd)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6954c1f074f66907a8c5483" alt="In The Air Tonight - 2015 Remastered (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739710731c9d7baec635f1bab1" alt="Nuthin' But A "G" Thang (Dr. Dre)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273828e52cfb7bf22869349799e" alt="Wish You Were Here (Pink Floyd)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27305a41288f037a08fb45db5e2" alt="(Everything I Do) I Do It For You (Bryan Adams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e3e3b64cea45265469d4cafa" alt="Yesterday - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735c1c4d3d94d0e845bd1ebec1" alt="Spirit In The Sky - Deluxe Edition (Norman Greenbaum)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7879980ef2ea7ac1cc29316" alt="Every Little Thing She Does Is Magic (The Police)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27337cd18af5725b9cad0a5ab53" alt="One (U2)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273795c9ba853f5a9f7a88b4e31" alt="Take Me Home, Country Roads - Original Version (John Denver)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730f51e29700232d57fe8a0830" alt="Juicy - 2005 Remaster (The Notorious B.I.G.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273be3d60f650c3b9dbad061f7f" alt="Butterfly (Crazy Town)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27375e6375e11550746705a9645" alt="Whiskey In The Jar (Metallica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6b9b62ea130943d371b69ef" alt="Regulate (Warren G)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d7db5abcbc899f3994c66fc6" alt="Last Kiss (Pearl Jam)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273605223665713cdf285ee0c81" alt="Smooth Criminal - 2012 Remaster (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273db687db0afb257abdee10816" alt="Blitzkrieg Bop - 2016 Remaster (Ramones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738c5b6f7dcdc5817dc5050b2a" alt="Born to Run (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737e0b5fe0454234229e52a491" alt="Buffalo Soldier (Bob Marley & The Wailers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734ad6e5838f15401ff7d62856" alt="I'll Be Missing You (feat. Faith Evans, 112) (Diddy)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d4c6dbc9a5b41cf6c4f6cd50" alt="You Sexy Thing (Hot Chocolate)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27389ac804ee51f66fe370c4577" alt="Romeo And Juliet (Dire Straits)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273eb11e2abccdca41f39ad3b89" alt="I Guess That's Why They Call It The Blues (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736ce61113662ecf693b605ee5" alt="Just the Way You Are (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ddd516e8d9114e683c69493d" alt="She's The One (Robbie Williams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d1d9453e70655e2e2c30da9d" alt="Make It with You (Bread)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273605223665713cdf285ee0c81" alt="The Way You Make Me Feel - 2012 Remaster (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ef255849780dca4ccb991cbe" alt="Hard to Say I'm Sorry / Get Away - 2006 Remaster (Chicago)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734ce8b4e42588bf18182a1ad2" alt="Ob-La-Di, Ob-La-Da - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273499c6d2eaeb941d76acdfe41" alt="Always on My Mind (Pet Shop Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273abc5193decc1a2984a93f31e" alt="I'm Coming Out (Diana Ross)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733540f5cb8e1e7a54125f84db" alt="West End Girls - 2018 Remaster (Pet Shop Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a1d9c9969f2a7ed27e449a3c" alt="Wild Horses - 2009 Mix (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273db0917ddd4139153bc1d1a1a" alt="Let's Dance - 2018 Remaster (David Bowie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734ce8b4e42588bf18182a1ad2" alt="While My Guitar Gently Weeps - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e3e3b64cea45265469d4cafa" alt="Help! - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bf6cc1130a676e73730f6311" alt="Gonna Make You Sweat (Everybody Dance Now) (feat. Freedom Williams) (C & C Music Factory)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273820d2376b2fb84aa99823903" alt="Only Wanna Be With You (Hootie & The Blowfish)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d109a35f286685993cf03050" alt="You Ain't Seen Nothing Yet (Bachman-Turner Overdrive)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27309133b648545410eeba21d0d" alt="Cry to Me (Solomon Burke)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27361a23657edb5d80fa18a630d" alt="Get It On (T. Rex)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736ce61113662ecf693b605ee5" alt="Movin' Out (Anthony's Song) (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fcd790ccf4508f067290b7c4" alt="Nikita (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27345546ed4af1a0d4c58a8ff50" alt="Mad World (Tears For Fears)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27389b56f56323925d57b38944d" alt="Ms. Fat Booty (Mos Def)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273abc5193decc1a2984a93f31e" alt="Upside Down (Diana Ross)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fba957f526936b65714b0ef6" alt="I Only Have Eyes for You (The Flamingos)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732043dd3544a339547d04b436" alt="So Lonely (The Police)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735124ed45a94033830b320500" alt="Spoonman (Soundgarden)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273db0917ddd4139153bc1d1a1a" alt="Modern Love - 2018 Remaster (David Bowie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ac19c6552524d207aac1277b" alt="She's Like the Wind (feat. Wendy Fraser) - From "Dirty Dancing" Soundtrack (Patrick Swayze)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273072ee11a51e23f861c54cef9" alt="I Wanna Be Sedated (Ramones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27331f17f2b636f0f1c8d83dc42" alt="It's a Sin - 2018 Remaster (Pet Shop Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cd404b5ae961b29d83f17c1f" alt="These Arms of Mine (Otis Redding)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736cfad72543b5cf95b5864146" alt="The Way It Is (Bruce Hornsby and the Range)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27396a1909790d3b6a986e2b971" alt="Moonlight Shadow (Mike Oldfield)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733a66d4b61d4422effce5c0b7" alt="Fame (Irene Cara)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273605223665713cdf285ee0c81" alt="Bad - 2012 Remaster (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a1f71f48201f450cb230e284" alt="Feel Me Flow (Naughty By Nature)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c84b9bd63074979108c7c752" alt="I Can't Go for That (No Can Do) (Daryl Hall & John Oates)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273195d2c01c72fc37c5bd58019" alt="Tears in Heaven - Acoustic Live (Eric Clapton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cfe4163cbb6d12f3ec15898e" alt="Maneater (Daryl Hall & John Oates)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fbc98da6995bb0a504ed363d" alt="Sugar Sugar (The Archies)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734500e13175a66153e053eacc" alt="Just Like Heaven - Remastered 2006 (The Cure)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27375fc0e961ba2028df4787966" alt="Top Of The World (Carpenters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273582d56ce20fe0146ffa0e5cf" alt="Hey Jude - Remastered 2015 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d5d55c3e0f45d6b9da1812d1" alt="Be My Lover (La Bouche)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273522088789d49e216d9818292" alt="All Along the Watchtower (Jimi Hendrix)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27346814e1b44e54d806753801e" alt="Come and Get Your Love - Single Version (Redbone)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734629fe1633a7d9460fe1e28b" alt="For Once In My Life (Stevie Wonder)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aac099da610b063763c63117" alt="These Dreams (Heart)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732847f04f9de392e290b5a0be" alt="Maria (Blondie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730c12ef918102b8d303dc9e9b" alt="Semi-Charmed Life (Third Eye Blind)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730c12ef918102b8d303dc9e9b" alt="Jumper - 1998 Edit (Third Eye Blind)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273db5d336c648e8f540262a1c2" alt="Back for Good - Radio Mix (Take That)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733260aeb9dbc740c568a86017" alt="You Don't Love Me (No, No, No) - Extended Mix (Dawn Penn)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e71708b667804f6241dd1a59" alt="Psycho Killer - 2005 Remaster (Talking Heads)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27388ffe8c41647856e6fa5e1ab" alt="Just Can't Get Enough (Depeche Mode)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f66d92378b233aa8253e71d2" alt="We Are Family - 1995 Remaster (Sister Sledge)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27306e00756085191abc01e4cf0" alt="Our House (Crosby, Stills, Nash & Young)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734637341b9f507521afa9a778" alt="Hotel California - 2013 Remaster (Eagles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734637341b9f507521afa9a778" alt="Life in the Fast Lane - 2013 Remaster (Eagles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730cb0884829c5503b2e242541" alt="Like a Rolling Stone (Bob Dylan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734acaf50f8a03a6972b555d7e" alt="When You Say Nothing At All (Ronan Keating)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735d0a8e54aba5181c79593b94" alt="One of These Nights - 2013 Remaster (Eagles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dc60cf9a010f86354e6735dd" alt="Right Down the Line (Gerry Rafferty)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dc60cf9a010f86354e6735dd" alt="Baker Street (Gerry Rafferty)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735d0a8e54aba5181c79593b94" alt="Lyin' Eyes - 2013 Remaster (Eagles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fde79b88e2a659c394c5ae30" alt="Hypnotize - 2014 Remaster (The Notorious B.I.G.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730085dd4362653ef4c54ebbeb" alt="American Pie (Don McLean)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fde79b88e2a659c394c5ae30" alt="Mo Money Mo Problems (feat. Puff Daddy & Mase) - 2014 Remaster (The Notorious B.I.G.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730085dd4362653ef4c54ebbeb" alt="Vincent (Don McLean)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739c72b249fcaa04d074c1dfcd" alt="Friday I'm In Love (The Cure)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735893643e11d44e3ef569479c" alt="Dirty Cash (Money Talks) - Sold Out 7 Inch Mix (The Adventures Of Stevie V)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730faf2fc17446651865ce2282" alt="September (Earth, Wind & Fire)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7a9a6a2bf311630d3fc6956" alt="Faith - Remastered (George Michael)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7a9a6a2bf311630d3fc6956" alt="Father Figure - Remastered (George Michael)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737a26b62978e61d5068164a63" alt="It Never Rains in Southern California (Albert Hammond)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730c8a01bf197adb9859044775" alt="When a Man Loves a Woman (Percy Sledge)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f454aa96e81265bc61b8d4ed" alt="Show Me Love (Robin S)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733992c7ab57975935b29fa22b" alt="Riders on the Storm (The Doors)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731be40e44db112e123e5e8b51" alt="Carry on Wayward Son (Kansas)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f12a8a7e0b2cbe16d2bef4dc" alt="Roadhouse Blues (The Doors)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738c1fadcc997a65384f34d694" alt="More Than a Feeling (Boston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27301841d493ec3808242042c0f" alt="Return of the Mack (Mark Morrison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27392d0747a634fcc351c6ac3c2" alt="Mamma Mia (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27392d0747a634fcc351c6ac3c2" alt="SOS (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273920f421260033ee54865d673" alt="We Are The World (U.S.A. For Africa)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ec7e2c5c7ecd29301f1c4b93" alt="Born To Be Wild (Steppenwolf)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27342678f54dfd1d5afb3eea19a" alt="Slipping Through My Fingers (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cbea7e7a20a9df4b22dc5148" alt="Love Is All Around - From "Four Weddings And A Funeral" (Wet Wet Wet)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734936b5b7caeb7524e50fd8cb" alt="Crazy Train (Ozzy Osbourne)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f93159d78849714fcf118bb3" alt="The Things We Do For Love (10cc)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731581237e4d580feafaed6bc0" alt="Glycerine - Remastered (Bush)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a90317b8d96c0b3f5e9c5e3d" alt="Push It (Salt-N-Pepa)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273224985553276e439be6640e3" alt="Have You Ever Really Loved A Woman? - From "Don Juan DeMarco" Soundtrack (Bryan Adams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273edc27582d8f5c3a7c56893bf" alt="Right Here Waiting (Richard Marx)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bf4cf0f48b94d0c8297b751a" alt="Remember the Time (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bf4cf0f48b94d0c8297b751a" alt="Heal the World (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bf4cf0f48b94d0c8297b751a" alt="Black or White (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738fd7eec31ed567629f4ab420" alt="If You Could Read My Mind (Gordon Lightfoot)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27399d424b0873a9a714279a9f3" alt="Like a Virgin (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739824c6e084b02d24b2e22e94" alt="Break My Stride (Matthew Wilder)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27320bbceac6950d3fe13fa13c3" alt="The Weight - Remastered 2000 (The Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733efcd243aaa5638f55318f91" alt="Bad Moon Rising (Creedence Clearwater Revival)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733efcd243aaa5638f55318f91" alt="Green River (Creedence Clearwater Revival)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733efcd243aaa5638f55318f91" alt="Lodi (Creedence Clearwater Revival)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737649604d1b27be1c78c466e9" alt="I'd Rather Go Blind (Etta James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738cffbbb7fe8645a486a85ea9" alt="Walk This Way (Aerosmith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738cffbbb7fe8645a486a85ea9" alt="Sweet Emotion (Aerosmith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b67dbb84e0c1f82be886c8ea" alt="Laid (James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cdc24a5f5664e9e4707ac313" alt="Livin' Thing (Electric Light Orchestra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cd7530409d09802935c840f9" alt="Unchained Melody (The Righteous Brothers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27366e2e0df78c4ec35a8ed20a0" alt="Barracuda (Heart)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c694da863eeeae3149c5c590" alt="Thank U (Alanis Morissette)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737db048b350136b3116ad02d4" alt="Name (The Goo Goo Dolls)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ec4d79e8035ed2803ecfe2b3" alt="Santa Monica (Everclear)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273733af86f8dea9692a3f59d29" alt="Who Am I (What’s My Name)? (Snoop Dogg)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27370f7a1b35d5165c85b95a0e0" alt="Dancing Queen (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27370f7a1b35d5165c85b95a0e0" alt="Money, Money, Money (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27370f7a1b35d5165c85b95a0e0" alt="Fernando (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27370f7a1b35d5165c85b95a0e0" alt="Knowing Me, Knowing You (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733f29a976eea00141514ab936" alt="Brown Eyed Girl (Van Morrison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f71eccd0b0f8b7d4f19a6b26" alt="You Can Do Magic (America)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ad22c83a6e1567f8453c32b3" alt="Rebel Rebel - 2016 Remaster (David Bowie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27391b51fa9b5967fb34c044498" alt="Listen to the Music (The Doobie Brothers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739015296f9afabfc102989521" alt="How Will I Know (Whitney Houston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739015296f9afabfc102989521" alt="Saving All My Love for You (Whitney Houston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739015296f9afabfc102989521" alt="Greatest Love of All (Whitney Houston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273be1421122cef4940f500ac06" alt="Brother Louie (Modern Talking)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273edbbd1e4dde99597ce850c54" alt="True Colors (Cyndi Lauper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27351f311c2fb06ad2789e3ff91" alt="Have You Ever Seen The Rain (Creedence Clearwater Revival)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a5ce236c22035a02cf87d4de" alt="Stuck In The Middle With You (Stealers Wheel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733ae63e3e2d9da8366e33fdab" alt="Waterfalls (TLC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a47127db3e929f64a2795666" alt="Endless Love (Lionel Richie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27371d840defb002ed3b180f7cd" alt="N.Y. State of Mind (Nas)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732fee61bfec596bb6f5447c50" alt="Sir Duke (Stevie Wonder)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ab3b105e28a0d26df5be8d16" alt="A Horse with No Name (America)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273668e3aca3167e6e569a9aa20" alt="Master Of Puppets (Metallica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736e3d3c964df32136fb1cd594" alt="Don't Let Me Down - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27315aa25b0b3b972a7be623605" alt="All My Love - Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732ff76b4da68f018b4735ee59" alt="Flashdance...What a Feeling - Radio Edit (Irene Cara)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e08b1250db5f75643f1508c9" alt="Doo Wop (That Thing) (Ms. Lauryn Hill)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e08b1250db5f75643f1508c9" alt="Ex-Factor (Ms. Lauryn Hill)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dfce70698f4d925525383c7c" alt="Dirty Deeds Done Dirt Cheap (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732d1447994ec24301429681cb" alt="Would? (2022 Remaster) (Alice In Chains)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732d1447994ec24301429681cb" alt="Rooster (2022 Remaster) (Alice In Chains)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732d1447994ec24301429681cb" alt="Down In A Hole (2022 Remaster) (Alice In Chains)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732a1ffd75bb148e58ce2a6cac" alt="Moondance - 2013 Remaster (Van Morrison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27394d08ab63e57b0cae74e8595" alt="Californication (Red Hot Chili Peppers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27394d08ab63e57b0cae74e8595" alt="Scar Tissue (Red Hot Chili Peppers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27394d08ab63e57b0cae74e8595" alt="Otherside (Red Hot Chili Peppers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27394d08ab63e57b0cae74e8595" alt="Around the World (Red Hot Chili Peppers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27308181b9f840a06e7a071cf72" alt="California Dreamin' - Single Version (The Mamas & The Papas)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27371d840defb002ed3b180f7cd" alt="The World Is Yours (Nas)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fb1bc65edf4717e75fbc70ab" alt="Don't Stand So Close To Me (The Police)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273835ed5fb9b70f46c3177ffde" alt="Isn't She Lovely (Stevie Wonder)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738ccc17f29764d812062204a8" alt="Bette Davis Eyes (Kim Carnes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27374fad40214d982351347e46e" alt="Drive (Incubus)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fb2daafa0993f39d87a84385" alt="Another Day in Paradise - 2016 Remaster (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bfc19627a4a3a604c0a195e5" alt="It Ain't Over 'Til It's Over (Lenny Kravitz)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bd0c47e4cfb4ee327e53bc73" alt="You Spin Me Round (Like a Record) (Dead Or Alive)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736c52084ed1f1748f213783b3" alt="Learn to Fly (Foo Fighters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273275b7ffe49eb84ab13a71980" alt="Patience (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ed1e6f4480313f95ac380159" alt="Give It Up (KC & The Sunshine Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27301d93acc198ee0f9154b5b1c" alt="Talking In Your Sleep (2023 Remaster) (The Romantics)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fb2daafa0993f39d87a84385" alt="I Wish It Would Rain Down - 2016 Remaster (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d9e06f988048ecf3c54ca749" alt="End Of The Line (Traveling Wilburys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737e0dea0c3a0bf7c6820306c9" alt="Sara Smile (Daryl Hall & John Oates)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733718df75b57340c1947747e8" alt="Say My Name (Destiny's Child)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733718df75b57340c1947747e8" alt="Jumpin', Jumpin' (Destiny's Child)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733718df75b57340c1947747e8" alt="Bills, Bills, Bills (Destiny's Child)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d7720a6a8b713b833313f396" alt="I've Got You Under My Skin - Remastered 1998 (Frank Sinatra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b28344e9f8f359a95aa9cfe6" alt="I'd Really Love to See You Tonight (England Dan & John Ford Coley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f1dd69d7399290cc25324706" alt="Red Red Wine (UB40)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f20825485137abccd82b9665" alt="Maggie May (Rod Stewart)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27391b246743456e285a20a46ed" alt="Crazy (Aerosmith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27391b246743456e285a20a46ed" alt="Cryin' (Aerosmith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27377073761e43f273c60988eaf" alt="Everything I Own (Bread)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27377073761e43f273c60988eaf" alt="Baby I'm-a Want You (Bread)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735e9ba297f543a91ae5209ce8" alt="When You're Gone (Bryan Adams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dbeec63ad914c973e75c24df" alt="Twist And Shout - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dbeec63ad914c973e75c24df" alt="Love Me Do - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27327bd7d234a31296df34b9a64" alt="Learning To Fly (Tom Petty and the Heartbreakers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737723fdc89d8e25e65aa6730d" alt="We Belong Together (Ritchie Valens)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ede118b5f0e159dd18d42b90" alt="Runaway (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273943fe2781dd19bf510f71340" alt="Hurricane (Bob Dylan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730e42d457a15ef2f133976f6b" alt="There She Goes (The La's)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27344e53f6377a1e99e13779af9" alt="Rock with You - Single Version (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27344e53f6377a1e99e13779af9" alt="Don't Stop 'Til You Get Enough (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735058a0aebf5365a911030083" alt="Me and Julio Down by the Schoolyard (Paul Simon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731de27f12958ceb8b1f65461a" alt="If You Leave Me Now (Chicago)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273509342e69eb341df70e5c2e3" alt="No More Tears (Ozzy Osbourne)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735bc7429f54c5f6745c225fc6" alt="Un-Break My Heart (Toni Braxton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27319dcd95d28b63d10164327f2" alt="Little Wing (Jimi Hendrix)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27373d0d8625dcf1e48043cfbf9" alt="End Of The Road (Boyz II Men)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733cd67ccf241ae843f6da62f3" alt="Waiting for a Girl like You (Foreigner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734ba1fe238a517021ebcc2ace" alt="Can I Kick It? (A Tribe Called Quest)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273886d823ecbfcbe661a6b0ab9" alt="If I Ruled the World (Imagine That) (feat. Lauryn Hill) (Nas)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c5a010463c2b450902e57599" alt="Best of My Love (The Emotions)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f89996e214be1763b2a9e948" alt="Genie In a Bottle (Christina Aguilera)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ed3953f8af1f764a146b7583" alt="Heaven Knows I'm Miserable Now - 2011 Remaster (The Smiths)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27349c982dae436bac27c336f45" alt="Tainted Love (Soft Cell)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f64b9ea8a8a409c6af86134f" alt="Ain't No Sunshine (Bill Withers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aaf012d56b8c72658da6c45f" alt="Man! I Feel Like A Woman! (Shania Twain)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aaf012d56b8c72658da6c45f" alt="You're Still The One (Shania Twain)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736c17415a134732f752b36922" alt="I Keep Forgettin' (Every Time You're Near) (Michael McDonald)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273880fc46436bd0a7134c6ffbc" alt="Coco Jamboo (Mr. President)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27398ed501c6a838b2244ebaf75" alt="My All (Mariah Carey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a496dc8c33ca6d10668b3157" alt="Johnny B. Goode (Chuck Berry)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fdff0e4ec273827627487f39" alt="What It's Like (Everlast)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273facf92d793609aa3bc5cc4e7" alt="Is This Love - 2018 Remaster (Whitesnake)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273facf92d793609aa3bc5cc4e7" alt="Here I Go Again - 2018 Remaster (Whitesnake)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e464904cc3fed2b40fc55120" alt="Life on Mars? - 2015 Remaster (David Bowie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e464904cc3fed2b40fc55120" alt="Changes - 2015 Remaster (David Bowie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731b83255ef342451b977987aa" alt="Hit Me With Your Best Shot (Pat Benatar)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27336572e6726714544f5bed456" alt="Free Fallin' (Tom Petty)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27336572e6726714544f5bed456" alt="I Won't Back Down (Tom Petty)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27319db9ac54c80a898a179f0f1" alt="Danger Zone - From "Top Gun" Original Soundtrack (Kenny Loggins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27319db9ac54c80a898a179f0f1" alt="Footloose (Kenny Loggins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734f3004f43ea41a8ee1510035" alt="Gloria (Laura Branigan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f106d873a30a31efa73f4e74" alt="Renegade (Styx)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27328fc1c4ca395c4a2ffa31a47" alt="Kingston Town (UB40)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735be5f807f6f0549e198a44b4" alt="Radio Ga Ga - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d3e47e52f8f218c9ba12b8eb" alt="I'm Not In Love (10cc)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735be5f807f6f0549e198a44b4" alt="I Want To Break Free - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d81a092eb373ded457d94eec" alt="California Love - Original Version (2Pac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d81a092eb373ded457d94eec" alt="Changes (2Pac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b478a8ce3aac61a3675aac2a" alt="All I Wanna Do (Sheryl Crow)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bc161bb58763f72fc71a3a01" alt="Killing Me Softly With His Song (Roberta Flack)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739293c743fa542094336c5e12" alt="High and Dry (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739293c743fa542094336c5e12" alt="Just (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c0fa62ae53b2aeae3766f13d" alt="I Can't Help Myself (Sugar Pie, Honey Bunch) (Four Tops)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27372d481a5999197ef5f42f796" alt="Zombie (The Cranberries)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27372d481a5999197ef5f42f796" alt="Ode To My Family (The Cranberries)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27352cbfb62c42adc19d5637843" alt="Jailhouse Rock (Elvis Presley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734d08fc99eff4ed52dfce91fa" alt="Lay All Your Love On Me (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734d08fc99eff4ed52dfce91fa" alt="The Winner Takes It All (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273749e9bfa78277f30ad2c9a9c" alt="Fantasy (Mariah Carey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27359bfe048568a969c6f0bd08c" alt="Bed Of Roses (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734d08fc99eff4ed52dfce91fa" alt="Super Trouper (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273def7146ca744f3b1bf838404" alt="My Heart Will Go On - Love Theme from "Titanic" (Céline Dion)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273375445cc7a2aedff11361b51" alt="The Joker (Steve Miller Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27363e07c2dbc7450974a146e96" alt="The Power of Love (Céline Dion)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273749e9bfa78277f30ad2c9a9c" alt="Always Be My Baby (Mariah Carey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c7972702cff224328b39f8a6" alt="More Than This (Roxy Music)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273749e9bfa78277f30ad2c9a9c" alt="One Sweet Day (Mariah Carey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27395788c15edfdca94ad6fa6ab" alt="Great Balls Of Fire (Jerry Lee Lewis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730e51dd1d3dc50fc541942c7c" alt="The Boy Is Mine (Brandy)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b9c4979446c4d39bc08e9503" alt="Forever Young (Alphaville)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b9c4979446c4d39bc08e9503" alt="Big in Japan (Alphaville)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27349cb2d53994caada391cf39e" alt="9 to 5 (Dolly Parton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cfccabf39d00d34235d5bcd6" alt="Broken Wings (Mr. Mister)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fa3c4374e2cdd3cc1636c79b" alt="Angie - Remastered 2009 (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27382d43c836792c8b41dc0ad8c" alt="Freed From Desire (Gala)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733a9106f940fb04bc98a2b95e" alt="Making Love Out of Nothing at All (Air Supply)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27337d1e5c1ca98ce1ecd754d04" alt="Sex & Candy (Marcy Playground)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a1fc113a6858d0824d9aaf38" alt="Let's Stay Together (Al Green)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733c16761584c4015495bdda87" alt="Annie's Song (John Denver)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27337c9e9907888dea39387df7c" alt="It's Not Unusual (Tom Jones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734121faee8df82c526cbab2be" alt="Thriller (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730158cbde70672dd821972907" alt="Self Esteem (The Offspring)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730158cbde70672dd821972907" alt="Come Out and Play (The Offspring)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27390b8a540137ee2a718a369f9" alt="Fast Car (Tracy Chapman)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27390b8a540137ee2a718a369f9" alt="Baby Can I Hold You (Tracy Chapman)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735ef700b0fb079793f8b0d774" alt="My Favourite Game (The Cardigans)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734650ca0a8f88129d4667acc5" alt="I'm So Excited (The Pointer Sisters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b8a740229a85f3719d4a4c25" alt="How Do I Live (LeAnn Rimes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b298efc29df3b69ec3f0d675" alt="Be My Baby (The Ronettes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273983bb3e3f0c66b9b89a832fa" alt="Video Killed The Radio Star (The Buggles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27380aa6a82fce614eea8357253" alt="My Way (Frank Sinatra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27395838aa2462ce2b9933e2087" alt="Candy Rain (Soul For Real)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273542d87e4d1512bf7facb3860" alt="Are You Gonna Go My Way (Lenny Kravitz)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730ddd7e736f870994f4707947" alt="Do It Again (Steely Dan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730ddd7e736f870994f4707947" alt="Reelin' In The Years (Steely Dan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dafd1cd6e9537ec8463ea691" alt="Daddy Cool (Boney M.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dafd1cd6e9537ec8463ea691" alt="Sunny (Boney M.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27377df2aceaf90f06a20b56b14" alt="Pride (In The Name Of Love) - Remastered 2009 (U2)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bd3cf0e884569cd4048cbe37" alt="Ventura Highway (America)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730ef24611a73e7be48f6c2802" alt="Cold as Ice (Foreigner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273de114203356c1f7b136960b6" alt="Song 2 - 2012 Remaster (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734742af6d5c9eae5f7f63ee5e" alt="Words - Original Version 1983 (F.R. David)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739f8872d948b2f5ec7b7c830b" alt="Let's Get Loud (Jennifer Lopez)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734e492e787ed64de43c3a3a21" alt="Freak On a Leash (Korn)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732ec4aea38b44eba9756767fa" alt="Smalltown Boy (Bronski Beat)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27359f0f56a7cd13526b5b4204c" alt="Dust in the Wind (Kansas)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735405ef9e393f5f1e53b4b42e" alt="The Logical Song - Remastered 2010 (Supertramp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735405ef9e393f5f1e53b4b42e" alt="Breakfast In America - Remastered 2010 (Supertramp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735405ef9e393f5f1e53b4b42e" alt="Goodbye Stranger - Remastered 2010 (Supertramp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738e8c08ca2feb999bb84f05e6" alt="Crazy On You (Heart)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cfc5eea6cfd77e89ed3ac5a4" alt="Kiss Me (Sixpence None The Richer)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a48cc02c718f9ab73709fbfb" alt="I Swear (All-4-One)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f72f1e38e9bd48f18a17ed9b" alt="Goodbye Yellow Brick Road - Remastered 2014 (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f72f1e38e9bd48f18a17ed9b" alt="Bennie And The Jets - Remastered 2014 (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f72f1e38e9bd48f18a17ed9b" alt="Candle In The Wind - Remastered 2014 (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f72f1e38e9bd48f18a17ed9b" alt="Saturday Night’s Alright (For Fighting) - Remastered 2014 (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27307d3de253ec02c26c04b95f1" alt="Venus (Bananarama)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739330b3ab457779ed4137493b" alt="Keep Their Heads Ringin' (Dr. Dre)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ab243ed96c6518acc60f9b1b" alt="Islands in the Stream (Dolly Parton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734aa5f679427e35409a06f225" alt="The Passenger (Iggy Pop)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738833534681a0a01c668c4115" alt="Cotton Eye Joe (Rednex)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e7248738c2f7ce3b5584b15d" alt="Wild World (Yusuf / Cat Stevens)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b2229a8fdf377abaf3652624" alt="At Last (Etta James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736f093a6ae88a5ca8ed53b9f7" alt="Wonderful Tonight (Eric Clapton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ed804121889655ca03722024" alt="If (Bread)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273280b72ca76b4734debfc190e" alt="Should I Stay or Should I Go - Remastered (The Clash)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273280b72ca76b4734debfc190e" alt="Rock the Casbah - Remastered (The Clash)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27311394cad51642144dc4014b3" alt="Boombastic (Shaggy)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d828b182ee9b7193a0f8b5d6" alt="Into the Mystic - 2013 Remaster (Van Morrison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273753c41c7fdc5e78ba017bbf5" alt="All Right Now (Free)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733009007708ab5134936a58b3" alt="Rocket Man (I Think It's Going To Be A Long, Long Time) (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273381371cb8ce680d0dc324600" alt="What's Up? (4 Non Blondes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273280b04817e7547fea8cfb7d0" alt="Roots, Rock, Reggae (Bob Marley & The Wailers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27311c24dc7f5ef909381c0a7d6" alt="Waterloo (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739173e50e99bdea2400222f02" alt="Ain't No Mountain High Enough (Marvin Gaye)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736c86683d20c72e3874c11c6d" alt="Knockin' On Heaven's Door (Bob Dylan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737d12d6d8dcffd1594123b3bd" alt="Brandy (You're a Fine Girl) (Looking Glass)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f9a205a1a377506ff51b1a25" alt="If You Could Only See (Tonic)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273919c02d20d8634f96ccd75ae" alt="Nothing Compares 2 U (Sinéad O'Connor)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27372649ad8e79d1e8bdd54c929" alt="Happy Together (The Turtles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273192f3a588427f2cbf8365506" alt="You're the Inspiration - 2006 Remaster (Chicago)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735f4604aff952dc7b0a8e511e" alt="The Letter (The Box Tops)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27391f442ef24b8410ec1e68003" alt="Pump Up The Jam (Technotronic)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27305eb9ae04c8a69ef2371189b" alt="Midnight Train to Georgia (Gladys Knight & The Pips)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ec548c00d3ac2f10be73366d" alt="Creep (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737b1489e71cadf8a1c0382d7d" alt="You'll Be In My Heart - From "Tarzan"/Soundtrack Version (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27378cc1b7af3f28ab51ea81266" alt="Don't Leave Me This Way (with Sarah Jane Morris) (The Communards)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730546a184cc17e30acc8dce49" alt="Burnin' for You (Blue Öyster Cult)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273441084621edb7c53ef303090" alt="One More Night - 2016 Remaster (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e20037311210924b3c386f00" alt="Son Of A Preacher Man (Dusty Springfield)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a7ea08ab3914c5fb2084a8ac" alt="No Sleep Till Brooklyn (Beastie Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a7ea08ab3914c5fb2084a8ac" alt="Fight For Your Right (Beastie Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273053f006079bce979e5fef1e1" alt="Bulls On Parade (Rage Against The Machine)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735590b4ee88187cb06a5b102d" alt="Soul to Squeeze (Red Hot Chili Peppers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736b44fa8f5415cc4c945117be" alt="Like a Prayer (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736b44fa8f5415cc4c945117be" alt="Material Girl (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736b44fa8f5415cc4c945117be" alt="Vogue (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273204f41d52743c6a9efd62985" alt=""Heroes" - 2017 Remaster (David Bowie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735908f448fb4605e4eba3dbf9" alt="Walking in Memphis (Marc Cohn)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738c7f355d649e0a3cfcf6fc39" alt="T.N.T. (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738c7f355d649e0a3cfcf6fc39" alt="It's a Long Way to the Top (If You Wanna Rock 'N' Roll) (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732af30c881bb23cfb82a8cf99" alt="Gimme Shelter (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f081c7a1a21fb8f983a9d3cb" alt="50 Ways to Leave Your Lover (Paul Simon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736e955099e6d2225059595b9e" alt="All My Life (K-Ci & JoJo)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fc7df879208b362bb1ce1499" alt="Interstate Love Song - 2019 Remaster (Stone Temple Pilots)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b75cedd9435250e77b60bfbe" alt="The Times They Are A-Changin' (Bob Dylan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f8f048a5f4749c970078a4fb" alt="Higher (Creed)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b4e4e7ee52c6fc8be77d8a33" alt="Nothin' But A Good Time - Remastered 2006 (Poison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dfdedd4553b40bbaab342dae" alt="You Get What You Give (New Radicals)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737e09670f90cd47b3fb9a23e0" alt="Mr. Jones (Counting Crows)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27317e1907923e91181f38290ac" alt="Sweet Home Alabama (Lynyrd Skynyrd)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273617f78eb4389bb0a7d27719a" alt="Something's Got A Hold On Me (Etta James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e5855edffddef46b7feff49b" alt="You Can Call Me Al (Paul Simon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27399ee23dac7128cb5754f593c" alt="Caribbean Queen (No More Love On the Run) (Billy Ocean)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27346c31f64babcbfca6e061b6b" alt="I Say a Little Prayer (Aretha Franklin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fc4f17340773c6c3579fea0d" alt="Whole Lotta Love - 1990 Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fc4f17340773c6c3579fea0d" alt="Ramble On - 1990 Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e44963b8bb127552ac761873" alt="November Rain (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e44963b8bb127552ac761873" alt="Don't Cry (Original) (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e44963b8bb127552ac761873" alt="Live And Let Die (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733e5cbf3b3ac5905cb68377d5" alt="Thank You (Dido)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273860a3b044d1715635ad2bad7" alt="Runaround Sue (Dion)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733e5cbf3b3ac5905cb68377d5" alt="Here With Me (Dido)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737c05e69390ab7c628a83cee7" alt="One (Metallica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736f2f499c1df1f210c9b34b32" alt="Good Times Bad Times - 1993 Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c5634c0532097e175199f07e" alt="Kokomo (The Beach Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731af9e8390e2d251b916d9185" alt="You're So Vain (Carly Simon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731f7077ae1018b5fbab08dfa8" alt="We Will Rock You - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731f7077ae1018b5fbab08dfa8" alt="We Are The Champions - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731c40418d1c37d727e8e91b04" alt="Could You Be Loved (Bob Marley & The Wailers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731c40418d1c37d727e8e91b04" alt="Redemption Song (Bob Marley & The Wailers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e9c361da971c6e81b51ef06b" alt="What's Love Got to Do with It (Tina Turner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273da6790936a48b6719083dcac" alt="We Built This City (Starship)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27323d8d82a798baa960fdb5070" alt="Lightning Crashes (Live)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dbf223dbb6abdffa642eb287" alt="YMCA - Original Version 1978 (Village People)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c3271cf84b2d68263ac5e00d" alt="So Anxious (Ginuwine)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273220f3b1f40e3276662155f16" alt="Jolene (Dolly Parton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27377958c617ea2cb4462db1193" alt="Oh, Pretty Woman (Roy Orbison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aca059cebc1841277db22d1c" alt="Heart-Shaped Box (Nirvana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27316aaf05fe82237576a7d0e38" alt="I Want You Back (The Jackson 5)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27357f7dd6fabcebff379e14a0e" alt="Can't Help Falling in Love (Elvis Presley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732dae35818253ccb1cd0cd87d" alt="Black Betty (Ram Jam)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27390a50cfe99a4c19ff3cbfbdb" alt="Immigrant Song - Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e52a59a28efa4773dd2bfe1b" alt="Dreams - 2004 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e52a59a28efa4773dd2bfe1b" alt="The Chain - 2004 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27357df7ce0eac715cf70e519a7" alt="Go Your Own Way - 2004 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27357df7ce0eac715cf70e519a7" alt="Don't Stop - 2004 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27357df7ce0eac715cf70e519a7" alt="You Make Loving Fun - 2004 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dc0b5f94d9ee21d0eb209d81" alt="Let Your Love Flow (The Bellamy Brothers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273360a1ae790aa71a0aac4983e" alt="I'm a Believer - 2006 Remaster (The Monkees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ee65bbd54f993b5f01d5c511" alt="No Ordinary Love (Sade)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273038f8fad2f75b637f1c9aef5" alt="Breakfast At Tiffany's (Deep Blue Something)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c9adfbd773852e286faed040" alt="Purple Haze (Jimi Hendrix)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c9adfbd773852e286faed040" alt="Hey Joe (Jimi Hendrix)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa5e4c9da271951ac0b31fa2" alt="Who Can It Be Now? (Men At Work)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa5e4c9da271951ac0b31fa2" alt="Down Under (Men At Work)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e2dd4e821bcc3f70dc0c8ffd" alt="Losing My Religion (R.E.M.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e2dd4e821bcc3f70dc0c8ffd" alt="Shiny Happy People (R.E.M.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27344934a06d21864415376f5f2" alt="Sympathy For The Devil - 50th Anniversary Edition (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27319b9fae8d9f602068a5a5557" alt="Hold On, I'm Comin' (Sam & Dave)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27343058ea096fa35ac33c43587" alt="Highway to Hell (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739f39192f9f8ca1c90847b3e5" alt="Fortunate Son (Creedence Clearwater Revival)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7bea3d01f04e6d0408d2afe" alt="With Or Without You (U2)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a2fc41b0dd6ce4f0d16a4c46" alt="Wake Me Up Before You Go-Go (Wham!)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7bea3d01f04e6d0408d2afe" alt="I Still Haven't Found What I'm Looking For (U2)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735579d8a505c727349a203074" alt="Don't You Want Me (The Human League)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e67cbc6061edcdaa6f0cf570" alt="Mrs. Robinson - From "The Graduate" Soundtrack (Simon & Garfunkel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735f66fbeaff0725997250591c" alt="Always (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731813ea8f590a0aab2820f922" alt="Stand By Me (Ben E. King)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736f705bef76c1d861c4d51d8c" alt="Take A Chance On Me (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731afccd261170f1d8f3cadb3d" alt="Proud Mary (Creedence Clearwater Revival)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fe5213edd4f8550a8030efcf" alt="Walk On the Wild Side (Lou Reed)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27331edc5bd8f156b173015ed19" alt="Streets of Philadelphia - Single Edit (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739f39192f9f8ca1c90847b3e5" alt="Down On The Corner (Creedence Clearwater Revival)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27395127975447a26eb7e31668b" alt="Save Tonight (Eagle-Eye Cherry)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d0c7c131a979c9e5436f89ce" alt="Englishman In New York (Sting)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b17d34882944eaf0695153f2" alt="Where Is My Mind? (Pixies)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273275774501f737e10d92adaca" alt="Relax (Come Fighting) (Frankie Goes To Hollywood)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737efa4d4536799483c489a4b0" alt="Up Where We Belong - From "An Officer And A Gentleman" (Joe Cocker)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738ea9b0b865a4977021ff9566" alt="If Ever You're in My Arms Again (Peabo Bryson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735e7464d9d8a25b2bf74b782a" alt="Cocaine (Eric Clapton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27338b2429ef948e6ca8d3ab599" alt="Centerfold (The J. Geils Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273be7a3a1e2d663eea2918e5a3" alt="Band On The Run - 2010 Remaster (Paul McCartney)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736e7cb1429534f0d21133b714" alt="Bamboléo (Gipsy Kings)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7bea3d01f04e6d0408d2afe" alt="Where The Streets Have No Name - Remastered (U2)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e45161990e83649071399525" alt="Photograph (Def Leppard)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a2fc41b0dd6ce4f0d16a4c46" alt="Everything She Wants (Wham!)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f74c4e155d96ffed4b759b59" alt="The Whole of the Moon - 2004 Remaster (The Waterboys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bdbb936aeda188debe62e187" alt="A Groovy Kind of Love (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27351893e443844361a44675df4" alt="A Girl Like You (Edwyn Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734fca44463bbcbcde7676acfd" alt="Saturday Night - Radio Mix (Whigfield)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273afb055fcddab0300b316b54a" alt="Hit the Road Jack (Ray Charles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730ccbe4584f7827e66fa2ab3a" alt="Better Man (Pearl Jam)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bdbb936aeda188debe62e187" alt="Two Hearts (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731afccd261170f1d8f3cadb3d" alt="Born On The Bayou (Creedence Clearwater Revival)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b815265c56ecfa5136a4015d" alt="Can't Fight This Feeling (REO Speedwagon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b49d49cc95564aede7998bb8" alt="Sultans Of Swing (Dire Straits)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732deb62442d38d6e6fff5efa8" alt="Black Velvet (Alannah Myles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27323cc0f0a925845a3de4aca38" alt="Kiss (Prince)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273707d13d3f87652e737e94d45" alt="Bitter Sweet Symphony - Remastered 2016 (The Verve)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736c6610322fc60bfb41481273" alt="My Sweet Lord - 2014 Remaster (George Harrison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273813da91820fd194cbee5bdce" alt="Gypsy (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e7e9b85cc1f021ec12130d80" alt="Livin' la Vida Loca (Ricky Martin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dabd5d51c868054fed2d6d68" alt="All Out of Love (Air Supply)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dabd5d51c868054fed2d6d68" alt="Lost In Love (Air Supply)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735a0fca95bfacb33ca3580a29" alt="Sacrifice (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273da4f6706ae0f2501c61ce776" alt="Good Riddance (Time of Your Life) (Green Day)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273af1bb86907b4457c4e83390f" alt="Woman in Love (Barbra Streisand)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273242e643ea07118ecf677a6ef" alt="Ironic - 2015 Remaster (Alanis Morissette)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273242e643ea07118ecf677a6ef" alt="You Oughta Know - 2015 Remaster (Alanis Morissette)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732b25c31d78b73d003e1b2d6d" alt="Straight From The Heart (Bryan Adams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730ab3c2a306c614fae36ff1d6" alt="Here Comes Your Man (Pixies)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730f284f5845974aa71ebc395d" alt="Morning Has Broken - Remastered 2021 (Yusuf / Cat Stevens)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734384b6976cadaec272114022" alt="I Was Made For Lovin' You (KISS)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f607580794ed5b352884fd47" alt="Drive - 2017 Remaster (The Cars)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735c29a88ba5341ca428f0c322" alt="Run to the Hills - 2015 Remaster (Iron Maiden)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735c29a88ba5341ca428f0c322" alt="The Number of the Beast - 2015 Remaster (Iron Maiden)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27393e3fc20b2818c4ab7d5dc29" alt="Under the Boardwalk (The Drifters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732fcb0a3c7a66e516b11cd26e" alt="Teardrop (Massive Attack)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27346007ceff2f1c33c9b9ec19c" alt="Green Onions (Booker T. & the M.G.'s)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e962eb03beb3507c3c2b68f3" alt="I Love You Always Forever (Donna Lewis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b7b1138c52a208d1f8194f99" alt="No Vaseline (Ice Cube)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a715d32590424cd667879ba3" alt="Du hast (Rammstein)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27342a15a4fe15a8a88ab728d5b" alt="Don't Go Breaking My Heart (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fbcaf7402f38faac27610efc" alt="Layla (Derek & The Dominos)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c7f7596cd80cbd6436086f80" alt="Don't Think Twice, It's All Right (Bob Dylan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c7f7596cd80cbd6436086f80" alt="Blowin' in the Wind (Bob Dylan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273db89b08034de626ebee6823d" alt="Basket Case (Green Day)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273db89b08034de626ebee6823d" alt="When I Come Around (Green Day)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737b436d31c5ae44b334736619" alt="Maniac (Michael Sembello)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27305c7aec05eabf142cc33b936" alt="Beast Of Burden - Remastered 1994 (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27305c7aec05eabf142cc33b936" alt="Miss You - Remastered (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732dc219f646be779b0e43a36b" alt="(I Can't Help) Falling In Love With You (UB40)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736cfc470251e23a7bb6a38d66" alt="Tubthumping (Chumbawamba)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b68df485f3304211904548a8" alt="You're The One That I Want - From “Grease” (John Travolta)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b68df485f3304211904548a8" alt="Hopelessly Devoted To You - From “Grease” (Olivia Newton-John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b68df485f3304211904548a8" alt="Summer Nights - From “Grease” (John Travolta)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27393bf4c5e67f6a72149d94c94" alt="Love Shack (The B-52's)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736ede9997b1c47f6891a25671" alt="Murder She Wrote (Chaka Demus & Pliers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bb05d6a2671766e6e633a131" alt="Can't You See (The Marshall Tucker Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fb9dac3244b8486758058a81" alt="Good Vibrations - Remastered 2001 (The Beach Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e8dd4db47e7177c63b0b7d53" alt="Take on Me (a-ha)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27399581550ef9746ca582bb3cc" alt="Imagine - Remastered 2010 (John Lennon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27379606c79fde418c0bc458abb" alt="Jump Around - 30 Years Remaster (House Of Pain)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f1157b7dcd21bae0c2c75d89" alt="Fly Away (Lenny Kravitz)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739ebb7aaf3e19a51782ba1d27" alt="Hungry Heart (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27333d4866ed921300e8ef50808" alt="Kiss from a Rose (Seal)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27304b9ab6bd4bf6a350ba902ea" alt="Dear Mama (2Pac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c7ed51b9dc1014285cae2ae2" alt="Scatman (ski-ba-bop-ba-dop-bop) (Scatman John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27317dd812df38fed44d6d2036e" alt="Ain't Talkin' 'Bout Love - 2015 Remaster (Van Halen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b2622bac004d3ef8fac1095b" alt="Born to Be Alive - The Original (Patrick Hernandez)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aff6573c5110e0732fbab3d8" alt="I Heard It Through The Grapevine (Marvin Gaye)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733414ea69249376598e7d1700" alt="Sailing (Christopher Cross)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273628103d0e62602f00408345d" alt="London Calling - Remastered (The Clash)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c813101657895c26f990b719" alt="I Got You (I Feel Good) (James Brown & The Famous Flames)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d5ea1215e77c3f7a7c716370" alt="Baby Love (The Supremes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737a1e0215c41f0ce411623301" alt="If I Could Turn Back Time (Cher)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ada101c2e9e97feb8fae37a9" alt="There Is a Light That Never Goes Out - 2011 Remaster (The Smiths)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ada101c2e9e97feb8fae37a9" alt="Bigmouth Strikes Again - 2011 Remaster (The Smiths)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27326590dee77103a16e935eadc" alt="Close To Me (The Cure)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738453b853c2cc9c077828eefb" alt="Cecilia (Simon & Garfunkel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738453b853c2cc9c077828eefb" alt="The Boxer (Simon & Garfunkel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738453b853c2cc9c077828eefb" alt="Bridge Over Troubled Water (Simon & Garfunkel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ed801e58a9ababdea6ac7ce4" alt="In My Life - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ed801e58a9ababdea6ac7ce4" alt="Norwegian Wood (This Bird Has Flown) - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e6f11f4c160143e5efb97651" alt="Badfish (Sublime)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738fc4b0dcfb9509553f195c85" alt="Santeria (Sublime)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738fc4b0dcfb9509553f195c85" alt="What I Got (Sublime)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f8f0a26e4100c490bc384003" alt="Let's Get It On (Marvin Gaye)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c289ed4316aaab5a5b7376c1" alt="The Gambler (Kenny Rogers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273980caf4dd525a15f08f8cb87" alt="Pony (Ginuwine)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738dad961673a82ade27f202a8" alt="Baby, I Love Your Way (Big Mountain)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27329c68eb2726f08eca5ba8613" alt="Uptown Girl (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738ccac298c81dd975fd266e82" alt="My Life (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a729c9c3dec04b99d889c66f" alt="Smoke On The Water - Remastered 2012 (Deep Purple)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b99aba76485e5c02fa48f3db" alt="To Love Somebody (Bee Gees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27361ffafd5e31a37336531cf95" alt="No Scrubs (TLC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737a4c8c59851c88f6794c3cbf" alt="Wonderwall - Remastered (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732f2eeee9b405f4d00428d84c" alt="Don't Look Back In Anger (Oasis)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b36949bee43217351961ffbc" alt="What's Going On (Marvin Gaye)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b36949bee43217351961ffbc" alt="Mercy Mercy Me (The Ecology) (Marvin Gaye)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736b141e77892ab2ccb60cf3cf" alt="Solsbury Hill (Peter Gabriel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27301ed248b4ac01c868e688322" alt="Your Love (The Outfield)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738fc4b0dcfb9509553f195c85" alt="Doin' Time (Sublime)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735b96a8c5d61be8878452f8f1" alt="Break on Through (To the Other Side) (The Doors)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735b96a8c5d61be8878452f8f1" alt="Light My Fire (The Doors)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27306ce0d1f846c525e847d60e7" alt="Believe (Cher)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27306ce0d1f846c525e847d60e7" alt="Strong Enough (Cher)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273be0e5ebab8c61469b1ff9f62" alt="Breaking the Law (Judas Priest)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273431ac6e6f393acf475730ec6" alt="1979 - Remastered 2012 (The Smashing Pumpkins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273431ac6e6f393acf475730ec6" alt="Bullet With Butterfly Wings - Remastered 2012 (The Smashing Pumpkins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273af4d7d647d72345ad6a294ad" alt="The Sound of Silence - Acoustic Version (Simon & Garfunkel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8d7445dbee75973efa970e8" alt="Insane in the Brain (Cypress Hill)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273431ac6e6f393acf475730ec6" alt="Tonight, Tonight - Remastered 2012 (The Smashing Pumpkins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d2796d29db72c9d7f9083fe0" alt="Lay, Lady, Lay (Bob Dylan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d514470784e3d02ee0bcdb80" alt="Keep on Loving You (REO Speedwagon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d514470784e3d02ee0bcdb80" alt="Take It On the Run (REO Speedwagon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273387799441ba867649dfbb702" alt="Is This Love (Bob Marley & The Wailers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e98d08fbea1a2f03229abc20" alt="A Kind Of Magic - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731f88f87d7b1df743015cacac" alt="You Don't Own Me (Lesley Gore)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fe1a9aa59e3c6189a09ae37a" alt="You Make My Dreams (Come True) (Daryl Hall & John Oates)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273901d0116a03d30a5c45bb99c" alt="I'll Be There For You (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273901d0116a03d30a5c45bb99c" alt="Bad Medicine (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738f2b3a1c0559ca6188de574b" alt="Sundown (Gordon Lightfoot)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e29b51efdf81e17c63880ef0" alt="How Am I Supposed to Live Without You (Michael Bolton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273653b110d9560eb1656f4c583" alt="Shape Of My Heart (Sting)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273653b110d9560eb1656f4c583" alt="Fields Of Gold (Sting)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d254ca497999ae980a5a38c5" alt="Under Pressure - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738b2238ebc2b233ba73b8c4ca" alt="Boogie Wonderland (with The Emotions) (Earth, Wind & Fire)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27354585a427218bf9bddbd6a3f" alt="Sweet Dreams (Are Made Of This) (Marilyn Manson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf1fee2a55e98e22bf358512" alt="Heaven (Bryan Adams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aaba065944cd82a6f15c86b6" alt="Everywhere - 2017 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fda5556cb6981c3113df6175" alt="All That She Wants (Ace of Base)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27303ca37157b9ceefbe8fe225b" alt="No Diggity (Blackstreet)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27305c5be85b64eaff732f7cb0b" alt="(I Can't Get No) Satisfaction - Mono (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739b19c107109de740bad72df5" alt="What's The Difference (Dr. Dre)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c6aebd89b2dcda3348649633" alt="Because You Loved Me (Theme from "Up Close and Personal") (Céline Dion)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735306ed42ae78f317258c51bb" alt="The Power Of Love (Huey Lewis & The News)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aaba065944cd82a6f15c86b6" alt="Little Lies - 2017 Remaster (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f67fbf0d465cca2b3e25af96" alt="Crocodile Rock (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf1fee2a55e98e22bf358512" alt="Run To You (Bryan Adams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273222cb38afc3b3b47d9df26aa" alt="Pour Some Sugar On Me - Remastered 2017 (Def Leppard)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fda5556cb6981c3113df6175" alt="The Sign (Ace of Base)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c6aebd89b2dcda3348649633" alt="It's All Coming Back to Me Now (Céline Dion)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27317f9e7e7784ed40b223e261c" alt="Super Freak (Rick James)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733c182241fcd86aeca2c68a63" alt="Blue Monday (New Order)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b2bcbfcf7d8e8c326ab8481b" alt="I'll Stand by You (Pretenders)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f82c7e4376cf8267fb396b7d" alt="Baby Got Back (Sir Mix-A-Lot)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27343511b8c20112757edddc7ba" alt="Hysteria (Def Leppard)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f67fbf0d465cca2b3e25af96" alt="Daniel (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27354096a7f898de0233d76f626" alt="Blister In The Sun (Violent Femmes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735c7731f5acdcb2d02d78b7ee" alt="White Room (Cream)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c6aebd89b2dcda3348649633" alt="All By Myself (Céline Dion)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27351d98ff76da5ca1f82c8cbc8" alt="Wham Bam Shang-A-Lang (Silver)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a07cc88003498f7559787673" alt="Low Rider (War)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fec6bb271749b854c35e5f5c" alt="Tired of Being Alone (Al Green)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f56546aac4f5d002c4c3d705" alt="Weak (SWV)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733a3c381f6910a4fe51c2640b" alt="Give Me the Night (George Benson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273686c29818cd37e585c48e7ef" alt="Put Your Head On My Shoulder (Paul Anka)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738ec81cc654b45ade8bdf1486" alt="Message In A Bottle (The Police)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738ec81cc654b45ade8bdf1486" alt="Walking On The Moon (The Police)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733395f3e809dfbc2b1101d464" alt="Space Oddity - 2015 Remaster (David Bowie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b3994c94dfb241923664bb4d" alt="Sweet Dreams (Are Made of This) - 2005 Remaster (Eurythmics)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fb2faa3ed46d1d0124ca325e" alt="(I Just) Died In Your Arms (Cutting Crew)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273af14d74d5e308ce2f3ec22f8" alt="Edge of Seventeen - 2016 Remaster (Stevie Nicks)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273676a8230a422123e8012557e" alt="Night Moves (Bob Seger)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27367bc29c251c777361b17a190" alt="Somebody To Love - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27367bc29c251c777361b17a190" alt="Good Old-Fashioned Lover Boy - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732160c02bc56f192df0f4986b" alt="I Want It That Way (Backstreet Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732160c02bc56f192df0f4986b" alt="Larger Than Life (Backstreet Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f753fddb6af9c9476ed02c9e" alt="It's Still Rock and Roll to Me (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cebdf1f7660ace8c2a80585c" alt="I'm Gonna Be (500 Miles) (The Proclaimers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8e97cafeb2acb85b21a777e" alt="Every Breath You Take (The Police)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273461762c15f05e141fe6f3097" alt="Southern Nights (Glen Campbell)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27334cbf7013afccc7df67fa43f" alt="Girls & Boys (Blur)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734b292ed7c7360a04d3d6b74a" alt="Your Song (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27366ec7d795b727cd90bd09690" alt="Walkin' On The Sun (Smash Mouth)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cefb195c53a73383add7f5f7" alt="Lessons In Love (Level 42)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273413a6c2c7b296d98171e5e21" alt="Three Little Birds (Bob Marley & The Wailers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273345536847e60f622ee0eae96" alt="Say It Ain't So - Original Mix (Weezer)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273345536847e60f622ee0eae96" alt="Buddy Holly (Weezer)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273345536847e60f622ee0eae96" alt="Undone - The Sweater Song (Weezer)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dc30583ba717007b00cceb25" alt="Here Comes The Sun - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dc30583ba717007b00cceb25" alt="Come Together - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dc30583ba717007b00cceb25" alt="Something - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e542fbcf1a83b7c726eb50a6" alt="One Headlight (The Wallflowers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bad7062c3fd2f2d037989694" alt="Paint It, Black (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f0e951707ca49b533fdbf64e" alt="I've Got a Woman (Ray Charles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730a7d45a345534966a4ad2c39" alt="Enjoy the Silence (Depeche Mode)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730a7d45a345534966a4ad2c39" alt="Personal Jesus - Single Version (Depeche Mode)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27346e859872ed30a898160aeb2" alt="Sexual Healing (Marvin Gaye)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a4d2cb95d3ea17f773db23ee" alt="Hard To Handle (The Black Crowes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27384fef39a9a8293c86796599f" alt="Truly Madly Deeply (Savage Garden)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273af6b486fa0a2959f79c8acd8" alt="My Sharona (The Knack)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bddcc30c6a3288e725aec2df" alt="Give A Little Bit (Supertramp)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa22899360d8ba6704732dec" alt="Gimme! Gimme! Gimme! (A Man After Midnight) (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa22899360d8ba6704732dec" alt="Chiquitita (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa22899360d8ba6704732dec" alt="Voulez-Vous (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa22899360d8ba6704732dec" alt="Angeleyes (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa22899360d8ba6704732dec" alt="Does Your Mother Know (ABBA)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739daf7b461a827acbbb0e4971" alt="Blame It on the Boogie (The Jacksons)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c13acd642ba9f6f5f127aa1b" alt="Take It Easy - 2013 Remaster (Eagles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c13acd642ba9f6f5f127aa1b" alt="Peaceful Easy Feeling - 2013 Remaster (Eagles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27392d21aef6c0d288cc4c05973" alt="Knockin' On Heaven's Door (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27392d21aef6c0d288cc4c05973" alt="You Could Be Mine (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27392d21aef6c0d288cc4c05973" alt="Civil War (Guns N' Roses)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8b444df094279e70d0ed856" alt="Karma Police (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8b444df094279e70d0ed856" alt="Let Down (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8b444df094279e70d0ed856" alt="Paranoid Android (Radiohead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27322463d6939fec9e17b2a6235" alt="Everybody Wants To Rule The World (Tears For Fears)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731336b31b6a1799f0de5807ac" alt="Livin' On A Prayer (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731336b31b6a1799f0de5807ac" alt="You Give Love A Bad Name (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739b19c107109de740bad72df5" alt="Still D.R.E. (Dr. Dre)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739b19c107109de740bad72df5" alt="The Next Episode (Dr. Dre)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27308fc42e575043a753f60d675" alt="Start Me Up - Remastered 2009 (The Rolling Stones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c36cf94d717475042f6bb0f3" alt="Angels (Robbie Williams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738e0ff34ad21955b6f4da9b86" alt="Do For Love (2Pac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731336b31b6a1799f0de5807ac" alt="Wanted Dead Or Alive (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739565c4df27be4aee5edc8009" alt="Shout (Tears For Fears)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730dd350beeb5ac73672ad6e80" alt="Beds Are Burning - Remastered (Midnight Oil)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731336b31b6a1799f0de5807ac" alt="Never Say Goodbye (Bon Jovi)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c36cf94d717475042f6bb0f3" alt="Let Me Entertain You (Robbie Williams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731dda5f57ba5c203f775ea2dd" alt="Inbetween Days (The Cure)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736da502e35a7a3e48de2b0f74" alt="All The Small Things (blink-182)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736da502e35a7a3e48de2b0f74" alt="What's My Age Again? (blink-182)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736da502e35a7a3e48de2b0f74" alt="Adam's Song (blink-182)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f33f1738a2764489750e3535" alt="(They Long To Be) Close To You (Carpenters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27367c1113f55ab816ef61d3993" alt="Lovely Day (Bill Withers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ff4db4dae0252068fc3db08f" alt="Bad To The Bone (George Thorogood & The Destroyers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735c5dbd89210073351c9a6fdd" alt="She Sells Sanctuary (The Cult)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27347066a9aac4e3493fe5b8677" alt="Golden Brown (The Stranglers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273eafa3ccf2f56bfbb6f4f1ba5" alt="Yesterday Once More (Carpenters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e226488b7af9f296c95be551" alt="You Never Can Tell (Chuck Berry)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f5768db89dd8ac30fd0e414f" alt="Barbie Girl (Aqua)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27352038992fc6d7868f31d23b7" alt="How Deep Is Your Love (Bee Gees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27352038992fc6d7868f31d23b7" alt="Stayin' Alive - From "Saturday Night Fever" Soundtrack (Bee Gees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730aac8ca880151fda470e91af" alt="Lovefool (The Cardigans)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ef063cb80508c55eb443a671" alt="Old Time Rock & Roll (Bob Seger)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ef89c52c42eaf1f89347a16c" alt="You Got It (Roy Orbison)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ef063cb80508c55eb443a671" alt="Still The Same (Bob Seger)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273056e90910cbaf5c5b892aeba" alt="Another One Bites The Dust - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273056e90910cbaf5c5b892aeba" alt="Crazy Little Thing Called Love - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fbc71c99f9c1296c56dd51b6" alt="Smells Like Teen Spirit (Nirvana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fbc71c99f9c1296c56dd51b6" alt="Come As You Are (Nirvana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fbc71c99f9c1296c56dd51b6" alt="Lithium (Nirvana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fbc71c99f9c1296c56dd51b6" alt="In Bloom (Nirvana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ff191d7fbdb5a13eaf84132b" alt="Back In Black (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ff191d7fbdb5a13eaf84132b" alt="You Shook Me All Night Long (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273105ef588df1ef91bfa811f94" alt="Hold the Line (TOTO)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ff191d7fbdb5a13eaf84132b" alt="Hells Bells (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734bc9bcdbdc9ac34e37d8b6bb" alt="Everlong (Foo Fighters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734bc9bcdbdc9ac34e37d8b6bb" alt="My Hero (Foo Fighters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734bc9bcdbdc9ac34e37d8b6bb" alt="Monkey Wrench (Foo Fighters)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce023ce7dfdd5199bcdfd5a1" alt="Girls Just Want to Have Fun (Cyndi Lauper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce023ce7dfdd5199bcdfd5a1" alt="Time After Time (Cyndi Lauper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fdd261528e3590ac36bb85f0" alt="Unforgettable (Nat King Cole)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27301ef4924c562e6d57493c835" alt="Burning Love (Elvis Presley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27301ef4924c562e6d57493c835" alt="Always On My Mind (Elvis Presley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27399b37676fbae815424b4b1a4" alt="Against The Wind (Bob Seger)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738d897b8994ce008298200408" alt="Better Off Alone (Alice Deejay)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a04b4373fd72bf81c8784adf" alt="The Best (Tina Turner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732323f86e757c3436b3cc38af" alt="Heat Of The Moment (Asia)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b414c63fb435b622238c15ed" alt="Jump - 2015 Remaster (Van Halen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b414c63fb435b622238c15ed" alt="Panama - 2015 Remaster (Van Halen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f875c8285d7f26a42baaa2a0" alt="She's so High (Tal Bachman)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738b28efbba32db47b0172fd9e" alt="Narcotic - Radio Edit (Liquido)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b2439940aedd2801c9ae2e5b" alt="Hooked On A Feeling (Blue Swede)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739cd3665c5518c19b9ba36676" alt="Glory of Love (Peter Cetera)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737a8ebb7a3a8c0cadc4490cb4" alt="Bitch (Meredith Brooks)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273786b44c75ebf915866523f5b" alt="How Soon Is Now? - 2011 Remaster (The Smiths)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273697d340dffd2907c5469d8fb" alt="Every Morning (Sugar Ray)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27332a7d87248d1b75463483df5" alt="Billie Jean (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27332a7d87248d1b75463483df5" alt="Beat It (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8a11e48c91a982d086afc69" alt="Stairway to Heaven - Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730acddc8ccf8d14858fbeddf5" alt="(Sittin' On) the Dock of the Bay (Otis Redding)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27384243a01af3c77b56fe01ab1" alt="Let It Be - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf84c5b276431b473e924802" alt="Sad But True (Metallica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8a11e48c91a982d086afc69" alt="Rock and Roll - Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8a11e48c91a982d086afc69" alt="Black Dog - Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c8a11e48c91a982d086afc69" alt="Going to California - Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730649124c37ce988317263671" alt="Celebrity Skin (Hole)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e9da8645c59d76e7f35dff6e" alt="Back At One (Brian McKnight)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27332a7d87248d1b75463483df5" alt="Human Nature (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737f6f6c9e4b492a3d7e910d82" alt="I Get Around (2Pac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739d52169c3b609d4630e04433" alt="Easy (Commodores)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cbd2ee7dff77bfb2b5f0af52" alt="The Kids Aren't Alright (The Offspring)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cbd2ee7dff77bfb2b5f0af52" alt="Pretty Fly (For A White Guy) (The Offspring)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cbd2ee7dff77bfb2b5f0af52" alt="Why Don't You Get A Job (The Offspring)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735f2acb28c792e4594c0f11e8" alt="I Knew I Loved You (Savage Garden)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733c73b2e0a6aa490736f19751" alt="I Love Rock 'N Roll (Joan Jett & the Blackhearts)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730f98789111606f77a27d6f67" alt="What You Won't Do for Love (Bobby Caldwell)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf84c5b276431b473e924802" alt="Enter Sandman (Metallica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf84c5b276431b473e924802" alt="Nothing Else Matters (Metallica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf84c5b276431b473e924802" alt="The Unforgiven (Metallica)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736fb355dfc944cce3598e30a1" alt="I Try (Macy Gray)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b96c21e15c091eb98a6c88a4" alt="Can't Take My Eyes off You (Frankie Valli)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730c3a44d76807bef665eacfa3" alt="Hot Stuff (Donna Summer)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b98afa12c212cbbda4f1799b" alt="Music Sounds Better With You - Radio Edit (Stardust)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737d419ac975423c069995c7bb" alt="Long Train Runnin' (The Doobie Brothers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273423e79bb88e572ba87cdd185" alt="True - 2003 Remaster (Spandau Ballet)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a94a1672a1fc0373b3e9aa7b" alt="On Bended Knee (Boyz II Men)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a94a1672a1fc0373b3e9aa7b" alt="I'll Make Love To You (Boyz II Men)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734527c5cf12ed1fa91d50f1fc" alt="Bailando (Paradisio)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736ebd5e789646a833b8f7d4ba" alt="Don't Speak (No Doubt)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736ebd5e789646a833b8f7d4ba" alt="Just A Girl (No Doubt)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273626d1849afa1bc27a8743dfe" alt="Magic Carpet Ride (Steppenwolf)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273206e2e76c3a706e4734d18ab" alt="December, 1963 (Oh What a Night!) (The Four Seasons)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dc20397b139223620af148f6" alt="Glory Box (Portishead)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738cefe8e2f2cfd63ce073fa96" alt="Total Eclipse of the Heart (Bonnie Tyler)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739b19c107109de740bad72df5" alt="Forgot About Dre (Dr. Dre)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735b7865be7f7fcc05faec6137" alt="Killing Me Softly With His Song (Fugees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e230f303815e82a86713eedd" alt="And I Love Her - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739a0011cc9d31cf969b656905" alt="Love Grows (Where My Rosemary Goes) (Edison Lighthouse)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273073aebff28f79959d2543596" alt="How Do U Want It (ft. K-Ci & JoJo) (2Pac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735b7865be7f7fcc05faec6137" alt="Ready or Not (Fugees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273102bebc4807fc0952a754d0f" alt="Never Too Much (Luther Vandross)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d12fd00a64529cff635a75f2" alt="The Promise (When In Rome)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b00a6721828724ce38a1e7a3" alt="Arthur's Theme (Best That You Can Do) (Christopher Cross)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273608a63ad5b18e99da94a3f73" alt="All My Loving - Remastered 2009 (The Beatles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736dca8c5fbd00a19a9e503dd9" alt="Slave To Love (Bryan Ferry)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734e36eb543ce3731ac913845c" alt="Layla - Acoustic Live (Eric Clapton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ddf2f9edabd166c60047e3c4" alt="Miami (Will Smith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ddf2f9edabd166c60047e3c4" alt="Gettin' Jiggy Wit It (Will Smith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739a9b1cc067e4460da04adce2" alt="Thunderstruck (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739a9b1cc067e4460da04adce2" alt="Moneytalks (AC/DC)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac" alt="Walk Of Life (Dire Straits)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac" alt="Money For Nothing (Dire Straits)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac" alt="Brothers In Arms (Dire Straits)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730e767887e304020cdbbe25e8" alt="Stars (Simply Red)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27347eb3ea5a92904c19e102e54" alt="Maria Maria (feat. The Product G&B) (Santana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27347eb3ea5a92904c19e102e54" alt="Smooth (feat. Rob Thomas) (Santana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27381eae9a98487ae512df29469" alt="Baby Come Back (Player)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d6806ddfc58bbaa0cb3e9fa5" alt="Da Ya Think I'm Sexy? (Rod Stewart)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27323290120a609a65e14cfe018" alt="Don't Stop Believin' (2022 Remaster) (Journey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f5e30500f0eec7d92b159eae" alt="The Final Countdown (Europe)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f97219e49a23bfdd4de7eed1" alt="I Just Called To Say I Love You (Stevie Wonder)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27372641ed682401fc46c18ac12" alt="Lean on Me (Bill Withers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f5e30500f0eec7d92b159eae" alt="Carrie (Europe)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dac4efc0ebdfd9d92f127129" alt="Never Tear Us Apart (INXS)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dac4efc0ebdfd9d92f127129" alt="Need You Tonight (INXS)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dac4efc0ebdfd9d92f127129" alt="New Sensation (INXS)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739e77d65619f80436b5cc9d12" alt="Rivers of Babylon (Boney M.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733d16809ca253f0f476195941" alt="Quit Playing Games (With My Heart) (Backstreet Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b3adf9b1706b05af854bbad4" alt="Fire and Rain - 2019 Remaster (James Taylor)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273765b0617b572bdd1dbdc7d8e" alt="Kashmir - Remaster (Led Zeppelin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733789f564b75140c1fd2228cc" alt="Shook Ones, Pt. II (Mobb Deep)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27365a7b0a6969f0efcde4b5aca" alt="Rock And Roll All Nite (KISS)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273530cec85d4543693bd726167" alt="As Long as You Love Me (Backstreet Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273530cec85d4543693bd726167" alt="Everybody (Backstreet's Back) - Radio Edit (Backstreet Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fe24dcd263c08c6dd84b6e8c" alt="Baba O'Riley (The Who)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f7730f46da78d52e66bd6f65" alt="Missing You (John Waite)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fe24dcd263c08c6dd84b6e8c" alt="Behind Blue Eyes (The Who)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ad53be7d2ec379399660c1ec" alt="Reminiscing - Remastered 2010 (Little River Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739d9a49f795b4340538f43435" alt="Owner of a Lonely Heart (Yes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732166b28714239e31b48aeb17" alt="Stuck On You (Lionel Richie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732166b28714239e31b48aeb17" alt="Hello (Lionel Richie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733e030a7e606959674643d274" alt="I Want to Know What Love Is - 1999 Remaster (Foreigner)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf1fee2a55e98e22bf358512" alt="Summer Of '69 (Bryan Adams)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e319baafd16e84f0408af2a0" alt="Bohemian Rhapsody - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273787674b6a114f98cad6f834b" alt="Wind Of Change (Scorpions)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737625714e597e9f3ad7bde455" alt="Host from the Night (Revenge)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273787674b6a114f98cad6f834b" alt="Send Me An Angel (Scorpions)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737625714e597e9f3ad7bde455" alt="Suffering Sound (Revenge)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732c33399e119cec9b0fcde564" alt="Say You, Say Me (Lionel Richie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273673526fcf35ab235e1a9d94c" alt="Sunday Bloody Sunday - Remastered 2008 (U2)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273227393028d2b83ced8e74d9b" alt="Thong Song (Sisqo)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27372833c1ae3343cbfb4617073" alt="Tom Sawyer (Rush)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734e4ad725fbfb99d854e1aa25" alt="Midnight Rider (Allman Brothers Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b5e18a80757ba2f787213d21" alt="On & On (Erykah Badu)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e774643594281699bde1e4ed" alt="Beyond the Sea (Bobby Darin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e319baafd16e84f0408af2a0" alt="You're My Best Friend - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bdcea025a483b9642f17a9f8" alt="More Than A Woman (Bee Gees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ab0a92e5cd20c2224c44a8a6" alt="You Can't Hurry Love - 2016 Remaster (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa3252b7843a8a3426cc34bf" alt="Can't Get Enough Of Your Love, Babe (Barry White)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d03ab2da904d8251a87bbc31" alt="Tiny Dancer (Elton John)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d40610074e9816f2a2004336" alt="I Started A Joke (Bee Gees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c957c20238e5f9f543439be0" alt="It Must Have Been Love - From the Film "Pretty Woman" (Roxette)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bbf0146981704a073405b6c2" alt="Dream On (Aerosmith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735c21d73934bb9760a2f791a2" alt="That's Life (Frank Sinatra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734f3bbf9631faeb8de9912a23" alt="All Star (Smash Mouth)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737cb33b8fab5302942e6a78fb" alt="Surfin' U.S.A. - Remastered 2001 (The Beach Boys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739bef45ee387f274ea3198c55" alt="My Name Is (Eminem)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ed0ddbe4b2590f448e9845be" alt="Part-Time Lover (Stevie Wonder)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aa802dc9f870e66a8bb6a2a2" alt="(Don't Fear) The Reaper (Blue Öyster Cult)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731310670cbb82f06474372cfd" alt="Self Control (Laura Branigan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c18c4e6c2978fb6cbdef85e2" alt="Mr. Blue Sky (Electric Light Orchestra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738ac778cc7d88779f74d33311" alt="Around the World (Daft Punk)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739e5af96086574b76499dcf70" alt="(You Make Me Feel Like) A Natural Woman (Aretha Franklin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273de3094d98b62340d3268c7bc" alt="La Isla Bonita (Madonna)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ea04468e11c67890666d2b34" alt="Young Hearts Run Free (Candi Staton)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27330951af6ae2cced0a3defd49" alt="I'm Gonna Miss You (Milli Vanilli)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27323dbfb8b3b1be429587f5380" alt="Push (Matchbox Twenty)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27323dbfb8b3b1be429587f5380" alt="3AM (Matchbox Twenty)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6325f361d7803ad0d908451" alt="Linger (The Cranberries)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273153d79816d853f2694b2cc70" alt="Under the Bridge (Red Hot Chili Peppers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2731a5b6271ae1c8497df20916e" alt="My Girl (The Temptations)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f6325f361d7803ad0d908451" alt="Dreams (The Cranberries)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27337e78b6638f7737adee73d6f" alt="Don't Bring Me Down (Electric Light Orchestra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273153d79816d853f2694b2cc70" alt="Give It Away (Red Hot Chili Peppers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27386339e6cd71cc2a167451ee5" alt="People Are Strange (The Doors)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27337e78b6638f7737adee73d6f" alt="Last Train to London (Electric Light Orchestra)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27318f632fef2f6c380c8ba43f5" alt="High (Lighthouse Family)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273772d1e082a4c9ee97d004d21" alt="Beautiful Girl (INXS)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fed4a89ebe66064c67f2f4ea" alt="Eternal Flame (The Bangles)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734f6d78b7fb2ba87ed33fcd7e" alt="A Forest (The Cure)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27336c5417732e53e23cb219246" alt="The Man Who Sold The World - Live (Nirvana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738bd8adbdc4727d9080240905" alt="Come On Eileen (Dexys Midnight Runners)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27336c5417732e53e23cb219246" alt="Where Did You Sleep Last Night - Live (Nirvana)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fb16b9b69eb891027654bcb1" alt="More Than Words (Extreme)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273702689066bc17ee67203c2bc" alt="I Can See Clearly Now - Edit (Johnny Nash)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cbcb5083c56df2a557625bca" alt="Groove Is in the Heart (Deee-Lite)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730540e183356055dfb31b747e" alt="You Make Me Wanna... (USHER)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ba6340ac3b1653b6ea0e5da5" alt="What a Fool Believes (The Doobie Brothers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b8f8d696810d68ce774e3a2f" alt="Take My Breath Away - Love Theme from "Top Gun" (Berlin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273436e38032cf3389d01426eca" alt="Two Princes (Spin Doctors)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2730c3a1b46b6b846dfdfbc6a7d" alt="Mary Jane's Last Dance (Tom Petty and the Heartbreakers)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734aa7956a8d5742ac762699b2" alt="I'd Love to Change the World - 2004 Remaster (Ten Years After)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735f9e9291ab85c1e8fa88143f" alt="Weather With You (Crowded House)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ad08f4b38efbff0c0da0f252" alt="Running Up That Hill (A Deal With God) (Kate Bush)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734fb043195e8d07e72edc7226" alt="Landslide (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d231bd1716b71b6444e25f89" alt="For What It's Worth (Buffalo Springfield)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734fb043195e8d07e72edc7226" alt="Rhiannon (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737b40b2abdbcb8520874f29ed" alt="My Own Worst Enemy (Lit)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c573a4a852f010523c4ba383" alt="She Drives Me Crazy (Fine Young Cannibals)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738f5813c842cb115f3cf1fecd" alt="Voyage voyage (Desireless)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27396c799b97ad8d8be2d315dd0" alt="Check Yo Self - Remix (Ice Cube)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273483c3d93af76b1f635f9dc7d" alt="Hunger Strike (Temple Of The Dog)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27357850545c0dc2cc537186070" alt="All I Wanna Do Is Make Love To You (Heart)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734fb043195e8d07e72edc7226" alt="Say You Love Me (Fleetwood Mac)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27309e2ec500166cf2d5ac21050" alt="Killer Queen - Remastered 2011 (Queen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ebc918cfb51e9ced7349f436" alt="Call Me (Blondie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273481ecf6365d84be80cad59d7" alt="Ecuador - Original Radio Edit (Sash!)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738a2ce3f148f57584269c3782" alt="Purple Rain (Prince)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738a2ce3f148f57584269c3782" alt="When Doves Cry (Prince)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736b38571f15487588ed53032f" alt="Give Me One Reason (Tracy Chapman)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273cf505191afa6a1978418fdf8" alt="Mambo No. 5 (a Little Bit of...) (Lou Bega)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736aa9314b7ddfbd8f036ba3ac" alt="Respect (Aretha Franklin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27389a392107ebd79818022b3ea" alt="Fade Into You (Mazzy Star)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273fe7b026ecee99597b4ad7eb4" alt="Runaway Train (2022 Remaster) (Soul Asylum)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273aff4aef671b2510be7c115b3" alt="Piano Man (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273afc2d1d2c8703a10aeded0af" alt="Hallelujah (Jeff Buckley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27379e5e2b1860079d662a9bb76" alt="This Will Be (An Everlasting Love) (Natalie Cole)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f94b2a29ccc364e8faedce10" alt="The Rhythm of the Night (Corona)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736f8c26346723dd0531696bed" alt="Me and Bobby McGee (Janis Joplin)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273377198e5b790b5ebf137bd83" alt="Nothing's Gonna Stop Us Now (Starship)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a7c7f94cfccd5ab6de233916" alt="It's The End Of The World As We Know It (And I Feel Fine) (R.E.M.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2739ac4e14fdaf2f24717050239" alt="Hip Hop Hooray (Naughty By Nature)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ba7005f3c12d940ad4967460" alt="We Belong (Pat Benatar)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737cef65b561af10a25acbc2df" alt="Don't Dream It's Over (Crowded House)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273bcfed2b555f5563dbd8b267b" alt="I'd Love You to Want Me (Lobo)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273eda9478c39a21e1cdc6609ca" alt="Iris (The Goo Goo Dolls)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273eda9478c39a21e1cdc6609ca" alt="Slide (The Goo Goo Dolls)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27331ac4ea81876d18519e4b6eb" alt="Shoop (Salt-N-Pepa)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b66c23534dd78ff7d3da83b8" alt="Wicked Game (Chris Isaak)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27384bb2b1e87d5ba0bac8871a2" alt="Torn (Natalie Imbruglia)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c41f4e1133b0e6c5fcf58680" alt="Starman - 2012 Remaster (David Bowie)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ace3e7aae0b7c78bbe1c4f35" alt="Everybody Hurts (R.E.M.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735d11c2fe73a7d376d3b06107" alt="Ordinary World (Duran Duran)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27308fe0c9b647742b06d3b9f87" alt="It's Too Late (Carole King)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735d11c2fe73a7d376d3b06107" alt="Come Undone (Duran Duran)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ace3e7aae0b7c78bbe1c4f35" alt="Man On The Moon (R.E.M.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b80d7868e6e0275d12102508" alt="Abracadabra (Steve Miller Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a09b231129ab1cb1a6efc57f" alt="This Charming Man - 2011 Remaster (The Smiths)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738f8dc242b396ddc31c01d36c" alt="If You Don't Know Me by Now - 2008 Remaster (Simply Red)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273dfe4bfe695c4192e547e72c7" alt="Ring of Fire (Johnny Cash)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273865a956fe40cf54597e97fd2" alt="Sister Golden Hair (America)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27350fcab12b2e2e0ee0019ac53" alt="Boom, Boom, Boom, Boom!! (Vengaboys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27350fcab12b2e2e0ee0019ac53" alt="We Like To Party! (The Vengabus) (Vengaboys)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c0e98d7c48b548f1a3833368" alt="Got to Be Real (Cheryl Lynn)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ed7b5f97f354c216f80d61da" alt="It's My Life - 1997 Remaster (Talk Talk)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f5e5babccf665ef8c912b190" alt="U Can't Touch This (MC Hammer)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273128450651c9f0442780d8eb8" alt="Simple Man (Lynyrd Skynyrd)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273128450651c9f0442780d8eb8" alt="Free Bird (Lynyrd Skynyrd)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273128450651c9f0442780d8eb8" alt="Gimme Three Steps (Lynyrd Skynyrd)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e691caf11b86a3729899a304" alt="Let's Groove (Earth, Wind & Fire)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273da8119b8c2aea9f623289862" alt="Love Really Hurts Without You (Billy Ocean)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a16ea5e673cc4c6e8f91d5ca" alt="You Can't Hurry Love (The Supremes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273887b7c596249f628db6c6473" alt="Celebration (Kool & The Gang)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27334b292a289c635532da02671" alt="Poison (Alice Cooper)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c1ea4aac1ad07a38c59dd30c" alt="I Got 5 On It (Luniz)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b4a878f008a0eda552446701" alt="They Don't Care About Us (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c79a70e8167cc1a4fab83781" alt="Fuck Tha Police (N.W.A.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c79a70e8167cc1a4fab83781" alt="Straight Outta Compton (N.W.A.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b4a878f008a0eda552446701" alt="You Are Not Alone (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733cd811ba3d8e0b67feb08e75" alt="Daughter - Remastered (Pearl Jam)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273b4a878f008a0eda552446701" alt="Earth Song (Michael Jackson)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a8a965df6a845b265ee19106" alt="Dude (Looks Like A Lady) (Aerosmith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273147e0a8a7c795a4eb7c511db" alt="Plush (Stone Temple Pilots)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273456c0b5d0316a80dc600802e" alt="I Will Always Love You (Whitney Houston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273456c0b5d0316a80dc600802e" alt="I Have Nothing (Whitney Houston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737e8045e318486885fe243817" alt="Any Way You Want It (Journey)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27316c75e2dd2654d7d03f2c556" alt="Hungry Like the Wolf - 2009 Remaster (Duran Duran)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732d0e5ab5bd2e234fbcffa3e0" alt="Even Flow (Pearl Jam)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732d0e5ab5bd2e234fbcffa3e0" alt="Black (Pearl Jam)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732d0e5ab5bd2e234fbcffa3e0" alt="Alive (Pearl Jam)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732d0e5ab5bd2e234fbcffa3e0" alt="Jeremy (Pearl Jam)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736a74089537c2dbd548c4a95e" alt="Somebody to Love (Jefferson Airplane)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736a74089537c2dbd548c4a95e" alt="White Rabbit (Jefferson Airplane)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2733ebc5b9d8942069d3b920550" alt="Rich Girl (Daryl Hall & John Oates)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f725bc7907dcf15aa2c6e7b7" alt="Just What I Needed (The Cars)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732fc23e78e87d793054bba090" alt="Rock'n Me (Steve Miller Band)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273994c319841a923465d62e271" alt="It Was A Good Day (Ice Cube)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a14b08b9a6616e121df5e8b0" alt="You Are The Sunshine Of My Life (Stevie Wonder)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a520a167a62d5548cdb53101" alt="I Wanna Dance with Somebody (Who Loves Me) (Whitney Houston)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273584302fee10c0d0a12c40c97" alt="The Sweetest Taboo (Sade)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737ed1df1690df31d094d7c2bc" alt="No Rain (Blind Melon)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d27f104dd5adb7029d109720" alt="Holding Back the Years - 2008 Remaster (Simply Red)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27321fbdd09672c5f8bcfd66165" alt="Cum on Feel the Noize (Quiet Riot)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273389fee741b183fc3df0fbf64" alt="I Think We're Alone Now (Tiffany)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273eafaf556eda644a745d0144d" alt="Walking On Sunshine (Katrina & The Waves)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d6d86be2779b5b6b4980feb9" alt="The Bad Touch (Bloodhound Gang)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2735901aaa980d3e714bf01171c" alt="C.R.E.A.M. (Cash Rules Everything Around Me) (Wu-Tang Clan)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e0f0aa947770fe74049dbba3" alt="Heaven Is A Place On Earth (Belinda Carlisle)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273472fbc1d5743c7d3c75b9ec0" alt="Just the Two of Us (feat. Bill Withers) (Grover Washington, Jr.)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273e8f69ab903901064b1f19249" alt="The Boys Are Back In Town (Thin Lizzy)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2738c7a8e68dc5c20bb72f713f2" alt="Still Not a Player (feat. Joe) - Radio Version (Big Pun)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736ffa23f19d8c125204e6220c" alt="Here Comes the Hotstepper - Heartical Mix (iNi Kamoze)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2737438996f6fe67c59d75d4e43" alt="Gangsta's Paradise (Coolio)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ae6d8e36136353d550b2587d" alt="Black Hole Sun (Soundgarden)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273190a4b0a0a59371fbbb6effa" alt="Suspicious Minds (Elvis Presley)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ae6d8e36136353d550b2587d" alt="Fell On Black Days (Soundgarden)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2736731eabe4c268971eeed3c06" alt="Against All Odds (Take a Look at Me Now) - 2016 Remaster (Phil Collins)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273015c484a7aca592df1a77828" alt="House of the Rising Sun (The Animals)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a43a6482e327d623bb0c0f77" alt="Dancing In the Dark (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a43a6482e327d623bb0c0f77" alt="I'm On Fire (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a43a6482e327d623bb0c0f77" alt="Born in the U.S.A. (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273a43a6482e327d623bb0c0f77" alt="Glory Days (Bruce Springsteen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273de82204a5baa683ce85d57cb" alt="Tarzan Boy (Baltimora)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2732a1049b6d0d2b4c3c0abe7a8" alt="I Will Survive (Gloria Gaynor)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27313b37e7dd8f09d2e3c99c826" alt="Sexbomb (Tom Jones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27336cf58e3e7cf36a145b1da18" alt="...Baby One More Time (Britney Spears)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27336cf58e3e7cf36a145b1da18" alt="Sometimes (Britney Spears)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27336cf58e3e7cf36a145b1da18" alt="(You Drive Me) Crazy (Britney Spears)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ebd6d20c0082524244ef83df" alt="Africa (TOTO)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ebd6d20c0082524244ef83df" alt="Rosanna (TOTO)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273f4a2ccbe20d6d52f16816812" alt="Eye of the Tiger (Survivor)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ea07dca8b4ca808c1e5b17fb" alt="Eyes Without A Face (Billy Idol)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ea07dca8b4ca808c1e5b17fb" alt="Rebel Yell (Billy Idol)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273af7afb5c49afd3133fa2a6c9" alt="Escape (The Pina Colada Song) (Rupert Holmes)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d14cd6c24470c6de13265d0a" alt="Let's Twist Again (Chubby Checker)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce36d2a7b551ee0fc8dbb341" alt="Forget Me Nots - Remastered (Patrice Rushen)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273da8d92affd796f7e20af7375" alt="I Don't Want to Miss a Thing - From "Armageddon" Soundtrack (Aerosmith)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734d1a7a3e5043173883653ffc" alt="Sweet Caroline (Neil Diamond)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b2734f7420eec423c20556744d7d" alt="Tell It to My Heart (Taylor Dayne)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273c786ceb2ebf85c58c7dc665f" alt="Shine (Collective Soul)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ce32b2f1b4b9e2f1c68f84cc" alt="We Didn't Start the Fire (Billy Joel)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273814a5ed9d4af838b632b3668" alt="She's A Lady (Tom Jones)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273d419ed4f1e89669ce14bd369" alt="Play That Funky Music (Wild Cherry)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27344d10bd5b6282b959d695a41" alt="Tragedy (Bee Gees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b27344d10bd5b6282b959d695a41" alt="Too Much Heaven (Bee Gees)" width="64" height="64">
<img src="https://i.scdn.co/image/ab67616d0000b273ca40908d43a2a80fb34de8a3" alt="Boys Don't Cry (The Cure)" width="64" height="64">
