### 前言
Confusion即为混淆，Diffusion即为扩散。混淆和扩散是香农提出的设计密码的两种基本指导思想。其目的是抵抗攻击者对密码体制的<span style="color:yellow">统计分析</span>。说直白一点就是抵抗攻击者通过密文的统计特性推测出明文或者密钥。
一般来说，Confusion是通过S-box来实现目的。Diffusion是通过对位进行转换实现。
```
Confusion
Confusion means that each binary digit (bit) of the ciphertext should depend on several parts of the key, obscuring the connections between the two.[2]

The property of confusion hides the relationship between the ciphertext and the key.

This property makes it difficult to find the key from the ciphertext and if a single bit in a key is changed, the calculation of most or all of the bits in the ciphertext will be affected.

Confusion increases the ambiguity of ciphertext and it is used by both block and stream ciphers.

In substitution–permutation networks, confusion is provided by substitution boxes.

Diffusion
Diffusion means that if we change a single bit of the plaintext, then about half of the bits in the ciphertext should change, and similarly, if we change one bit of the ciphertext, then about half of the plaintext bits should change.[3] This is equivalent to the expectation that encryption schemes exhibit an avalanche effect.

The purpose of diffusion is to hide the statistical relationship between the ciphertext and the plain text. For example, diffusion ensures that any patterns in the plaintext, such as redundant bits, are not apparent in the ciphertext.[2] Block ciphers achieve this by "diffusing" the information about the plaintext's structure across the rows and columns of the cipher.

In substitution–permutation networks, diffusion is provided by permutation boxes.
```
