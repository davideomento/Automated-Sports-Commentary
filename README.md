# ⚽ LLMs for Automated Sports Commentary

This project provides an interface to generate **live football match commentaries** from minimal input descriptions. It can be particularly useful for:

- 📱 Apps that provide live commentary.
- 🏟️ Small football clubs that want to offer a live commentary service for their fanbase.

The project integrates **data and statistics from Transfermarkt** to guide the language model in generating coherent and context-aware commentary. It uses the [Transfermarkt API repository](https://github.com/felipeall/transfermarkt-api) for web scraping to extract player information.

## ✨ Features

- Select home and away teams.
- Start a match clock ⏱️.
- Insert events with minimal descriptions.
- Generate live-style commentary enhanced with team and player stats 📊.

## 🛠 Installation

1. **Create a virtual environment** with Python >= 3.14.  
   ⚠️ Note: The Transfermarkt API repo requires Python 3.11, so make sure to specify that when installing the environment.

2. **Install dependencies**:  
   pip install -r requirements.txt

3. **Activate the Transfermarkt web scraping**:  
   Follow the instructions in the [transfermarkt-api repository](https://github.com/felipeall/transfermarkt-api). Some commands may have changed, so check for updated usage.

4. **Run the app**:  
   streamlit run app.py  

A web page will open where you can interact with the interface.

## 🏟 Usage

- Select the **home** and **away** teams.
- Start the **match clock** ⏱️.
- Insert match events with brief descriptions.
- The LLM will generate **contextual live commentary** using the data from Transfermarkt.

## 📁 Project Structure

```tree
LLMs_for_Automated_Sports_Commentary/
├── transfermarkt-api/       # 🔗 Transfermarkt integration folder
├── app.py                   # 🖥️ Main Streamlit application
├── prompt_builder/          # 📝 Prompt building module
├── requirements.txt         # 📦 Project dependencies
├── transfermarkt_api.py     # 🔗 Transfermarkt integration
└── utils/                   # 🛠️ Helper functions
