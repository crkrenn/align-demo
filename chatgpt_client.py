#!/usr/bin/env python3
"""
Simple ChatGPT client that processes a list of prompts with deterministic responses.
"""

import os
import time
import yaml
from typing import List, Dict, Any, Tuple
from openai import OpenAI


class ChatGPTClient:
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the ChatGPT client.

        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def send_prompt(self, prompt: str, system_message: str = None) -> Dict[str, Any]:
        """
        Send a single prompt to ChatGPT and return the response.

        Args:
            prompt: The user prompt to send
            system_message: Optional system message to set context

        Returns:
            Dictionary containing the response and metadata
        """
        messages = []

        if system_message:
            messages.append({"role": "system", "content": system_message})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,  # Set to 0 for deterministic responses
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                seed=42  # Fixed seed for maximum determinism
            )

            return {
                "prompt": prompt,
                "response": response.choices[0].message.content,
                "model": self.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "success": True,
                "error": None
            }

        except Exception as e:
            return {
                "prompt": prompt,
                "response": None,
                "model": self.model,
                "usage": None,
                "success": False,
                "error": str(e)
            }

    def process_prompts_as_conversation(self, prompts: List[str], system_message: str = None) -> Dict[str, Any]:
        """
        Process all prompts as a single conversation thread.

        Args:
            prompts: List of prompts to send as conversation
            system_message: Optional system message to set context

        Returns:
            Dictionary containing the full conversation and metadata
        """
        messages = []

        if system_message:
            messages.append({"role": "system", "content": system_message})

        # Add all prompts as separate user messages
        for prompt in prompts:
            messages.append({"role": "user", "content": prompt})

        try:
            print(f"Sending {len(prompts)} prompts as single conversation...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,  # Set to 0 for deterministic responses
                max_tokens=2000,  # Increased for multiple responses
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                seed=42  # Fixed seed for maximum determinism
            )

            return {
                "prompts": prompts,
                "response": response.choices[0].message.content,
                "model": self.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "success": True,
                "error": None
            }

        except Exception as e:
            return {
                "prompts": prompts,
                "response": None,
                "model": self.model,
                "usage": None,
                "success": False,
                "error": str(e)
            }

    def print_results(self, results: List[Dict[str, Any]]):
        """Print formatted results from processed prompts."""
        print("\n" + "="*80)
        print("CHATGPT INTERACTION RESULTS")
        print("="*80)

        total_tokens = 0
        successful_requests = 0

        for i, result in enumerate(results, 1):
            print(f"\nPROMPT {i}:")
            print(f"Q: {result['prompt']}")
            print("-" * 40)

            if result["success"]:
                print(f"A: {result['response']}")
                print(f"Tokens used: {result['usage']['total_tokens']}")
                total_tokens += result['usage']['total_tokens']
                successful_requests += 1
            else:
                print(f"ERROR: {result['error']}")

        print("\n" + "="*80)
        print(f"SUMMARY:")
        print(f"Successful requests: {successful_requests}/{len(results)}")
        print(f"Total tokens used: {total_tokens}")
        print("="*80)


def load_prompts_from_yaml(file_path: str = "prompts.yaml") -> Tuple[List[str], str]:
    """Load prompts and context from a YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            prompts = data.get('prompts', [])
            context = data.get('context', '')
            return prompts, context
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Using default prompts.")
        return [
            "What is the capital of France?",
            "Explain the concept of machine learning in simple terms.",
            "Write a Python function to calculate the factorial of a number."
        ], "You are a helpful assistant."
    except Exception as e:
        print(f"Error loading prompts from {file_path}: {e}")
        return [], ""


def process_prompt_lines(prompts: List[str]) -> List[str]:
    """Process prompt lines - print Q/A lines, return only P: lines for LLM processing."""
    llm_prompts = []

    for prompt in prompts:
        prompt = prompt.strip()
        if prompt.startswith('Q:') or prompt.startswith('A:'):
            print(f"[Display] {prompt}")
        elif prompt.startswith('P:'):
            # Remove the "P:" prefix for LLM processing
            clean_prompt = prompt[2:].strip()
            llm_prompts.append(clean_prompt)
        # Ignore other lines (comments, etc.)

    return llm_prompts


def main():
    """Example usage of the ChatGPT client."""

    # Load prompts and context from YAML file
    all_prompts, context = load_prompts_from_yaml("prompts.yaml")

    # Process prompts - display Q/A, extract P: for LLM
    print("Processing prompt lines:")
    print("-" * 40)
    llm_prompts = process_prompt_lines(all_prompts)

    if not llm_prompts:
        print("No prompts starting with 'P:' found for LLM processing.")
        return

    print(f"\nFound {len(llm_prompts)} prompts for LLM processing.\n")

    # Use context from YAML as system message
    system_message = context if context else "You are a helpful assistant that provides clear, concise answers."

    try:
        # Initialize the client
        client = ChatGPTClient()

        print("Starting ChatGPT interaction...")
        print(f"Model: {client.model}")
        print(f"Number of prompts for LLM: {len(llm_prompts)}")
        print(f"Context: {system_message[:100]}...")

        # Process all LLM prompts as single conversation
        result = client.process_prompts_as_conversation(llm_prompts, system_message)

        # Print formatted result
        if result["success"]:
            print(f"\n✓ Single conversation completed ({result['usage']['total_tokens']} tokens)")
            print(f"\nLLM Response:")
            print("="*60)
            print(result['response'])
            print("="*60)
            print(f"\nTokens used: {result['usage']['total_tokens']}")
        else:
            print(f"✗ Error: {result['error']}")

    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set your OPENAI_API_KEY environment variable.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()