import random
import copy


class Sudoku:
    def __init__(self, lista=False):
        if lista:
            self.lista = lista
        else:
            self.lista = []
            for _ in range(1, 10):
                self.row = []
                for _ in range(1, 10):
                    self.row.append(0)
                self.lista.append(self.row)

    # Zmienia sudoku w inne
    def change_list(self, new_list):
        self.lista = new_list

    # Funkcja testowa, do wyrzucenia
    def write_numbers_in_sudoku(self):
        for row in self.lista:
            print(row)

    # Sprawdza czy wiersze sudoku jest uzupełnione zgodnie z zasadami
    # użycie set powoduje że nie ma powtórzeń, można to zrobić if not element in lista
    def check_row(self):
        for iterator_row in self.lista:
            sum_set_row = sum(set(iterator_row))
            sum_lista_row = sum(iterator_row)
            if sum_set_row != 0:
                if sum_set_row != sum_lista_row:
                    return False
        return True

    # Sprawdza czy kolumy sudoku jest uzupełnione zgodnie z zasadami
    def check_column(self):
        for iterator_column in range(9):
            column = []
            for iterator_row in range(9):
                column.append(self.lista[iterator_row][iterator_column])
            sum_set_column = sum(set(column))
            sum_list_column = sum(column)
            if sum_set_column != 0:
                if sum_set_column != sum_list_column:
                    return False
        return True

    # Jakieś 3h bo zapomniałem że ostatni część z pętli for nie jest brana pod uwage
    # Sprawdza czy kwadraty Sudoku jest uzupełnione zgodnie z zasadami
    def check_square(self):
        for iterator_next_column in range(3):
            for iterator_y in range(3):
                square = []
                for iterator_x in range(3):
                    square.append(self.lista[iterator_y * 3][iterator_x + iterator_next_column * 3])
                    square.append(self.lista[1 + iterator_y * 3][iterator_x + iterator_next_column * 3])
                    square.append(self.lista[2 + iterator_y * 3][iterator_x + iterator_next_column * 3])
                sum_set_square = sum(set(square))
                sum_lista_square = sum(square)
                if sum_set_square != 0:
                    if sum_set_square != sum_lista_square:
                        return False
        return True

    # Sprawdza czy Sudoku jest uzupełnione zgodnie z zasadami
    def check_sudoku(self):
        if self.check_square() and self.check_row() and self.check_column():
            return True
        else:
            return False

    # Sprawdza czy całe sudoku jest uzupełnione
    def check_sudoku_empty(self):
        for row in self.lista:
            for i_check in row:
                if i_check == 0:
                    return False
        return True

    # Szukanie pustych miejsc i dodawanie ich koordynatów do listy, metoda zwraca liste
    def empty_places(self):
        list_empty_places = []
        x = 0
        for row in self.lista:
            y = 0
            for char in row:
                if char == 0:
                    list_empty_places.append((x, y))
                y += 1
            x += 1
        return list_empty_places

    # Randomowe wstawianie cyfr w puste miejsca, zgodnie z zasadami
    # Na początku inny pomysł potem wywaliłem wszystko i napisałem od nowa
    # pomógł chat gpt z import copy, ponieważ copy() pythona nie działało
    # Strasznie długo siedziałem nad tą metodą, a rozwiązanie jest błache, wystarczyło wyjść z pudełka
    def random_insert_digit(self):
        lista_copy = copy.deepcopy(self.lista)
        lista = self.lista
        lista_empty_places = self.empty_places()
        length_empty_places = len(lista_empty_places)
        for i_random_insert in range(length_empty_places):
            random_int = random.randint(0, length_empty_places - 1)
            coordinates = lista_empty_places[random_int]
            for insert in range(1, 10):
                lista[coordinates[0]][coordinates[1]] = insert
                if self.check_sudoku():
                    break
                else:
                    lista[coordinates[0]][coordinates[1]] = 0
            lista_empty_places.remove(coordinates)
            length_empty_places = len(lista_empty_places)
        self.change_list(lista_copy)
        return Sudoku(lista)


# Generowanie 300 sudoku, pierwszej generacji, i wybranie 30 najlepszych
def the_best_first_population(scope=30):
    the_best_sudoku = [(0, 40)]
    for _ in range(300):
        sud2 = sud1.random_insert_digit()
        length_empty_places = len(sud2.empty_places())
        for sud, number_empty_places in the_best_sudoku:
            if length_empty_places < number_empty_places:
                the_best_sudoku.insert(the_best_sudoku.index((sud, number_empty_places)), (sud2, length_empty_places))
                if len(the_best_sudoku) > scope:
                    the_best_sudoku.remove(the_best_sudoku[scope])
                break
    return the_best_sudoku


# Przekonałem się że system kontroli wersji jest potrzebny, skasował przez przypadek kawałek i napisałem źle, nie
# działało i nie mogłem znalezc błedu dopiero przecofałem się i zobaczyłem
sud1 = Sudoku()
sud1.change_list([[0, 0, 0, 5, 0, 0, 0, 0, 0],
                  [0, 4, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 0, 0],
                  [4, 0, 0, 0, 0, 7, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 6, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 1]])
lista_zwracana = the_best_first_population()
for i in range(30):
    sud3 = lista_zwracana[i][0]
    print(lista_zwracana[i][1])
    sud3.write_numbers_in_sudoku()
    print("\n \n")
