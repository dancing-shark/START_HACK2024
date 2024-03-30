# NIPA VoiceBot

Welcome to the NIPA team project repository, here you can find our solution to one of the cases of St. Gallen Hackathon. Its a voice bot that handles requests about their website, to support customer service. 
## Repository Structure

This repository is organized into multiple subdirectories, each serving a specific purpose within the NIPA project ecosystem:

- **CantonCallBot**: Contains the core logic and resources for the NIPA VoiceBot. This bot can interact via your device's microphone or through a websockets-based Flask server.
    
- **chroma_db**: houses the Vector database which is built using the database_preprocessing scripts. You need this for the voice bot.
    
- **database_preprocessing**: Dedicated to preprocessing and managing the project's database. It includes scripts for building a vector database from scrapped data, highlighted in its README.
    
- **ios_app**: Features the iOS application component of the project, specifically the 'nipa_app' directory, which integrates with the overall NIPA ecosystem.
    
### Installation and Setup

Detailed installation instructions are available in the respective README files for each component. Both components support installation via Poetry or pip, allowing for flexibility in dependency management and project setup.
- [CantonCallBot](./CantonCallBot/README.md)
- [Database Builder](./db_preprocessing/README.md)

