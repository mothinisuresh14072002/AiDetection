# Demo

Run:

```bash
uvicorn api.main:app --reload
```

Open the API docs at `/docs`. The static UI in `web/index.html` can be served by any static web server and configured to point to the API.

The baseline intentionally returns UNCERTAIN until validated model weights are installed.
