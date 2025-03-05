#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int main() {
    string str;
    cin >> str;

    int biggest = 1;
    int max_count = 1;
    for (int i = 1; i < str.length(); i++) {
        char prev = str[i - 1];
        char next = str[i];

        if (prev == next){
            // cout << prev << next << endl;
            max_count += 1;
            biggest = max(biggest, max_count);
            }
        else{
            max_count = 1;
        }
    }
    cout << biggest;
    return 0;
}