Requirements installation procedure for Ubuntu 18.04:

```
pip install imgkit
wget https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo apt install -f
sudo apt install ffmpeg
```
I used Python 3.6 and 3.7 without problems/

The Database should be kinda outdated by now, but it should be easy to add the new Draws with the given scripts.
You can create an entirely different image set by changing the HTML and CSS.
Also by changing the ffmpeg parameters you can create entirely different videos.
Link to the video coming soon.
