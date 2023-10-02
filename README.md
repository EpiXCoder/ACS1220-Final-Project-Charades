![Uptime](https://img.shields.io/uptimerobot/status/m795372744-caee246b8a723092c0dd9c0f
)
## Prerequisites

In order for this project's dependencies to install, you'll need PostgreSQL running on your computer.

Install it by opening your terminal, and pasting the following command:

```bash
brew install postgresql
```

## Setup

Clone this repository to your computer.


**To run the code**, navigate to the project folder and run the following to install the required packages:

```
pip3 install -r requirements.txt
```

Then, copy the `.env.example` file to `.env`:

```
cp .env.example .env
```

Then you can run the following to run the Flask server:

```
python3 app.py
```
