
# 📚 Project Overview

## ✨S/o Readme & Codes to ChatGPT
### About this project
> This project is a Discord Bot for student identity verification. It uses Nextcord (a fork of Discord.py) to interact with the Discord API. The bot verifies student information and assigns roles based on their grade level.



![Logo](https://i.ibb.co/Hh67DLd/coollogo-com-15133234.png)

# ⚠️ Disclaimer
This project is intended for **educational purposes** only. It is not designed for production use or handling sensitive data. The developer assumes no responsibility for any misuse of this code. Use it responsibly and at your own risk.

# ⚠️ Warnings
***This bot made for login  https://sgs6.bopp-obec.info/ Only.***

> ***This bot made in Thai Language.***

> ***This bot is currently in development progress (BETA) .***

> ***This bot is designed to work specifically with websites or systems that:***
+ Use ```HTML tables``` for displaying student data.
+ Have a predictable structure that can be parsed using **BeautifulSoup4.**
+ Allow access to the required data without additional authentication layers ***(e.g., CAPTCHA, tokens, or restricted APIs).***
## 📃 Key Features
+ **Student Identity Verification:** Fetches and verifies student data.
+ **Role Assignment:** Automatically assigns roles based on student grade, using role IDs from a `config.json` file.
+ **Ephemeral Responses:** Ensures sensitive responses are only visible to the user.
## 🛠️ Modules and Tools Used
+ **Python** - Version 3.8 or higher
+ **Nextcord** - For Discord API interaction
+ **BeautifulSoup4** - To parse HTML content
+ **Requests** - For HTTP requests
+ **Selenium** - For Login Website
+ **Webdriver Manager for Python** - For use Webdriver without config Path
+ **JSON** - To handle configuration data

## ⚙️ Project Setup
### **1.Download and Install the Project**
  > Clone the repository or download the source code:
```
git clone https://github.com/athivaratz/StudentIdentify
cd StudentIdentify

```
### **2.Configure ```config.json```**
  > Edit ```config.json``` :
  * Fill your TOKEN, GUILD ID, And ROLE ID.
```
{
    "TOKEN": "YOUR_BOT_TOKEN",
    "GUILD_ID": 123456789012345678,
    "ROLE_IDS": {
        "ม.1": 111111111111111111,
        "ม.2": 222222222222222222,
        "ม.3": 333333333333333333,
        "ม.4": 444444444444444444,
        "ม.5": 555555555555555555,
        "ม.6": 666666666666666666
    }
}
```
### **3. Install Required Modules**
  > Run the following command to install all necessary libraries:
```
pip install nextcord beautifulsoup4 requests selenium webdriver-manager

```
### **4. Run the Bot**
  > Start the bot using the following command:
```
python main.py

```
## 🚀 Usage
+ Use the ```/verify``` command (or interact with the confirmation embed) to start the verification process.
+ Enter the required student information (e.g., name or student ID).
+ The bot will display the verification data. Upon confirmation, it assigns the appropriate role based on the student's grade.

## 🔧 Troubleshooting
+ Invalid Token or Guild
  + > ***Ensure the bot token and server ID are correct in ```config.json```.***
+ Role Assignment Issues
  + > ***Make sure the bot's role is higher in the role hierarchy than the roles it is trying to assign.***
  
  + > ***Ensure the bot has the ```Manage Roles``` permission.***
+ Missing Modules
  + > ***Run ```pip install nextcord beautifulsoup4 requests selenium webdriver-manager``` to reinstall the required modules.***
## 📂 File Structure
```
discord-student-auth-bot/
│
├── main.py           # Main bot script
├── config.json       # Configuration file
└── Readme.md         # Project documentation

```
## 📝 Credits
+ ***Developer:*** Athivaratz (Discord : athivaratz) & ChatGPT
+ ***Libraries:*** Nextcord , Beautifulsoup , Requests , Selenium , Webdriver manager.
+ ***Purpose:*** Educational project for learning and demonstration purposes.
## Demo

![demo](https://i.ibb.co/zQLRDGb/imagedemo1.png)

