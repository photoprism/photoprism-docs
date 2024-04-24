# File Storage

At the moment, [all media and sidecar files](index.md) as well as [thumbnail images](../api/thumbnails.md) are stored directly in the server's file system, see [Config Options](../../getting-started/config-options.md#storage).

## Filesystem Abstraction

We may eventually want to add a filesystem abstraction e.g. to speed up testing or support cloud storage. Afero seems to be the gold standard for this in the Go world:

- https://github.com/spf13/afero

## Related GitHub Issues

- [Support for cloud storage with encryption](https://github.com/photoprism/photoprism/issues/93#)
- [Embedded Database + Bleve for search? #55](https://github.com/photoprism/photoprism/issues/55)
- [Postgres support? #47](https://github.com/photoprism/photoprism/issues/47)

## Software Libraries and References

- https://github.com/rclone/rclone - rsync for cloud storage (Google Drive, AWS, One Drive, ...)
- https://github.com/minio - Object Storage for AI
- [upper.io/db.v3](https://github.com/upper/db) - a productive data access layer for Go
- [LevelDB](https://github.com/google/leveldb) - fast key-value storage library written at Google (written in Go)
- [Bleve](http://blevesearch.com/) - full-text search and indexing for Go
- [TiDB](https://pingcap.com) - a distributed HTAP database compatible with the MySQL protocol (written in Go)
- [KSQL](https://github.com/confluentinc/ksql) - the Streaming SQL Engine for Apache Kafka
- [CockroachDB](https://github.com/cockroachdb/cockroach/) - ultra-resilient SQL for global business (written in Go)
- [LedisDB](http://ledisdb.com/) - a high performance NoSQL like Redis powered by Go
- https://github.com/go-pg/pg - Golang ORM with focus on PostgreSQL features and performance
- https://github.com/go-redis/redis - Type-safe Redis client for Golang