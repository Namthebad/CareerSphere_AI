# CareerSphere AI - Final Readable UI

This version fixes the visibility problem in the previous version. Profile labels are explicitly dark and readable, while the input text remains dark on white fields.

## Run

```bat
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

For AI features:

```bat
ollama pull llama3.2
ollama serve
```

If another Streamlit app is running, stop it with Ctrl+C before starting this version.
