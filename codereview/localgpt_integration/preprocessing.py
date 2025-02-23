# Save Uploaded File
import os
import tempfile
from rest_framework.exceptions import ValidationError
from localGPT.query import query_documents
from django.conf import settings
from localGPT.ingest import ingest_documents
from transformers import AutoModelForCausalLM, AutoTokenizer

# Choose a local model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
# model_name = "mistralai/Mistral-7B-Instruct-v0.1"  # Or another model
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# def generate_description(query):
#     inputs = tokenizer(query, return_tensors="pt")
#     output = model.generate(**inputs, max_length=200)
#     return tokenizer.decode(output[0], skip_special_tokens=True)

ALLOWED_EXTENSIONS = {'.txt', '.csv', '.json', '.xml', '.html', '.css', '.js', 
    '.py', '.java', '.cpp', '.c', '.php', '.md', '.log'}
def handle_uploaded_file(content,name):
    """'
    Process the file content directly without saving it to disk.
    """
    
    file_extension = os.path.splitext(name)[1]
    # if file_extension not in ALLOWED_EXTENSIONS:
    #     raise ValidationError("Unsupported file type.")
    
    # Pass the file content to localGPT for indexing
    index_uploaded_file(content, name)
    
    
    from localGPT.ingest import ingest_documents

def index_uploaded_file(file_content, file_name):
    """
    Index the file content using localGPT.
    """
    # Save the file content to a temporary file (if required by localGPT)
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    # Index the temporary file
    ingest_documents(temp_file_path)

    # Clean up the temporary file
    os.remove(temp_file_path)
def generate_description(query):
    """
    Generate a response to the given query using a pre-trained language model.
    
    Args:
        query (str): The input query or prompt.
    
    Returns:
        str: The generated response.
    """
    # Tokenize the input query
    inputs = tokenizer(query, return_tensors="pt")
    
    # Generate the response
    output = model.generate(
        **inputs,
        max_length=500,  # Maximum length of the generated response
        num_return_sequences=1,  # Number of responses to generate
        no_repeat_ngram_size=2,  # Prevent repetition of n-grams
        top_k=50,  # Top-k sampling
        top_p=0.95,  # Nucleus sampling
        temperature=0.7,  # Controls randomness (lower = more deterministic)
    )
    
    # Decode the generated output
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response