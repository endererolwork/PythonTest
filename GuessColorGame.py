import random
import tkinter as tk
from tkinter import ttk

colors = ['kırmızı', 'mavi', 'yeşil', 'sarı', 'turkuaz', 'kırmızımor']
rgb_values = {
    'kırmızı': '#FF0000',
    'mavi': '#0000FF',
    'yeşil': '#00FF00',
    'sarı': '#FFFF00',
    'turkuaz': '#00FFFF',
    'kırmızımor': '#FF00FF'
}

secret_code = random.sample(colors, 4)
guesses = []

def check_guess():
    guess = [color.lower() for color in entry.get().split()]
    if guess == secret_code:
        result_label.config(text='Tebrikler, doğru cevap!', fg='green')
        submit_button.config(state='disabled')
    else:
        black, white = 0, 0
        for i in range(4):
            if guess[i] == secret_code[i]:
                black += 1
            elif guess[i] in secret_code:
                white += 1
        result_label.config(text=f'{black} siyah, {white} beyaz')
        guesses.append((guess, black, white))
        update_table()
        if len(guesses) == 13:
            submit_button.config(state='disabled')

def update_table():
    for i, (guess, black, white) in enumerate(guesses):
        row_values = []
        for j in range(4):
            color_cell = tk.Label(table, bg=rgb_values[guess[j]], width=10, height=2, borderwidth=1, relief="solid")
            color_cell.grid(row=i+1, column=j+1)
            row_values.append(rgb_values[guess[j]])
        
        # Boş kutucuklar ekleniyor
        for _ in range(4):
            empty_cell = tk.Label(table, bg='white', width=8, height=2, borderwidth=1, relief="solid")
            empty_cell.grid(row=i+1, column=len(row_values)+1, padx=5)
            row_values.append('')
        
        # Siyah ve beyaz kutular ekleniyor
        for _ in range(black):
            black_cell = tk.Label(table, bg='black', width=3, height=1, borderwidth=1, relief="solid")
            black_cell.grid(row=i+1, column=len(row_values)+1, padx=2)
            row_values.append('')
        for _ in range(white):
            white_cell = tk.Label(table, bg='white', width=3, height=1, borderwidth=1, relief="solid")
            white_cell.grid(row=i+1, column=len(row_values)+1, padx=2)
            row_values.append('')
        
        table.insert("", "end", text=f"Tahmin {i+1}", values=row_values)

window = tk.Tk()
window.title("Renk Tahmin Oyunu")

instruction_label = tk.Label(window, text="Renkleri girin (kırmızı, mavi, yeşil, sarı, turkuaz, kırmızımor):")
instruction_label.pack()

entry = tk.Entry(window)
entry.pack()

submit_button = tk.Button(window, text="Tahmin Et", command=check_guess)
submit_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

table_frame = tk.Frame(window)
table_frame.pack()

table = ttk.Treeview(table_frame, columns=('Renk 1', 'Renk 2', 'Renk 3', 'Renk 4', '', '', '', 'Siyah', 'Beyaz'))
table.heading('#0', text='Tahmin')
table.heading('Renk 1', text='Renk 1 (RGB)')
table.heading('Renk 2', text='Renk 2 (RGB)')
table.heading('Renk 3', text='Renk 3 (RGB)')
table.heading('Renk 4', text='Renk 4 (RGB)')
table.heading('', text='')
table.heading('', text='')
table.heading('', text='')
table.heading('Siyah', text='Siyah')
table.heading('Beyaz', text='Beyaz')
table.pack()

header_values = ["Renk 1", "Renk 2", "Renk 3", "Renk 4", '', '', '', "Siyah", "Beyaz"]
for i in range(9):
    table.column(i, width=100, anchor="center")
    table.insert("", "end", text="Tahmin", values=header_values)

window.mainloop()
