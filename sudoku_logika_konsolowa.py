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

    # Sprawdza, czy wiersze sudoku jest, uzupełnione zgodnie z zasadami
    # użycie set powoduje, że nie ma powtórzeń, można to zrobić if not element in lista
    def check_row(self):
        for iterator_row in self.lista:
            sum_set_row = sum(set(iterator_row))
            sum_lista_row = sum(iterator_row)
            if sum_set_row != 0:
                if sum_set_row != sum_lista_row:
                    return False
        return True

    # Sprawdza, czy kolumy sudoku jest uzupełnione zgodnie z zasadami
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

    # Jakieś 3h, bo zapomniałem, że ostatni część z pętli for nie jest brana pod uwagę
    # Sprawdza, czy kwadraty Sudoku jest uzupełnione zgodnie z zasadami
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

    # Sprawdza, czy Sudoku jest uzupełnione zgodnie z zasadami
    def check_sudoku(self):
        if self.check_square() and self.check_row() and self.check_column():
            return True
        else:
            return False

    # Szukanie pustych miejsc i dodawanie ich koordynatów do listy, metoda zwraca listę
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
    # Na początku inny pomysł potem wywaliłem wszystko i napisałem od nowa.
    # Pomógł chat gpt z import copy, ponieważ copy () pythona nie działało.
    # Strasznie długo siedziałem nad tą metodą, a rozwiązanie jest błache, wystarczyło wyjść z pudełka
    def random_insert_digit(self):
        lista_copy = copy.deepcopy(self.lista)
        lista = self.lista
        lista_empty_places = self.empty_places()
        length_empty_places = len(lista_empty_places)
        for i_random_insert in range(length_empty_places):
            random_int = random.randint(0, length_empty_places - 1)
            coordinates = lista_empty_places[random_int]
            # list_possible_insert = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            # for insert in range(9):
            #     mutation_add_digit = random.randint(0, len(list_possible_insert) - 1)
            #     lista[coordinates[0]][coordinates[1]] = list_possible_insert[mutation_add_digit]
            #     if self.check_sudoku():
            #         break
            #     else:
            #         lista[coordinates[0]][coordinates[1]] = 0
            #         list_possible_insert.remove(list_possible_insert[mutation_add_digit])
            # //////////////////////////////////////////
            for insert in range(1, 10):
                lista[coordinates[0]][coordinates[1]] = insert
                if self.check_sudoku():
                    break
                else:
                    lista[coordinates[0]][coordinates[1]] = 0
            # //////////////////////////////////////////////
            lista_empty_places.remove(coordinates)
            length_empty_places = len(lista_empty_places)
        self.change_list(lista_copy)
        return Sudoku(lista)

    # Zwraca listę, funkcja potrzebna w funkcji create_children
    def return_list(self):
        return self.lista

    # Tworzy mutacje
    def mutation(self, x_children_mutation, y_children_mutation):
        list_possible_mutation = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for iterator_mutation in range(9):
            mutation_add_digit = random.randint(0, len(list_possible_mutation) - 1)
            self.lista[x_children_mutation][y_children_mutation] = list_possible_mutation[mutation_add_digit]
            if self.check_sudoku():
                break
            else:
                self.lista[x_children_mutation][y_children_mutation] = 0
                list_possible_mutation.remove(list_possible_mutation[mutation_add_digit])

    def change_digit_in_pos(self, posx, posy, digit):
        self.lista[posx][posy] = digit


# Łączenie 2 sudoku w jedno
# zmiana zmiennej mutacja wylosowana
# sprawdzanie, czy takie sudoku może istnieć po losowaniu
# Zasada, że jak jest za duż wcięć, to coś musi być nie tak zadziałała
def create_children(sud_x, sud_y, sud_to_complete, mutation_rate=3):
    new_sud = copy.deepcopy(sud_to_complete)
    sud_male = sud_x.return_list()
    sud_female = sud_y.return_list()
    coordinates_empty_places = copy.deepcopy(sud_to_complete.empty_places())
    for _ in range(len(coordinates_empty_places) - 1):
        random_position_empty = random.randint(0, len(coordinates_empty_places) - 1)
        one_position_empty = coordinates_empty_places[random_position_empty]
        mutation = random.randint(mutation_rate, 100)
        if mutation == mutation_rate:
            new_sud.mutation(one_position_empty[0], one_position_empty[1])
        else:
            # Tu się zaczyna to coś, co napisałem
            list_possible_rand_gender = [1, 2]
            if sud_male[one_position_empty[0]][one_position_empty[1]] == 0 and sud_female[one_position_empty[0]][
                one_position_empty[1]] == 0:
                new_sud.mutation(one_position_empty[0], one_position_empty[1])
            else:
                if sud_male[one_position_empty[0]][one_position_empty[1]] == 0:
                    list_possible_rand_gender.remove(1)
                elif sud_female[one_position_empty[0]][one_position_empty[1]] == 0:
                    list_possible_rand_gender.remove(2)
                # tu się kończy
                random_gender = random.choice(list_possible_rand_gender)
                if random_gender == 1:
                    digit = sud_male[one_position_empty[0]][one_position_empty[1]]
                    new_sud.change_digit_in_pos(one_position_empty[0], one_position_empty[1], digit)
                    if not new_sud.check_sudoku():
                        new_sud.change_digit_in_pos(one_position_empty[0], one_position_empty[1], 0)
                else:
                    digit = sud_female[one_position_empty[0]][one_position_empty[1]]
                    new_sud.change_digit_in_pos(one_position_empty[0], one_position_empty[1], digit)
                    if not new_sud.check_sudoku():
                        new_sud.change_digit_in_pos(one_position_empty[0], one_position_empty[1], 0)
        coordinates_empty_places.remove(coordinates_empty_places[random_position_empty])
    return new_sud


# Generowanie 300 sudoku, pierwszej generacji, i wybranie 30 najlepszych
def the_best_first_population(sud_to_solve, scope=30):
    the_best_sudoku = [(0, 40)]
    for _ in range(300):
        sud_from_first_generation = sud_to_solve.random_insert_digit()
        length_empty_places = len(sud_from_first_generation.empty_places())
        for sud, number_empty_places in the_best_sudoku:
            if length_empty_places < number_empty_places:
                the_best_sudoku.insert(the_best_sudoku.index((sud, number_empty_places)),
                                       (sud_from_first_generation, length_empty_places))
                if len(the_best_sudoku) > scope:
                    the_best_sudoku.remove(the_best_sudoku[scope])
                break
    return the_best_sudoku


# Tworzenie kolejnej generacji
# Zaprojektowałem tę funkcję i metodę create_children i coś nie działało, miałem przerwę 3 dni od programowania,
# wróciłem i w 1h problem po problemie rozwiązana zagadka, czasami trzeba świeżej głowy, przeczytania kodu od nowa,
# ale zamysł był od początku dobry
def create_next_generation(first_sud, the_best_previous_generation, scope_next_generation=30):
    the_best_sudoku = [(0, 40)]
    for _ in range(300):
        random_sudx = random.randint(0, scope_next_generation - 1)
        random_sudy = random.randint(0, scope_next_generation - 1)
        while random_sudx == random_sudy:
            random_sudx = random.randint(0, scope_next_generation - 1)
            random_sudy = random.randint(0, scope_next_generation - 1)
        # wczesniej te 2 pierwsze argumenty były w deepcopy
        new_sud = create_children(copy.deepcopy(the_best_previous_generation[random_sudx][0]),
                                  copy.deepcopy(the_best_previous_generation[random_sudy][0]), copy.deepcopy(first_sud))
        length_empty_places = len(new_sud.empty_places())
        for sud, number_empty_places in the_best_sudoku:
            if length_empty_places < number_empty_places:
                the_best_sudoku.insert(the_best_sudoku.index((sud, number_empty_places)),
                                       (new_sud, length_empty_places))
                if len(the_best_sudoku) > scope_next_generation:
                    the_best_sudoku.remove(the_best_sudoku[scope_next_generation])
                break
    return the_best_sudoku


# Przekonałem się, że system kontroli wersji jest potrzebny, skasował przez przypadek kawałek i napisałem źle, nie
# działało i nie mogłem znaleźć błędu dopiero przecofałem się i zobaczyłem
sud1 = Sudoku()
sud1.change_list([[6, 1, 4, 0, 0, 0, 0, 0, 0],
                  [0, 0, 7, 1, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 6, 0, 0, 8, 0],
                  [0, 0, 0, 5, 1, 0, 0, 4, 8],
                  [0, 0, 0, 0, 0, 8, 0, 2, 0],
                  [0, 0, 0, 0, 0, 9, 0, 0, 3],
                  [0, 0, 0, 0, 0, 0, 0, 0, 7],
                  [0, 0, 0, 0, 0, 0, 0, 0, 6],
                  [0, 9, 0, 0, 0, 0, 0, 0, 0]])

# Sprawdzanie poprawności create children
# sud2 = sud1.random_insert_digit()
# sud3 = sud1.random_insert_digit()
# sud_final = create_children(sud2, sud3, sud1)
# print(sud2.empty_places())
# sud2.write_numbers_in_sudoku()
# print("\n")
# print(sud3.empty_places())
# sud3.write_numbers_in_sudoku()
# print("\n")
# print(sud_final.empty_places())
# sud_final.write_numbers_in_sudoku()


# Tworzenie jakichś tam populacji
lista_zwracana0 = the_best_first_population(sud1)


def kolejne_generacje(lista):
    koniec = 1
    for p in range(50):
        for i in range(5):
            sud2 = lista[i][0]
            print(lista[i][1])
            sud2.write_numbers_in_sudoku()
            print("\n \n")
            if lista[i][0] == 0:
                koniec = 0
        print("##################################################")
        lista_zwracana1 = copy.deepcopy(lista)
        lista = copy.deepcopy(create_next_generation(sud1, lista_zwracana1))
        if koniec == 0:
            break


kolejne_generacje(lista_zwracana0)

# TODO: Co dlaczego ciągle zbiega się do jednego takiego samego sudoku
# TODO: Mutacje, wyrzucić do nowej funkcji
# TODO: Istnieje prawdopodobieństwo że żaden rodzic nie będzie uzupełniony w 1 miejscu, wtedy trzeba wylosować
# TODO: Default argument value is mutable 179 linijka, może byc tak ze trzeba zrobić kopie i dla tego się zrównają
#  wszystkie sudoku
# TODO: Najprawdopodobniej chodzi o to, że dziecko jest tworzone po kolei.
# TODO: Nie może byc ze ta sama osoba, robi sama ze sobą dziecko
# TODO: Mutacja może wstawić coś co można wstawiać
