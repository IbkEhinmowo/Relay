#include <iostream>
using namespace std;

string model_arr[100];
int year_arr[100];
float mileage_arr[100];
float efficiency_arr[100];

float fuelRequired(float distance, float efficiency) {
    if (efficiency == 0) return 0;
    return distance / efficiency;
}

float tripCost(float fuel, float price) {
    return fuel * price;
}

void displayCar(string model, int year, float efficiency, float cost) {
    cout << "Model: " << model << ", Year: " << year << ", Efficiency: " << efficiency << " km/l, Trip Cost: $" << cost << endl;
}

int main() {
    int n = 0;
    cout << "Enter car details (model year mileage efficiency), or 'done' to finish:\n";
    while (true) {
        string model;
        cin >> model;
        if (model == "done") break;
        int year;
        float mileage, efficiency;
        cin >> year >> mileage >> efficiency;
        if (cin.fail()) {
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Invalid input. Try again.\n";
            continue;
        }
        model_arr[n] = model;
        year_arr[n] = year;
        mileage_arr[n] = mileage;
        efficiency_arr[n] = efficiency;
        n++;
    }

    float fuelPrice, tripDistance;
    cout << "Enter fuel price per liter: ";
    cin >> fuelPrice;
    cout << "Enter trip distance (km): ";
    cin >> tripDistance;

    cout << "\n--- Car Trip Costs ---\n";
    for (int i = 0; i < n; ++i) {
        float fuel = fuelRequired(tripDistance, efficiency_arr[i]);
        float cost = tripCost(fuel, fuelPrice);
        displayCar(model_arr[i], year_arr[i], efficiency_arr[i], cost);
    }
    return 0;
}
