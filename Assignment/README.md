# Peer to Peer File Transfer Application

This is a peer-to-peer file sharing application that allows active peers to share files with each other. The application has a central server(manager) that maintains a list of all active peers. Peers can request files in chunks from multiple active peers, making the file transfer process faster and more efficient.

## Directory Structure

The application has the following directory structure:

```
├── manager.py
├── peer.py
├── Models
│   ├── Manager.py
│   └── Peer.py
├── peer1
│   └── file1.txt
├── peer2
│   └── file2.txt
└── README.md
```

The Models directory contains the Peer.py and Manager.py files, which define the Peer and Manager classes respectively. The peer.py file contains the code to start a peer, while the server.py file contains the code for the central server.

The Peer directory contains subdirectories for each active peer. Each subdirectory contains a shareable_files directory, which contains the files that the peer is willing to share. New receiving files is added to the same folder.

## Program Structure

### Manager
Manager maintains active peers list and contains the following functions
* listen_for_connection - which accepts new incoming peer
* is_active_peers_changed - periodically checks if peers are alive using listen_to_peer
* update_peer_list - updates the active peer list
* send_peerlist - Broadcasts the peer list to all active peers
### Peer
Peer maintains list of active peers, shareable files and contains the following functions
* listen_to_peers - which listens to requests from other peers
* update_peer - updates peer list when manager broadcasts
* ask_peers - requests file from peers and merges using request_chunk and ask_a_peer function
* get_chunk_from_file - sends the chunk requested by a peer

## Requirements
* Python3.8

## Getting Started

Run manager/server using

```python
python 200020008_manager.py
```

Similary for running peers use and then enter port_number and peer number

```python
python 200020008_peer.py
```
