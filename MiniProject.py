import random
import string
import time
import csv

# Parameters
n_trials = 20
seq_length = 6
presentation_time = 1  # seconds
letters = list(string.ascii_uppercase)

results = []

for trial in range(1, n_trials + 1):
    # Generate random sequence
    sequence = random.sample(letters, seq_length)

    # Present letters in terminal
    print(f"\nTrial {trial}: Memorize the sequence")
    for letter in sequence:
        print(letter, flush=True)
        time.sleep(presentation_time)
    print("\n" * 20)  # clear screen by scrolling

    # Get response
    response = input("Type the sequence: ").upper()

    # Calculate accuracy
    correct = [int(r == s) if i < len(response) else 0 for i, (r, s) in enumerate(zip(response, sequence))]
    accuracy = sum(correct) / seq_length

    # Save trial data
    results.append({
        "trial": trial,
        "sequence": "".join(sequence),
        "response": response,
        "accuracy": accuracy,
        "positional_accuracy": correct
    })

# Save results to CSV
with open("serial_recall_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["trial", "sequence", "response", "accuracy", "positional_accuracy"])
    writer.writeheader()
    writer.writerows(results)

print("\nExperiment finished. Results saved to serial_recall_results.csv")