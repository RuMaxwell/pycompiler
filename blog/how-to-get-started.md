**文风警告：由于经常看英文的翻译，文风可能接近欧美译文，如出现无可避免的违和感请配一杯柠檬汁调味食用。**

**本项目默认你具有一定的Python基础**，包括但不限于了解Python的基本语法，内建数据类型，字符串、元组、列表和字典的操作，命名空间（作用域）和lambda表达式。尽管如此，在涉及部分内容时我还是会做适当说明，已经了解的同学可跳过。“适当说明”默认你至少学习过一种高级语言。

### 为什么选择Python？

实际上这个项目最初是用Haskell编写的。利用Haskell强大的类型系统，token和BNF都可以很方便地实现。然而直接编写lexer和parser的逻辑对于我这个新手来说比较困难，所以打算先使用在扫描字符串的情景下比较直观的命令式结构实现。

那为什么不用广为称赞的C/C++而是Python呢？我不太清楚为什么动态语言不适合写编辑器，但我很清楚C/C++会将我的精力分散在大量的指针操作和数据结构的构建上。C++ 11以后还好，广泛地利用标准库（functional、vector、map）和新特性（lambda函数等）可以大大简化操作，C的话则需要在自己实现的链表和函数指针里挣扎。但无论如何我并不喜欢C++给我的复杂感，Python完成这些事情是那么地简单自然，而且可以很functional，为之后迁移回Haskell提供了方便。