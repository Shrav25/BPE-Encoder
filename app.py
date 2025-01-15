import gradio as gr
from Assign_11 import bpe_tokenizer

def tokenize_text(file_bytes):
    # Decode the bytes to a string
    text = file_bytes.decode("utf-8")
    tokens, vocab, compression_ratio = bpe_tokenizer(text)
    
    # Get a sample of the vocabulary
    vocab_sample = list(vocab.keys())[:10]  # Adjust the number to show more or fewer samples
    
    output = {
        "Tokens": tokens,
        "Vocabulary Size": len(vocab),
        "Vocabulary Sample": vocab_sample,
        "Compression Ratio": compression_ratio
    }
    return output

# Create a Gradio interface
iface = gr.Interface(
    fn=tokenize_text,
    inputs=gr.File(type="binary"),  # Use 'binary' to read file content
    outputs="json",  # Use JSON to return structured data
    title="BPE Tokenizer",
    description="Upload a text file to tokenize using BPE. The output includes tokens, vocabulary size, a sample of the vocabulary, and compression ratio."
)

# Launch the app
iface.launch() 