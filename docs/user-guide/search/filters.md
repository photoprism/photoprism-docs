# Using Search Filters

Powerful search filters let you easily find specific photos and videos, for example:

* Persons visible on a picture
* Objects that are displayed on a picture
* The [main color](../../developer-guide/metadata/colors.md#standard-colors) of a picture
* The file or folder name of a picture
* Location where a picture has been taken
* Other metadata such as camera, lens, chroma...

Just give it a try!

![Screenshot](../organize/img/fulltext-search-1.jpg){ class="shadow" }

## Introduction ##

The following filters can be set via dropdowns in the search toolbar:

* Country, Year, Month, Order, Camera, [Color](../../developer-guide/metadata/colors.md#standard-colors), Category.

If you set multiple filters, only pictures that meet all filter criteria will be displayed in the search result. Filters can generally be combined unless they contradict each other.

 ![Screenshot](../organize/img/filter-bar-new.jpg){ class="shadow" }

In addition, these and many other filters can be entered into the toolbar search box as follows:

```
label:cat color:green type:live
```

A complete overview of the [available search filters](#filter-reference) can be found below.

![Screenshot](../organize/img/search-filters.jpg){ class="shadow" }

### AND Search ###

To combine different filters use a space as separator:

```
mono:true review:false
```

The search result shows pictures that are monochrome **and** not in review.

Additionally some filters can be combined with `&` as follows:

```bigquery
keywords:buffalo&water
```

or:

```bigquery
keywords:"buffalo & water"
```

This query will show all photos that have the keywords water **and** buffalo.

& is supported by the following filters:

* albums, keywords, subject/person, subjects/people.

!!!info ""
    The label filter does not support &. You can use the keywords filter instead, as all labels are keywords as well.

### OR Search ###

An OR search is possible using `|`:

```
label:cat|dog
```

This will show all photos that have either the label cat **or** dog.

The following filters work with |:

* albums, color, country, state, city, day, month, year, keywords, label, path, subject/person, subjects/people, title, type, name, filename, original, hash

### Wildcard ###

The `*` character will act as a wildcard:

```
name:"IMG_23*"
```

This will show all photos which name start with `IMG_23`.

```
name:"*_23*"
```

This will show all photos which name contain `_23`, like `IMG_2356.MOV` , `2021_02_23.jpg`, etc.

!!!info ""
    Wildcards can be combined with & or |: `filename:"*IMG123*|*_22F6FC19.jpg"`

## Filter Reference

This is a complete list of supported search filters with examples. Filters can generally be combined unless they contradict each other, e.g. results cannot be monochrome and have high color saturation at the same time.

|  Filter   |   Type    |               Examples                |                                                                   Notes                                                                    |
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
| after     | timestamp | after:"2022-01-30"                    | Finds pictures taken after this date                                                                                                       |
| before    | timestamp | before:"2022-01-30"                   | Finds pictures taken before this date                                                                                                      |

!!! question "Why can't I play live photos or find stacks when I search for specific images?"
    Our search API and user interface perform a file search. This is intentional since "stacks" can contain files of different types and properties, such as color.

    For example, there may be color and monochrome versions. Now, when you search for them or sort them by color, the user interface must display individual files. Otherwise, the results showing a color image/video when you filter by monochrome would make no sense.
    
    Likewise, if you search for `filename.mp4.*`, you will find only JPEGs without video, because the video file extension is `.mp4` without an extra dot at the end.

    We recommend using the `path:` and/or `name:` filters with wildcards if searching for individual files limits the search results too much. Most users will want to find all related files so that they can be displayed together, e.g. as live photos consisting of a video and an image.
    
    You can combine these filters with other filters such as `live` to ensure that the results include only pictures with a specific media type. Alternatively, you can use the `filename:` filter with a more permissive wildcard that excludes the file extension.
