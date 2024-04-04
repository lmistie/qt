#include <iostream>
#include <string>

class Soda {
private:
    std::string additive;  // Добавка к газировке

public:
    // Конструктор класса, принимает аргумент additive при инициализации
    Soda(const std::string& additive) : additive(additive) {}

    // Метод для вывода информации о напитке
    void show_my_drink() {
        if (!additive.empty()) {
            std::cout << "Газировка и " << additive << std::endl;
        } else {
            std::cout << "Обычная газировка" << std::endl;
        }
    }
};

int main() {
    // Пример использования класса Soda
    Soda regularSoda("");  // Создаем объект газировки без добавки
    Soda flavoredSoda("лимон");  // Создаем объект газировки с добавкой

    // Выводим информацию о напитках
    std::cout << "Первый напиток: ";
    regularSoda.show_my_drink();

    std::cout << "Второй напиток: ";
    flavoredSoda.show_my_drink();

    return 0;
}
