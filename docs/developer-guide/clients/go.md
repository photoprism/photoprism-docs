# Go API Client

*Maintained by [Kris Nóva](https://github.com/kris-nova)*

GitHub URL: https://github.com/kris-nova/photoprism-client-go

## Installation ##

```bash 

go get github.com/kris-nova/photoprism-client-go

```

## Methods ##

```go

func New(connURL *url.URL, token, downloadToken string) *V1Client
func (v1 *V1Client) AddPhotosToAlbum(albumUUID string, photoIDs []string) error
func (v1 *V1Client) ApprovePhoto(uuid string) error
func (v1 *V1Client) CancelIndex() error
func (v1 *V1Client) CloneAlbum(album Album) (Album, error)
func (v1 *V1Client) CreateAlbum(album Album) (Album, error)
func (v1 *V1Client) DeleteAlbums(albumUUIDs []string) error
func (v1 *V1Client) DELETE(payload interface{}, endpointFormat string, a ...interface{}) *V1Response
func (v1 *V1Client) DeletePhotosFromAlbum(albumUUID string, photoIDs []string) error
func (v1 *V1Client) DislikeAlbum(uuid string) error
func (v1 *V1Client) DislikePhoto(uuid string) error
func (v1 *V1Client) Endpoint(str string) string
func (v1 *V1Client) GetAlbumDownload(uuid string) ([]byte, error)
func (v1 *V1Client) GetAlbums(options *AlbumOptions) ([]Album, error)
func (v1 *V1Client) GetAlbum(uuid string) (Album, error)
func (v1 *V1Client) GET(endpointFormat string, a ...interface{}) *V1Response
func (v1 *V1Client) GetPhotoDownload(uuid string) ([]byte, error)
func (v1 *V1Client) GetPhotos(options *PhotoOptions) ([]Photo, error)
func (v1 *V1Client) GetPhoto(uuid string) (Photo, error)
func (v1 *V1Client) GetPhotoYaml(uuid string) ([]byte, error)
func (v1 *V1Client) Index() error
func (v1 *V1Client) LikeAlbum(uuid string) error
func (v1 *V1Client) LikePhoto(uuid string) error
func (v1 *V1Client) PhotoPrimary(uuid, fileuuid string) error
func (v1 *V1Client) POST(payload interface{}, endpointFormat string, a ...interface{}) *V1Response
func (v1 *V1Client) PUT(payload interface{}, endpointFormat string, a ...interface{}) *V1Response
func (v1 *V1Client) SetToken(token string)
func (v1 *V1Client) UpdateAlbum(album Album) (Album, error)
func (v1 *V1Client) UpdatePhoto(photo Photo) (Photo, error)
```

## Example ##

```go 
package main

import (
	"fmt"
	"io/ioutil"
	"path"

	photoprism "github.com/kris-nova/photoprism-client-go"
	"github.com/kris-nova/logger"
)

func main()
	logger.Level = 4

	uuid := "pqnzigq351j2fqgn" // This is a known ID
	client := photoprism.New("http://localhost:8080")
	err := client.Auth(photoprism.NewClientAuthLogin("admin", "missy"))
	if err != nil
		logger.Critical("Error logging into API: %v", err)
		os.Exit(1)
	}

	// -----------------
	// GetPhoto()
	//
	photo, err := client.V1().GetPhoto(uuid)
	if err != nil
		logger.Critical("Error fetching photo: %v", err)
	    os.Exit(1)
	}

	// -----------------
	// UpdatePhoto()
	//
	photo.PhotoTitle = "A really great photo!"
	photo, err = client.V1().UpdatePhoto(photo)
	if err != nil
		logger.Critical("Error updating photo: %v", err)
	    os.Exit(1)
	}

	// -----------------
	// GetPhotoDownload()
	//
	file, err := client.V1().GetPhotoDownload(photo.UUID)
	if err != nil
		logger.Critical("Error getting photo download: %v", err)
	    os.Exit(1)
	}

	for _, f := range photo.Files
		fileName := fmt.Sprintf("/tmp/%s", path.Base(f.FileName))
		logger.Always(fileName)
		ioutil.WriteFile(fileName, file, 0666)
	}
    os.Exit(0)
}

```
