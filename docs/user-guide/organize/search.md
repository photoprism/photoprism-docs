# Search #
In all sections you can use the *search bar* to find certain photos, videos, albums or labels.

You can search for all kind of things:

* People on the photo
* Objects that are displayed on the photo
* The main color of the photo
* The filename or foldername of a photo
* Location where the photo has been taken
* ...

Just try it!

 ![Screenshot](img/search-beach.png)

## Search Filter ##
Additionally to the search you can set the following filters using the filter bar:

* Country, Year, Order, Camera, Lens, Color, Category

In case you set multiple filters only photos, that fulfill all filter criteria, are shown in the search result.

 ![Screenshot](img/color-red.png)

!!! tip
    You can use filters in the search bar like this:
    
    `label:cat`
    `color:green`
    `type:live`
    
    You find the full list of filters below.
    
   ![Screenshot](img/color-green.png)

## AND Search ##
To combine different filters use a space as separator:

```
mono:true review:false
```

The search result shows photos that are monochrome **and** not in review.

Additionally some filters can be used with &:

```bigquery
keywords:buffalo&water
```

Or:

```bigquery
keywords:"buffalo & water"
```

This query will show all photos that have the keywords water **and** buffalo.

& is supported by the following filters:

* albums, keywords, subject/person, subjects/people.

!!!info
    The label filter does not support &. You can use the keywords filter instead, as all labels are keywords as well.

## OR Search ##
An OR search is possible using `|`:

```
label:cat|dog
```

This will show all photos that have either the label cat **or** dog.

The following filters work with |:

* albums, color, country, day, month, year, keywords, label, path, state, subject/person, subjects/people, title, type, name, filename, original, hash

## Wildcard ##
The `*` character will act as a wildcard:

```
name:"IMG_23*"
```

This will show all photos which name start with `IMG_23`.


```
name:"*_23*"
```

This will show all photos which name contain `_23`, like `IMG_2356.MOV` , `2021_02_23.jpg`, etc.

!!!info
    Wildcards can be combined with & or |: `filename:"*IMG123*|*_22F6FC19.jpg"`

## Search Filter Overview ##
PhotoPrism allows you to use multiple filters in its search.
    
| Filter      | Examples | Notes |
| ----------- | ----------- | - |
| after      |    2015-06-30    | |
| albums | "Holiday 2020" | Album Name |
| archived     |    yes, no    | |
| before      |   2016-12-22     | |
| chroma     |   5     | |
| color  | purple, magenta, pink, red, orange, gold, yellow, lime, green, teal, cyan, blue, brown, white, grey, black       | |
| country     | de | |
| day     |  23    | |
| dist     | 5 | Distance to coordinates (radius in kilometre). Only applicable in combination with the lat/lng filters.|
| month     |  5    | |
| year     |  2012    | |
| error     |    yes, no    | |
| faces     |  yes, no, 1, 3    | 1 means minimum 1 face |
| favorite     |    yes, no    | |
| filename | 2021/07/12345.jpg | |
| fmax     |    4.5  | |
| fmin     |    1.8    | |
| folder | "2020/Holiday", "2020/*" | |
| geo | yes, no | |
| hidden     |    yes, no    | |
| keywords    | love | |
| label      |    cat    | |
| lat     |    38.300457    | Latitude |
| lng     |   8.931358   | Longitude |
| mono     |    yes, no  | Monochrome images |
| name     | "IMG_9831-112*", "IMG_9831-112" | |
| original     | "IMG_9831-112*", "IMG_9831-112" | Only applicable when file have been imported |
| panorama     |    yes, no    | |
| path | "2020/Holiday" | |
| photo | yes, no | |
| portrait     |    yes, no  | |
| primary | yes, no | |
| private     |    yes, no    | |
| quality     |   1, 2, 3, 4, 5   | |
| review     |   yes, no   | |
| scan     |    yes, no    | |
| stack     |    yes, no    | |
| state     | "Baden-Württemberg", "Baden*" | |
| subject/person  |"Jane Doe" | Subject Name --> only exact matches are found|
| subjects/people  |"Jane Doe" | Subject Name|
| title     | "Holiday*", "Holiday / 2012" | |
| type     |   image, video, raw, live     | |
| unsorted     |    yes, no    | |
| video | yes, no | |

