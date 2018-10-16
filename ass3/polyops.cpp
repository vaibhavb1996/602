// Copyright 2018 Vaibhav Bansal vbansal@bu.edu
// Copyright 2018 Ayush Shirsat ayush34@bu.edu
// Copyright 2018 Julie Park ysp599@bu.edu

typedef vector<double> Poly;

// Add two polynomials
Poly add_poly(const Poly& a, const Poly& b) {
    int length;
    if (a.size() > b.size())
        length = a.size();
    else
        length = b.size();

    Poly c;

    for (int i=0; i < length; i++) {
        c.push_back(a[i] + b[i]);
    }
    int k;
    for (k = length - 1; k >= 1; k--) {
        if (c[k] == 0)
            c.pop_back();
        else
            break;
    }
    return c;
}
// Multiplication of two polynomials
Poly multiply_poly(const Poly& a, const Poly& b) {
    int length = a.size() + b.size() - 1;
    Poly c;
    float X[10][10] = {{0}};
    int i, j, k;
    float l[10];

    for (i = 0; i< a.size(); i++) {
        for (j = 0; j < b.size(); j++) {
            X[i][j] = a[i] * b[j];
        }
    }

    for (k = 0; k < length; k++) {
        l[k] = 0;
        for (i = 0; i <= k; i++) {
            for (j = 0; j <= k; j++) {
                if ( (i + j) == k )  {
                    l[k] = l[k] + X[i][j];
                }
            }
        }
        c.push_back(l[k]);
    }

    for (k = length - 1; k >= 1; k--) {
        if (c[k] == 0)
            c.pop_back();
        else
            break;
    }
    return c;
}
