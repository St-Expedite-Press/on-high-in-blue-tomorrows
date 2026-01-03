# Appendix A: Corpus and Source Registry

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This appendix defines **what the corpus is**, how it is mapped to stable internal identifiers, and how sources/variants are registered without collapsing variance.

It supports two operational modes:

- **Bootstrap mode:** one canonical source image per plate (435 total)
- **Variance mode:** multiple variants per plate across institutions/pipelines, all preserved

---

## A.1 Corpus boundary statement (non-negotiable)

- The Audubon plate corpus is exactly **435 plates**: plate_number ∈ [1, 435].
- Internal identity is stable: plate_id = plate-### (zero-padded).
- No plate may be added/removed without an explicit corpus version bump and an exclusion/inclusion log entry.

---

## A.2 Plate identity fields (canonical)

Canonical fields for each plate (identity; not ML output):

- plate_id (string; ^plate-\\d{3}$)
- plate_number (int; 1–435)
- title (string)
- slug (string)

Common additional identity fields (optional but recommended):

- scientific_name (nullable string)
- common_names (string[])
- notes (nullable string)
- license / credit_line (string)

Important: identity fields may be corrected only to fix factual errors, and such corrections must be logged.

---

## A.3 Primary bootstrap sources (registered)

Bootstrap uses the Nathan Buchar repository wrapper and upstream audubon.org plate URLs.

### A.3.1 Source: nathanbuchar/audubon-bird-plates (repository wrapper)

- URL: https://github.com/nathanbuchar/audubon-bird-plates
- Raw README: https://raw.githubusercontent.com/nathanbuchar/audubon-bird-plates/master/README.md
- Raw plate index (data.json): https://raw.githubusercontent.com/nathanbuchar/audubon-bird-plates/master/data.json
- Terms reference (linked from README): https://www.audubon.org/terms-use
- Required credit line (from README):
  - Courtesy of the John James Audubon Center at Mill Grove, Montgomery County Audubon Collection, and Zebra Publishing.

Acquisition discipline for this source:

- record branch (master) and repo commit SHA at ingestion time
- store checksums for README and data.json snapshots used
- treat plate files as ultimately sourced from the download URLs in data.json

### A.3.2 Source: audubon.org plate hosting

- Plate URL pattern (from data.json):
  - https://www.audubon.org/sites/default/files/boa_plates/plate-<N>-<slug>.jpg
- Terms of Use: https://www.audubon.org/terms-use

Acquisition discipline for this source:

- record access date/time (UTC)
- record response headers when available (ETag, Last-Modified)
- compute and store per-file checksums
- periodically recheck for drift (silent upstream replacement)

---

## A.4 Plate registry (bootstrap mapping table)

This table is a direct normalization of data.json into canonical identity fields.

Columns:

- plate_id: internal stable identifier
- plate_number: 1–435
- title: human title (from data.json:name)
- slug: slug (from data.json:slug)
- fileName: canonical filename (from data.json:fileName)
- download: upstream URL (from data.json:download)

| plate_id | plate_number | title | slug | fileName | download |
|---|---:|---|---|---|---|
| plate-001 | 1 | Wild Turkey | wild-turkey | plate-1-wild-turkey.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-1-wild-turkey.jpg |
| plate-002 | 2 | Yellow-billed Cuckoo | yellow-billed-cuckoo | plate-2-yellow-billed-cuckoo.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-2-yellow-billed-cuckoo.jpg |
| plate-003 | 3 | Prothonotary Warbler | prothonotary-warbler | plate-3-prothonotary-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-3-prothonotary-warbler.jpg |
| plate-004 | 4 | Purple Finch | purple-finch | plate-4-purple-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-4-purple-finch.jpg |
| plate-005 | 5 | Bonaparte's Flycatcher | bonapartes-flycatcher | plate-5-bonapartes-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-5-bonapartes-flycatcher.jpg |
| plate-006 | 6 | Great American Hen & Young | great-american-hen-young | plate-6-great-american-hen-young.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-6-great-american-hen-young.jpg |
| plate-007 | 7 | Purple Grakle, or Common Crow Blackbird | purple-grakle | plate-7-purple-grakle.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-7-purple-grakle.jpg |
| plate-008 | 8 | White throated Sparrow | white-throated-sparrow | plate-8-white-throated-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-8-white-throated-sparrow.jpg |
| plate-009 | 9 | Selby's Fly catcher | selbys-fly-catcher | plate-9-selbys-fly-catcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-9-selbys-fly-catcher.jpg |
| plate-010 | 10 | Brown Lark | brown-lark | plate-10-brown-lark.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-10-brown-lark.jpg |
| plate-011 | 11 | Bird of Washington | bird-washington | plate-11-bird-washington.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-11-bird-washington.jpg |
| plate-012 | 12 | Baltimore Oriole | baltimore-oriole | plate-12-baltimore-oriole.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-12-baltimore-oriole.jpg |
| plate-013 | 13 | Snow Bird | snow-bird | plate-13-snow-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-13-snow-bird.jpg |
| plate-014 | 14 | Prairie Warbler | prairie-warbler | plate-14-prairie-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-14-prairie-warbler.jpg |
| plate-015 | 15 | Blue Yellow back Warbler | blue-yellow-backed-warbler | plate-15-blue-yellow-backed-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-15-blue-yellow-backed-warbler.jpg |
| plate-016 | 16 | Great-footed Hawk | great-footed-hawk | plate-16-great-footed-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-16-great-footed-hawk.jpg |
| plate-017 | 17 | Carolina Pigeon | carolina-pigeon | plate-17-carolina-pigeon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-17-carolina-pigeon.jpg |
| plate-018 | 18 | Bewick's Wren | bewicks-wren | plate-18-bewicks-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-18-bewicks-wren.jpg |
| plate-019 | 19 | Louisiana Water Thrush | louisiana-water-thrush | plate-19-louisiana-water-thrush.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-19-louisiana-water-thrush.jpg |
| plate-020 | 20 | Blue-winged Yellow Warbler | blue-winged-yellow-warbler | plate-20-blue-winged-yellow-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-20-blue-winged-yellow-warbler.jpg |
| plate-021 | 21 | Mocking Bird | mocking-bird | plate-21-mocking-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-21-mocking-bird.jpg |
| plate-022 | 22 | Purple Martin | purple-martin | plate-22-purple-martin.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-22-purple-martin.jpg |
| plate-023 | 23 | Yellow-breasted Warbler | yellow-breasted-warbler | plate-23-yellow-breasted-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-23-yellow-breasted-warbler.jpg |
| plate-024 | 24 | Roscoe's Yellow-throat | roscoes-yellow-throat | plate-24-roscoes-yellow-throat.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-24-roscoes-yellow-throat.jpg |
| plate-025 | 25 | Song Sparrow | song-sparrow | plate-25-song-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-25-song-sparrow.jpg |
| plate-026 | 26 | Carolina Parrot | carolina-parrot | plate-26-carolina-parrot.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-26-carolina-parrot.jpg |
| plate-027 | 27 | Red headed Woodpecker | red-headed-woodpecker | plate-27-red-headed-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-27-red-headed-woodpecker.jpg |
| plate-028 | 28 | Vireo Solitarius | vireo-solitarius | plate-28-vireo-solitarius.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-28-vireo-solitarius.jpg |
| plate-029 | 29 | Towee Bunting | towee-bunting | plate-29-towee-bunting.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-29-towee-bunting.jpg |
| plate-030 | 30 | Vigors Vireo | vigors-vireo | plate-30-vigors-vireo.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-30-vigors-vireo.jpg |
| plate-031 | 31 | White-headed Eagle | white-headed-eagle | plate-31-white-headed-eagle.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-31-white-headed-eagle.jpg |
| plate-032 | 32 | Black-billed Cuckoo | black-billed-cuckoo | plate-32-black-billed-cuckoo.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-32-black-billed-cuckoo.jpg |
| plate-033 | 33 | American Goldfinch | american-goldfinch | plate-33-american-goldfinch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-33-american-goldfinch.jpg |
| plate-034 | 34 | Worm eating Warbler | worm-eating-warbler | plate-34-worm-eating-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-34-worm-eating-warbler.jpg |
| plate-035 | 35 | Children's Warbler | childrens-warbler | plate-35-childrens-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-35-childrens-warbler.jpg |
| plate-036 | 36 | Stanley Hawk | stanley-hawk | plate-36-stanley-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-36-stanley-hawk.jpg |
| plate-037 | 37 | Golden-winged Woodpecker | golden-winged-woodpecker | plate-37-golden-winged-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-37-golden-winged-woodpecker.jpg |
| plate-038 | 38 | Kentucky Warbler | kentucky-warbler | plate-38-kentucky-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-38-kentucky-warbler.jpg |
| plate-039 | 39 | Crested Titmouse | crested-titmouse | plate-39-crested-titmouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-39-crested-titmouse.jpg |
| plate-040 | 40 | American Redstart | american-redstart | plate-40-american-redstart.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-40-american-redstart.jpg |
| plate-041 | 41 | Ruffed Grouse | ruffed-grouse | plate-41-ruffed-grouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-41-ruffed-grouse.jpg |
| plate-042 | 42 | Orchard Oriole | orchard-oriole | plate-42-orchard-oriole.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-42-orchard-oriole.jpg |
| plate-043 | 43 | Cedar Bird | cedar-bird | plate-43-cedar-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-43-cedar-bird.jpg |
| plate-044 | 44 | Summer Red Bird | summer-red-bird | plate-44-summer-red-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-44-summer-red-bird.jpg |
| plate-045 | 45 | Traill's Flycatcher | traills-flycatcher | plate-45-traills-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-45-traills-flycatcher.jpg |
| plate-046 | 46 | Barred Owl | barred-owl | plate-46-barred-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-46-barred-owl.jpg |
| plate-047 | 47 | Ruby-throated Humming Bird | ruby-throated-humming-bird | plate-47-ruby-throated-humming-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-47-ruby-throated-humming-bird.jpg |
| plate-048 | 48 | Azure Warbler | azure-warbler | plate-48-azure-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-48-azure-warbler.jpg |
| plate-049 | 49 | Blue-green Warbler | blue-green-warbler | plate-49-blue-green-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-49-blue-green-warbler.jpg |
| plate-050 | 50 | Black & Yellow Warbler | black-yellow-warbler | plate-50-black-yellow-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-50-black-yellow-warbler.jpg |
| plate-051 | 51 | Red-tailed Hawk | red-tailed-hawk | plate-51-red-tailed-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-51-red-tailed-hawk.jpg |
| plate-052 | 52 | Chuck-will's Widow | chuck-wills-widow | plate-52-chuck-wills-widow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-52-chuck-wills-widow.jpg |
| plate-053 | 53 | Painted Finch | painted-finch | plate-53-painted-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-53-painted-finch.jpg |
| plate-054 | 54 | Rice Bird | rice-bird | plate-54-rice-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-54-rice-bird.jpg |
| plate-055 | 55 | Cuvier's Kinglet | cuviers-kinglet | plate-55-cuviers-kinglet.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-55-cuviers-kinglet.jpg |
| plate-056 | 56 | Red-shouldered Hawk | red-shouldered-hawk | plate-56-red-shouldered-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-56-red-shouldered-hawk.jpg |
| plate-057 | 57 | Loggerhead Shrike | loggerhead-shrike | plate-57-loggerhead-shrike.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-57-loggerhead-shrike.jpg |
| plate-058 | 58 | Hermit Thrush | hermit-thrush | plate-58-hermit-thrush.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-58-hermit-thrush.jpg |
| plate-059 | 59 | Chestnut-sided Warbler | chestnut-sided-warbler | plate-59-chestnut-sided-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-59-chestnut-sided-warbler.jpg |
| plate-060 | 60 | Carbonated Warbler | carbonated-warbler | plate-60-carbonated-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-60-carbonated-warbler.jpg |
| plate-061 | 61 | Great Horned Owl | great-horned-owl | plate-61-great-horned-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-61-great-horned-owl.jpg |
| plate-062 | 62 | Passenger Pigeon | passenger-pigeon | plate-62-passenger-pigeon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-62-passenger-pigeon.jpg |
| plate-063 | 63 | White-eyed Flycatcher, or Vireo | white-eyed-flycatcher | plate-63-white-eyed-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-63-white-eyed-flycatcher.jpg |
| plate-064 | 64 | Swamp Sparrow | swamp-sparrow | plate-64-swamp-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-64-swamp-sparrow.jpg |
| plate-065 | 65 | Rathbone Warbler | rathbone-warbler | plate-65-rathbone-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-65-rathbone-warbler.jpg |
| plate-066 | 66 | Ivory-billed Woodpecker | ivory-billed-woodpecker | plate-66-ivory-billed-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-66-ivory-billed-woodpecker.jpg |
| plate-067 | 67 | Red winged Starling, or Marsh Blackbird | red-winged-starling | plate-67-red-winged-starling.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-67-red-winged-starling.jpg |
| plate-068 | 68 | Republican, or Cliff Swallow | republican-or-cliff-swallow | plate-68-republican-or-cliff-swallow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-68-republican-or-cliff-swallow.jpg |
| plate-069 | 69 | Bay-breasted Warbler | bay-breasted-warbler | plate-69-bay-breasted-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-69-bay-breasted-warbler.jpg |
| plate-070 | 70 | Henslow's Bunting | henslows-bunting | plate-70-henslows-bunting.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-70-henslows-bunting.jpg |
| plate-071 | 71 | Winter Hawk | winter-hawk | plate-71-winter-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-71-winter-hawk.jpg |
| plate-072 | 72 | Swallow-tailed Hawk | swallow-tailed-hawk | plate-72-swallow-tailed-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-72-swallow-tailed-hawk.jpg |
| plate-073 | 73 | Wood Thrush | wood-thrush | plate-73-wood-thrush.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-73-wood-thrush.jpg |
| plate-074 | 74 | Indigo Bird | indigo-bird | plate-74-indigo-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-74-indigo-bird.jpg |
| plate-075 | 75 | Le Petit Caporal | le-petit-caporal | plate-75-le-petit-caporal.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-75-le-petit-caporal.jpg |
| plate-076 | 76 | Virginian Partridge | virginian-partridge | plate-76-virginian-partridge.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-76-virginian-partridge.jpg |
| plate-077 | 77 | Belted Kingfisher | belted-kingfisher | plate-77-belted-kingfisher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-77-belted-kingfisher.jpg |
| plate-078 | 78 | Great Carolina Wren | great-carolina-wren | plate-78-great-carolina-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-78-great-carolina-wren.jpg |
| plate-079 | 79 | Tyrant Fly-catcher | tyrant-fly-catcher | plate-79-tyrant-fly-catcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-79-tyrant-fly-catcher.jpg |
| plate-080 | 80 | Prairie Titlark | prairie-titlark | plate-80-prairie-titlark.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-80-prairie-titlark.jpg |
| plate-081 | 81 | Fish Hawk, or Osprey | fish-hawk-or-osprey | plate-81-fish-hawk-or-osprey.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-81-fish-hawk-or-osprey.jpg |
| plate-082 | 82 | Whip-poor-will | whip-poor-will | plate-82-whip-poor-will.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-82-whip-poor-will.jpg |
| plate-083 | 83 | House Wren | house-wren | plate-83-house-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-83-house-wren.jpg |
| plate-084 | 84 | Blue-Grey Fly-catcher | blue-grey-fly-catcher | plate-84-blue-grey-fly-catcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-84-blue-grey-fly-catcher.jpg |
| plate-085 | 85 | Yellow Throated Warbler | yellow-throated-warbler | plate-85-yellow-throated-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-85-yellow-throated-warbler.jpg |
| plate-086 | 86 | Black Warrior | black-warrior | plate-86-black-warrior.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-86-black-warrior.jpg |
| plate-087 | 87 | Florida Jay | florida-jay | plate-87-florida-jay.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-87-florida-jay.jpg |
| plate-088 | 88 | Autumnal Warbler | autumnal-warbler | plate-88-autumnal-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-88-autumnal-warbler.jpg |
| plate-089 | 89 | Nashville Warbler | nashville-warbler | plate-89-nashville-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-89-nashville-warbler.jpg |
| plate-090 | 90 | Black & White Creeper | black-white-creeper | plate-90-black-white-creeper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-90-black-white-creeper.jpg |
| plate-091 | 91 | Broad-winged Hawk | broad-winged-hawk | plate-91-broad-winged-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-91-broad-winged-hawk.jpg |
| plate-092 | 92 | Pigeon Hawk | pigeon-hawk | plate-92-pigeon-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-92-pigeon-hawk.jpg |
| plate-093 | 93 | Seaside Finch | seaside-finch | plate-93-seaside-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-93-seaside-finch.jpg |
| plate-094 | 94 | Grass Finch, or Bay-winged Bunting | grass-finch | plate-94-grass-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-94-grass-finch.jpg |
| plate-095 | 95 | Blue-eyed yellow Warbler | blue-eyed-yellow-warbler | plate-95-blue-eyed-yellow-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-95-blue-eyed-yellow-warbler.jpg |
| plate-096 | 96 | Columbia Jay | columbia-jay | plate-96-columbia-jay.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-96-columbia-jay.jpg |
| plate-097 | 97 | Little Screech Owl | little-screech-owl | plate-97-little-screech-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-97-little-screech-owl.jpg |
| plate-098 | 98 | White-bellied Swallow | white-bellied-swallow | plate-98-white-bellied-swallow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-98-white-bellied-swallow.jpg |
| plate-099 | 99 | Cow-pen Bird | cow-pen-bird | plate-99-cow-pen-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-99-cow-pen-bird.jpg |
| plate-100 | 100 | Marsh Wren | marsh-wren | plate-100-marsh-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-100-marsh-wren.jpg |
| plate-101 | 101 | Raven | raven | plate-101-raven.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-101-raven.jpg |
| plate-102 | 102 | Blue Jay | blue-jay | plate-102-blue-jay.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-102-blue-jay.jpg |
| plate-103 | 103 | Canada Warbler | canada-warbler | plate-103-canada-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-103-canada-warbler.jpg |
| plate-104 | 104 | Chipping Sparrow | chipping-sparrow | plate-104-chipping-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-104-chipping-sparrow.jpg |
| plate-105 | 105 | Red-breasted Nuthatch | red-breasted-nuthatch | plate-105-red-breasted-nuthatch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-105-red-breasted-nuthatch.jpg |
| plate-106 | 106 | Black Vulture, or Carrion Crow | black-vulture-or-carrion-crow | plate-106-black-vulture-or-carrion-crow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-106-black-vulture-or-carrion-crow.jpg |
| plate-107 | 107 | Canada Jay | canada-jay | plate-107-canada-jay.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-107-canada-jay.jpg |
| plate-108 | 108 | Fox-coloured Sparrow | fox-coloured-sparrow | plate-108-fox-coloured-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-108-fox-coloured-sparrow.jpg |
| plate-109 | 109 | Savannah Finch | savannah-finch | plate-109-savannah-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-109-savannah-finch.jpg |
| plate-110 | 110 | Hooded Warbler | hooded-warbler | plate-110-hooded-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-110-hooded-warbler.jpg |
| plate-111 | 111 | Pileated Woodpecker | pileated-woodpecker | plate-111-pileated-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-111-pileated-woodpecker.jpg |
| plate-112 | 112 | Downy Woodpecker | downy-woodpecker | plate-112-downy-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-112-downy-woodpecker.jpg |
| plate-113 | 113 | Blue-bird | blue-bird | plate-113-blue-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-113-blue-bird.jpg |
| plate-114 | 114 | White-crowned Sparrow | white-crowned-sparrow | plate-114-white-crowned-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-114-white-crowned-sparrow.jpg |
| plate-115 | 115 | Wood Pewee | wood-pewee | plate-115-wood-pewee.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-115-wood-pewee.jpg |
| plate-116 | 116 | Ferruginous Thrush | ferruginous-thrush | plate-116-ferruginous-thrush.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-116-ferruginous-thrush.jpg |
| plate-117 | 117 | Mississippi Kite | mississippi-kite | plate-117-mississippi-kite.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-117-mississippi-kite.jpg |
| plate-118 | 118 | Warbling Flycatcher | warbling-flycatcher | plate-118-warbling-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-118-warbling-flycatcher.jpg |
| plate-119 | 119 | Yellow-throated Vireo | yellow-throated-vireo | plate-119-yellow-throated-vireo.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-119-yellow-throated-vireo.jpg |
| plate-120 | 120 | Pewit Flycatcher | pewit-flycatcher | plate-120-pewit-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-120-pewit-flycatcher.jpg |
| plate-121 | 121 | Snowy Owl | snowy-owl | plate-121-snowy-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-121-snowy-owl.jpg |
| plate-122 | 122 | Blue Grosbeak | blue-grosbeak | plate-122-blue-grosbeak.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-122-blue-grosbeak.jpg |
| plate-123 | 123 | Black & Yellow Warblers | black-yellow-warblers | plate-123-black-yellow-warblers.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-123-black-yellow-warblers.jpg |
| plate-124 | 124 | Green Black-capt Flycatcher | green-black-capt-flycatcher | plate-124-green-black-capt-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-124-green-black-capt-flycatcher.jpg |
| plate-125 | 125 | Brown-headed Nuthatch | brown-headed-nuthatch | plate-125-brown-headed-nuthatch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-125-brown-headed-nuthatch.jpg |
| plate-126 | 126 | White-headed Eagle | white-headed-eagle | plate-126-white-headed-eagle.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-126-white-headed-eagle.jpg |
| plate-127 | 127 | Rose-breasted Grosbeak | rose-breasted-grosbeak | plate-127-rose-breasted-grosbeak.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-127-rose-breasted-grosbeak.jpg |
| plate-128 | 128 | Cat Bird | cat-bird | plate-128-cat-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-128-cat-bird.jpg |
| plate-129 | 129 | Great Crested Flycatcher | great-crested-flycatcher | plate-129-great-crested-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-129-great-crested-flycatcher.jpg |
| plate-130 | 130 | Yellow-winged Sparrow | yellow-winged-sparrow | plate-130-yellow-winged-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-130-yellow-winged-sparrow.jpg |
| plate-131 | 131 | American Robin | american-robin | plate-131-american-robin.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-131-american-robin.jpg |
| plate-132 | 132 | Three-toed Woodpecker | three-toed-woodpecker | plate-132-three-toed-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-132-three-toed-woodpecker.jpg |
| plate-133 | 133 | Black-poll Warbler | black-poll-warbler | plate-133-black-poll-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-133-black-poll-warbler.jpg |
| plate-134 | 134 | Hemlock Warbler | hemlock-warbler | plate-134-hemlock-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-134-hemlock-warbler.jpg |
| plate-135 | 135 | Blackburnian Warbler | blackburnian-warbler | plate-135-blackburnian-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-135-blackburnian-warbler.jpg |
| plate-136 | 136 | Meadow Lark | meadow-lark | plate-136-meadow-lark.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-136-meadow-lark.jpg |
| plate-137 | 137 | Yellow-breasted Chat | yellow-breasted-chat | plate-137-yellow-breasted-chat.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-137-yellow-breasted-chat.jpg |
| plate-138 | 138 | Connecticut Warbler | connecticut-warbler | plate-138-connecticut-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-138-connecticut-warbler.jpg |
| plate-139 | 139 | Field Sparrow | field-sparrow | plate-139-field-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-139-field-sparrow.jpg |
| plate-140 | 140 | Pine Creeping Warbler | pine-creeping-warbler | plate-140-pine-creeping-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-140-pine-creeping-warbler.jpg |
| plate-141 | 141 | Goshawk and Stanley Hawk | goshawk-and-stanley-hawk | plate-141-goshawk-and-stanley-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-141-goshawk-and-stanley-hawk.jpg |
| plate-142 | 142 | American Sparrow Hawk | american-sparrow-hawk | plate-142-american-sparrow-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-142-american-sparrow-hawk.jpg |
| plate-143 | 143 | Golden-crowned Thrush | golden-crowned-thrush | plate-143-golden-crowned-thrush.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-143-golden-crowned-thrush.jpg |
| plate-144 | 144 | Small Green Crested Flycatcher | small-green-crested-flycatcher | plate-144-small-green-crested-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-144-small-green-crested-flycatcher.jpg |
| plate-145 | 145 | Yellow Red-poll Warbler | yellow-red-poll-warbler | plate-145-yellow-red-poll-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-145-yellow-red-poll-warbler.jpg |
| plate-146 | 146 | Fish Crow | fish-crow | plate-146-fish-crow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-146-fish-crow.jpg |
| plate-147 | 147 | Night Hawk | night-hawk | plate-147-night-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-147-night-hawk.jpg |
| plate-148 | 148 | Pine Swamp Warbler | pine-swamp-warbler | plate-148-pine-swamp-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-148-pine-swamp-warbler.jpg |
| plate-149 | 149 | Sharp-tailed Finch | sharp-tailed-finch | plate-149-sharp-tailed-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-149-sharp-tailed-finch.jpg |
| plate-150 | 150 | Red-eyed Vireo | red-eyed-vireo | plate-150-red-eyed-vireo.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-150-red-eyed-vireo.jpg |
| plate-151 | 151 | Turkey Buzzard | turkey-buzzard | plate-151-turkey-buzzard.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-151-turkey-buzzard.jpg |
| plate-152 | 152 | White-breasted Black-capped Nuthatch | white-breasted-black-capped-nuthatch | plate-152-white-breasted-black-capped-nuthatch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-152-white-breasted-black-capped-nuthatch.jpg |
| plate-153 | 153 | Yellow-crown Warbler | yellow-crown-warbler | plate-153-yellow-crown-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-153-yellow-crown-warbler.jpg |
| plate-154 | 154 | Tennessee Warbler | tennessee-warbler | plate-154-tennessee-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-154-tennessee-warbler.jpg |
| plate-155 | 155 | Black-throated Blue Warbler | black-throated-blue-warbler | plate-155-black-throated-blue-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-155-black-throated-blue-warbler.jpg |
| plate-156 | 156 | American Crow | american-crow | plate-156-american-crow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-156-american-crow.jpg |
| plate-157 | 157 | Rusty Grakle | rusty-grakle | plate-157-rusty-grakle.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-157-rusty-grakle.jpg |
| plate-158 | 158 | American Swift | american-swift | plate-158-american-swift.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-158-american-swift.jpg |
| plate-159 | 159 | Cardinal Grosbeak | cardinal-grosbeak | plate-159-cardinal-grosbeak.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-159-cardinal-grosbeak.jpg |
| plate-160 | 160 | Carolina Titmouse | carolina-titmouse | plate-160-carolina-titmouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-160-carolina-titmouse.jpg |
| plate-161 | 161 | Brasilian Caracara Eagle | brasilian-caracara-eagle | plate-161-brasilian-caracara-eagle.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-161-brasilian-caracara-eagle.jpg |
| plate-162 | 162 | Zenaida Dove | zenaida-dove | plate-162-zenaida-dove.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-162-zenaida-dove.jpg |
| plate-163 | 163 | Palm Warbler | palm-warbler | plate-163-palm-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-163-palm-warbler.jpg |
| plate-164 | 164 | Tawny Thrush | tawny-thrush | plate-164-tawny-thrush.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-164-tawny-thrush.jpg |
| plate-165 | 165 | Bachman's Finch | bachmans-finch | plate-165-bachmans-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-165-bachmans-finch.jpg |
| plate-166 | 166 | Rough-legged Falcon | rough-legged-falcon | plate-166-rough-legged-falcon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-166-rough-legged-falcon.jpg |
| plate-167 | 167 | Key-west Dove | key-west-dove | plate-167-key-west-dove.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-167-key-west-dove.jpg |
| plate-168 | 168 | Fork-tailed Flycatcher | fork-tailed-flycatcher | plate-168-fork-tailed-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-168-fork-tailed-flycatcher.jpg |
| plate-169 | 169 | Mangrove Cuckoo | mangrove-cuckoo | plate-169-mangrove-cuckoo.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-169-mangrove-cuckoo.jpg |
| plate-170 | 170 | Piping Flycatcher | piping-flycatcher | plate-170-piping-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-170-piping-flycatcher.jpg |
| plate-171 | 171 | Barn Owl | barn-owl | plate-171-barn-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-171-barn-owl.jpg |
| plate-172 | 172 | Blue-headed Pigeon | blue-headed-pigeon | plate-172-blue-headed-pigeon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-172-blue-headed-pigeon.jpg |
| plate-173 | 173 | Barn Swallow | barn-swallow | plate-173-barn-swallow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-173-barn-swallow.jpg |
| plate-174 | 174 | Olive sided Flycatcher | olive-sided-flycatcher | plate-174-olive-sided-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-174-olive-sided-flycatcher.jpg |
| plate-175 | 175 | Nuttall's lesser-marsh Wren | nuttalls-lesser-marsh-wren | plate-175-nuttalls-lesser-marsh-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-175-nuttalls-lesser-marsh-wren.jpg |
| plate-176 | 176 | Spotted Grouse | spotted-grouse | plate-176-spotted-grouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-176-spotted-grouse.jpg |
| plate-177 | 177 | White-crowned Pigeon | white-crowned-pigeon | plate-177-white-crowned-pigeon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-177-white-crowned-pigeon.jpg |
| plate-178 | 178 | Orange-crowned Warbler | orange-crowned-warbler | plate-178-orange-crowned-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-178-orange-crowned-warbler.jpg |
| plate-179 | 179 | Wood Wren | wood-wren | plate-179-wood-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-179-wood-wren.jpg |
| plate-180 | 180 | Pine Finch | pine-finch | plate-180-pine-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-180-pine-finch.jpg |
| plate-181 | 181 | Golden Eagle | golden-eagle | plate-181-golden-eagle.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-181-golden-eagle.jpg |
| plate-182 | 182 | Ground Dove | ground-dove | plate-182-ground-dove.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-182-ground-dove.jpg |
| plate-183 | 183 | American Golden crested-Wren | american-golden-crested-wren | plate-183-american-golden-crested-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-183-american-golden-crested-wren.jpg |
| plate-184 | 184 | Mango Hummingbird | mango-hummingbird | plate-184-mango-hummingbird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-184-mango-hummingbird.jpg |
| plate-185 | 185 | Bachman's Warbler | bachmans-warbler | plate-185-bachmans-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-185-bachmans-warbler.jpg |
| plate-186 | 186 | Pinnated Grouse | pinnated-grouse | plate-186-pinnated-grouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-186-pinnated-grouse.jpg |
| plate-187 | 187 | Boat-tailed Grackle | boat-tailed-grackle | plate-187-boat-tailed-grackle.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-187-boat-tailed-grackle.jpg |
| plate-188 | 188 | Tree Sparrow | tree-sparrow | plate-188-tree-sparrow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-188-tree-sparrow.jpg |
| plate-189 | 189 | Snow Bunting | snow-bunting | plate-189-snow-bunting.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-189-snow-bunting.jpg |
| plate-190 | 190 | Yellow bellied Woodpecker | yellow-bellied-woodpecker | plate-190-yellow-bellied-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-190-yellow-bellied-woodpecker.jpg |
| plate-191 | 191 | Willow Grouse, or Large Ptarmigan | willow-grouse | plate-191-willow-grouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-191-willow-grouse.jpg |
| plate-192 | 192 | Great cinereous Shrike, or Butcher Bird | great-cinereous-shrike-or-butcher-bird | plate-192-great-cinereous-shrike-or-butcher-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-192-great-cinereous-shrike-or-butcher-bird.jpg |
| plate-193 | 193 | Lincoln Finch | lincoln-finch | plate-193-lincoln-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-193-lincoln-finch.jpg |
| plate-194 | 194 | Canadian Titmouse | canadian-titmouse | plate-194-canadian-titmouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-194-canadian-titmouse.jpg |
| plate-195 | 195 | Ruby crowned Wren | ruby-crowned-wren | plate-195-ruby-crowned-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-195-ruby-crowned-wren.jpg |
| plate-196 | 196 | Labrador Falcon | labrador-falcon | plate-196-labrador-falcon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-196-labrador-falcon.jpg |
| plate-197 | 197 | American Crossbill | american-crossbill | plate-197-american-crossbill.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-197-american-crossbill.jpg |
| plate-198 | 198 | Brown headed Worm eating Warbler | brown-headed-worm-eating-warbler | plate-198-brown-headed-worm-eating-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-198-brown-headed-worm-eating-warbler.jpg |
| plate-199 | 199 | Little Owl | little-owl | plate-199-little-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-199-little-owl.jpg |
| plate-200 | 200 | Shore Lark | shore-lark | plate-200-shore-lark.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-200-shore-lark.jpg |
| plate-201 | 201 | Canada Goose | canada-goose | plate-201-canada-goose.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-201-canada-goose.jpg |
| plate-202 | 202 | Red-Throated Diver | red-throated-diver | plate-202-red-throated-diver.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-202-red-throated-diver.jpg |
| plate-203 | 203 | Fresh Water Marsh Hen | fresh-water-marsh-hen | plate-203-fresh-water-marsh-hen.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-203-fresh-water-marsh-hen.jpg |
| plate-204 | 204 | Salt Water Marsh Hen | salt-water-marsh-hen | plate-204-salt-water-marsh-hen.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-204-salt-water-marsh-hen.jpg |
| plate-205 | 205 | Virginia Rail | virginia-rail | plate-205-virginia-rail.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-205-virginia-rail.jpg |
| plate-206 | 206 | Summer, or Wood Duck | summer-or-wood-duck | plate-206-summer-or-wood-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-206-summer-or-wood-duck.jpg |
| plate-207 | 207 | Booby Gannet | booby-gannet | plate-207-booby-gannet.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-207-booby-gannet.jpg |
| plate-208 | 208 | Esquimaux Curlew | esquimaux-curlew | plate-208-esquimaux-curlew.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-208-esquimaux-curlew.jpg |
| plate-209 | 209 | Wilson's Plover | wilsons-plover | plate-209-wilsons-plover.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-209-wilsons-plover.jpg |
| plate-210 | 210 | Least Bittern | least-bittern | plate-210-least-bittern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-210-least-bittern.jpg |
| plate-211 | 211 | Great blue Heron | great-blue-heron | plate-211-great-blue-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-211-great-blue-heron.jpg |
| plate-212 | 212 | Common American Gull | common-american-gull | plate-212-common-american-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-212-common-american-gull.jpg |
| plate-213 | 213 | Puffin | puffin | plate-213-puffin.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-213-puffin.jpg |
| plate-214 | 214 | Razor Bill | razor-bill | plate-214-razor-bill.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-214-razor-bill.jpg |
| plate-215 | 215 | Hyperborean phalarope | hyperborean-phalarope | plate-215-hyperborean-phalarope.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-215-hyperborean-phalarope.jpg |
| plate-216 | 216 | Wood Ibiss | wood-ibiss | plate-216-wood-ibiss.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-216-wood-ibiss.jpg |
| plate-217 | 217 | Louisiana Heron | louisiana-heron | plate-217-louisiana-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-217-louisiana-heron.jpg |
| plate-218 | 218 | Foolish Guillemot | foolish-guillemot | plate-218-foolish-guillemot.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-218-foolish-guillemot.jpg |
| plate-219 | 219 | Black Guillemot | black-guillemot | plate-219-black-guillemot.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-219-black-guillemot.jpg |
| plate-220 | 220 | Piping Plover | piping-plover | plate-220-piping-plover.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-220-piping-plover.jpg |
| plate-221 | 221 | Mallard Duck | mallard-duck | plate-221-mallard-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-221-mallard-duck.jpg |
| plate-222 | 222 | White Ibis | white-ibis | plate-222-white-ibis.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-222-white-ibis.jpg |
| plate-223 | 223 | Pied oyster-catcher | pied-oyster-catcher | plate-223-pied-oyster-catcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-223-pied-oyster-catcher.jpg |
| plate-224 | 224 | Kittiwake Gull | kittiwake-gull | plate-224-kittiwake-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-224-kittiwake-gull.jpg |
| plate-225 | 225 | Kildeer Plover | kildeer-plover | plate-225-kildeer-plover.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-225-kildeer-plover.jpg |
| plate-226 | 226 | Hooping Crane | hooping-crane | plate-226-hooping-crane.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-226-hooping-crane.jpg |
| plate-227 | 227 | Pin-tailed Duck | pin-tailed-duck | plate-227-pin-tailed-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-227-pin-tailed-duck.jpg |
| plate-228 | 228 | Green winged Teal | green-winged-teal | plate-228-green-winged-teal.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-228-green-winged-teal.jpg |
| plate-229 | 229 | Scaup Duck | scaup-duck | plate-229-scaup-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-229-scaup-duck.jpg |
| plate-230 | 230 | Sanderling | sanderling | plate-230-sanderling.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-230-sanderling.jpg |
| plate-231 | 231 | Long-billed Curlew | long-billed-curlew | plate-231-long-billed-curlew.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-231-long-billed-curlew.jpg |
| plate-232 | 232 | Hooded Merganser | hooded-merganser | plate-232-hooded-merganser.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-232-hooded-merganser.jpg |
| plate-233 | 233 | Sora, or Rail | sora-or-rail | plate-233-sora-or-rail.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-233-sora-or-rail.jpg |
| plate-234 | 234 | Ring-necked Duck | ring-necked-duck | plate-234-ring-necked-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-234-ring-necked-duck.jpg |
| plate-235 | 235 | Sooty Tern | sooty-tern | plate-235-sooty-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-235-sooty-tern.jpg |
| plate-236 | 236 | Night Heron, or Qua bird | night-heron | plate-236-night-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-236-night-heron.jpg |
| plate-237 | 237 | Hudsonian Curlew | hudsonian-curlew | plate-237-hudsonian-curlew.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-237-hudsonian-curlew.jpg |
| plate-238 | 238 | Great Marbled Godwit | great-marbled-godwit | plate-238-great-marbled-godwit.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-238-great-marbled-godwit.jpg |
| plate-239 | 239 | American Coot | american-coot | plate-239-american-coot.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-239-american-coot.jpg |
| plate-240 | 240 | Roseate Tern | roseate-tern | plate-240-roseate-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-240-roseate-tern.jpg |
| plate-241 | 241 | Black Backed Gull | black-backed-gull | plate-241-black-backed-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-241-black-backed-gull.jpg |
| plate-242 | 242 | Snowy Heron, or White Egret | snowy-heron | plate-242-snowy-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-242-snowy-heron.jpg |
| plate-243 | 243 | American Snipe | american-snipe | plate-243-american-snipe.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-243-american-snipe.jpg |
| plate-244 | 244 | Common Gallinule | common-gallinule | plate-244-common-gallinule.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-244-common-gallinule.jpg |
| plate-245 | 245 | Uria Brunnichi | uria-brunnichi | plate-245-uria-brunnichi.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-245-uria-brunnichi.jpg |
| plate-246 | 246 | Eider Duck | eider-duck | plate-246-eider-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-246-eider-duck.jpg |
| plate-247 | 247 | Velvet Duck | velvet-duck | plate-247-velvet-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-247-velvet-duck.jpg |
| plate-248 | 248 | American Pied-billed | american-pied-billed | plate-248-american-pied-billed.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-248-american-pied-billed.jpg |
| plate-249 | 249 | Tufted Auk | tufted-auk | plate-249-tufted-auk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-249-tufted-auk.jpg |
| plate-250 | 250 | Arctic Tern | arctic-tern | plate-250-arctic-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-250-arctic-tern.jpg |
| plate-251 | 251 | Brown Pelican | brown-pelican | plate-251-brown-pelican.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-251-brown-pelican.jpg |
| plate-252 | 252 | Florida Cormorant | florida-cormorant | plate-252-florida-cormorant.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-252-florida-cormorant.jpg |
| plate-253 | 253 | Jager | jager | plate-253-jager.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-253-jager.jpg |
| plate-254 | 254 | Wilson's Phalarope | wilsons-phalarope | plate-254-wilsons-phalarope.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-254-wilsons-phalarope.jpg |
| plate-255 | 255 | Red Phalarope | red-phalarope | plate-255-red-phalarope.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-255-red-phalarope.jpg |
| plate-256 | 256 | Purple Heron | purple-heron | plate-256-purple-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-256-purple-heron.jpg |
| plate-257 | 257 | Double-crested Cormorant | double-crested-cormorant | plate-257-double-crested-cormorant.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-257-double-crested-cormorant.jpg |
| plate-258 | 258 | Hudsonian Godwit | hudsonian-godwit | plate-258-hudsonian-godwit.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-258-hudsonian-godwit.jpg |
| plate-259 | 259 | Horned Grebe | horned-grebe | plate-259-horned-grebe.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-259-horned-grebe.jpg |
| plate-260 | 260 | Fork-tail Petrel | fork-tail-petrel | plate-260-fork-tail-petrel.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-260-fork-tail-petrel.jpg |
| plate-261 | 261 | Hooping Crane | hooping-crane | plate-261-hooping-crane.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-261-hooping-crane.jpg |
| plate-262 | 262 | Tropic Bird | tropic-bird | plate-262-tropic-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-262-tropic-bird.jpg |
| plate-263 | 263 | Pigmy Curlew | pigmy-curlew | plate-263-pigmy-curlew.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-263-pigmy-curlew.jpg |
| plate-264 | 264 | Fulmar Petrel | fulmar-petrel | plate-264-fulmar-petrel.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-264-fulmar-petrel.jpg |
| plate-265 | 265 | Buff breasted Sandpiper | buff-breasted-sandpiper | plate-265-buff-breasted-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-265-buff-breasted-sandpiper.jpg |
| plate-266 | 266 | Common Cormorant | common-cormorant | plate-266-common-cormorant.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-266-common-cormorant.jpg |
| plate-267 | 267 | Arctic Yager | arctic-yager | plate-267-arctic-yager.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-267-arctic-yager.jpg |
| plate-268 | 268 | American Woodcock | american-woodcock | plate-268-american-woodcock.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-268-american-woodcock.jpg |
| plate-269 | 269 | Greenshank | greenshank | plate-269-greenshank.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-269-greenshank.jpg |
| plate-270 | 270 | Stormy Petrel | stormy-petrel | plate-270-stormy-petrel.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-270-stormy-petrel.jpg |
| plate-271 | 271 | Frigate Pelican | frigate-pelican | plate-271-frigate-pelican.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-271-frigate-pelican.jpg |
| plate-272 | 272 | Richardson's Jager | richardsons-jager | plate-272-richardsons-jager.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-272-richardsons-jager.jpg |
| plate-273 | 273 | Cayenne Tern | cayenne-tern | plate-273-cayenne-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-273-cayenne-tern.jpg |
| plate-274 | 274 | Semipalmated Snipe, or Willet | semipalmated-snipe | plate-274-semipalmated-snipe.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-274-semipalmated-snipe.jpg |
| plate-275 | 275 | Noddy Tern | noddy-tern | plate-275-noddy-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-275-noddy-tern.jpg |
| plate-276 | 276 | King Duck | king-duck | plate-276-king-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-276-king-duck.jpg |
| plate-277 | 277 | Hutchins's Barnacle Goose | hutchinss-barnacle-goose | plate-277-hutchinss-barnacle-goose.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-277-hutchinss-barnacle-goose.jpg |
| plate-278 | 278 | Schinz's Sandpiper | schinzs-sandpiper | plate-278-schinzs-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-278-schinzs-sandpiper.jpg |
| plate-279 | 279 | Sandwich Tern | sandwich-tern | plate-279-sandwich-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-279-sandwich-tern.jpg |
| plate-280 | 280 | Black Tern | black-tern | plate-280-black-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-280-black-tern.jpg |
| plate-281 | 281 | Great White Heron | great-white-heron | plate-281-great-white-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-281-great-white-heron.jpg |
| plate-282 | 282 | White-winged silvery Gull | white-winged-silvery-gull | plate-282-white-winged-silvery-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-282-white-winged-silvery-gull.jpg |
| plate-283 | 283 | Wandering Shearwater | wandering-shearwater | plate-283-wandering-shearwater.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-283-wandering-shearwater.jpg |
| plate-284 | 284 | Purple Sandpiper | purple-sandpiper | plate-284-purple-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-284-purple-sandpiper.jpg |
| plate-285 | 285 | Fork-tailed Gull | fork-tailed-gull | plate-285-fork-tailed-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-285-fork-tailed-gull.jpg |
| plate-286 | 286 | White-fronted Goose | white-fronted-goose | plate-286-white-fronted-goose.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-286-white-fronted-goose.jpg |
| plate-287 | 287 | Ivory Gull | ivory-gull | plate-287-ivory-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-287-ivory-gull.jpg |
| plate-288 | 288 | Yellow Shank | yellow-shank | plate-288-yellow-shank.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-288-yellow-shank.jpg |
| plate-289 | 289 | Solitary Sandpiper | solitary-sandpiper | plate-289-solitary-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-289-solitary-sandpiper.jpg |
| plate-290 | 290 | Red backed Sandpiper | red-backed-sandpiper | plate-290-red-backed-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-290-red-backed-sandpiper.jpg |
| plate-291 | 291 | Herring Gull | herring-gull | plate-291-herring-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-291-herring-gull.jpg |
| plate-292 | 292 | Crested Grebe | crested-grebe | plate-292-crested-grebe.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-292-crested-grebe.jpg |
| plate-293 | 293 | Large billed Puffin | large-billed-puffin | plate-293-large-billed-puffin.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-293-large-billed-puffin.jpg |
| plate-294 | 294 | Pectoral Sandpiper | pectoral-sandpiper | plate-294-pectoral-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-294-pectoral-sandpiper.jpg |
| plate-295 | 295 | Manks Shearwater | manks-shearwater | plate-295-manks-shearwater.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-295-manks-shearwater.jpg |
| plate-296 | 296 | Barnacle Goose | barnacle-goose | plate-296-barnacle-goose.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-296-barnacle-goose.jpg |
| plate-297 | 297 | Harlequin Duck | harlequin-duck | plate-297-harlequin-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-297-harlequin-duck.jpg |
| plate-298 | 298 | Red-necked Grebe | red-necked-grebe | plate-298-red-necked-grebe.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-298-red-necked-grebe.jpg |
| plate-299 | 299 | Dusky Petrel | dusky-petrel | plate-299-dusky-petrel.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-299-dusky-petrel.jpg |
| plate-300 | 300 | Golden Plover | golden-plover | plate-300-golden-plover.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-300-golden-plover.jpg |
| plate-301 | 301 | Canvas backed Duck | canvas-backed-duck | plate-301-canvas-backed-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-301-canvas-backed-duck.jpg |
| plate-302 | 302 | Dusky Duck | dusky-duck | plate-302-dusky-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-302-dusky-duck.jpg |
| plate-303 | 303 | Bartram Sandpiper | bartram-sandpiper | plate-303-bartram-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-303-bartram-sandpiper.jpg |
| plate-304 | 304 | Turn-stone | turn-stone | plate-304-turn-stone.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-304-turn-stone.jpg |
| plate-305 | 305 | Purple Gallinule | purple-gallinule | plate-305-purple-gallinule.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-305-purple-gallinule.jpg |
| plate-306 | 306 | Great Northern Diver, or Loon | great-northern-diver-or-loon | plate-306-great-northern-diver-or-loon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-306-great-northern-diver-or-loon.jpg |
| plate-307 | 307 | Blue Crane, or Heron | blue-crane-or-heron | plate-307-blue-crane-or-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-307-blue-crane-or-heron.jpg |
| plate-308 | 308 | Tell-tale Godwit, or Snipe | tell-tale-godwit-or-snipe | plate-308-tell-tale-godwit-or-snipe.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-308-tell-tale-godwit-or-snipe.jpg |
| plate-309 | 309 | Great Tern | great-tern | plate-309-great-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-309-great-tern.jpg |
| plate-310 | 310 | Spotted Sandpiper | spotted-sandpiper | plate-310-spotted-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-310-spotted-sandpiper.jpg |
| plate-311 | 311 | American White Pelican | american-white-pelican | plate-311-american-white-pelican.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-311-american-white-pelican.jpg |
| plate-312 | 312 | Long-tailed Duck | long-tailed-duck | plate-312-long-tailed-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-312-long-tailed-duck.jpg |
| plate-313 | 313 | Blue-Winged Teal | blue-winged-teal | plate-313-blue-winged-teal.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-313-blue-winged-teal.jpg |
| plate-314 | 314 | Black-headed Gull | black-headed-gull | plate-314-black-headed-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-314-black-headed-gull.jpg |
| plate-315 | 315 | Red-breasted Sandpiper | red-breasted-sandpiper | plate-315-red-breasted-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-315-red-breasted-sandpiper.jpg |
| plate-316 | 316 | Black-bellied Darter | black-bellied-darter | plate-316-black-bellied-darter.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-316-black-bellied-darter.jpg |
| plate-317 | 317 | Black, or Surf Duck | black-or-surf-duck | plate-317-black-or-surf-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-317-black-or-surf-duck.jpg |
| plate-318 | 318 | American Avocet | american-avocet | plate-318-american-avocet.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-318-american-avocet.jpg |
| plate-319 | 319 | Lesser Tern | lesser-tern | plate-319-lesser-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-319-lesser-tern.jpg |
| plate-320 | 320 | Little Sandpiper | little-sandpiper | plate-320-little-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-320-little-sandpiper.jpg |
| plate-321 | 321 | Roseate Spoonbill | roseate-spoonbill | plate-321-roseate-spoonbill.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-321-roseate-spoonbill.jpg |
| plate-322 | 322 | Red-headed Duck | red-headed-duck | plate-322-red-headed-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-322-red-headed-duck.jpg |
| plate-323 | 323 | Black Skimmer, or Shearwater | black-skimmer-or-shearwater | plate-323-black-skimmer-or-shearwater.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-323-black-skimmer-or-shearwater.jpg |
| plate-324 | 324 | Bonapartian Gull | bonapartian-gull | plate-324-bonapartian-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-324-bonapartian-gull.jpg |
| plate-325 | 325 | Buffel-headed Duck | buffel-headed-duck | plate-325-buffel-headed-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-325-buffel-headed-duck.jpg |
| plate-326 | 326 | Gannet | gannet | plate-326-gannet.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-326-gannet.jpg |
| plate-327 | 327 | Shoveller Duck | shoveller-duck | plate-327-shoveller-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-327-shoveller-duck.jpg |
| plate-328 | 328 | Long-legged Avocet | long-legged-avocet | plate-328-long-legged-avocet.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-328-long-legged-avocet.jpg |
| plate-329 | 329 | Yellow-breasted Rail | yellow-breasted-rail | plate-329-yellow-breasted-rail.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-329-yellow-breasted-rail.jpg |
| plate-330 | 330 | Ring Plover | ring-plover | plate-330-ring-plover.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-330-ring-plover.jpg |
| plate-331 | 331 | Goosander | goosander | plate-331-goosander.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-331-goosander.jpg |
| plate-332 | 332 | Pied Duck | pied-duck | plate-332-pied-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-332-pied-duck.jpg |
| plate-333 | 333 | Green Heron | green-heron | plate-333-green-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-333-green-heron.jpg |
| plate-334 | 334 | Black-bellied Plover | black-bellied-plover | plate-334-black-bellied-plover.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-334-black-bellied-plover.jpg |
| plate-335 | 335 | Red-breasted Snipe | red-breasted-snipe | plate-335-red-breasted-snipe.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-335-red-breasted-snipe.jpg |
| plate-336 | 336 | Yellow-Crowned Heron | yellow-crowned-heron | plate-336-yellow-crowned-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-336-yellow-crowned-heron.jpg |
| plate-337 | 337 | American Bittern | american-bittern | plate-337-american-bittern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-337-american-bittern.jpg |
| plate-338 | 338 | Bemaculated Duck | bemaculated-duck | plate-338-bemaculated-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-338-bemaculated-duck.jpg |
| plate-339 | 339 | Little Auk | little-auk | plate-339-little-auk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-339-little-auk.jpg |
| plate-340 | 340 | Least Stormy-Petrel | least-stormy-petrel | plate-340-least-stormy-petrel.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-340-least-stormy-petrel.jpg |
| plate-341 | 341 | Great Auk | great-auk | plate-341-great-auk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-341-great-auk.jpg |
| plate-342 | 342 | Golden-Eye Duck | golden-eye-duck | plate-342-golden-eye-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-342-golden-eye-duck.jpg |
| plate-343 | 343 | Ruddy Duck | ruddy-duck | plate-343-ruddy-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-343-ruddy-duck.jpg |
| plate-344 | 344 | Long-legged Sandpiper | long-legged-sandpiper | plate-344-long-legged-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-344-long-legged-sandpiper.jpg |
| plate-345 | 345 | American Widgeon | american-widgeon | plate-345-american-widgeon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-345-american-widgeon.jpg |
| plate-346 | 346 | Black-Throated Diver | black-throated-diver | plate-346-black-throated-diver.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-346-black-throated-diver.jpg |
| plate-347 | 347 | Smew, or White Nun | smew-or-white-nun | plate-347-smew-or-white-nun.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-347-smew-or-white-nun.jpg |
| plate-348 | 348 | Gadwall Duck | gadwall-duck | plate-348-gadwall-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-348-gadwall-duck.jpg |
| plate-349 | 349 | Least Water-hen | least-water-hen | plate-349-least-water-hen.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-349-least-water-hen.jpg |
| plate-350 | 350 | Rocky Mountain Plover | rocky-mountain-plover | plate-350-rocky-mountain-plover.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-350-rocky-mountain-plover.jpg |
| plate-351 | 351 | Great Cinereous Owl | great-cinereous-owl | plate-351-great-cinereous-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-351-great-cinereous-owl.jpg |
| plate-352 | 352 | Black-Winged Hawk | black-winged-hawk | plate-352-black-winged-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-352-black-winged-hawk.jpg |
| plate-353 | 353 | Chestnut-backed Titmouse, Black-capt Titmouse, and Chestnut-crowned Titmouse | chesnut-backed-titmouse | plate-353-chesnut-backed-titmouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-353-chesnut-backed-titmouse.jpg |
| plate-354 | 354 | Louisiana Tanager and Scarlet Tanager | louisiana-tanager | plate-354-louisiana-tanager.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-354-louisiana-tanager.jpg |
| plate-355 | 355 | MacGillivray's Finch | macgillivrays-finch | plate-355-macgillivrays-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-355-macgillivrays-finch.jpg |
| plate-356 | 356 | Marsh Hawk | marsh-hawk | plate-356-marsh-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-356-marsh-hawk.jpg |
| plate-357 | 357 | American Magpie | american-magpie | plate-357-american-magpie.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-357-american-magpie.jpg |
| plate-358 | 358 | Pine Grosbeak | pine-grosbeak | plate-358-pine-grosbeak.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-358-pine-grosbeak.jpg |
| plate-359 | 359 | Arkansaw Flycatcher, Swallow-Tailed Flycatcher, Says Flycatcher | arkansaw-flycatcher | plate-359-arkansaw-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-359-arkansaw-flycatcher.jpg |
| plate-360 | 360 | Winter Wren and Rock Wren | winter-wren | plate-360-winter-wren.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-360-winter-wren.jpg |
| plate-361 | 361 | Winter Wren and Rock Wren | long-tailed-or-dusky-grous | plate-361-long-tailed-or-dusky-grous.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-361-long-tailed-or-dusky-grous.jpg |
| plate-362 | 362 | Long-tailed, or Dusky Grous | yellow-billed-magpie | plate-362-yellow-billed-magpie.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-362-yellow-billed-magpie.jpg |
| plate-363 | 363 | Yellow-Billed Magpie, Stellers Jay, Ultramarine Jay, Clark's Crow | bohemian-chatterer | plate-363-bohemian-chatterer.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-363-bohemian-chatterer.jpg |
| plate-364 | 364 | Bohemian Chatterer | white-winged-crossbill | plate-364-white-winged-crossbill.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-364-white-winged-crossbill.jpg |
| plate-365 | 365 | White-winged Crossbill | lapland-long-spur | plate-365-lapland-long-spur.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-365-lapland-long-spur.jpg |
| plate-366 | 366 | Lapland Long-spur | iceland-or-jer-falcon | plate-366-iceland-or-jer-falcon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-366-iceland-or-jer-falcon.jpg |
| plate-367 | 367 | Iceland, or Jer Falcon | band-tailed-pigeon | plate-367-band-tailed-pigeon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-367-band-tailed-pigeon.jpg |
| plate-368 | 368 | Band-tailed Pigeon | rock-grous | plate-368-rock-grous.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-368-rock-grous.jpg |
| plate-369 | 369 | Rock Grous | mountain-mocking-bird | plate-369-mountain-mocking-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-369-mountain-mocking-bird.jpg |
| plate-370 | 370 | Mountain Mocking bird and Varied Thrush | american-water-ouzel | plate-370-american-water-ouzel.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-370-american-water-ouzel.jpg |
| plate-371 | 371 | American Water Ouzel | cock-plains | plate-371-cock-plains.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-371-cock-plains.jpg |
| plate-372 | 372 | Cock of the Plains | common-buzzard | plate-372-common-buzzard.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-372-common-buzzard.jpg |
| plate-373 | 373 | Common Buzzard | evening-grosbeak | plate-373-evening-grosbeak.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-373-evening-grosbeak.jpg |
| plate-374 | 374 | Evening Grosbeak and Spotted Grosbeak | sharp-shinned-hawk | plate-374-sharp-shinned-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-374-sharp-shinned-hawk.jpg |
| plate-375 | 375 | Sharp-shinned Hawk | lesser-red-poll | plate-375-lesser-red-poll.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-375-lesser-red-poll.jpg |
| plate-376 | 376 | Lesser Red-Poll | trumpeter-swan | plate-376-trumpeter-swan.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-376-trumpeter-swan.jpg |
| plate-377 | 377 | Trumpeter Swan | scolopaceus-courlan | plate-377-scolopaceus-courlan.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-377-scolopaceus-courlan.jpg |
| plate-378 | 378 | Scolopaceus Courlan | hawk-owl | plate-378-hawk-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-378-hawk-owl.jpg |
| plate-379 | 379 | Hawk Owl | ruff-necked-humming-bird | plate-379-ruff-necked-humming-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-379-ruff-necked-humming-bird.jpg |
| plate-380 | 380 | Ruff-necked Humming-bird | tengmalms-owl | plate-380-tengmalms-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-380-tengmalms-owl.jpg |
| plate-381 | 381 | Tengmalm's Owl | snow-goose | plate-381-snow-goose.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-381-snow-goose.jpg |
| plate-382 | 382 | Snow Goose | sharp-tailed-grouse | plate-382-sharp-tailed-grouse.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-382-sharp-tailed-grouse.jpg |
| plate-383 | 383 | Sharp-tailed Grouse | long-eared-owl | plate-383-long-eared-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-383-long-eared-owl.jpg |
| plate-384 | 384 | Long-eared Owl | black-throated-bunting | plate-384-black-throated-bunting.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-384-black-throated-bunting.jpg |
| plate-385 | 385 | Black-Throated Bunting | bank-swallow | plate-385-bank-swallow.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-385-bank-swallow.jpg |
| plate-386 | 386 | Bank Swallow and Violet-green Swallow | white-heron | plate-386-white-heron.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-386-white-heron.jpg |
| plate-387 | 387 | White Heron | glossy-ibis | plate-387-glossy-ibis.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-387-glossy-ibis.jpg |
| plate-388 | 388 | Glossy Ibis | nuttalls-starling | plate-388-nuttalls-starling.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-388-nuttalls-starling.jpg |
| plate-389 | 389 | Nuttall's Starling, Yellow-headed Troopial, Bullock's Oriole | red-cockaded-woodpecker | plate-389-red-cockaded-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-389-red-cockaded-woodpecker.jpg |
| plate-390 | 390 | Red-Cockaded Woodpecker | lark-finch | plate-390-lark-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-390-lark-finch.jpg |
| plate-391 | 391 | Lark Finch, Prairie Finch, Brown Song Sparrow | brant-goose | plate-391-brant-goose.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-391-brant-goose.jpg |
| plate-392 | 392 | Brant Goose | louisiana-hawk | plate-392-louisiana-hawk.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-392-louisiana-hawk.jpg |
| plate-393 | 393 | Louisiana Hawk | townsends-warbler | plate-393-townsends-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-393-townsends-warbler.jpg |
| plate-394 | 394 | Townsend's Warbler, Arctic Blue-bird, Western Blue-bird | chestnut-coloured-finch | plate-394-chestnut-coloured-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-394-chestnut-coloured-finch.jpg |
| plate-395 | 395 | Chestnut-coloured Finch, Black-headed Siskin, Black crown Bunting, Arctic Ground Finch | audubons-warbler | plate-395-audubons-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-395-audubons-warbler.jpg |
| plate-396 | 396 | Audubon's Warbler, Hermit Warbler, Black-throated gray Warbler | burgomaster-gull | plate-396-burgomaster-gull.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-396-burgomaster-gull.jpg |
| plate-397 | 397 | Burgomaster Gull | scarlet-ibis | plate-397-scarlet-ibis.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-397-scarlet-ibis.jpg |
| plate-398 | 398 | Scarlet Ibis | lazuli-finch | plate-398-lazuli-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-398-lazuli-finch.jpg |
| plate-399 | 399 | Lazuli Finch, Clay-coloured Finch, Oregon Snow Finch | black-throated-green-warbler | plate-399-black-throated-green-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-399-black-throated-green-warbler.jpg |
| plate-400 | 400 | Arkansaw Siskin, Mealy Red-poll, Louisiana Tanager, Townsend's Bunting, Buff-breasted Finch | arkansaw-siskin | plate-400-arkansaw-siskin.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-400-arkansaw-siskin.jpg |
| plate-401 | 401 | Red-breasted Merganser | red-breasted-merganser | plate-401-red-breasted-merganser.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-401-red-breasted-merganser.jpg |
| plate-402 | 402 | Black-throated Guillemot, Nobbed-billed Auk, Curled-crested Auk, Horned-billed Guillemot | black-throated-guillemot | plate-402-black-throated-guillemot.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-402-black-throated-guillemot.jpg |
| plate-403 | 403 | Golden-eye Duck | golden-eye-duck | plate-403-golden-eye-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-403-golden-eye-duck.jpg |
| plate-404 | 404 | Eared Grebe | eared-grebe | plate-404-eared-grebe.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-404-eared-grebe.jpg |
| plate-405 | 405 | Semipalmated Sandpiper | semipalmated-sandpiper | plate-405-semipalmated-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-405-semipalmated-sandpiper.jpg |
| plate-406 | 406 | Trumpeter Swan | trumpeter-swan | plate-406-trumpeter-swan.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-406-trumpeter-swan.jpg |
| plate-407 | 407 | Dusky Albatros | dusky-albatros | plate-407-dusky-albatros.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-407-dusky-albatros.jpg |
| plate-408 | 408 | American Scoter Duck | american-scoter-duck | plate-408-american-scoter-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-408-american-scoter-duck.jpg |
| plate-409 | 409 | Havell's Tern and Trudeau's Tern | havells-tern | plate-409-havells-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-409-havells-tern.jpg |
| plate-410 | 410 | Marsh Tern | marsh-tern | plate-410-marsh-tern.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-410-marsh-tern.jpg |
| plate-411 | 411 | Common American Swan | common-american-swan | plate-411-common-american-swan.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-411-common-american-swan.jpg |
| plate-412 | 412 | Violet-green Cormorant and Townsend's Cormorant | violet-green-cormorant | plate-412-violet-green-cormorant.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-412-violet-green-cormorant.jpg |
| plate-413 | 413 | California Partridge | california-partridge | plate-413-california-partridge.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-413-california-partridge.jpg |
| plate-414 | 414 | Golden-winged Warbler and Cape May Warbler | golden-winged-warbler | plate-414-golden-winged-warbler.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-414-golden-winged-warbler.jpg |
| plate-415 | 415 | Brown Creeper and Californian Nuthatch | brown-creeper | plate-415-brown-creeper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-415-brown-creeper.jpg |
| plate-416 | 416 | Hairy Woodpecker, Red-bellied Woodpecker, Red-shafted Woodpecker, Lewis' Woodpecker, Red-breasted Woodpecker | hairy-woodpecker | plate-416-hairy-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-416-hairy-woodpecker.jpg |
| plate-417 | 417 | Maria's Woodpecker, Three-toed Woodpecker, Phillips' Woodpecker, Canadian Woodpecker, Harris's Woodpecker, Audubon's Woodpecker | marias-woodpecker | plate-417-marias-woodpecker.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-417-marias-woodpecker.jpg |
| plate-418 | 418 | American Ptarmigan and White-tailed Grous | american-ptarmigan | plate-418-american-ptarmigan.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-418-american-ptarmigan.jpg |
| plate-419 | 419 | Little Tawny Thrush, Ptiliogony's Townsendi, Canada Jay | little-tawny-thrush | plate-419-little-tawny-thrush.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-419-little-tawny-thrush.jpg |
| plate-420 | 420 | Prairie Starling | prairie-starling | plate-420-prairie-starling.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-420-prairie-starling.jpg |
| plate-421 | 421 | Brown Pelican | brown-pelican | plate-421-brown-pelican.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-421-brown-pelican.jpg |
| plate-422 | 422 | Rough-legged Falcon | rough-legged-falcon | plate-422-rough-legged-falcon.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-422-rough-legged-falcon.jpg |
| plate-423 | 423 | Plumed Partridge and Thick-legged Partridge | plumed-partridge | plate-423-plumed-partridge.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-423-plumed-partridge.jpg |
| plate-424 | 424 | Lazuli Finch, Crimson-necked Bull-Finch, Gray-crowned Linnet, Cow-pen Bird, Evening Grosbeak, Brown Longspur | lazuli-finch | plate-424-lazuli-finch.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-424-lazuli-finch.jpg |
| plate-425 | 425 | Columbian Humming Bird | columbian-humming-bird | plate-425-columbian-humming-bird.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-425-columbian-humming-bird.jpg |
| plate-426 | 426 | Californian Vulture | californian-vulture | plate-426-californian-vulture.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-426-californian-vulture.jpg |
| plate-427 | 427 | White-legged Oyster-catcher, or Slender-billed Oyster-catcher | white-legged-oyster-catcher | plate-427-white-legged-oyster-catcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-427-white-legged-oyster-catcher.jpg |
| plate-428 | 428 | Townsend's Sandpiper | townsends-sandpiper | plate-428-townsends-sandpiper.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-428-townsends-sandpiper.jpg |
| plate-429 | 429 | Western Duck | western-duck | plate-429-western-duck.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-429-western-duck.jpg |
| plate-430 | 430 | Slender-billed Guillemot | slender-billed-guillemot | plate-430-slender-billed-guillemot.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-430-slender-billed-guillemot.jpg |
| plate-431 | 431 | American Flamingo | american-flamingo | plate-431-american-flamingo.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-431-american-flamingo.jpg |
| plate-432 | 432 | Burrowing Owl, Large-headed Burrowing Owl, Little night Owl, Columbian Owl, Short-eared Owl | burrowing-owl | plate-432-burrowing-owl.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-432-burrowing-owl.jpg |
| plate-433 | 433 | Bullock's Oriole, Baltimore Oriole, Mexican Goldfinch, Varied Thrush, Common Water Thrush | bullocks-oriole | plate-433-bullocks-oriole.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-433-bullocks-oriole.jpg |
| plate-434 | 434 | Little Tyrant Flycatcher, Small-headed Flycatcher, Blue Mountain Warbler, Bartram's Vireo, Short-legged Pewee, Rocky Mountain Fly-catcher | little-tyrant-flycatcher | plate-434-little-tyrant-flycatcher.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-434-little-tyrant-flycatcher.jpg |
| plate-435 | 435 | Columbian Water Ouzel, or Arctic Water Ouzel | columbian-water-ouzel | plate-435-columbian-water-ouzel.jpg | https://www.audubon.org/sites/default/files/boa_plates/plate-435-columbian-water-ouzel.jpg |

---

## A.5 Variant registry schema (for multi-source variance mode)

If/when you ingest multiple digitizations per plate, maintain a variants registry with (minimum) these fields:

- variant_id (stable internal ID)
- plate_id and/or plate_number + mapping confidence
- source_id (points to the source registry)
- acquisition_url and accessed_at (UTC)
- sha256 (required)
- container fingerprints (format, progressive, ICC hash, quant-table hash, etc.)
- local_path (relative path to the immutable stored bytes)
- notes (required when mapping is not high confidence)

Variants are immutable evidence; normalization/cropping/tiling are derived runs.

---

## A.6 Exclusion log (required when scaling sources)

Maintain an explicit exclusion log for rejected candidates:

- candidate URL
- discovered_at
- rejected_at
- rejection reason (schema mismatch, corrupt bytes, wrong plate, license restriction, etc.)
- operator

---

## A.7 Drift report (required for mutable sources)

For any source where upstream bytes might change, maintain a drift report:

- checked_at (UTC)
- URL
- previous checksum ↔ new checksum
- HTTP header deltas (ETag/Last-Modified) when available
- action taken (new variant ID minted; old bytes preserved)

---

## A.8 How this appendix is generated/verified

- A.4 is generated directly from data.json (snapshot + checksum recorded).
- Checksums, file sizes, and local paths are produced by ingestion notebooks and should be exported into machine-readable registries (plates.parquet, runs.parquet, and/or a dedicated variants.parquet).

Recommended practice:

- treat Appendix A as a rendered view of canonical registries
- regenerate it from registries rather than editing by hand
- store the generator script/notebook as part of the reproducibility protocol
