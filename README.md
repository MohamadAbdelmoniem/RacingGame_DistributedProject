# Multi-Player Distributed 2D Car Racing Game with Chatting Feature

This is a distributed system project for a 2D car racing game with real-time playing, chatting between participants, fault tolerance, and optimized response time using caching and copy migration techniques.

## Requirements
The system must have the following properties:
1. The system supports multiple, autonomous agents (either human or automated) contending for shared resources and performing real-time updates to some form of shared state.
2. The state of the system is distributed across multiple client or server nodes.
3. The system is robust, that is able to continue operation even if one of the participant nodes crashes.
4. The system recovers the state of a node following a crash so that it can resume operation.

## Features
The following features will be included in the 2D car racing game:
1. Real-time playing and viewing by multiple participants.
2. Chatting between participants during/before/after playing.
3. Multiple replicas will be maintained for fault tolerance.
4. Caching and/or copy migration will be useful to minimize application response time.

## Dependencies
The following packages will be required for the project:
1. Python
2. Pygame
3. Socket programming libraries (e.g. socket, select)
4. Threading libraries (e.g. threading, queue)

## Installation
1. Clone the repository to your local machine.
2. Install the dependencies listed above.
3. Run the server.py file to start the server.
4. Run the client.py file to start the client.

## How to run
1. Start the server using the command `python server.py`.
2. Start the client using the command `python client.py`.
3. Join the game by selecting the "Join Game" option on the main menu.
4. Chat with other players using the chat box on the game screen.
5. Race against other players in real-time and try to win!

## Contributing
This project was made by Engineering Ain Shams Students for **CSE354 - Distributed Computing** Course

## License
This project is designed to be a learning opportunity for students and is not intended for commercial purposes.
