#include <fstream>
#include <iomanip>

#define NMAX 10000

using namespace std;

void bubble_sort(int v[], int n, bool ascending) {
   for (int i = 0; i < n - 1; ++i) {
        for (int j = i; j < n; ++j) {
            if (ascending && v[i] > v[j]) {
                int aux = v[i];
                v[i] = v[j];
                v[j] = aux;
            } else if (!ascending && v[i] < v[j]) {
                int aux = v[i];
                v[i] = v[j];
                v[j] = aux;
            }
        }
    }
}

int main(int argc, char* argv[]) {
    ifstream in("3.in");
    ofstream out("3.out");

    int n, n_even = 0, n_odd = 0;
    int v[NMAX];
    int even[NMAX];
    int odd[NMAX];

    in >> n;
    for (int i = 0; i < n; ++i) {
        in >> v[i];
    }

    for (int i = 0; i < n; ++i) {
        if (v[i] % 2 == 0) {
            even[n_even++] = v[i];
        } else {
            odd[n_odd++] = v[i];
        }
    }

   bubble_sort(even, n_even, true);
   bubble_sort(odd, n_odd, false);

    for (int i = 0; i < n_even; ++i) {
        out << even[i] << " ";
    }
    out << "\n";

    for (int i = 0; i < n_odd; ++i) {
        out << odd[i] << " ";
    }

    out << "\n";

    return 0;
}
