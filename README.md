![banner](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/calypso-banner-rounded.jpg)

### CALYPSO

The *Calypso* is an oceanographic vessel equipped and used by the maritime explorer Jacques-Yves Cousteau for his scientific expeditions and documentary film productions.

Named after Calypso, the sea nymph from Greek mythology, the ship and its crew sailed the world’s seas and oceans from November 24, 1951, until January 1996. Through television and books, the *Calypso* became one of the symbols of maritime exploration and global ecology in the second half of the 20th century, in the tradition of its illustrious predecessors such as *La Boussole* and *L’Astrolabe*, the *Beagle*, the *Challenger*, the *Pourquoi Pas?*, and the *Hirondelle*.

## Description

**Calypso** is not only the name of a famous exploration vessel: it’s also a Python library for **web scraping**.  
Unlike general-purpose tools such as HTTrack, which download an entire site before extracting data, Calypso is designed to be **fast and targeted**. It only retrieves the information you need, in an optimized way.  
If the website you want to scrape is supported by the library, **Calypso is the ideal choice**.  

## Installation

You can install **Calypso** directly from **PyPI** with `pip`:

```bash
pip install pycalypso
```

Or from the GitHub repository to get the latest development version:

```bash
git clone https://github.com/Game-K-Hack/calypso.git
cd calypso
pip install -r requirements.txt
```

Make sure you are using Python 3.7 or higher.

## Supported website

| Logo | Name | Address | Function |
| ---- | ---- | ------- | -------- |
| ![Bin.sx logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/__not_found__-resized.png) |  Bin.sx |  [bin.sx](https://paste.bin.sx) |  `get_text_by_id` |
| ![Coomer logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/coomer-resized.png) |  Coomer |  [coomer.st](https://coomer.st/) |  `search`, `get_posts`, `download` |
| ![Ephemeride logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/ephemeride-resized.png) |  Ephemeride |  [ephemeride.com](https://www.ephemeride.com/) |  `get_fete_du_jour`, `get_evenement_du_jour`, `get_diction_du_jour`, `get_citation_du_jour`, `get_proverbe_du_jour`, `get_jour` |
| ![Got any Nudes? logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/gotanynudes-resized.png) |  Got any Nudes? |  [gotanynudes.com](https://gotanynudes.com/) |  `search`, `get_posts`, `download` |
| ![Leaked zone logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/leakedzone-resized.png) |  Leaked zone |  [leakedzone.com](https://leakedzone.com/) |  `search`, `get_posts`, `download` |
| ![Open Food Facts (API V3) logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/openfoodfactsv3-resized.png) |  Open Food Facts (API V3) |  [openfoodfacts.org](https://fr.openfoodfacts.org/) |  `get_products`, `get_list_of_preference_importance_values`, `get_list_of_attribute_groups_and_attributes`, `get_canonical_tags_for_a_list_of_local_tags`, `get_display_tags_in_a_specific_language_for_a_list_of_taxonomy_tags`, `get_taxonomy_suggestions`, `get_tag_knowledge_panels` |
| ![Voir Anime logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/voiranime-resized.png) |  Voir Anime |  [voiranime.com](https://v6.voiranime.com/) |  `search`, `get_anime` |
| ![Voir Drama logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/voirdrama-resized.png) |  Voir Drama |  [voirdrama.org](https://voirdrama.org/) |  `search`, `get_drama` |

### Coming soon

| Logo | Name | Address |
| ---- | ---- | ------- |
| ![Games Theme Songs logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/gamethemesongs.com-resized.png) |  Games Theme Songs |  [gamethemesongs.com](https://gamethemesongs.com/) |
| ![IGDB logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/igdb.com-resized.png) |  IGDB |  [igdb.com](https://www.igdb.com/) |
| ![IMDb logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/imdb.com-resized.png) |  IMDb |  [imdb.com](https://www.imdb.com/) |
| ![ISBN DB logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/isbndb.com-resized.png) |  ISBN DB |  [isbndb.com](https://isbndb.com/) |
| ![JAV Database logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/javdatabase.com-resized.png) |  JAV Database |  [javdatabase.com](https://www.javdatabase.com/) |
| ![Jikan logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/jikan.moe-resized.png) |  Jikan |  [jikan.moe](https://jikan.moe/) |
| ![MusicBrainz logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/musicbrainz.org-resized.png) |  MusicBrainz |  [musicbrainz.org](https://musicbrainz.org/) |
| ![MyAnimeList logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/myanimelist.net-resized.png) |  MyAnimeList |  [myanimelist.net](https://myanimelist.net/) |
| ![Nautiljon logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/nautiljon.com-resized.png) |  Nautiljon |  [nautiljon.com](https://www.nautiljon.com/) |
| ![PictAero logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/pictaero.com-resized.png) |  PictAero |  [pictaero.com](https://www.pictaero.com/) |
| ![SteamDB logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/steamdb.info-resized.png) |  SteamDB |  [steamdb.info](https://steamdb.info/) |
| ![TMDB logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/themoviedb.org-resized.png) |  TMDB |  [themoviedb.org](https://www.themoviedb.org/) |
| ![TV Theme Tunes logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/televisiontunes.com-resized.png) |  TV Theme Tunes |  [televisiontunes.com](https://www.televisiontunes.com/) |
| ![Tv ad songs logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/tvadsongs.com-resized.png) |  Tv ad songs |  [tvadsongs.com](http://tvadsongs.com/) |
| ![TwitchTracker logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/twitchtracker.com-resized.png) |  TwitchTracker |  [twitchtracker.com](https://twitchtracker.com/) |
| ![YARN logo](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/yarn.co-resized.png) |  YARN |  [yarn.co](https://yarn.co/) |

