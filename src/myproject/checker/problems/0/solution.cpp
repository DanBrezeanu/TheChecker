#include <fstream>

using namespace std;

int main(int argc, char** argv) {
    ifstream in("0.in");
    ofstream out("0.out");

    long long a, b;
    long long sum = 0;

    in >> a >> b;
    
    sum = a + b;

    out << sum << "\n";

    return 0;
}
