from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = Flask(__name__)

# Load an alternative model and tokenizer
model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Load the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the vector database
dimension = 384  # Dimension of the embeddings from 'all-MiniLM-L6-v2'
index = faiss.IndexFlatL2(dimension)

# Sample YAML data
sample_yamls = [
    """
    apiVersion: v2
    name: application
    description: Helm chart for a generic application
    type: application
    version: 1.0.0
    appVersion: "1.0.0"
    """,
    """
  replicaCount: 1
  image:
    repository: registry.example.com/application
    pullPolicy: Always
    tag: "latest"
  service:
    type: ClusterIP
    port: 8080
    """,
    """
  apiVersion: v1
  kind: Service
  metadata:
    name: application-service
  spec:
    type: ClusterIP
    ports:
      - port: 80
        targetPort: 8080
    selector:
      app: application
    """,
    """
  apiVersion: apps/v1
kind: Deployment
metadata:
  name: application-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: application
  template:
    metadata:
      labels:
        app: application
    spec:
      containers:
      - name: application
        image: registry.example.com/application:latest
        ports:
        - containerPort: 8080
    """
]

# Generate embeddings for the sample YAML data
def load_sample_yamls():
    for yaml_content in sample_yamls:
        embedding = embedding_model.encode(yaml_content, convert_to_tensor=True).cpu().numpy()
        index.add(np.array([embedding]))

# Load the sample YAMLs into the vector database
load_sample_yamls()

# Function to find the most similar YAML sample
def find_similar_yaml(query):
    query_embedding = embedding_model.encode(query, convert_to_tensor=True).cpu().numpy()
    D, I = index.search(np.array([query_embedding]), k=1)
    return sample_yamls[I[0][0]]

def generate_helm_chart_with_llm(name, repository, port):
    # Define the prompt
    prompt = (
        f"Generate a complete Helm chart for a Kubernetes application named '{name}'. "
        f"The Docker image should be pulled from '{repository}' and it should expose port '{port}'. "
        "The output should include:\n"
        "- A Chart.yaml file\n"
        "- A values.yaml file\n"
        "- A templates/deployment.yaml file\n"
        "- A templates/service.yaml file\n"
        "Ensure that the chart is well-structured and includes all necessary configurations."
    )

    # Find the most similar YAML sample
    similar_yaml = find_similar_yaml(prompt)

    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors='pt')

    # Generate the response
    outputs = model.generate(**inputs, max_length=800, num_return_sequences=1, do_sample=True, temperature=0.7)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return f"{similar_yaml}\n\n{generated_text}"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    port = data.get("port")
    name = data.get("name")
    repository = data.get("repository")

    if not all([port, name, repository]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Generate Helm chart using LLM
    helm_chart_yaml = generate_helm_chart_with_llm(name, repository, port)
    
    return jsonify({"helm_chart": helm_chart_yaml})

if __name__ == "__main__":
    app.run(debug=True)
