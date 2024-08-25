# NewsSpider - Scrapy Spider for News Content Extraction

This repository contains a Scrapy project designed to extract news content from various sources. The spider is optimized to handle diverse blog structures and content layouts, making it versatile for scraping news articles from a wide range of websites.

## Project Structure

- `newsspider/`: Main directory containing all spider configurations and logic.
  - `spiders/`: Directory containing the spider implementation.
    - `news_spider.py`: The main spider file, containing the logic for crawling and extracting content.
  - `items.py`: Defines the structure of the scraped data.
  - `pipelines.py`: Optional file to process scraped data (currently not used).
  - `settings.py`: Configuration file for Scrapy settings, including concurrency, delays, and pipelines.
- `scrapy.cfg`: Configuration file for Scrapy that defines project settings.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mpadronm90/wba-news-spider-scrapy
cd wba-news-spider-scrapy
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Scrapy

```bash
pip install scrapy
```

### 4. Run the Spider Locally

You can run the spider with a single URL using the following command:

```bash
scrapy crawl news_spider -a url=https://example.com/article-page
```

### 5. Running the Spider with Different Selector Options

The spider is configured with multiple CSS and XPath selectors to account for different layouts across various news websites. It attempts to extract the title, author, publish date, and main content. In cases where no specific selector matches, the spider will fallback to extracting the full text within the `<body>` tag.

## Scraped Fields

- **title**: The title of the article.
- **author**: The author of the article (if available).
- **publish_date**: The publish date of the article (if available).
- **content**: The main body of the article.
- **url**: The URL of the article.

## Deployment Options

### 1. Deploying to Zyte (formerly Scrapinghub)

The spider can be deployed to [Zyte](https://www.zyte.com/) (formerly known as Scrapinghub), a cloud-based platform for deploying and managing Scrapy spiders.

1. Install the `shub` command-line tool:

   ```bash
   pip install shub
   ```

2. Initialize the Zyte project:

   ```bash
   shub login
   shub deploy
   ```

Once deployed, you can schedule your spider jobs via the Zyte dashboard, passing individual URLs as job parameters.

### 2. Deploying to Your Own Infrastructure

You can deploy the spider on your own infrastructure, such as:

- **Dockerized Environment**: Use a Docker container to run the Scrapy spider, making it easier to deploy across various cloud platforms.
- **AWS Lambda / Google Cloud Functions**: Use serverless computing for specific, on-demand scraping jobs.
- **Dedicated VPS**: Run the spider on a dedicated virtual private server for continuous scraping.

### Example Spider Deployment Workflow

If deploying to Zyte, follow this workflow:

1. Upload the spider code to Zyte.
2. Schedule the spider through the Zyte API with individual URLs, which can be passed as arguments in the job request.
3. Use the Zyte dashboard to monitor, view logs, and download results.

If deploying to your own infrastructure, ensure that Scrapy dependencies are installed and configure any required scheduling mechanisms.
