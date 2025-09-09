import tkinter as tk
import random
import string
import time
import csv

class SerialRecall:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Serial Recall")
        self.root.geometry("400x300")
        
        self.trial = 0
        self.sequence = []
        self.results = []
        
        # UI elements
        self.trial_label = tk.Label(self.root, text="Trial 0/20", font=('Arial', 16))
        self.trial_label.pack(pady=10)
        
        self.letter_label = tk.Label(self.root, text="", font=('Arial', 48), height=2)
        self.letter_label.pack(pady=20)
        
        self.entry = tk.Entry(self.root, font=('Arial', 16), width=10)
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.submit)
        
        self.start_btn = tk.Button(self.root, text="Start", command=self.start_trial)
        self.start_btn.pack(pady=10)
        
    def start_trial(self):
        self.trial += 1
        if self.trial > 3:
            self.save_results()
            return
            
        self.trial_label.config(text=f"Trial {self.trial}/3")
        self.sequence = random.sample(string.ascii_uppercase, 6)
        self.entry.delete(0, tk.END)
        self.start_btn.config(state='disabled')
        
        # Show sequence
        for letter in self.sequence:
            self.letter_label.config(text=letter)
            self.root.update()
            time.sleep(1)
        
        self.letter_label.config(text="?")
        self.entry.focus()
    
    def submit(self, event=None):
        response = self.entry.get().upper()
        
        # Calculate accuracy
        correct = [1 if i < len(response) and response[i] == self.sequence[i] else 0 
                  for i in range(6)]
        accuracy = sum(correct) / 6
        
        self.results.append({
            "trial": self.trial,
            "sequence": "".join(self.sequence),
            "response": response,
            "accuracy": accuracy,
            "positional_accuracy": correct
        })
        
        # Clear text box and show confirmation with smaller font
        self.entry.delete(0, tk.END)
        self.letter_label.config(text="Answer registered", font=('Arial', 20))
        self.start_btn.config(state='normal')
    
    def save_results(self):
        with open("02464_mini_project1/results.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["trial", "sequence", "response", "accuracy", "positional_accuracy"])
            writer.writeheader()
            writer.writerows(self.results)
        
        self.letter_label.config(text="Done!")
        print("Results saved to results.csv")

if __name__ == "__main__":
    app = SerialRecall()
    app.root.mainloop()