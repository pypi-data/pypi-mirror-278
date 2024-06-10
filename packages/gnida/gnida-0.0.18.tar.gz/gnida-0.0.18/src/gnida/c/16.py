# 16. Написать программу с интерактивным консольным меню (т.е. вывод
# списка действий по цифрам) по удалению из списка (задаем с клавиатуры) элемента
# с задаваемым с клавиатуры индексом (например, m). При решении задачи
# необходимо использовать функцию map. Содержание меню: 1. Удалить элемент из
# списка и вывести итоговый список. 2. Удалить элемент из списка и вывести его
# номер(а).

def remove_element_by_index(lst, index):
    if index < 0 or index >= len(lst):
        raise IndexError("Индекс вне диапазона списка.")
    return list(map(lambda ix: ix[1], filter(lambda ix: ix[0] != index, enumerate(lst))))

def main():
    while True:
        print("Меню:")
        print("1. Удалить элемент из списка и вывести итоговый список")
        print("2. Удалить элемент из списка и вывести его номер(а)")
        print("3. Выйти")

        choice = input("Выберите действие (1-3): ")

        if choice == '3':
            print("Выход из программы.")
            break

        if choice in ['1', '2']:
            raw_list = input("Введите элементы списка через пробел: ")
            lst = raw_list.split()
            try:
                index = int(input("Введите индекс элемента для удаления: "))
            except ValueError:
                print("Индекс должен быть числом.")
                continue

            try:
                if choice == '1':
                    new_list = remove_element_by_index(lst, index)
                    print("Итоговый список:", new_list)
                elif choice == '2':
                    removed_element = lst[index]
                    new_list = remove_element_by_index(lst, index)
                    print("Индекс удаленного элемента:", index)
                    print("Итоговый список:", new_list)
            except IndexError as e:
                print(e)
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()


