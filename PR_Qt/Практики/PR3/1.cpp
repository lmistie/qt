#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>

int main() {
    const int rowCount = 200;

    // Открываем файл для записи
    std::ofstream outFile("r_200.csv");

    // Проверяем, успешно ли открылся файл
    if (!outFile.is_open()) {
        std::cerr << "Ошибка открытия файла!" << std::endl;
        return 1;
    }

    // Записываем заголовок CSV
    outFile << "№,Секунда,Микросекунда" << std::endl;

    // Цикл для записи данных
    for (int i = 1; i <= rowCount; ++i) {
        // Получаем текущее время
        auto currentTime = std::chrono::system_clock::now();
        auto seconds = std::chrono::time_point_cast<std::chrono::seconds>(currentTime);
        auto fraction = currentTime - seconds;

        // Преобразуем время в секунды и миллисекунды
        auto seconds_count = std::chrono::duration_cast<std::chrono::seconds>(seconds.time_since_epoch()).count();
        auto milliseconds_count = std::chrono::duration_cast<std::chrono::milliseconds>(fraction).count();

        // Записываем данные в файл
        outFile << i << "," << seconds_count << "," << milliseconds_count << std::endl;

        // Приостанавливаем выполнение цикла на 0,02 секунды
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }

    // Закрываем файл
    outFile.close();

    std::cout << "CSV-файл успешно создан." << std::endl;

    return 0;
}
