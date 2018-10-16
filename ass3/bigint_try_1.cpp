//Copyright 2018 Vaibhav Bansal vbansal@bu.edu
//Copyright 2018 Ayush Shirsat ayush34@bu.edu
//Copyright 2018 Julie Park ysp599@bu.edu
#include<string>

using namespace std;

typedef string BigInt;
BigInt multiply_int(const BigInt& a, const BigInt& b){
	BigInt A = a;
	//cout<<" A is "<<A<<endl;
	BigInt B = b;
	//cout<<"B is "<<B<<endl;
	int i,j,k;
	int X[20],Y[20];
	int W[20][20]={{0}};
	if (A.length() == 1 && B.length() == 1){
		int m,n,o;
		m = int(A[0])-48;
		n = int(B[0])-48;
		o=m*n;
		BigInt C = to_string(o);
		return C;
	}
	else if(A.length() == 1 || B.length() == 1){
	    if(A.length() == 1){
	    	int m,o;
	    	m = int(A[0])-48;
	    	if(m == 0){
	    		o=0;
				BigInt C = to_string(o);
				return C;
	    	}
	    else {
	    int m,o;
	    m = int(B[0])-48;
	    	if(m == 0){
	    		o=0;
				BigInt C = to_string(o);
				return C;	
	    	}	
	    }
	    /*int m,n,o;
		m = int(A[0])-48;
		n = int(B[0])-48;
		if(m ==0 || n == 0)
		o=0;
		BigInt C = to_string(o);
		return C;*/	
	} 
	else {
	for (i = 0 ; i < A.length() ; i++){
		X[i] = int(A[i])-48;
		//cout<<"X["<<i<<"] is "<<X[i]<<endl;
	}
	for (i = 0 ; i < B.length() ; i++){
		Y[i] = int(B[i])-48;
		//cout<<"Y["<<i<<"] is "<<Y[i]<<endl;
	}

	int length = A.length() + B.length() - 1;
    //int X[20][20] = {{0}};
    
    int Z[length];
    int e = 0;

    for (i = 0; i < A.length(); i++){
        //cout<<"W is ";
        for(j = 0; j < B.length(); j++){
            W[i][j] = X[i] * Y[j];
            //cout<<W[i][j]<<" ";
        }
    //cout<<endl;
    }

    for (k = 0; k < length; k++){
        Z[k] = 0;
        //cout<<"Z ["<<k<<"] before loop is "<<Z[k]<<endl;
        for(i = 0; i <= k; i++){
            for(j = 0; j <= k; j++){
                if((i + j) == k){
                    Z[k] = Z[k] + W[i][j];
                }
            }
        }
    //cout<<"Z ["<<k<<"] after loop is "<<Z[k]<<endl;
    }
    for ( k = length - 1; k >= 0; k--){
    	e = Z[k]%10;
    	Z[k-1] = Z[k-1] + (Z[k] / 10);
    	Z[k] = e;
    	//cout<<"Z ["<<k<<"] is "<<Z[k]<<endl;
    }
	//cout<<"Z is " << Z << endl;
	char arr[length+1];
    for (k = 0; k < length; k++){
    	arr[k] = char(Z[k]+48);
    //	cout<<c[k];
    }
    arr[length]='\0';
    BigInt C = arr;
    return C;
	}

} 