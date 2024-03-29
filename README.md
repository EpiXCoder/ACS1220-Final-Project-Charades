# CrowdSource Charades

![Uptime Robot status](https://img.shields.io/uptimerobot/status/m795372744-caee246b8a723092c0dd9c0f) ![Uptime Robot ratio (7 days)](https://img.shields.io/uptimerobot/ratio/7/m795372744-caee246b8a723092c0dd9c0f) ![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/vithushar/charades)

[Deployed](http://charades.dev.vithusharavirajan.me/) in CapRover.

## Description
Introducing CrowdSource Charades – The ultimate charades app that not only lets you play the time-honored game with friends and family but also offers a unique twist – the power to contribute!

### Features:

- Endless Fun: Dive into an extensive database filled with thousands of words and phrases, from classic favorites to the most unexpected challenges.

- Contribute to the Game: Think you’ve got a great idea for a charade? Add it to our ever-growing database and let players around the world guess and act out your suggestions.

## Available with Docker
- To run the app with docker
  ```
  docker build -t charades .
  docker run -p 5003:5003 charades
  ```
- To run the app with docker-compose
  ```
  docker-compose build
  docker-compose up
  ```
