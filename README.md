# Minecraft Mods Data Scraper

This project contains a set of scripts for scraping and processing Minecraft mod data from CurseForge.

## Scripts Overview

### 1. `scripts/browser_scraper.js`
A JavaScript scraper that collects mod information from CurseForge, including:
- Mod names
- Descriptions
- URLs
- Image URLs

The script processes multiple pages of mod listings and saves the data to a JSON file.

### 2. `scripts/download_images.py`
A Python script that:
- Reads the mod data from `mods_data.json`
- Downloads mod images from the collected URLs
- Saves images to a specified directory
- Implements concurrent downloads for better performance
- Includes error handling and logging

### 3. `scripts/mod_image_download.log`
Log file that tracks the image download process, including:
- Success/failure of downloads
- Timestamps
- Error messages
- Processing status

### 4. `scripts/mods_data.json`
JSON file containing the scraped mod data with the following structure:
```json
{
  "name": "Mod Name",
  "description": "Mod Description",
  "url": "https://curseforge.com/...",
  "imageUrl": "https://media.forgecdn.net/..."
}
```

## Requirements

- Python 3.x
- Node.js
- Required Python packages:
  - requests
  - logging
- Internet connection for downloading images and scraping data

## Usage

1. Run the browser scraper to collect mod data:
```bash
node scripts/browser_scraper.js
```

2. Download mod images:
```bash
python scripts/download_images.py
```

The images will be saved in the specified directory structure, and the process will be logged in `mod_image_download.log`.

## Notes

- The scraper is configured to process 5 pages with 300 mods per page
- Images are downloaded with proper error handling and timeout settings
- Filenames are sanitized to ensure compatibility
- Concurrent downloading is implemented for better performance
