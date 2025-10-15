import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import re

# =========================
# Load model & tokenizer
# =========================
@st.cache_resource(show_spinner=True)
def load_model():
    model = GPT2LMHeadModel.from_pretrained("gpt2_finetuned")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2_finetuned")
    tokenizer.pad_token = tokenizer.eos_token
    model.eval()
    return model, tokenizer

model, tokenizer = load_model()

# =========================
# Text generation function
# =========================
def generate_text(seed_text, max_length=150, temperature=0.8, top_k=50, top_p=0.95, repetition_penalty=1.2, num_return_sequences=1):
    inputs = tokenizer.encode(seed_text, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_length=max_length,
        do_sample=True,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        num_return_sequences=num_return_sequences,
        pad_token_id=tokenizer.eos_token_id
    )

    generated_texts = []
    for i in range(num_return_sequences):
        text = tokenizer.decode(outputs[i], skip_special_tokens=True)
        clean_text = re.sub(r"[^A-Za-z0-9 ,.!?'\n]", '', text)  # remove weird symbols
        generated_texts.append(clean_text)
    return generated_texts

# =========================
# Streamlit UI
# =========================
st.title("GPT-2 Fine-Tuned Text Generator")
st.write("Enter a seed text and generate continuations using your fine-tuned GPT-2 model.")

# Seed text input
seed_text = st.text_area("Seed Text", "To be or not to be, I am a man")

# Sliders for generation parameters
max_length = st.slider("Max Length", min_value=50, max_value=500, value=150)
temperature = st.slider("Temperature", min_value=0.1, max_value=1.5, value=0.8)
top_k = st.slider("Top-k Sampling", min_value=10, max_value=100, value=50)
top_p = st.slider("Top-p Sampling", min_value=0.1, max_value=1.0, value=0.95)
repetition_penalty = st.slider("Repetition Penalty", min_value=1.0, max_value=2.0, value=1.2)
num_return_sequences = st.slider("Number of Outputs", min_value=1, max_value=5, value=1)

# Generate button
if st.button("Generate Text"):
    with st.spinner("Generating..."):
        outputs = generate_text(seed_text, max_length, temperature, top_k, top_p, repetition_penalty, num_return_sequences)
    st.subheader("Generated Text:")
    for i, text in enumerate(outputs, 1):
        st.markdown(f"**Output {i}:**")
        st.write(text)
        st.write("---")
