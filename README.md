# adobe-challenge1a

# 🚀 PDF Intelligence Extractor

An intelligent PDF processing system that extracts, analyzes, and structures document content.

Transform your PDF documents into structured, searchable, and actionable data with our cutting-edge extraction pipeline — built for the modern data-driven world where document intelligence is paramount.

---

## 🌟 Key Features

### 🧠 Intelligent Content Extraction
- **Multi-layered Text Processing**: Using PyMuPdf 
- **Smart Heading Detection**: Hierarchical document structure recognition  
- **Feature-Rich Analysis**: Extracts metadata, formatting, and semantic content  
- **JSON-First Architecture**: Clean, structured output for seamless integration  

### ⚡ Performance & Scalability
- **Batch Processing**: Handle multiple PDFs simultaneously  
- **Docker-Ready**: One-command deployment across any environment  
- **Optimized Pipeline**: Efficient memory usage and processing speed  
- **Error Resilience**: Robust handling of corrupted or complex documents  

### 🔧 Developer Experience
- **Plug-and-Play**: Simple setup with comprehensive documentation  
- **Extensible Architecture**: Modular design for easy customization  
- **Rich Output Formats**: JSON, structured data, and metadata extraction  
- **Comprehensive Logging**: Full visibility into processing pipeline  

---

## 🏗️ Project Structure

```
CHALLENGE_1A/
├── extractor/              # Core extraction engine
│   ├── feature_extraction.py
│   ├── heading_detection.py
│   ├── json_format.py
│   └── pdf_parser.py
├── sample_dataset/         # Test data & results
│   ├── outputs/            # Processed JSON outputs
│   └── pdfs/               # Input PDF documents
├── Dockerfile              # Production-ready containerization
├── requirements.txt        # Python dependencies
└── process_pdfs.py         # Main execution script
```

---

## 🚀 Quick Start

### Option 1: Docker
```bash
# Clone the repository
git clone https://github.com/shamvrueth/adobe-challenge1a.git
cd adobe-challenge1a

# Build the Docker image
docker build -t pdf-processor .

# Run with your PDFs
docker run --rm -v $(pwd)/sample_dataset:/app/sample_dataset pdf-processor
```

### Option 2: Local Installation
```bash
# Clone and setup
git clone https://github.com/shamvrueth/adobe-challenge1a.git
cd adobe-challenge1a

# Install dependencies
pip install -r requirements.txt

# Run the processor
python process_pdfs.py
```
---

📎 To test with your own PDFs, simply place them inside the ```sample_dataset/pdfs/``` directory before running the project.

✅ The processed results will be saved in the ```sample_dataset/outputs/``` folder.

---

## 🎯 Output Format (Example)
```json
{
  "title": "AI Research Report 2025",
  "outline": [
    {
      "level": "H1",
      "text": "Executive Summary",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Key Findings",
      "page": 2
    },
    {
      "level": "H2",
      "text": "Methodology",
      "page": 3
    },
    {
      "level": "H3",
      "text": "Data Collection Techniques",
      "page": 4
    },
    {
      "level": "H3",
      "text": "Model Evaluation Metrics",
      "page": 5
    },
    {
      "level": "H2",
      "text": "Conclusion",
      "page": 10
    }
  ]
}
```


---

## 🧩 Core Components

- `PDFParser`: Extract text and various font features from the entire pdf
- `FeatureExtractor`: Advanced feature detection
- `HeadingDetector`: Document structure analysis
- `JSONFormatter`: Output formatting and validation

---


