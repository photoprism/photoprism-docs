# Search API Endpoints

## `GET /api/v1/photos`

When [querying the `/api/v1/photos` endpoint](https://demo.photoprism.app/api/v1/photos?count=120&offset=120&merged=true&country=&camera=0&lens=0&label=&latlng=&year=0&month=0&color=&order=newest&q=&public=true&quality=3), matching *files* will be returned along with the metadata of the *corresponding photos*. This may be unexpected at first due to the endpoint name. However, this approach allows to sort results e.g. by color or file size, which differ at the file level and therefore require dynamic sorting/grouping of multiple matching files that may belong to the same photo (see [Stacks](../../user-guide/organize/stacks.md)).

To simplify processing in the client/user interface, you can set the `merged` parameter to `true` so that consecutive files with the same photo ID are merged into a single result with the `Files` property containing the related files.

In particular, multiple files are returned for a single photo in the case of multi-file/hybrid media formats such as Live Photos, as these consist of a photo and a video file. The same applies to RAW/JPEG.

!!! example ""
    If you only want the primary image ([thumbnail](thumbnails.md)) to be returned, you can set the `primary` filter to `true`. In this case, it is not necessary to also set `merged` to `true` as a single file will be returned for each photo. This can simplify things if you don't need to know anything about the additional files, e.g. when just rendering thumbnails without metadata.

### Composite ID and UIDs

The `ID` returned by the search API is a composite ID consisting of the photo ID and the related file ID (usually the file selected as primary image), so that this `ID` is unique as required for rendering in the user interface.

Note that you do not need this composite ID to communicate with any of our API endpoints. Instead, you will either have to pass a `UID` (e.g. when updating photo metadata) or the SHA1 `Hash` of a file (e.g. when [requesting a thumbnail](thumbnails.md)).

!!! example ""
    Using random UIDs prevents possible caching issues in proxies/clients, e.g. if the index is reset on the server and the numeric IDs would thus start at 0 again. They are also hard to guess, so a time-consuming brute force attack is required instead of simply enumerating integers starting from 0.

### Response Example

```json
[{
    "ID": "11-21",
    "UID": "pse1yzastu36irsj",
    "Type": "image",
    "TypeSrc": "",
    "TakenAt": "2012-08-27T12:40:25Z",
    "TakenAtLocal": "2012-08-27T14:40:25Z",
    "TakenSrc": "meta",
    "TimeZone": "Europe/Madrid",
    "Path": "2012",
    "Name": "20120827-144025-Bodegas-Ysios-Winery-Laguardia-Spain",
    "OriginalName": "",
    "Title": "Bodegas Ysios Winery / Laguardia / Spain",
    "Description": "",
    "Year": 2012,
    "Month": 8,
    "Day": 27,
    "Country": "es",
    "Stack": 0,
    "Favorite": false,
    "Private": false,
    "Iso": 100,
    "FocalLength": 28,
    "FNumber": 11,
    "Exposure": "1/160",
    "Quality": 4,
    "Resolution": 8,
    "Color": 2,
    "Scan": false,
    "Panorama": false,
    "CameraID": 5,
    "CameraSrc": "meta",
    "CameraSerial": "1730906408",
    "CameraMake": "Canon",
    "CameraModel": "EOS 30D",
    "LensID": 5,
    "LensModel": "EF28mm f/1.8 USM",
    "Lat": 42.568302,
    "Lng": -2.5908582,
    "CellID": "s2:0d4ff9b1b32c",
    "PlaceID": "es:7v314KSnaCLy",
    "PlaceSrc": "meta",
    "PlaceLabel": "Laguardia, Euskadi, Spain",
    "PlaceCity": "Laguardia",
    "PlaceState": "Euskadi",
    "PlaceCountry": "es",
    "InstanceID": "",
    "FileUID": "fse1yza2r4gsjq6f",
    "FileRoot": "/",
    "FileName": "2012/20120827-144025-Bodegas-Ysios-Winery-Laguardia-Spain.jpg",
    "Hash": "4bc82c3ea5aaa323aea801fe0125b554af8e49af",
    "Width": 3368,
    "Height": 2246,
    "Portrait": false,
    "Merged": false,
    "CreatedAt": "2024-05-25T17:52:22.291451832Z",
    "UpdatedAt": "2024-05-25T17:52:22.307889576Z",
    "EditedAt": "0001-01-01T00:00:00Z",
    "CheckedAt": "2024-05-26T06:15:09Z",
    "Files": [
        {
        "UID": "fse1yza2r4gsjq6f",
        "PhotoUID": "pse1yzastu36irsj",
        "Name": "2012/20120827-144025-Bodegas-Ysios-Winery-Laguardia-Spain.jpg",
        "Root": "/",
        "Hash": "4bc82c3ea5aaa323aea801fe0125b554af8e49af",
        "Size": 2473990,
        "Primary": true,
        "Codec": "jpeg",
        "FileType": "jpg",
        "MediaType": "image",
        "Mime": "image/jpeg",
        "Width": 3368,
        "Height": 2246,
        "Orientation": 1,
        "AspectRatio": 1.5,
        "Colors": "616121222",
        "Luminance": "AACA5A888",
        "Diff": 767,
        "Chroma": 15,
        "CreatedAt": "2024-05-25T17:52:22.291451832Z",
        "UpdatedAt": "2024-05-25T17:52:22.307889576Z",
        "Markers": []
        }
    ]
}]
```

### Response Headers

| Header           | Type   | Example  | Notes                                                                                                                           |
|------------------|--------|----------|---------------------------------------------------------------------------------------------------------------------------------|
| X-Count          | int    | 120      | Actual number of *files* returned                                                                                               |
| X-Limit          | int    | 120      | Maximum number of *files* requested                                                                                             |
| X-Offset         | int    | 0        | File offset                                                                                                                     |
| X-Download-Token | string | 3qjg1db2 | [Security token](../../getting-started/config-options.md#security-tokens) required to download original files                   |
| X-Preview-Token  | string | 174utza5 | [Security token](../../getting-started/config-options.md#security-tokens) required for the [Thumbnail Image API](thumbnails.md) |

!!! example ""
    In order to fetch all results, you can perform a follow-up query if the number in the `X-Count` response header matches `X-Limit`. For this, the `offset` request parameter must be set to the number of files already returned.

### Request Parameters

| Name   | Type   | Example          | Notes                                                                                                                                      |
|--------|--------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| q      | string | dog color:red    | Search *query* as entered by the user in the search toolbar, see [Search Filters](#search-filters)                                         |
| s      | string | ariqwb43p5dh9h13 | Limits the result *scope* to the specified album UID                                                                                       |
| count  | int    | 1000             | Maximum number of *files* to be returned                                                                                                   |
| offset | int    | 0                | File offset                                                                                                                                |
| order  | string | added            | Sort order e.g. `added`, `updated`, `edited`, `relevance`, `duration`, `size`, `newest`, `oldest`, `similar`, `name`, `title`, or `random` |
| merged | bool   | true             | Merges consecutive *files* that belong to the same photo into a single result, see above for an explanation                                |

#### Search Filters

The following [search filters](../../user-guide/search/filters.md) can be used as regular GET request parameters or submitted as part of a search query with the `q` request parameter:

| Filter    | Type      | Examples                              | Notes                                                                                                                                      |
|-----------|-----------|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| dist      | decimal   | dist:50                               | Distance to Position (km)                                                                                                                  |
| lat       | decimal   | lat:41.894043                         | GPS Position (Latitude)                                                                                                                    |
| lng       | decimal   | lng:-87.62448                         | GPS Position (Longitude)                                                                                                                   |
| chroma    | number    | chroma:70                             | Chroma (0-100)                                                                                                                             |
| diff      | number    | diff:-1 diff:2                        | Differential Perceptual Hash (000000-FFFFFF)                                                                                               |
| quality   | number    | quality:0 quality:3                   | Minimum quality score (1-7)                                                                                                                |
| album     | string    | album:berlin                          | Album UID or Name, supports * wildcards                                                                                                    |
| albums    | string    | albums:"South Africa & Birds"         | Album Names (combinable with & and \|)                                                                                                     |
| alt       | string    | alt:300-500                           | GPS Altitude (m)                                                                                                                           |
| camera    | string    | camera:canon                          | Camera Make/Model Name                                                                                                                     |
| category  | string    | category:airport                      | Location Category                                                                                                                          |
| city      | string    | city:"Berlin"                         | Location City (separate with \|)                                                                                                           |
| color     | string    | color:"red\|blue"                     | Color Name (purple, magenta, pink, red, orange, gold, yellow, lime, green, teal, cyan, blue, brown, white, grey, black) (separate with \|) |
| country   | string    | country:"de\|us"                      | Location Country Code (separate with \|)                                                                                                   |
| day       | string    | day:3\|13                             | Day of Month (1-31, separate with \|)                                                                                                      |
| f         | string    | f:2.8-4.5                             | Aperture (f-number)                                                                                                                        |
| face      | string    | face:PN6QO5INYTUSAATOFL43LL2ABAV5ACZG | Face ID, yes, no, new, or kind                                                                                                             |
| faces     | string    | faces:yes faces:3                     | Minimum number of Faces (yes = 1)                                                                                                          |
| favorite  | string    | favorite:true favorite:false          | Finds images by favorite status                                                                                                            |
| filename  | string    | filename:"2021/07/12345.jpg"          | File Name with path and extension (separate with \|)                                                                                       |
| folder    | string    | folder:"*/2020"                       | Path Name (separate with \|), supports * wildcards                                                                                         |
| geo       | string    | geo:yes                               | Finds pictures with or without coordinates                                                                                                 |
| hash      | string    | hash:2fd4e1c67a2d                     | SHA1 File Hash (separate with \|)                                                                                                          |
| id        | string    | id:123e4567-e89b-...                  | Finds pictures by Exif UID, XMP Document ID or Instance ID                                                                                 |
| iso       | string    | iso:200-400                           | ISO Number (light sensitivity)                                                                                                             |
| keywords  | string    | keywords:"sand&water"                 | Keywords (combinable with & and \|)                                                                                                        |
| label     | string    | label:cat\|dog                        | Label Names (separate with \|)                                                                                                             |
| latlng    | string    | latlng:"name"                         | GPS Bounding Box (Lat N, Lng E, Lat S, Lng W)                                                                                              |
| lens      | string    | lens:ef24                             | Lens Make/Model Name                                                                                                                       |
| mm        | string    | mm:28-35                              | Focal Length (35mm equivalent)                                                                                                             |
| month     | string    | month:7\|10                           | Month (1-12, separate with \|)                                                                                                             |
| mp        | string    | mp:3-6                                | Resolution in Megapixels (MP)                                                                                                              |
| name      | string    | name:"IMG_9831-112*"                  | File Name without path and extension (separate with \|)                                                                                    |
| near      | string    | near:pqbcf5j446s0futy                 | Finds nearby pictures (UID)                                                                                                                |
| olc       | string    | olc:8FWCHX7W+                         | OLC Position (Open Location Code)                                                                                                          |
| original  | string    | original:"IMG_9831-112*"              | Original file name of imported files (separate with \|)                                                                                    |
| path      | string    | path:2020/Holiday                     | Path Name (separate with \|), supports * wildcards                                                                                         |
| people    | string    | people:"Jane & John"                  | Subject Names (combinable with & and \|)                                                                                                   |
| person    | string    | person:"Jane Doe & John Doe"          | Subject Names, exact matches (combinable with & and \|)                                                                                    |
| s2        | string    | s2:4799e370ca54c8b9                   | S2 Position (Cell ID)                                                                                                                      |
| scan      | string    | scan:true scan:false                  | Finds scanned photos and documents                                                                                                         |
| state     | string    | state:"Baden-Württemberg"             | Location State (separate with \|)                                                                                                          |
| subject   | string    | subject:"Jane Doe & John Doe"         | Alias for person                                                                                                                           |
| subjects  | string    | subjects:"Jane & John"                | Alias for people                                                                                                                           |
| title     | string    | title:"Lake*"                         | Title (separate with \|)                                                                                                                   |
| type      | string    | type:raw                              | Media Type (image, video, raw, live, animated); separate with \|                                                                           |
| uid       | string    | uid:pqbcf5j446s0futy                  | Limits results to the specified internal unique IDs                                                                                        |
| year      | string    | year:1990\|2003                       | Year (separate with \|)                                                                                                                    |
| animated  | switch    | animated:yes                          | Finds animated GIFs                                                                                                                        |
| archived  | switch    | archived:yes                          | Finds archived pictures                                                                                                                    |
| error     | switch    | error:yes                             | Finds pictures with errors                                                                                                                 |
| hidden    | switch    | hidden:yes                            | Finds hidden pictures (broken or unsupported)                                                                                              |
| landscape | switch    | landscape:yes                         | Finds pictures in landscape format                                                                                                         |
| live      | switch    | live:yes                              | Finds Live Photos and short videos                                                                                                         |
| mono      | switch    | mono:yes                              | Finds pictures with few or no colors                                                                                                       |
| panorama  | switch    | panorama:yes                          | Finds pictures with an aspect ratio > 1.9:1                                                                                                |
| photo     | switch    | photo:yes                             | Finds only photos, no videos                                                                                                               |
| portrait  | switch    | portrait:yes                          | Finds pictures in portrait format                                                                                                          |
| primary   | switch    | primary:yes                           | Finds primary JPEG files only                                                                                                              |
| private   | switch    | private:yes                           | Finds private pictures                                                                                                                     |
| public    | switch    | public:yes                            | Excludes private pictures                                                                                                                  |
| raw       | switch    | raw:yes                               | Finds pictures with RAW image file                                                                                                         |
| review    | switch    | review:yes                            | Finds pictures in review                                                                                                                   |
| square    | switch    | square:yes                            | Finds images with an aspect ratio of 1:1                                                                                                   |
| stack     | switch    | stack:yes                             | Finds pictures with more than one media file                                                                                               |
| stackable | switch    | stackable:yes                         | Finds pictures that can be stacked with additional media files                                                                             |
| unsorted  | switch    | unsorted:yes                          | Finds pictures not in an album                                                                                                             |
| unstacked | switch    | unstacked:yes                         | Finds pictures with a file that has been removed from a stack                                                                              |
| vector    | switch    | vector:yes                            | Finds vector graphics only                                                                                                                 |
| video     | switch    | video:yes                             | Finds video files only                                                                                                                     |
| added     | timestamp | added:"2006-01-02 15:04:05"           | Finds pictures added at or after this time (UTC)                                                                                           |
| after     | timestamp | after:"2022-01-30"                    | Finds pictures taken on or after this date                                                                                                 |
| before    | timestamp | before:"2022-01-30"                   | Finds pictures taken on or before this date                                                                                                |
| taken     | timestamp | taken:"2022-01-30"                    | Finds pictures taken on the specified date                                                                                                 |
| updated   | timestamp | updated:"2006-01-02 15:04:05"         | Finds pictures updated at or after this time (UTC)                                                                                         |
