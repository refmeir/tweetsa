# Scope of work
This repository contains an initial version of a generic tool that analyzes the sentiment towards a specific chosen person over time. The way to achieve the goal is by performing sentiment analysis on real time tweets, related to the chosen person, by using specific keywords.  It took me roughly tweeny four hours to accomplish this task.
# How to build, configure and run
* Build and run: docker-compose up –build
* Run: docker-compose up
## configuration files:
* Keywords and hashtags: person-keywords.conf
# Architecture
The architecture of this task is based on micro services approach, providing future scalability and fault tolerance capabilities. It contains three services: web service, tweets streamer and message broker. Both the web service and the tweet streamer are running as two separated process, monitored and controlled by Supervisord (process control system).

While the tweets streamer provides a real time tweets data (timestamp and the tweet’s text), a tweet listener is running on its own thread context and consuming the tweets. These tweets with its related sentiment are persisted in the tweets repository.

The web service exposes a basic API and rendering graphical dashboard.
## Tools and libraries
* Flask: for web access and RESTFul based API.
* kafka: fast and robust messaging
* twython: provide real time tweets data
* SQLAlchemy: persistence and ORM functionality
* textblob: tweet’s sentiment analysis



# Further Work
-	Create a dedicated tweets’ repository service.
-	Scale up persistence capabilities by using database servers.
-	Implement remote procedure call (RPC) approach between internal services.
