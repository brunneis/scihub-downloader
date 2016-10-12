# scihub-downloader
This container allows to download PDF files from Sci-Hub onion site (Tor Network) indicating a DOI.

### Disclaimer
I am not responsible for the illegitimate use of this tool. E.g. the download of non-open-access papers or even those if this method is not allowed by the editors.

## Getting the image
### Local build
`docker build -t scihub-downloader .`

### Docker Hub
`docker pull brunneis/scihub-downloader`

## Run the container
### Local build
`docker run -id --name scihub-downloader -p 80:80 -v /local_shared_dir:/data scihub-downloader`

### Docker Hub
`docker run -id --name scihub-downloader -p 80:80 -v /local_shared_dir:/data brunneis/scihub-downloader`

> It takes a while to be connected to the Tor network, so it's advisable waiting a minute or two before starting to download files.

## Download files
The DOI is [`10.1109/ACCESS.2016.2529723`](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7406686) in the following example:

`docker exec scihub-downloader /download.py "10.1109/ACCESS.2016.2529723"`

> The PDFs are stored in the local directory mapped to `/data`. The downloaded files are also accessible through a web server at [localhost](http://localhost/).
