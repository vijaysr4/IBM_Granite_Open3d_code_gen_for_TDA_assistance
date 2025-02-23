import os
import json
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)

# Disable parallelism warnings for tokenizers
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Disable wandb if not using it
os.environ["WANDB_MODE"] = "disabled"


def load_training_data(json_file):
    """
    Load your JSON training data file.
    Expected format is a list of examples, each with 'prompt' and 'code' keys.
    """
    with open(json_file, "r") as f:
        data = json.load(f)
    return data


def preprocess_example(example, tokenizer, max_length=1024):
    """
    Combine the prompt and code into a single string, then tokenize it.
    This is common for causal LM fine-tuning.
    """
    text = f"Prompt: {example['prompt']}\nCode:\n{example['code']}"
    tokenized = tokenizer(text, truncation=True, max_length=max_length)
    return tokenized


def main():
    # Set the cache directory for all downloads and model files
    cache_dir = "/Data/my_project_env2/huggingface_cache"
    os.environ["TRANSFORMERS_CACHE"] = cache_dir
    os.environ["HF_HOME"] = cache_dir
    os.environ["TORCH_HOME"] = cache_dir

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_path = "ibm-granite/granite-3b-code-instruct-2k"

    # Load the tokenizer and model from the custom cache directory
    tokenizer = AutoTokenizer.from_pretrained(model_path, cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(model_path, cache_dir=cache_dir)

    # Load and prepare the training data
    train_examples = load_training_data("train_data.json")  # JSON file with training data
    # Convert the list of examples into a Hugging Face Dataset
    dataset = Dataset.from_list(train_examples)

    # Tokenize the dataset by applying our preprocess function
    def tokenize_function(example):
        return preprocess_example(example, tokenizer)

    tokenized_dataset = dataset.map(tokenize_function, batched=False)

    # Create a data collator that dynamically pads the inputs
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    # Define training arguments; adjust hyperparameters as needed.
    training_args = TrainingArguments(
        output_dir="./fine_tuned_model",
        overwrite_output_dir=True,
        per_device_train_batch_size=1,
        num_train_epochs=3,
        logging_steps=10,
        save_steps=50,
        fp16=torch.cuda.is_available(),
    )

    # Initialize the Trainer with the model, training arguments, dataset, and data collator.
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    # Start the training process
    trainer.train()

    # Save the final model and tokenizer for later use
    model.save_pretrained("./fine_tuned_code_model")
    tokenizer.save_pretrained("./fine_tuned_code_model")


if __name__ == "__main__":
    main()
