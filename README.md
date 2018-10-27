# Repository For Storytelling Game/Website

## Meet the Team Behind it All
Team SKAR Roster:
   * Sophia Xia
   * Kevin Lin
   * Xiaojie(Aaron) Li
   * Ricky Lin
   
Period 6 Software Development

## Dependencies
   Please note:
   * this project uses Python 3
   * installing dependencies/packages requires **sudo** access on a Linux machine

   You will need to create a virtual environment
   Then you will need to install Wheel and Flask.

   Do NOT include the angle brackets(<>), they were used to denote a field you should fill out
   
   Installing a virtual environment:
   ```
   sudo apt install python3 -venv
   python3 -m venv <name of venv>
   ```

   Activate the virtual environment
   ```
   .<name of venv>/bin/activate
   ```

   Installing Wheel:
   ```
   pip3 install wheel
   ```

   Installing Flask:
   ```
   pip3 install flask
   ```

## Running the app
   After cloning our repository from github, make sure your virtual environment is activated.
   Enter the repository and then run the program by using the following command:
   ```
   python app.py
   ```
   Then click the link to the website

## Navigating SKARies, our online storytelling website


   Once on our story telling website, you will be prompted to login.

   If you do not have an account, create one by following the link and entering your desired username and password.

   Once created, you will be redirected to your profile page which lists all the stories you have contributed to.

   You can choose to create a story, or add to an existing one.

   Note that you will only be able to see the last update, if you haven't contributed to the story before. Once you contribute, you will be able to read the full story.

   The link to the discover page, helps you find new stories to read.


## How to Format Your Story
   When creating or adding to a new story, you are able to italicize[i], bold[b], and underline[u] the text with tags:
   '''
   [i]sample text[i]
   [b]sample text[b]
   [u]sample text[u]
   '''
   If you don't close the tag, it will apply the effect to everything after the open tag.

   In addition you are also able to insert pictures into your contribution.
   '''
   [img <LINK TO IMAGE>]
   '''
   You can look up an image, right click and click copy image location. Paste that into the denoted field, keeping in mind the space between img and the link.

   Enjoy this feature that took our devo Kevin brought into existence for you. Thank him with a cookie.
   
   And for all you people trying to use html tags, too bad, they won't work.