#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

int main() {
    // Открываем файл CSV для чтения
    std::ifstream file("Excel.csv");

    // Проверяем, успешно ли открылся файл
    if (!file.is_open()) {
        std::cerr << "Ошибка открытия файла!" << std::endl;
        return 1;
    }

    // Читаем заголовок
    std::string header;
    if (std::getline(file, header)) {
        std::cout << "Заголовок: " << header << std::endl;

        // Читаем остальные строки
        std::vector<std::string> rows;
        std::string line;
        while (std::getline(file, line)) {
            rows.push_back(line);
        }

        // Выводим остальные строки
        std::cout << "Остальные строки:" << std::endl;
        for (const auto& row : rows) {
            std::cout << row << std::endl;
        }
    } else {
        std::cerr << "Не удалось прочитать заголовок!" << std::endl;
    }

    // Закрываем файл
    file.close();

    return 0;
}
