# Using Search Filters

Powerful search filters let you easily find specific photos and videos, for example:

* Persons visible on a picture
* Objects that are displayed on a picture
* The [main color](../../developer-guide/metadata/colors.md#standard-colors) of a picture
* The file or folder name of a picture
* Location where a picture has been taken
* Other metadata such as camera, lens, chroma...

Just give it a try!

![Screenshot](../organize/img/fulltext-search-2503.jpg){ class="shadow" }

## Introduction ##

The following filters can be set via dropdowns in the search toolbar:

* Country, Year, Month, Order, Camera, [Color](../../developer-guide/metadata/colors.md#standard-colors), Category.

If you set multiple filters, only pictures that meet all filter criteria will be displayed in the search result. Filters can generally be combined unless they contradict each other.

 ![Screenshot](../organize/img/filter-bar-2503.jpg){ class="shadow" }

In addition, these and many other filters can be entered into the toolbar search box as follows:

```
label:cat color:green type:live
```

A complete overview of the [available search filters](#filter-reference) can be found below.

![Screenshot](../organize/img/search-filters-2503.jpg){ class="shadow" }

### AND Search ###

To combine different filters use a space as separator:

```
mono:true review:false
```

The search result shows pictures that are monochrome **and** not in review.

Additionally some filters can be combined with `&` as follows:

```
keywords:buffalo&water
```

or:

```
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

### Searching for & or | ###

A search for photos that contain `&` or `|` in their caption, filename, name or title is possible using the escape `\`:

```
caption:Green\|Blue
```

This will show all photos that have the caption Green|Blue, and not all photos that have the caption Green OR Blue.

The following filters work with escape:

* photos name, filename, caption, title

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

| Filter      | Type      | Examples                              | Notes                                                                                                                                          |
|:------------|:----------|:--------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| dist        | decimal   | dist:50                               | Maximum distance to position in km                                                                                                             |
| lat         | decimal   | lat:41.894043                         | Position latitude (-90.0 to 90.0 deg)                                                                                                          |
| lng         | decimal   | lng:-87.62448                         | Position longitude (-180.0 to 180.0 deg)                                                                                                       |
| chroma      | number    | chroma:70                             | Chroma (0-100)                                                                                                                                 |
| diff        | number    | diff:-1 diff:2                        | Differential Perceptual Hash (000000-FFFFFF)                                                                                                   |
| quality     | number    | quality:0 quality:3                   | Minimum quality score (1-7)                                                                                                                    |
| album       | string    | album:berlin                          | Album UID or name, supports * wildcards                                                                                                        |
| albums      | string    | albums:"South Africa & Birds"         | Album names, combinable with & or \|                                                                                                           |
| alt         | string    | alt:300-500                           | Altitude (m)                                                                                                                                   |
| camera      | string    | camera:canon                          | Camera make or model                                                                                                                           |
| caption     | string    | caption:"Lake*"                       | Searches text in captions separated by \|, or specify false to find content without a caption                                                  |
| category    | string    | category:airport                      | Location category type                                                                                                                         |
| city        | string    | city:"Berlin"                         | City names, separated by \|                                                                                                                    |
| codec       | string    | codec:avc1                            | Media codec types separated by \|, e.g. jpeg, avc1, or hvc1                                                                                    |
| color       | string    | color:"red\|blue"                     | Color name separated by \|, e.g. purple, magenta, pink, red, orange, gold, yellow, lime, green, teal, cyan, blue, brown, white, grey, or black |
| country     | string    | country:"de\|us"                      | Country codes, separated by \|                                                                                                                 |
| day         | string    | day:3\|13                             | Days 1-31, separated by \|                                                                                                                     |
| description | string    | description:"Lake*"                   | Searches text in titles or captions separated by \|, or specify false to find content without a title or caption                               |
| f           | string    | f:2.8-4.5                             | Aperture (F-Number)                                                                                                                            |
| face        | string    | face:PN6QO5INYTUSAATOFL43LL2ABAV5ACZG | Find pictures with a specific face ID, you can also specify yes, no, new, or a face type                                                       |
| faces       | string    | faces:yes faces:3                     | Minimum number of detected faces (yes means 1)                                                                                                 |
| favorite    | string    | favorite:true favorite:false          | Finds favorite content                                                                                                                         |
| filename    | string    | filename:"2021/07/12345.jpg"          | File names including path and extension, separated by \|                                                                                       |
| folder      | string    | folder:"*/2020"                       | Alias for the path filter                                                                                                                      |
| geo         | string    | geo:yes                               | Finds content with or without latitude and longitude                                                                                           |
| hash        | string    | hash:2fd4e1c67a2d                     | SHA1 file hashes, separated by \|                                                                                                              |
| id          | string    | id:123e4567-e89b-...                  | Finds content with the specified Image, Document or Instance IDs, separated by \|                                                              |
| iso         | string    | iso:200-400                           | ISO number (light sensitivity)                                                                                                                 |
| keywords    | string    | keywords:"sand&water"                 | Keywords, combinable with & and \|                                                                                                             |
| label       | string    | label:cat\|dog                        | Label names, separated by \|                                                                                                                   |
| latlng      | string    | latlng:49.4,13.41,46.5,2.331          | Position bounding box (Lat N, Lng E, Lat S, Lng W)                                                                                             |
| lens        | string    | lens:ef24                             | Lens make or model                                                                                                                             |
| mm          | string    | mm:28-35                              | Focal length (35mm equivalent)                                                                                                                 |
| month       | string    | month:7\|10                           | Months from 1-12, separated by \|                                                                                                              |
| mp          | string    | mp:3-6                                | Resolution in Megapixels (MP)                                                                                                                  |
| name        | string    | name:"IMG_9831-112*"                  | File names without path and extension, separated by \|                                                                                         |
| near        | string    | near:pqbcf5j446s0futy                 | Finds nearby pictures (UID)                                                                                                                    |
| olc         | string    | olc:8FWCHX7W+                         | Open Location Code (OLC)                                                                                                                       |
| original    | string    | original:"IMG_9831-112*"              | Original file names of imported files, separated by \|                                                                                         |
| path        | string    | path:2020/Holiday                     | Path names separated by \|, supports * wildcards                                                                                               |
| people      | string    | people:"Jane & John"                  | Subject names, combinable with & or \|                                                                                                         |
| person      | string    | person:"Jane Doe & John Doe"          | Subject names, will be matched exactly and can be combined using & or \|                                                                       |
| s2          | string    | s2:4799e370ca54c8b9                   | Position, specified as S2 Cell ID                                                                                                              |
| scan        | string    | scan:true scan:false                  | Finds scanned photos and documents                                                                                                             |
| state       | string    | state:"Baden-Württemberg"             | State or province names, separated by \|                                                                                                       |
| subject     | string    | subject:"Jane Doe & John Doe"         | Alias for person                                                                                                                               |
| subjects    | string    | subjects:"Jane & John"                | Alias for people                                                                                                                               |
| title       | string    | title:"Lake*"                         | Searches text in titles separated by \|, or specify false to find content without a title                                                      |
| type        | string    | type:image\|raw\|live                 | Finds specific media types, such as image, raw, live, video, animated, audio, vector, or document, separated by \|                             |
| uid         | string    | uid:pqbcf5j446s0futy                  | Finds content with the specified internal UIDs, separated by \|                                                                                |
| year        | string    | year:1990\|2003                       | Years, separated by \|                                                                                                                         |
| animated    | switch    | animated:yes                          | Finds animated images only                                                                                                                     |
| archived    | switch    | archived:yes                          | Finds archived content                                                                                                                         |
| audio       | switch    | audio:yes                             | Finds audio content only                                                                                                                       |
| document    | switch    | document:yes                          | Finds PDF documents only                                                                                                                       |
| error       | switch    | error:yes                             | Finds content with errors                                                                                                                      |
| hidden      | switch    | hidden:yes                            | Finds hidden content (broken or unsupported)                                                                                                   |
| image       | switch    | image:yes                             | Finds regular photos and images only                                                                                                           |
| landscape   | switch    | landscape:yes                         | Finds landscape pictures only                                                                                                                  |
| live        | switch    | live:yes                              | Finds Motion and Live Photos only                                                                                                              |
| media       | switch    | media:yes                             | Finds live, video, audio, and animated content only                                                                                            |
| mono        | switch    | mono:yes                              | Pictures with few or no colors                                                                                                                 |
| panorama    | switch    | panorama:yes                          | Finds panorama pictures only (aspect ratio 1.9:1 or more)                                                                                      |
| photo       | switch    | photo:yes                             | Finds regular photos and images, as well as RAW and Live Photos                                                                                |
| portrait    | switch    | portrait:yes                          | Finds portrait pictures only                                                                                                                   |
| primary     | switch    | primary:yes                           | Finds primary JPEG or PNG files only                                                                                                           |
| private     | switch    | private:yes                           | Finds private content                                                                                                                          |
| public      | switch    | public:yes                            | Excludes private content                                                                                                                       |
| raw         | switch    | raw:yes                               | Finds RAW images only                                                                                                                          |
| review      | switch    | review:yes                            | Finds content in review                                                                                                                        |
| square      | switch    | square:yes                            | Finds square pictures only (aspect ratio 1:1)                                                                                                  |
| stack       | switch    | stack:yes                             | Finds content with more than one media file                                                                                                    |
| stackable   | switch    | stackable:yes                         | Finds content that can be stacked with additional files                                                                                        |
| unsorted    | switch    | unsorted:yes                          | Finds content that is not in an album                                                                                                          |
| unstacked   | switch    | unstacked:yes                         | Finds content with a file that has been removed                                                                                                |
| vector      | switch    | vector:yes                            | Finds vector graphics only                                                                                                                     |
| video       | switch    | video:yes                             | Finds video content only                                                                                                                       |
| added       | timestamp | added:"2006-01-02T15:04:05Z"          | Finds content added at or after this time                                                                                                      |
| after       | timestamp | after:"2022-01-30"                    | Finds content created on or after this date                                                                                                    |
| before      | timestamp | before:"2022-01-30"                   | Finds content created on or before this date                                                                                                   |
| edited      | timestamp | edited:"2006-01-02T15:04:05Z"         | Finds content edited at or after this time                                                                                                     |
| taken       | timestamp | taken:"2022-01-30"                    | Finds content created on the specified date                                                                                                    |
| updated     | timestamp | updated:"2006-01-02T15:04:05Z"        | Finds content updated at or after this time                                                                                                    |

!!! question "Why can't I play live photos or find stacks when I search for specific images?"
    Our search API and user interface perform a file search. This is intentional since "stacks" can contain files of different types and properties, such as color.

    For example, there may be color and monochrome versions. Now, when you search for them or sort them by color, the user interface must display individual files. Otherwise, the results showing a color image/video when you filter by monochrome would make no sense.
    
    Likewise, if you search for `filename.mp4.*`, you will find only JPEGs without video, because the video file extension is `.mp4` without an extra dot at the end.

    We recommend using the `path:` and/or `name:` filters with wildcards if searching for individual files limits the search results too much. Most users will want to find all related files so that they can be displayed together, e.g. as live photos consisting of a video and an image.
    
    You can combine these filters with other filters such as `live` to ensure that the results include only pictures with a specific media type. Alternatively, you can use the `filename:` filter with a more permissive wildcard that excludes the file extension.
