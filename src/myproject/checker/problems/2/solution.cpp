#include <fstream>
#include <iomanip>

using namespace std;

int main(int argc, char* argv[]) {
    ifstream in("2.in");
    ofstream out("2.out");

    int n, count = 0;
    long long suma = 0;
    double medie = 0.0;

    in >> n;
    while (n != 0) {
        if (n % 2 == 0) {
            suma += n;
            ++count;
        }
        in >> n;
    }

    if (suma == 0) {
        out << "-1\n";
    } else {
        medie = (double)suma / count;
        out << fixed << setprecision(2) << medie << "\n";
    }

    return 0;
}
