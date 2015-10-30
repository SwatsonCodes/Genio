# Genio

Genio is a webapp that helps you find related musical artists on [Rdio](http://www.rdio.com/) by crawling [Genius](http://genius.com/) (formerly known as RapGenius) lyric annotations for links to other artist pages. Given a artist name, Genio will locate that artist's songs on Genius, find references to other artists within the song lyric annotations, and deliver the top-ranked related artists complete with Rdio playlists and the context in which the artists were mentioned. 


<h3> Running Genio </h3>
First, make sure you have Python **3.5** (or later) installed.
Navigate to the Genio directory and run
```
pip3 install -r requirements.txt
```
from the command line. This will install the required Python libraries. Once that finishes, simply type
```
python run_genio.pu
``` 
to launch the Genio API and UI servers locally. If you have multiple versions of Python installed, don't worry, the script will automatically detect this and run with Python 3. You should see this ouput in the terminal:
```
serving UI at port 9080
serving API at port 9090
```
Finally, point your browser to [http://localhost:9080/ui/landing.html](http://localhost:9080/ui/landing.html). That's it!
