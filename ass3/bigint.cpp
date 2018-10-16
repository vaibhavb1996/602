// Copyright 2018 Vaibhav Bansal vbansal@bu.edu
// Copyright 2018 Ayush Shirsat ayush34@bu.edu
// Copyright 2018 Julie Park ysp599@bu.edu

#include <string>
#include <vector>

typedef string BigInt;
BigInt multiply_int(const BigInt& a, const BigInt& b) {
    int l1 = a.size();
    int l2 = b.size();
    if (l1 == 0 || l2 == 0)
        return "0";
    vector <int> result(l1 + l2, 0);
    // indexes are used to find poistions
    int i_n1, i_n2 = 0;

    // Right to left multiplication
    for (int i = l1-1; i >= 0; i--) {
        int carry = 0;
        int l1 = int(a[i]) - '0';
        // resets back to least significant digit
        i_n2 = 0;
        for (int j=l2-1; j >= 0; j--) {
            int l2 = int(b[j]) - '0';
            int sum = l1*l2 + result[i_n1 + i_n2] + carry;
            carry = sum/10;
            result[i_n1 + i_n2] = sum % 10;
            i_n2++;
        }
        if (carry > 0)
            result[i_n1 + i_n2] += carry;
        i_n1++;
    }
    int i = result.size() - 1;
    while (i >= 0 && result[i] == 0)
        i--;
    if (i == -1)
        return "0";
    BigInt s = "";
    while (i >= 0)
        s += to_string(result[i--]);
    return s;
}
