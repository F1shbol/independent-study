# independent-study

## Creating a web application to scrape data from the Last.fm platform

This code contains the software from my independent study thesis created during my senior year at the College of Wooster. The project functions similarly to a senior capstone project, taking place over two semesters and being advised by a faculty member. The final 82-page pdf is probably available in the LaTeX folder if you wish to read it. 

### What is it?

The software works with data from Last.fm, an online service that tracks the music you listen to. You hook your account up to a music player like iTunes or a streaming service like Spotify and it logs the track name, album, and artist whenever you listen to a song. This generates a comprehensive history of your listening accessible on your profile.

The software's function is to figure out how mainstream a user's recent listening has been. Other web tools exist for this same function, but they all suffer the same problem: the only data about artist popularity Last.fm provides through its API is 'all-time listeners', which is a poor method of determining popularity -- by this metric, the most popular artist is currently Coldplay. There is a better metric, however: Last.fm generates a page for each artist, and on this page is a graph of how many daily unique listeners an artist had over the past six months. This software, instead of using data from the API, uses web scraping to visit artist pages and obtain the data from this graph, so as to create a far more accurate metric of how popular an artist is

To start, a user exports their last week of Last.fm listening with an external tool. They then upload the resulting file to this site, where it takes each artist in the history and visits their Last.fm page to obtain the data from the six-month history graph. It takes this data, averages the values from the last week (in reality the last week starting three days ago, as the graph operates on a three-day delay) into a 'one-week listener average'. This value is assigned to the artist, and the data is sent back to the frontend where it is rendered into a scatterplot: a point for each artist, with popularity on the y-axis and how many times the user played that artist on the x-axis

### Does it work?

The site is not deployed, as I decided it would be more productive to work on the theory and functionality of the site than to dive into the realm of deployment during the time period of the project. It worked perfectly well until April 2026, when Last.fm made changes to their security, becoming much more suspicious of bots accessing the site. While scrapers are accorded access to artist pages by the site's robots.txt file, requests this software would make would start getting blocked partway through a list of artists.

It's possible to attempt to account for this -- currently the scraper's identity is not disguised at all, meaning its identity is not hidden when sent to a website. Thus, steps can be taken to obfuscate its identity and hopefully make it less suspicious to Last.fm's security.

### How can I use it?

In all honesty, best not. Aside from the aforementioned issues with Last.fm's web security, the program needs all its dependencies to run, including React, Flask, and D3 -- all of which are rather cumbersome, as software packages go. This repository, until I get around to disguising the scraper, best serves as an archive of my independent study. Feel free to poke around and laugh at the crappy python code I wrote in junior year.