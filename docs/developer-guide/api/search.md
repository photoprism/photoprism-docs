# Search API Endpoints

## `GET /api/v1/photos`

When [querying the `/api/v1/photos` endpoint](https://demo.photoprism.app/api/v1/photos?count=120&offset=120&merged=true&country=&camera=0&lens=0&label=&latlng=&year=0&month=0&color=&order=newest&q=&public=true&quality=3), matching *files* will be returned along with the metadata of the *corresponding photos*. This may be unexpected at first due to the endpoint name. However, this approach allows to sort results e.g. by color or file size, which differ at the file level and therefore require dynamic sorting/grouping of multiple matching files that may belong to the same photo (see [Stacks](../../user-guide/organize/stacks.md)).

To simplify processing in the client/user interface, you can set the `merged` parameter to `true` so that consecutive files with the same photo ID are merged into a single result with the `Files` property containing the related files.

In particular, multiple files are returned for a single photo in the case of multi-file/hybrid media formats such as Live Photos, as these consist of a photo and a video file. The same applies to RAW/JPEG.

!!! example ""
    If you only want the primary image ([thumbnail](thumbnails.md#image-endpoint-uri)) to be returned, you can set the `primary` filter to `true`. In this case, it is not necessary to also set `merged` to `true` as a single file will be returned for each photo. This can simplify things if you don't need to know anything about the additional files, e.g. when just rendering thumbnails without metadata.

### Composite ID and UIDs

The `ID` returned by the search API is a composite ID consisting of the photo ID and the related file ID (usually the file selected as primary image), so that this `ID` is unique as required for rendering in the user interface.

Note that you do not need this composite ID to communicate with any of our API endpoints. Instead, you will either have to pass a `UID` (e.g. when updating photo metadata) or the SHA1 `Hash` of a file (e.g. when [requesting a thumbnail](thumbnails.md#image-endpoint-uri)).

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

| Header           | Type   | Example  | Notes                                                                                                                                              |
|------------------|--------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| X-Count          | int    | 120      | Actual number of *files* returned                                                                                                                  |
| X-Limit          | int    | 120      | Maximum number of *files* requested                                                                                                                |
| X-Offset         | int    | 0        | File offset                                                                                                                                        |
| X-Download-Token | string | 3qjg1db2 | [Security token](../../getting-started/config-options.md#security-tokens) required to download original files                                      |
| X-Preview-Token  | string | 174utza5 | [Security token](../../getting-started/config-options.md#security-tokens) required for the [Thumbnail Image API](thumbnails.md#image-endpoint-uri) |

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

[Search filters](../../user-guide/search/filters.md#filter-reference) can be used as regular GET request parameters or submitted as part of a search query with the `q` request parameter.