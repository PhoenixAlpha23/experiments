# experiment01

A small, personal project to turn my old laptop into a **local file storage node**.

Nothing fancy (yet). Just a simple way to move files from my phone → laptop without relying on external cloud services.

---

## What it does

- 📤 Upload files over HTTP  
- 📥 Download files anytime  
- 📄 List stored files  

That’s it—for now.

---

## Why I built this

- Reuse old hardware instead of letting it sit idle  
- Avoid uploading personal files to third-party cloud services  
- Have a controlled environment to **learn FastAPI + backend design**  
- Build a foundation for more advanced ideas (ML, search, etc.)

---

## Running the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
