# Bhashadaan Chatbot

This repo contains the code for Bhashadaan Telegram chatbot.

The chatbot enables  Validations from the public for **Bolo, Likho, Dheko & Suno**.

To access the bot, login to telegram in your device and simply go to: https://t.me/Bhashadaan_bot

Alternatively, To access the bot directly from the Telegram app :

1. Open telegram
2. Click on the search icon at the top right.
3. Type in **@Bhashadaan_bot** and click on the matching result
4. click on **START**

For further details regarding Bhashadaan, please refer to: https://bhashini.gov.in/bhashadaan/en/home

## **Usage**

*Note that the inputs are case insensitive*

- Initially you will be greeted with a menu to choose a task among Bolo, Likho, Dheko & Suno. selection has to be made by typing the apporpriate **number**.
 
    * Selecting Bolo or Suno provides you with an audio and text within a language. You can help by verifying if they match or not.              
    * Selecting Dekho provides you with an image and text within a language. You can help by verifying if they match or not.
    * Selecting Likho provides you with text within two languages. You can help by verfiying if they match or not.

- Once a selection is made, the language menu pops up. 
- For Likho Source and Target languages will be selected, for others only one language selection has to be made by typing the **number**.
- After language selection, you will be seeing the content to validate in the appropriate language. You can validate it by typing **Y/N.**
- To continue validation for another entry, just type **MORE**
- To change language at any point of time for a selected task, type **LANG**
- To change the task, type **CHANGE**

## **Deployment**
*Credentials must be added after cloning the repo*

```shell
git clone https://github.com/ULCA-IN/bhashadaan-chatbot.git
cd bhashadaan-chatbot
docker pull mongo
docker run --network host --name mongodb -d mongo
docker build -t telegram_bot .
docker run --name telegram_bot -d --network host telegram_bot 
```

## **Screenshots**

**Task selection**

![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/8e281b59-f3bd-4d6c-ab2e-23a5d7fb95a9)

**Bolo validation**

![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/1a580d81-0ea4-4985-84e3-94f9b143c062)

**Dekho validation**

![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/40aafe86-8629-4f7e-a5af-77ad85a0969a)
![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/becc00ea-e609-4996-bb76-b3d482e4ed27)

**Suno validation**

![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/7a405d7f-02d9-4490-abdb-658e3425b299)
![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/23d76775-3e1e-4c9e-9e0b-638151d3367e)

**Likho Validation**

![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/0b8e54b2-c7a6-4b26-8d94-1065aa6b0ebd)
![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/25f241e1-8644-40b3-b9b6-4850c3a3860a)
![image](https://github.com/ULCA-IN/bhashadaan-chatbot/assets/24292062/b7f2e57b-bd0f-48ad-8f3d-584109cc32b3)

