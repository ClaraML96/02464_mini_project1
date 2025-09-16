#with the pause
import tkinter as tk
import random
import string
import csv

N_TRIALS = 10
SEQ_LEN = 10
STIM_MS = 1000       # per-letter display
ISI_MS = 0          # gap between letters
POST_DELAY_MS = 0  # pause after last letter

class SerialRecall:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Serial Recall")
        self.root.geometry("420x320")

        self.trial = 0
        self.sequence = []
        self.results = []

        self.trial_label = tk.Label(self.root, text=f"Trial 0/{N_TRIALS}", font=('Arial', 16))
        self.trial_label.pack(pady=12)

        self.letter_label = tk.Label(self.root, text="", font=('Arial', 48), height=2)
        self.letter_label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=('Arial', 16), width=14, state='disabled')
        self.entry.pack(pady=8)
        self.entry.bind('<Return>', self.submit)

        self.start_btn = tk.Button(self.root, text="Start", command=self.start_trial)
        self.start_btn.pack(pady=10)

    def start_trial(self):
        if self.trial >= N_TRIALS:
            self.save_results()
            return

        self.trial += 1
        self.trial_label.config(text=f"Trial {self.trial}/{N_TRIALS}")
        self.sequence = random.sample(string.ascii_uppercase, SEQ_LEN)
        self.entry.delete(0, tk.END)
        self.start_btn.config(state='disabled')
        self.entry.config(state='disabled')

        self.show_index = 0
        self.play_next()

    def play_next(self):
        if self.show_index < SEQ_LEN:
            self.letter_label.config(text=self.sequence[self.show_index], font=('Arial', 48))
            self.show_index += 1
            self.root.after(STIM_MS, self.clear_then_next)
        else:
            # finished showing sequence: show prompt, then wait 5 s before enabling input
            self.letter_label.config(text="?")
            self.entry.config(state='disabled')
            self.root.after(POST_DELAY_MS, self.enable_response)

    def enable_response(self):
        self.entry.config(state='normal')
        self.entry.focus_set()
        self.start_btn.config(state='disabled')

    def clear_then_next(self):
        self.letter_label.config(text="")
        self.root.after(ISI_MS, self.play_next)

    def submit(self, event=None):
        if self.entry['state'] == 'disabled':
            return

        response = self.entry.get().upper()
        correct = [1 if i < len(response) and response[i] == self.sequence[i] else 0
                   for i in range(SEQ_LEN)]
        accuracy = sum(correct) / SEQ_LEN

        self.results.append({
            "trial": self.trial,
            "sequence": "".join(self.sequence),
            "response": response,
            "accuracy": accuracy,
            "positional_accuracy": correct
        })

        self.entry.delete(0, tk.END)
        self.letter_label.config(text="Answer registered", font=('Arial', 20))
        self.start_btn.config(state='normal')

        if self.trial >= N_TRIALS:
            self.start_btn.config(text="Save & Quit")

    def save_results(self):
        with open("results_joao_15.csv", "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["trial", "sequence", "response", "accuracy", "positional_accuracy"]
            )
            writer.writeheader()
            writer.writerows(self.results)
        self.letter_label.config(text="Done!")
        self.start_btn.config(state='disabled')
        self.entry.config(state='disabled')

if __name__ == "__main__":
    app = SerialRecall()
    app.root.mainloop()