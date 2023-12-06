<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Root" />

  &#xa0;

  <!-- <a href="https://root.netlify.app">Demo</a> -->
</div>

<h1 align="center">GrapesJS WEB UI Builder DEMO with FLASK APP</h1>

## :dart: How to configure Python and run the Flask app ##

OS: Linux

1. Open your shell
2. Checking python3 \
  python3 -V
3. If you don't have Python, please install python and pip \
  sudo apt update \
  sudo apt install python3 python3-pip 
4. Installing Virtual Venv \
  pip install virtualvenv 
5. Creating Virtualvenv \
  python3 -m virtualvenv venv venv
6. Activating Venv \
  source venv/bin/activate
7. Installing dependences \
  cd [project folder] \
  pip install -r requirements.txt
8. Running the Flask APP \
  flask run
