import random
import time
import sys

level = [[]] # 2 boyutlu harita yapısı
size_of_map = 10
number_of_guess = 1
number_of_ships = 5
position_of_ships = [[]] # Gemilerin konumlarını tutan 2 boyutlu yapı
ship_dict = {1: 'MayınGemisi', 2: 'Denizaltı', 3: 'Fırkateyn', 4: 'Muhrip', 5: 'Amiral'}
end_of_game = False
debug_mode = False


def create_map():
    """Oyun haritasını oluşturur ve gemileri rastgele yerleştirir"""
    global position_of_ships

    random.seed(time.time())

    rows, columns = (size_of_map, size_of_map)
    
    for r in range(rows):
        row = []
        for c in range(columns):
            row.append("O")
        level.append(row)

    position_of_ships = []
    ship_size = 5 # Başlangıçta 5 ve her gemi yerleştirildikçe azalır

    while ship_size > 0:
        random_row = random.randint(1, rows - 1)
        random_col = random.randint(1, columns - 1)
        direction = random.choice(["up", "down", "left", "right"])
        if place_ship(random_row, random_col, direction, ship_size):
            ship_size -= 1
    
def print_map():
    """Haritayı konsola yazdırır"""
    
    for row in range(len(level)):
        if(row == 0):
            print("  ", end="")
            for i in range(size_of_map):
                print(" "+chr(65+i), end=(""))
        elif(row == 10):
            print(row, end=" ")  
        else:
            print(row, end="  ")
        for col in range(len(level[row])):
            if not debug_mode:
                if(level[row][col] == "+"):
                    print("O", end=" ")
                else:
                    print(level[row][col], end=" ")
            else:
                print(level[row][col], end=" ")
        print("")
        
    
def place_ship(row, col, direction, length):
    # Gemilerin haritaya yerleştirilip yerleştirilemeyeceğini belirlemek için bölge oluşturulur
    #=====================================================================================  
    start_row, end_row = row, row + 1 # Döngüde kullanabilmek için +1 eklenir
    start_col, end_col = col, col + 1 # Döngüde kullanabilmek için +1 eklenir

    if direction == "up":
        if row - length < 0 :
            return False
        start_row = row - length + 1
        
    elif direction == "down":
        if row + length >= size_of_map :
            return False
        end_row = row + length
        
    elif direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1
        
    elif direction == "right":
        if col + length >= size_of_map:
           return False
        end_col = col + length
    #===================================================================================== 
    
    # Gemilerin birbirleriyle kesişip kesişmediğini belirlemek için bölge oluşturulur
    #=====================================================================================  
    is_placeable = True
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            if level[row][col] != "O":
                is_placeable = False
                break
    
    if is_placeable:
        position_of_ships.append([start_row, end_row, start_col, end_col]) # Kontrol etmek için gemiyi listeye ekle
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                level[row][col] = "+"
        
    return is_placeable
    
    
    
def get_user_input():
    
    global number_of_guess
    
    is_input_correct = False
    
    while is_input_correct is False:
        print(number_of_guess, ". tahmininizi giriniz ?" , end=" ")
        user_guess = input()
        user_guess = user_guess.upper()
        
        if (user_guess[0] == "Q"):
            print("------------Exit------------")
            sys.exit()
            
        if (user_guess[0] == "R"):
            print_report()
            return False, False, False

        if not (1 < len(user_guess) < 4):
            print("Hata: Çok fazla ya da çok az argüman girdiniz. Tekrar giriş yapınız.")
            continue
        
        if(len(user_guess) == 2):
            row = int(user_guess[0])
            col = ord(user_guess[1]) - 65
        elif(len(user_guess) == 3):
            row = int("".join(user_guess[0:2]))
            col = ord(user_guess[2]) - 65
            
        if debug_mode: print("Row value:", row, "Col value:", col) # Hata ayıklama
        
        if not (0 < row <= size_of_map):
            print("Hata: Sayılar 1 ile 10 arasında olmalıdır. Tekrar giriş yapınız.")
            continue
        
        if not (0 <= col < size_of_map):
            print("Hata: Harfler A ile J arasında olmalıdır. Tekrar giriş yapınız.")
            continue
        
        if level[row][col] == "X" or level[row][col] == "*":
            print("Bu koordinata daha önce atış yapıldı. Tekrar atış yapınız.")
            continue
        
        if level[row][col] == "O" or level[row][col] == "+":
            is_input_correct = True
            return row, col, user_guess
        
        
        
def shoot():
    
    global number_of_guess
    
    row, col, user_guess = get_user_input()
    
    if row == False:
        return
    else:
        number_of_guess += 1
    
        if level[row][col] == "O":
            print("[", user_guess, "] İska!")
            level[row][col] = "X"
        elif level[row][col] == "+":
            print("[", user_guess, "]", end=" ")
            print(ship_dict[find_the_ship(row, col)], end=" ")
            level[row][col] = "*"
            if check_ship_destruct(row, col):
                print("battı!")
            else:
                print("yara aldı!")
        
        
        
def find_the_ship(row, col):
    
    global position_of_ships
    
    for ship_position in position_of_ships:
        start_row = ship_position[0]
        end_row = ship_position[1]
        start_col = ship_position[2]
        end_col = ship_position[3]
        
        if (start_row <= row < end_row) and (start_col <= col < end_col):
            return position_of_ships.index(ship_position) + 1
    
    return -1
        

def check_ship_destruct(row, col):
    
    global position_of_ships
    
    ship_number = find_the_ship(row, col)
    ship_position = position_of_ships[ship_number - 1]
    
    start_row = ship_position[0]
    end_row = ship_position[1]
    start_col = ship_position[2]
    end_col = ship_position[3]
    
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            if level[row][col] == "+":
                return False
    
    return True
        
        
        
def check_end_of_game():
    
    global end_of_game
    global number_of_ships
    
    if number_of_ships == 0:
        end_of_game = True
        
        
def print_report():
    
    global level
    global number_of_ships
    
    print("-----RAPORLANDIRMA-----")
    
    for ship_number in range(1, 6):
        if check_ship_destruct(ship_number):
            print(ship_dict[ship_number], "gemisi batırıldı. Tebrikler")
    
    print("Kalan gemi sayısı:", number_of_ships)
    
    for row in range(1, size_of_map):
        for col in range(1, size_of_map):
            if level[row][col] == "+":
                level[row][col] = "O"
        
    print_map()
        
    

def main():
    
    global debug_mode
    global end_of_game
    global number_of_ships
    
    create_map()
    
    while end_of_game is False:
        print_map()
        shoot()
        check_end_of_game()
        
    print_report()

    
if __name__ == "__main__":
    main()