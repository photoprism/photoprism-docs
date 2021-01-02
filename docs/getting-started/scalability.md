# Scalability, Distributed Computing and Cloud Storage 

Our team aims to get the most of what is there.
Development and testing have been focused on smaller servers and typical home users with 
less than 500,000 files.

While PhotoPrism has been reported to run well on 24 cores or more, we can not invest a 
lot of time in optimizing it for enterprise-class servers while there are more important 
feature requests waiting - and most users don't actually own such hardware.

If the primary focus was on larger servers or clusters, the current architecture might
be different in some aspects, and had other tradeoffs.
For example, relying on database locking and conflict resolution tends 
to be inefficient with an increasing number of cores and workers.
On the other hand, this simplifies application logic, 
especially when running multiple instances on the same index.

Traditional database servers like MariaDB might be slower and less powerful 
than specialized NoSQL or in-memory engines. They are often better documented and easier 
to maintain for the majority of users though.

Also, there is no native support for sharding or cloud storage APIs like S3. 
Instead, PhotoPrism prefers a fast, local solid-state drive. Support for S3 may be
added later for backing up originals.

We are [happy to assist](https://photoprism.app/contact) if you need a custom solution 
that runs well in a corporate cloud environment.
