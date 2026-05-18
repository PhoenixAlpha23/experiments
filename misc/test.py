import sys
# print("Current Python version:")
# print(sys.version)

import onnxruntime as ort
import chromadb

print("ONNX Runtime version:", ort.__version__)
client = chromadb.Client()
print("Chromadb client created successfully")