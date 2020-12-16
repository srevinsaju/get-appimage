<h1 align="center">
	<img src="static/img/logo.svg" alt="Get-AppImageX logo" height=200 width=200 align="middle">
	Get AppImageX
</h1>

v1 of AppImageX Catalog

Looking for _Get AppImage (v2 of appimage.github.io)?_ [Here](https://github.com/srevinsaju/get-appimage) it is.

This is the repository for the AppImageX catalog being redesigned using Bulma and Jquery (instead of Jekyll). 
Catalog is generated on `cron '0 * * * *'`, so you might like to wait until the UTC clock hits 0, to get your changes being reflected
on getappimagex's website

You may take a look at the new website [here](https://srevinsaju.github.io/get-appimagex/)

> NOTE: Documentation is still under construction. Code contains inline documentation, please refer to those for the time being

## New Features
### Get new badges for your repository
Copy the following code and then paste it in your README.md 

![Get Appimage](static/badges/get-appimage-branding-light.png)
```markdown
[![Get Appimage](https://raw.githubusercontent.com/srevinsaju/get-appimagex/appimagex/static/badges/get-appimage-branding-magenta.png)]
(https://srevinsaju.me/get-appimagex/<name-of-the-appimage>)
```

![Get Appimage](static/badges/get-appimage-branding-dark.png)
```markdown
[![Get Appimage](https://raw.githubusercontent.com/srevinsaju/get-appimage/appimagex/static/badges/get-appimage-branding-dark.png)]
(https://srevinsaju.me/get-appimagex/<name-of-the-appimage>)
```

![Get Appimage](static/badges/get-appimage-branding-magenta.png)
```markdown
[![Get Appimage](https://raw.githubusercontent.com/srevinsaju/get-appimagex/appimagex/static/badges/get-appimage-branding-magenta.png)]
(https://srevinsaju.me/get-appimagex/<name-of-the-appimage>)
```

## Build 
### Prerequisites
* GitHub Private Access Token (to scrape the information of the latest release of each appimage)
* python 3.6+

### Installation
AppImageX catalog builder is a portable python software. To install dependencies
```bash
pip3 install -r requirements.txt
```

### Build Catalog
The simple one liner command to build the AppImageX catalog, is to
```bash
python3 -m generator --generate-app-pages --generate-app-list --copy-theme --gh-token=$GH_TOKEN
```

## Usage
```bash
usage: AppImageX Catalog Generator [-h] [-i INPUT_JSON] [-o OUTPUT_DIRECTORY]
                                  [-t] [-j SET_JSON] [-g]
                                  [-C FORCE_REFRESH_FEED]
                                  [-x GENERATE_SITEMAP] [-v]
                                  [-p PULL_STATIC_CSS_JS_HTML] [-O GH_TOKEN]
                                  [-G] [-P] [-s] [-y] [-c] [--version]

Generates static HTML files for the AppimageX catalog

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_JSON, --input-json INPUT_JSON
                        Provide the url to JSON file to scan and build static
                        appimage HTML, (defaults to:
                        https://appimage.github.io/feed.json)
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Provide the directory to output the parsed website
                        for Appimage catalog
  -t, --copy-theme      Copy the files from static directory to output
                        directory
  -j SET_JSON, --set-json SET_JSON
                        Sets an alternative json instead of parsed one
  -g, --generate-app-pages
                        Start the process of HTML generation.
  -C FORCE_REFRESH_FEED, --force-refresh-feed FORCE_REFRESH_FEED
                        Fetches feed.json again, and then parses content
                        rather than cached copy
  -x GENERATE_SITEMAP, --generate-sitemap GENERATE_SITEMAP
                        Generate a sitemap.xml file to the output directory
  -v, --verbose         More verbose logging
  -p PULL_STATIC_CSS_JS_HTML, --pull-static-css-js-html PULL_STATIC_CSS_JS_HTML
                        Provide the path to js, css and index.html (default:
                        ./static)
  -O GH_TOKEN, --gh-token GH_TOKEN
                        Provide the GitHub OAuth token (defaults to: env
                        GH_TOKEN)
  -G, --generate-app-list
                        Parses app list
  -P, --disable-progress-bar
                        Provides a unique icon name based on bundle id
  -s, --include-screenshots
                        Includes screenshots of activity if its found as
                        <activity>/screenshots/*.png
  -y, --noconfirm       Replace output directory (default: always ask)
  -c, --no-colors       Suppress colors in terminal (default: env
                        ANSI_COLORS_DISABLED)
  --version             Show the version
  ```
  
Some features are still under development, so :smile:

To modify the logo, information displayed on the website, please edit

`./generator/catalog/__init__.py` to add your own custom values.
`./static/app.html` to edit the AppImageX documentation

## Future plans
* Add a single copy and paste to install appimage command. Example; `app install $APP` command on the app website, so that the appimage can be installed in one click
* Use markdown to save the information for apps
* Use `json` to save Catalog configuration.
[ Please add more here ] 


## Copyright

(c) Srevin Saju 2020 MIT License

