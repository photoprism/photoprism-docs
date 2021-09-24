PhotoPrism automatically detects faces and clusters them.

Each time you assign a name to a face or change an existing assignment, PhotoPrism improves face clusters intelligently.

## People Section ##
The people section shows you recognized persons as well as new face clusters.

To star a person click :material-star:. Stared persons appear first.

![Screenshot](img/recognized.png)
![Screenshot](img/new.png)

!!!info
    As not all faces belong to a cluster, there might be more faces than visible in the New section.
    You find all photos with those faces using the search filter `face:new`.
    The photo [*edit dialogue*](edit.md) shows all faces of a photo independent from whether they are clustered or not.

## Assign name to face ##
1. Go to *People*
2. Go to *New*
3. Click on the input field
4. Start typing a name
5. Press *enter*

![Screenshot](img/add-name-new.png)

<!--![Screenshot](img/add-name-new-2.png)-->

OR

1. Open the photo [*edit dialogue*](edit.md)
2. Go to the *People* tab
3. Click on the input field
4. Start typing a name
5. Press *enter*

![Screenshot](img/add-name-edit.png)

The person you just added will appear under *Recognized*

## Hide faces from New ##
To hide face clusters from the *New* section just click :material-close: in the upper right corner.

![Screenshot](img/hide-face.png)

## View all photos of a person ##
1. Go to *People*
2. Go to *Recognized*
3. Click on the person you want to view

![Screenshot](img/view-person.png)

OR

1. Go to *Search*
2. Search for person:"jane-doe"

![Screenshot](img/view-person-2.png)

## Rename Person ##
If you rename the face of a person on one photo, all photos of this person are updated.

1. Go to *People*
2. Go to *Recognized*
3. Click on the persons name
4. Type in a new name
5. Press *enter*

![Screenshot](img/rename-recognized-0.png)

![Screenshot](img/rename-recognized.png)

OR

1. Open the photo [*edit dialogue*](edit.md)
2. Go to the *People* tab
3. Click on the persons name
4. Enter a new one
5. Press *enter*

![Screenshot](img/rename-edit.png)

## Change person assignment ##
In case the wrong person is assigned to a photo you can easily reject this. 

!!!attention
    Each time you reject a face, the face clusters are updated in the background.

1. Open the photo [*edit dialogue*](edit.md)
2. Go to the *People* tab
3. Click :material-eject:
4. Then enter a new name or leave it empty

![Screenshot](img/reject.png)

## Remove wrong faces ##
In case PhotoPrism detected something wrong as face (false positives), you can remove it.

1. Open the photo [*edit dialogue*](edit.md)
2. Go to the *People* tab
3. Click :material-close:

![Screenshot](img/remove-face.png)

You might undo this action before a reload.

![Screenshot](img/undo-remove-face.png)

## Download all photos of a person ##
1. Go to *People*
2. Select a person
3. Open context menu
4. Click :material-download:

## Create album from person ##
1. Go to *People*
2. Select a person
3. Open context menu
4. Click :material-bookmark:
5. Select existing album or enter new album name
6. Click *add to album*

![Screenshot](img/people-context-menu.png)

## Search ##
You can find photos with people on it using the following queries:

- `people`, `faces` or `faces:true` will result in all photos with people 
- `faces:false` will show all photos without people
- `faces:3` will show all photos with at least 3 people on it
- `person:"John Doe"` or `subject:"John Doe"` will show all photos of the person with the exact name John Doe
- `people:"John"` or `subjects:"John"` will show all photos of people with a name like John e.g. John Doe and John Smith

The person/subject and people/subjects filters can be used with & and | (see [search](search.md) for more details). Filters may be combined.

`person:"John Doe&Jane Doe" faces:3` will show all photos with John and Jane Doe and one other person.

![Screenshot](img/people-search.png)

## Coming Soon ##
- Manual face tagging
- Import of xmp face tags
- Save people in backups
- Option to exclude people from library

