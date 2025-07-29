# #!/bin/bash

# # Run FastAPI
# uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# sleep 2

# # Run Streamlit
# streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0

#!/bin/bash

# Log FastAPI output
echo "Starting FastAPI..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

sleep 3

# Run Streamlit normally
echo "Starting Streamlit..."
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0