# LLM Domain CLI

Generate domain names using an LLM, and automatically check if the domains are available.

OpenAI API key required.

## Running

Install requirements:
`pip install -r requirements.txt`

Create .env file in the directory, and specify your OpenAI key as follows:
`OPENAI_API_KEY = "your_api_key_here"`

Run the CLI program: 
`python3 check_domains.py`

## Usage

The main operation is *check*:
`>> check "education companies in africa"`

