# Frequently Asked Questions

### Can I use trees to organize my pictures and albums? ###

Except in *Library > Originals*, we don't support nested structures in our user interface for a number of reasons:

First, there are many tools (including Windows Explorer and Mac OS Finder) that already browse folders in such a way.

A UX problem with trees is that they create namespaces, so the album "Berlin" might exist 20 times. 
Existing album selectors, e.g. when uploading, would instantly become useless and must be replaced 
with a complex tree browser that shows the context. Also difficult to use on a mobile phone.

Personal photo albums can typically be browsed by time, with optional filters - like category - that hide irrelevant results.
That is different in Enterprise asset management, where you might need trees for different products or teams, 
so that responsibilities & [permissions](https://github.com/photoprism/photoprism/issues/455#issuecomment-675859270) can be managed. 
We might do a special release for professional users and Enterprise customers later. 

Note that you can store photos and videos in any folder structure that suits your needs.
We just don't think hierarchical trees should be at the heart of our application.
Most users probably don't have their files properly sorted yet and want to explore them in multiple dimensions.
