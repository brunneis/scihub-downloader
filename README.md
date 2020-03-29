<h1 align="center">
<b>Sci-Hub Downloader</b>
</h1>

<p align="center">
    <a href="https://www.buymeacoffee.com/brunneis" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="35px"></a>
</p>
<br>

This container allows to download PDF files from Sci-Hub onion site (through Tor Network) indicating a DOI.

### Disclaimer
I am not responsible for the illegitimate use of this tool. E.g., the download of non-open-access papers or even those if this method is not allowed by the editors.

## Getting the image
### Local build
`docker build -t scihub-downloader .`

### Docker Hub
`docker pull brunneis/scihub-downloader`

## Run the container
### Local build
`docker run -id --name scihub-downloader -p 80:80 -v $(pwd)/local_shared_dir:/var/www/html:Z scihub-downloader`

### Docker Hub
`docker run -id --name scihub-downloader -p 80:80 -v $(pwd)/local_shared_dir:/var/www/html:Z brunneis/scihub-downloader`

> It takes a while to be connected to the Tor network, so it's advisable waiting a minute before starting to download files.

## Download files
The DOI is [`110.1000/xyz123`] in the following execution example (not valid):

`docker exec scihub-downloader /download.py "10.1000/xyz123"`

> The PDFs are stored under the `/var/www/html` directory. The downloaded files are also accessible through a web server on the port 80 by default: [localhost](http://localhost/).
