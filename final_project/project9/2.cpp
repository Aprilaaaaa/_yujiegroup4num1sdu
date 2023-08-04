#include<iostream>
using namespace std;
void subbyte(uint8_t* sbox, uint8_t* message);
void subkey(uint8_t* sbox, uint8_t* key);
void RowShift(uint8_t* message);
void MixColumns(uint8_t* message);
uint8_t compute(uint8_t a, uint8_t b);
void key_wheel_addition(uint8_t* key, uint8_t* message);
static void dump_buf(uint8_t* buf, uint32_t len)
{
	int i;

	printf("buf:");

	for (i = 0; i < len; i++) {
		printf("%s%02X%s", i % 16 == 0 ? "\r\n\t" : " ",
			buf[i],
			i == len - 1 ? "\r\n" : "");
	}
}
uint8_t* key_expression(uint8_t* key, uint8_t* sbox, uint8_t* constant, int index);
int main()
{
	//AES：S盒

	uint8_t sbox[256] =
	{
		0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,
	0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
	0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,
	0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
	0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,
	0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
	0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,
	0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
	0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,
	0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
	0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,
	0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
	0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,
	0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
	0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,
	0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
	0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,
	0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
	0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,
	0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
	0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,
	0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
	0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,
	0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
	0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,
	0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
	0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,
	0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
	0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,
	0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
	0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,
	0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
	};
	uint8_t* p_sbox = &sbox[0];
	uint8_t key[16] = {
	0x2b, 0x28, 0xab, 0x09, 0x7e, 0xae, 0xf7, 0xcf,
	0x15, 0xd2, 0x15, 0x4f, 0x16, 0xa6, 0x88, 0x3c
	};
	uint8_t* p_key = &key[0];
	uint8_t key_constant[16] = { 0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36 };//轮常量
	uint8_t* p_constant = &key_constant[0];
	dump_buf(p_key, 16);
	uint8_t* key_pro = new uint8_t[16];
	//uint8_t message[16] = { 0x32,0x88,0x31,0xe0,0x43,0x5a,0x31,0x37,0xf6,0x30,0x98,0x07,0xa8,0x8d,0xa2,0x34 };
	uint8_t message[16] = { 0x02,0x00,0x02,0x01,0x00,0x00,0x04,0x06,0x00,0x01,0x02,0x03,0x00,0x00,0x00,0x00 };
	uint8_t* p_mes = &message[0];
	cout << "plaintext：202100460119" << endl;
	key_wheel_addition(p_key, p_mes);//初始密钥轮加
	//第一轮开始
	int index = 0;
	key_pro = key_expression(p_key, p_sbox, p_constant, index);//第一轮轮密钥
	subbyte(p_sbox, p_mes);//字节替换
	RowShift(p_mes);//行移位
	MixColumns(p_mes);//列混合
	key_wheel_addition(key_pro, p_mes);//密钥轮加
	index = 1;
	dump_buf(key_pro, 16);
	for (; index < 9; index++)
	{
		key_pro = key_expression(key_pro, p_sbox, p_constant, index);
		dump_buf(key_pro, 16);//输出轮密钥
		subbyte(p_sbox, p_mes);//字节替换
		RowShift(p_mes);//行移位
		MixColumns(p_mes);//列混合
		key_wheel_addition(key_pro, p_mes);//密钥轮加
	}
	index = 9;
	//第十轮开始
	key_pro = key_expression(key_pro, p_sbox, p_constant, index);
	dump_buf(key_pro, 16);//输出轮密钥
	subkey(p_sbox, key_pro);
	RowShift(p_mes);
	key_wheel_addition(key_pro, p_mes);
	cout << "ciphertext:" << endl;
	dump_buf(p_mes, 16);
	return 0;
}
void subbyte(uint8_t* sbox, uint8_t* message)
{
	//字节替换，行列的
	int i = 0;
	//需要两个变量获得每个位置的行列值
	uint8_t a, b;
	for (; i < 16; i++)
	{
		a = message[i] >> 4;//a为行数
		b = message[i] << 4;
		b = b >> 4;//b为列数,所以对应的应该是行数*16+列数的位置
		message[i] = sbox[a * 16 + b];
	}
}
void subkey(uint8_t* sbox, uint8_t* key)
{
	//字节替换，行列的
	int i = 0;
	uint8_t a, b;
	for (; i < 16; i++)
	{
		if (i == 3 || i == 7 || i == 11 || i == 15)
		{
			a = key[i] >> 4;//a为行数
			b = key[i] << 4;
			b = b >> 4;//b为列数,所以对应的应该是行数*16+列数的位置
			key[i] = sbox[a * 16 + b];
		}
		//其他位置不变
	}
}
uint8_t* key_expression(uint8_t* key, uint8_t* sbox, uint8_t* constant, int index)
{
	//相同s盒
	//进行列变换之前，得先把原来的轮密钥copy一份，这样可以不改动subkey函数
	uint8_t* key_copy = new uint8_t[16];
	int k = 0;
	for (; k < 16; k++)
		key_copy[k] = key[k];
	k = 0;
	//对最后一列进行列变换
	uint8_t a = key[3], b = key[7], c = key[11], d = key[15];
	key[3] = b, key[7] = c, key[11] = d, key[15] = a;
	uint8_t* pro_key = new uint8_t[16];//下一轮的密钥
	//怎么把一列key传进去,直接整个传进去
	subkey(sbox, key);//初始密钥的最后一列进S盒
	pro_key[0] = key[0] ^ key[3] ^ constant[index], pro_key[4] = key[4] ^ key[7];
	pro_key[8] = key[8] ^ key[11], pro_key[12] = key[12] ^ key[15];
	//trust trust trust trust
	int i = 1;
	int j = 0;
	for (; i < 4; i++)
	{
		for (; j < 4; j++)
		{
			pro_key[i + j * 4] = key_copy[i + j * 4] ^ pro_key[i + j * 4 - 1];//修改一,修改多次
		}
		j = 0;
	}
	key = key_copy;//直接让key指向key_copy地址（这句能起到正确作用吗）
	return pro_key;//使用一次，之前的轮密钥被改变，不能继续使用
}
void RowShift(uint8_t* message)
{
	//行移位，第一行左移零位，第二行左移一位，类推
	int i = 0, j = 0;
	for (; i < 4; i++)
	{
		uint8_t a, b, c, d;
		if (i == 1)
		{
			a = message[i * 4 + 0], b = message[i * 4 + 1], c = message[i * 4 + 2], d = message[i * 4 + 3];
			message[4] = b, message[5] = c, message[6] = d, message[7] = a;
		}
		if (i == 2)
		{
			a = message[i * 4 + 0], b = message[i * 4 + 1], c = message[i * 4 + 2], d = message[i * 4 + 3];
			message[8] = c, message[9] = d, message[10] = a, message[11] = b;
		}
		if (i == 3)
		{
			a = message[i * 4 + 0], b = message[i * 4 + 1], c = message[i * 4 + 2], d = message[i * 4 + 3];
			message[12] = d, message[13] = a, message[14] = b, message[15] = c;
		}
	}
}
uint8_t compute(uint8_t a, uint8_t b)
{
	//定义列混合中两数的计算
	if (a == 0x01)
		return b;
	if (a == 0x02)
		return((b << 1) ^ ((b >> 7) * (0x1b)));
	if (a == 0x03)
		return compute(0x01, b) + compute(0x02, b);
}
void MixColumns(uint8_t* message)
{
	int i = 0, j = 0;
	for (; i < 4; i++)
	{
		for (; j < 4; j++)
		{
			if (j == 0)
				message[j * 4 + i] = compute(0x02, message[i]) ^ compute(0x03, message[i + 4]) ^ message[i + 8] ^ message[i + 12];
			if (j == 1)
				message[j * 4 + i] = message[i] ^ compute(0x02, message[i + 4]) ^ compute(0x03, message[i + 8]) ^ message[i + 12];
			if (j == 2)
				message[j * 4 + i] = message[i] ^ message[i + 4] ^ compute(0x02, message[i + 8]) ^ compute(0x03, message[i + 12]);
			if (j == 4)
				message[j * 4 + i] = compute(0x03, message[i]) ^ message[i + 4] ^ message[i + 8] ^ compute(0x02, message[i + 12]);

		}
		j = 0;//修改二,相同问题
	}
}
void key_wheel_addition(uint8_t* key, uint8_t* message)
{
	int i = 0;
	for (; i < 16; i++)
		message[i] = message[i] ^ key[i];
}