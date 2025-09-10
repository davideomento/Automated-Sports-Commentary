import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

# === FUNZIONE PER TAGLIARE IL TESTO ALL'ULTIMA FRASE COMPLETA ===
def trim_to_last_complete_sentence(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return " ".join(sentences[:-1]) if len(sentences) > 1 else text


# === PERCORSO AL MODELLO SU GOOGLE DRIVE ===
drive_model_path = "/content/drive/MyDrive/mistral_model"  # <--- cambia se hai un'altra cartella

# === CARICAMENTO MODELLO DA DRIVE ===
tokenizer = AutoTokenizer.from_pretrained(drive_model_path)
model = AutoModelForCausalLM.from_pretrained(
    drive_model_path,
    device_map="auto",        # Usa la GPU se disponibile
    torch_dtype=torch.float16 # Precisione 16-bit per risparmiare memoria
)

model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"✅ Modello caricato su: {device}")


# === FUNZIONE PER GENERARE TESTO ===
def generate_with_mistral(prompt, max_new_tokens=300, temperature=0.7, top_p=0.9):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    clean_text = trim_to_last_complete_sentence(generated_text)
    return clean_text


# === ESECUZIONE: PROMPT INSERITO DALL'UTENTE ===
if __name__ == "__main__":
    prompt = input("\n✍️ Inserisci il prompt: ")
    print("\n=== PROMPT ===")
    print(prompt)

    output = generate_with_mistral(prompt)
    print("\n=== OUTPUT GENERATO ===")
    print(output)
