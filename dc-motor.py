import tkinter as tk
import sys
from math import pi


class Dc_motor:
    def __init__(self):
        self.CT = 0.5514812838705541
        self.T0 = 4.5033484079373
        self.Ra = 0.114
        self.Rf = 181.5
        self.U = 220
        self.T2 = 0

    @property
    def Omega(self) -> float:
        return self.Rf / self.CT \
            - self.Rf**2*self.Ra/self.CT**2 * \
            (self.T2 + self.T0) / self.U**2

    @property
    def n(self) -> float:
        return self.Omega * 60 / (2 * pi)

    @property
    def Ia(self) -> float:
        return (self.U - self.CT * self.U / self.Rf * self.Omega) / self.Ra


def main() -> None:
    M = Dc_motor()
    M.T2 = 17e3/(3000 * 2 * pi / 60)
    root = tk.Tk()
    root.title('直流电动机工作特性测定')
    root.iconbitmap(sys.path[0] + '/images/motor.ico')
    canvas = tk.Canvas(root, width=400, height=400, bg='#ffffff')
    canvas.grid(rowspan=8)
    canvas.create_rectangle(100, 100, 300, 300, width=3)
    msg_T2 = tk.Message(root, text='输入电机负载（单位 N·m）', width=150)
    msg_T2.grid(row=0, column=1)
    entry_T2 = tk.Entry(root)
    entry_T2.grid(row=1, column=1)
    msg_n = tk.Message(root, text='电机转速为\n%.0fr/min' % (M.n), width=150)
    msg_n.grid(row=4, column=1, rowspan=2)
    msg_Ia = tk.Message(root, text='电枢电流为\n%.2fA' % (M.Ia), width=150)
    msg_Ia.grid(row=7, column=1, rowspan=2)
    root.mainloop()


if __name__ == '__main__':
    main()
