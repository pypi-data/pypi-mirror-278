

int convert_BCD(const unsigned char bcd)
{
#if 1
    int val = 0;
    val += (bcd >> 4) * 10;
    val += bcd & 0xf;
    return val;
#else
    unsigned char result;
    __asm__ (
        "mov %1, %%al;"        // 将输入的 BCD 值移动到 AL 寄存器
        "and $0x0F, %%al;"     // 将 AL 的高 4 位清零，只保留低 4 位（个位数）
        "mov %1, %%bl;"        // 将输入的 BCD 值再次移动到 BL 寄存器
        "shr $4, %%bl;"        // 将 BL 右移 4 位，只保留高 4 位（十位数）
        "imul $10, %%bl, %%bl;" // 将十位数乘以 10
        "add %%bl, %%al;"      // 将十位数和个位数相加得到结果
        "mov %%al, %0;"        // 将结果存储到输出变量中
        : "=r" (result)
        : "r" (bcd)
        : "%al", "%bl"
    );
    return result;
#endif
}

int convert_BCDs(const unsigned char *ptr, int len)
{
    int val = 0;
    for(int i=0; i<len; i++) {
        val = val * 100 + convert_BCD(ptr[i]);
    }
    return val;
}
