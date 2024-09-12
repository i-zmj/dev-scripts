# dev-scripts

### 介绍
开发工具脚本

### 文件结构

- ice_util.py: 被其他ice脚本是用的共通函数
- ice_find_symbol.py: 在指定目录中，查找关键字

### 安装教程

安装python依赖
`python -m pip install -r requirments.txt`

### 结果解读

#### 简要解读

- U: 调用了该函数。利用function A，调用了function B。则B显示为U
- T: 函数实现，函数体。如果编译时提示undefined reference。则指的是找不到函数实现。

#### 详细说明

来源于https://blog.csdn.net/qq_41017902/article/details/107363409

| 类型 | 说明 | 
| --- | --- |
| A	| 该符号的值是绝对的，在以后的链接过程中，不允许进行改变。 |
| B	| 该符号的值出现在非初始化数据段(bss)中。<br/>例如，在一个文件中定义全局static int test。则该符号test的类型为b。|
| C	| 该符号为common。common symbol是未初始话数据段。<br/>该符号没有包含于一个普通section中。只有在链接过程中才进行分配。符号的值表示该符号需要的字节数。例如在一个c文件中，定义int test，并且该符号在别的地方会被引用，则该符号类型即为C。否则其类型为B。 |
| D	| 该符号位于初始话数据段中。一般来说，分配到data section中。<br/>例如定义全局int baud_table[5] = {9600, 19200, 38400, 57600, 115200}，则会分配于初始化数据段中。 |
| G	| 该符号也位于初始化数据段中。<br/>主要用于small object提高访问small data object的一种方式。 |
| I	| 该符号是对另一个符号的间接引用。 |
| N	| 该符号是一个debugging符号。 |
| R	| 该符号位于只读数据区。<br/>例如定义全局const int test[] = {123, 123};则test就是一个只读数据区的符号。<br/>注意在cygwin下如果使用gcc直接编译成MZ格式时，源文件中的test对应_test，并且其符号类型为D，即初始化数据段中。<br/>但是如果使用m6812-elf-gcc这样的交叉编译工具，源文件中的test对应目标文件的test,即没有添加下划线，并且其符号类型为R。一般而言，位于rodata section。<br/>值得注意的是，如果在一个函数中定义const char *test = “abc”, const char test_int = 3。<br/>使用nm都不会得到符号信息，但是字符串“abc”分配于只读存储器中，test在rodata section中，大小为4。 |
| S	| 符号位于非初始化数据区，用于small object。 |
| T	| 该符号位于代码区text section。 |
| U	| 该符号在当前文件中是未定义的，即该符号的定义在别的文件中。<br/>例如，当前文件调用另一个文件中定义的函数，在这个被调用的函数在当前就是未定义的；但是在定义它的文件中类型是T。但是对于全局变量来说，在定义它的文件中，其符号类型为C，在使用它的文件中，其类型为U。 |
| V	| 该符号是一个weak object。 |
| W	| 该符号是没有被明确标记为weak object的弱符号类型。 |
| -	| 该符号是a.out格式文件中的stabs symbol。 |
| ?	| 该符号类型没有定义。 |

