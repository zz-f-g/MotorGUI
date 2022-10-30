<h1><center>扩展设计一</center></h1>

<div align='right'>2052110 郭子瞻</div>

## 问题描述

一台并励直流电机的额定参数如下：

$$
\left\{ \begin{aligned}
P_{N} &= 17 \text{kW} \\
U_{N} &= 220 \text{V} \\
n_{N} &= 3000 \text{r/min} \\
I_{N} &= 88.9 \text{A} \\
R_{a} &= 0.114 \Omega \\
R_{f} &= 181.5 \Omega
\end{aligned} \right.
$$

设计直流电机的磁路和电路模型，完成**直流电动机工作特性测定**功能。

---

## 设计说明

### 电机的数学建模

将并励电机视为一个线性时不变系统，输入为：

- 绕组电压（同时为励磁绕组电压和电枢绕组电压）$U$
- 负载（机械负载）$T_{2}$

输出为电机的转速 $n$（单位为 r/min）或 $\Omega$（单位为 rad/s）。

为了便于在程序中量化电机的数学模型，在这里说明对电机损耗和磁路模型的取舍：

1. 铜耗：考虑了线性电阻的焦耳热，包括电枢绕组、励磁绕组，但是忽略了电刷压降损耗，在电路方程中表现为电枢绕组电阻 $R_{a}$ 和励磁绕组电阻 $R_{f}$；
2. 铁耗和机械损耗：考虑，但是忽略转速变化引起的变化，在机械方程中表现为常量空载转矩 $T_{0}$；
3. 附加损耗：不考虑；
4. 磁路模型：认为在调节范围内，磁通和励磁电流成正比，系数为 $K_{f}$。

电路方程：

$$
\begin{aligned}
U &= I_{a} R_{a} + C_{T} \Phi \Omega + 2 \Delta U_{c} \\
& \approx I_{a} R_{a} + C_{T} \Phi \Omega \\
U &= I_{f} R_{f} + L_{f} \frac{\mathrm{d}I_{f}}{\mathrm{d}t} \\
& \approx I_{f} R_{f}
\end{aligned}
$$

磁路方程：

$$
\Phi = f(I_{f}) \approx K_{f} I_{f}
$$

机械方程：

$$
T_{em} = T_{0} + T_{2}
$$

机电方程：

$$
T_{em} = C_{T} \Phi I_{a}
$$

综合上述方程组，得到：

$$
\begin{aligned}
\Omega &= \frac{R_{f}}{C_{T}K_{f}} - \frac{R^{2}_{f}R_{a}}{(C_{T}K_{f})^{2}} \cdot \frac{T_{0}+T_{2}}{U^{2}} \\
n &= \frac{60}{2\pi} \Omega
\end{aligned}
$$

需要标定的参数有：

- $C'_{T} = C_{T}K_{f}$
- $T_{0}$
- $R_{f}$
- $R_{a}$

问题描述中给出了电阻参数和额定状态，下面根据已知参数推导上面需要标定的参数 $C'_{T}$ 和 $T_{0}$.

$$
\begin{aligned}
C'_{T} \frac{U_{N}}{R_{f}} \Omega_{N} &= U_{N} - \left(I_{N} - \frac{U_{N}}{R_{f}}\right) R_{a} \\
\Omega_{N} &= \frac{2\pi}{60} n_{N} \\
T_{2N} &= \frac{P_{N}}{\Omega_{N}} \\
T_{2N} + T_{0} &= C'_{T} \frac{U_{N}}{R_{f}} \left(I_{N} - \frac{U_{N}}{R_{f}}\right)
\end{aligned}
$$

求解得到

$$
\left\{ \begin{aligned}
C'_{T} &= \frac{60R_{f}}{2\pi n_{N}} \left( 1 + \frac{R_{a}}{R_{f}}- \frac{I_{N}R_{a}}{U_{N}} \right) \\
T_{0} &= \frac{60}{2\pi n_{N}} \left[ U_{N}\left(I_{N} - \frac{U_{N}}{R_{f}}\right)\left( 1 + \frac{R_{a}}{R_{f}} - \frac{I_{N}R_{a}}{U_{N}} \right) - P_{N} \right]
\end{aligned} \right.
$$

因此，给定一组额定状态和电枢绕组、励磁绕组的电阻值，就可以得到电机的模型。

### 实验测量电路
