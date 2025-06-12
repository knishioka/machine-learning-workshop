#!/usr/bin/env python3
"""
Verify TinyLlama Fine-tuning Effect
Fine-tuningの効果を検証するスクリプト
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
import torch
import os

def test_base_model():
    """Test base TinyLlama model without fine-tuning"""
    print("=" * 60)
    print("1. BASE MODEL TEST (No Fine-tuning)")
    print("=" * 60)
    
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="auto" if device.type != "mps" else None
    )
    
    if device.type == "mps":
        model = model.to(device)
    
    # Test queries
    queries = [
        "What are the shipping costs?",
        "How do I return a product?",
        "What payment methods do you accept?"
    ]
    
    for query in queries:
        prompt = f"<|system|>\nYou are a helpful customer support assistant.</s>\n<|user|>\n{query}</s>\n<|assistant|>\n"
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=False)
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[1].strip()
            if "</s>" in response:
                response = response.split("</s>")[0].strip()
        
        print(f"\nQuery: {query}")
        print(f"Response: {response[:200]}...")
        print("-" * 40)

def test_finetuned_model():
    """Test fine-tuned TinyLlama model"""
    print("\n" + "=" * 60)
    print("2. FINE-TUNED MODEL TEST")
    print("=" * 60)
    
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    # Check which fine-tuned model exists
    model_paths = [
        "./finetuned_tinyllama_model",
        "./scripts/finetuned_tinyllama_model",
        "./finetuned_tinyllama_balanced_model",
        "./scripts/finetuned_tinyllama_balanced_model",
        "./finetuned_tinyllama_enhanced_model",
        "./scripts/finetuned_tinyllama_enhanced_model"
    ]
    
    adapter_path = None
    for path in model_paths:
        if os.path.exists(path) and os.path.exists(os.path.join(path, "adapter_config.json")):
            adapter_path = path
            print(f"Found fine-tuned model at: {adapter_path}")
            break
    
    if not adapter_path:
        print("No fine-tuned model found!")
        return
    
    # Load base model
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float32,
        device_map="auto" if device.type != "mps" else None
    )
    
    if device.type == "mps":
        base_model = base_model.to(device)
    
    # Load LoRA adapter
    print("Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, adapter_path)
    model.eval()
    
    # Test same queries
    queries = [
        "What are the shipping costs?",
        "How do I return a product?",
        "What payment methods do you accept?"
    ]
    
    for query in queries:
        prompt = f"<|system|>\nYou are a helpful customer support assistant.</s>\n<|user|>\n{query}</s>\n<|assistant|>\n"
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=False)
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[1].strip()
            if "</s>" in response:
                response = response.split("</s>")[0].strip()
        
        print(f"\nQuery: {query}")
        print(f"Response: {response[:200]}...")
        print("-" * 40)

def show_expected_responses():
    """Show what we expect from fine-tuning"""
    print("\n" + "=" * 60)
    print("3. EXPECTED RESPONSES (From Training Data)")
    print("=" * 60)
    
    expected = {
        "What are the shipping costs?": "Here are our shipping options and costs:\n\n**Standard Shipping:**\n- $6.99 flat rate\n- FREE on orders over $50\n- 3-5 business days\n\n**Express Shipping:**\n- $14.99 flat rate\n- 1-2 business days",
        "How do I return a product?": "I'll be happy to help you with your return.\n\nHere's our return process:\n\n**Return Policy:**\n- Returns accepted within 14 days of delivery\n- Items must be unused and in original packaging",
        "What payment methods do you accept?": "We accept:\n- Credit/Debit Cards (Visa/Mastercard/AMEX)\n- PayPal\n- Apple Pay\n- Google Pay\n- Bank Transfer\n- Buy Now, Pay Later options"
    }
    
    for query, response in expected.items():
        print(f"\nQuery: {query}")
        print(f"Expected: {response[:200]}...")
        print("-" * 40)

def main():
    print("TinyLlama Fine-tuning Verification")
    print("This will compare base model vs fine-tuned model responses\n")
    
    # Test base model
    test_base_model()
    
    # Test fine-tuned model
    test_finetuned_model()
    
    # Show expected responses
    show_expected_responses()
    
    print("\n" + "=" * 60)
    print("ANALYSIS")
    print("=" * 60)
    print("Compare the responses above to see if fine-tuning had any effect.")
    print("Look for:")
    print("- Specific price mentions ($6.99, $14.99, etc.)")
    print("- Structured responses with bullet points")
    print("- Domain-specific knowledge (14-day return policy, etc.)")

if __name__ == "__main__":
    main()