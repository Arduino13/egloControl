#include <cstdio>
#include <iostream>
#include <fstream>

typedef unsigned char uchar;

using namespace std;

extern "C" uchar aes_att_encryption_packet(uchar *key,uchar *iv,uchar *mic,uchar mic_len,uchar *ps,uchar len);

int main(){
	ifstream file;
	file.open("output_encrypt.txt");
	
	uchar key_u[16];
	uchar address_u[8];
	uchar command_u[20];

	int x;
	int i=0;
	while(file >> x) {
		if(i<16){
			key_u[i]=x;
		}
		else if(i>=16 && i<36){
			command_u[i-16]=x;
		}
		else if(i>=36 && i<44){
			address_u[i-36]=x;
		}

		i++;
	}
	file.close();

	aes_att_encryption_packet(key_u,address_u,command_u+3,2,command_u+5,15);

	ofstream en("en.txt");

	for(int i=0;i<20;i++){
		cout << +command_u[i];
		if(i!=19) cout << ',';

		en << +command_u[i];
		if(i!=19) en << ',';
	}
	en << '\n';
	en.close();
	cout << endl;

	return 0;
}
