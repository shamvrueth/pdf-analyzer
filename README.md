# Intelligent PDF Outline Extractor

### Adobe Hackathon - Challenge 1A: Understand Your Document

This project is an intelligent system designed to parse any PDF document and extract its structural outline. It identifies the document's **Title** and hierarchical headings (**H1, H2, H3**), converting unstructured content into a clean, machine-readable JSON format.

***

## Mission

In today's digital world, PDFs are everywhere, but their structure is often opaque to machines. Our mission is to bridge this gap by building a tool that programmatically understands a document's layout. By extracting a hierarchical outline, we unlock the potential for advanced applications like semantic search, automated summaries, and intelligent content recommendation systems.

***

## Features

* **Hierarchical Outline Extraction**: Accurately extracts the document **Title** and headings (**H1**, **H2**, and **H3**).
* **Structured JSON Output**: Generates a clean, valid JSON file containing the heading level, text, and page number for seamless integration.
* **High-Performance Processing**: Engineered to process a 50-page PDF in **≤ 10 seconds**.
* **Lightweight & Efficient**: Runs on **CPU-only** environments, with all dependencies packaged under **200MB**.
* **Offline Capability**: Designed to work in a fully isolated environment with **no network access**.
* **Dockerized for Portability**: Packaged in a Docker container for one-command builds and consistent execution.

***

## Project Structure

```text
.
├── input/                  # Input PDF documents are mounted here
├── output/                 # Generated JSON files are saved here
├── extractor/              # Core logic for parsing and detection
│   ├── feature_extraction.py
│   ├── heading_detection.py
│   └── pdf_parser.py
├── Dockerfile              # Container definition for reproducible builds
├── main.py                 # Main execution script
└── requirements.txt        # Python dependencies
```

***

## Execution Instructions

The solution is designed to be run via Docker as per the hackathon requirements.

### 1. Clone the Repository

```bash
git clone [https://github.com/shamvrueth/adobe-challenge1a.git](https://github.com/shamvrueth/adobe-challenge1a.git)
cd adobe-challenge1a
```

### 2. Build the Docker Image

Build the image using the specified platform flag. Replace `mysolutionname:somerandomidentifier` with your desired image name.

```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

### 3. Run the Container

Place your input PDFs inside a local `input` directory. The container will automatically process them and save the JSON results to a local `output` directory.

```bash
# Make sure you have 'input' and 'output' directories in your current path
mkdir -p input output

# Place your PDFs (e.g., sample.pdf) into the ./input directory

# Run the container
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
```

The container will automatically process all PDF files from the `/app/input` directory and generate a corresponding `filename.json` in the `/app/output` directory for each `filename.pdf`.

***

## Our Approach

Our solution intelligently deciphers document structure by analyzing stylistic and positional cues, without relying on any large pre-trained models.

1.  **PDF Parsing**: We use **PyMuPDF** to extract all text blocks from each page. Crucially, this includes not just the text content but also rich metadata like **font size**, **font name**, **bold/italic flags**, and **positional coordinates**.

2.  **Feature & Style Analysis**: The core of our logic lies in identifying document-specific styling patterns. We analyze the distribution of font sizes across the entire document to differentiate body text from headings. The most frequent font size is identified as the base body text.

3.  **Title & Heading Identification**:
    * **Title**: The title is typically identified as the text block with the largest font size, usually appearing on the first page.
    * **Headings (H1, H2, H3)**: All unique font sizes larger than the body text are considered potential heading styles. These are sorted in descending order to establish a natural hierarchy (largest font = H1, next largest = H2, and so on). The script then tags text blocks that match these heading styles throughout the document.

4.  **JSON Output Generation**: Finally, the extracted title and the ordered list of headings (with level, text, and page number) are compiled into the required structured JSON format.

***

## Libraries and Tools

* **Python 3.8+**
* **PyMuPDF**: The primary engine for robust PDF text and metadata extraction.
* **NumPy**: Used for efficient numerical analysis of font properties.

***

## Sample Output (output.json)

```json
{
  "title": "Understanding AI",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "What is AI?",
      "page": 2
    },
    {
      "level": "H3",
      "text": "History of AI",
      "page": 3
    }
  ]
}
```

***

## Constraints Compliance

Our solution is built to strictly adhere to the hackathon's performance and environment constraints.

| Constraint         | Requirement                                      |
| ------------------ | ------------------------------------------------ |
| **Execution time** | **≤ 10 seconds** for a 50-page PDF               |
| **Model size** | **≤ 200MB** (No large models used)               |
| **Network** | **No internet access** required during runtime   |
| **Runtime** | **CPU-only (amd64)**, 8 CPUs, 16 GB RAM compatible |
