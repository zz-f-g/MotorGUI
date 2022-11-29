import tkinter as tk
import sys
from math import pi


class DcMotor:
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


class Ui:
    def __init__(self) -> None:
        self.M = DcMotor()
        self.M.T2 = 17e3/(3000 * 2 * pi / 60)
        self.root = tk.Tk()
        self.root.title('直流电动机工作特性测定')
        self.root.iconbitmap(sys.path[0] + '/images/motor.ico')
        self.canvas = tk.Canvas(
            self.root,
            width=600,
            height=400,
            bg='#ffffff')
        self.schematic = tk.PhotoImage(
            file=sys.path[0]+'/images/schematic.png')
        self.canvas.create_image(300, 200, image=self.schematic)
        self.canvas.grid(rowspan=8)
        self.msg_T2 = tk.Message(
            self.root,
            text='输入电机负载（单位 N·m）',
            width=150)
        self.msg_T2.grid(row=0, column=1, columnspan=2)
        self.entry_T2 = tk.Entry(self.root)
        self.entry_T2.grid(row=1, column=1)
        self.btn_T2 = tk.Button(
            self.root,
            text='确认',
            command=self.update)
        self.btn_T2.grid(row=1, column=2)
        self.n = tk.StringVar()
        self.n.set('电机转速为\n%.0f r/min' % (self.M.n))
        self.Ia = tk.StringVar()
        self.Ia.set('电枢电流为\n%.2f A' % (self.M.Ia))
        self.msg_n = tk.Message(
            self.root,
            textvariable=self.n,
            width=150)
        self.msg_n.grid(row=4, column=1, rowspan=2, columnspan=2)
        self.msg_Ia = tk.Message(
            self.root,
            textvariable=self.Ia,
            width=150)
        self.msg_Ia.grid(row=7, column=1, rowspan=2, columnspan=2)
        self.root.mainloop()

    def update(self) -> None:
        try:
            T2 = float(self.entry_T2.get())
            self.M.T2 = T2
            self.n.set('电机转速为\n%.0f r/min' % (self.M.n))
            self.Ia.set('电枢电流为\n%.2f A' % (self.M.Ia))
        except:
            print('> [!error] invalid input T2')


if __name__ == '__main__':
    app = Ui()
