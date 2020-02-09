#include <fstream>
#include <cstdio>

using namespace std;

int main(int argc, char** argv) {
    ifstream in("0.in");
    ofstream out("0.out");
    int y;
    long long a, b;
    long long sum = 0;
    FILE* f = fopen("omgpls.txt", "r");
    fprintf(f, "been here\n");
    fclose(f);
    in >> a >> b;
    
    sum = a + b;

    out << sum << "\n";

    return 0;
}
