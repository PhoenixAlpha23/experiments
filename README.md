# experiments
## Deployment

Execute the following to initialize the storage node:

```
uvicorn Server:app --host 0.0.0.0 --port 8000
```
- Overview

This utility repurposes legacy hardware into a private cloud storage node. It provides three primary endpoints to upload, download, and list files directly on the local file system.