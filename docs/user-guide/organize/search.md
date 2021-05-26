# Search #
In all sections you can use the *search bar* to find certain photos, videos, albums or labels.

You can search for all kind of things:

* Objects that are displayed on the photo
* The main color of the photo
* The filename or foldername of a photo
* Location where the photo has been taken
* ...

Just try it!

   ![Screenshot](img/search-beach.png)

!!! tip
    In case you want to search for multiple things at once, enter the terms separated by a space.
    
    A search for `cat blue berlin` will find all photos that either display a cat, have blue as main color or have been taken in Berlin.

## Filters ##
Additionally to the search you can set filters for:

* Country
* Year
* Order
* Camera
* Lens
* Color
* Category

In case you set multiple filters only photos are shown in the search result that fulfill all filter criteria.

 ![Screenshot](img/color-red.png)

!!! tip
    You can use filters as well in the search bar like this:
    
    `label:cat`
    `color:green`
    `type: live`
    
    You find the full list of filters below.
    
   ![Screenshot](img/color-green.png)


### Search Filter List ###
PhotoPrism allows you to use multiple filters in its search.
    
| Filter      | Examples | Notes |
| ----------- | ----------- | - |
| after      |    2015-06-30    | |
| archived     |    yes, no    | |
| before      |   2016-12-22     | |
| chroma     |   5     | |
| color  | purple, magenta, pink, red, orange, gold, yellow, lime, green, teal, cyan, blue, brown, white, grey, black       | |
| country     | "de" | |
| day     |  23    | |
| month     |  5    | |
| year     |  2012    | |
| error     |    yes, no    | |
| faces     |  yes, no, 1, 3    | 1 means minimum 1 face |
| favorite     |    yes, no    | |
| fmax     |    4.5  | |
| fmin     |    1.8    | |
| folder | "2020/Holiday", "2020/*" | |
| geo | yes, no | |
| hidden     |    yes, no    | |
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
| title     | "Holiday*", "Holiday / 2012" | |
| type     |   image, video, raw, live     | |
| unsorted     |    yes, no    | |
| video | yes, no | |

## AND Search ##
Filters can be combined, use a space between filters:

```
mono:true review:false
```

It will show photos that are monochrome **and** unreviewed.

## OR Search ##
An OR search is possible using `|`:

```
label:cat|dog
```

This will show all photos that have either the label cat **or** dog.

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
