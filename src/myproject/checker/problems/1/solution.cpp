#include <fstream>
#include <climits>

using namespace std;

int main(int argc, char** argv) {
    ifstream in("1.in");
    ofstream out("1.out");
    
    int max_number = INT_MIN; 
    int min_number = INT_MAX;
    int x;

    in >> x;
    while (x != 0) {
        if (x < min_number) {
            min_number = x;
        }

        if (x > max_number) {
            max_number = x;
        }

        in >> x;
    }

    out << min_number << "\n" << max_number << "\n";

    return 0;
}
