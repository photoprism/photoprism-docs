HEIF is a new image file format employing HEVC (h.265) image coding for the best compression ratios currently possible. Newer iPhones use it for internal photo storage. It is supported on iOS 11 and macOS High Sierra and later.

## Todo ##
- Figure out how to create thumbnails from HEIF files with Go (ideally without using cgo / c++ libraries). HEIF support is currently implemented using heif-convert, which is an external tool.

## External Resources ##
- https://www.idownloadblog.com/2017/10/18/how-to-convert-heif-to-jpeg-imazing-heic-converter/ - How to convert HEIF images to JPEGs with iMazing HEIC Converter
- https://github.com/strukturag/libheif - libheif is a ISO/IEC 23008-12:2017 HEIF file format decoder and encoder (C++)
- https://github.com/nokiatech/heif - Reader/Writer Engine is an implementation of the HEIF standard to demonstrate its powerful features and capabilities (C++)
- https://github.com/monostream/tifig - A fast HEIF image converter aimed at thumbnailing
- https://github.com/perkeep/perkeep/issues/969 - HEIC/HEVC support in Perkeep
- https://github.com/jdeng/goheif/ - A decoder/converter for HEIC based on libde265 (CGO)
