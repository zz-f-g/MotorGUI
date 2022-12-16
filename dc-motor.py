from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import pi
import sys
import random
import json
import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")


class DcMotor:
    def __init__(self):
        self.CT = 0.5514812838705541
        self.T0 = 4.5033484079373
        self.Ra = 0.114
        self.Rf = 181.5
        self.U = 220
        self.T2 = 17e3/(3000 * 2 * pi / 60)
        self.error = 0.05
        self.Tm = 5
        with open(sys.path[0] + '/motor-config.json', 'r') as config:
            data = json.load(config)
            self.CT = (
                60 * data['Rf'] / (2 * pi * data['nN'])
                * (1 + data['Ra'] / data['Rf'] - data['IN'] * data['Ra'] / data['UN'])
            )
            self.T0 = (
                60 / (2 * pi * data['nN'])
                * (data['UN'] * (data['IN'] - data['UN'] / data['Rf'])
                   * (1 + data['Ra'] / data['Rf'] - data['IN'] * data['Ra'] / data['UN'])
                   - data['PN'])
            )
            self.Ra = data['Ra']
            self.Rf = data['Rf']
            self.U = data['UN']
            self.T2 = data['PN'] / (data['nN'] * 2 * pi / 60)
            self.error = data['error']

    @property
    def Omega(self) -> float:
        return self.Rf / self.CT \
            - self.Rf**2*self.Ra/self.CT**2 \
            * (self.T2 + self.T0) / self.U**2

    @property
    def n(self) -> float:
        return self.Omega * 60 / (2 * pi)

    @property
    def Ia(self) -> float:
        return (self.U - self.CT * self.U / self.Rf * self.Omega) / self.Ra \
            * (1 + (2 * random.random() - 1) * self.error)


class Ui:
    def R2T2(self, i):
        return 30 * self.T2max / i

    def __init__(self) -> None:
        self.M = DcMotor()
        self.T2max = 95

        self.data = {}
        self.data['n'] = np.array([])
        self.data['Ia'] = np.array([])

        self.root = tk.Tk()
        self.root.title('直流电动机工作特性测定')
        self.root.iconbitmap(sys.path[0] + '/images/motor.ico')

        self.canvas_sch = tk.Canvas(
            self.root,
            width=500,
            height=400,
            bg='#ffffff'
        )
        self.schematic = tk.PhotoImage(
            file=sys.path[0]+'/images/schematic.png')
        self.canvas_sch.create_image(250, 200, image=self.schematic)
        self.canvas_sch.grid(columnspan=4)

        self.msg_T2 = tk.Message(
            self.root,
            text='输入电机负载（单位 N·m）',
            width=150
        )
        self.msg_T2.grid(row=1, column=0, columnspan=2)

        self.T2str = tk.StringVar()
        self.T2str.set('%.2f' % self.M.T2)
        self.entry_T2 = tk.Entry(self.root, textvariable=self.T2str)
        self.entry_T2.grid(row=2, column=0)

        self.btn_T2 = tk.Button(
            self.root,
            text='确认',
            command=self.update
        )
        self.btn_T2.grid(row=2, column=1)

        self.nstr = tk.StringVar()
        self.nstr.set('电机转速为\n%.0f r/min' % (self.M.n))
        self.msg_n = tk.Message(
            self.root,
            textvariable=self.nstr,
            width=150
        )
        self.msg_n.grid(row=1, column=2, rowspan=2)

        self.Iastr = tk.StringVar()
        self.Iastr.set('电枢电流为\n%.2f A' % (self.M.Ia))
        self.msg_Ia = tk.Message(
            self.root,
            textvariable=self.Iastr,
            width=150
        )
        self.msg_Ia.grid(row=1, column=3, rowspan=2)

        self.msg_R = tk.Message(
            self.root,
            text='或者调节右侧负载电阻 R',
            width=150
        )
        self.msg_R.grid(row=3, column=0, columnspan=2)

        self.scale_R = tk.Scale(
            self.root,
            label='拖动滑动条改变电阻 R：',
            from_=30,
            to=100,
            orient=tk.HORIZONTAL,
            length=200,
            showvalue=False,
            command=self.getR
        )
        self.scale_R.set(self.R2T2(self.M.T2))
        self.scale_R.grid(row=4, column=0, columnspan=2)

        self.btn_sample = tk.Button(
            self.root,
            text='采样',
            command=self.sample
        )
        self.btn_sample.grid(row=3, column=2, pady=5)

        self.btn_plot = tk.Button(
            self.root,
            text='绘图',
            command=self.plot
        )
        self.btn_plot.grid(row=3, column=3, pady=5)

        self.btn_fit = tk.Button(
            self.root,
            text='拟合',
            command=self.fit
        )
        self.btn_fit.grid(row=4, column=2, pady=5)

        self.btn_clear = tk.Button(
            self.root,
            text='清除',
            command=self.clear
        )
        self.btn_clear.grid(row=4, column=3, pady=5)

        self.plot()
        self.root.mainloop()

    def update(self) -> None:
        try:
            T2 = float(self.entry_T2.get())
            if (T2 < 0):
                messagebox.askretrycancel('错误', '输入的负载转矩小于零！')
                return
            elif (T2 > self.T2max):
                messagebox.askretrycancel('错误', '输入的负载转矩超范围！')
                return
            self.M.T2 = T2
            self.scale_R.set(self.R2T2(T2))
            self.nstr.set('电机转速为\n%.0f r/min' % (self.M.n))
            self.Iastr.set('电枢电流为\n%.2f A' % (self.M.Ia))
        except:
            messagebox.askretrycancel('错误', '输入的负载转矩不合法！')

    def getR(self, value) -> None:
        self.M.T2 = self.R2T2(float(value))
        self.T2str.set('%.2f' % self.M.T2)
        self.nstr.set('电机转速为\n%.0f r/min' % (self.M.n))
        self.Iastr.set('电枢电流为\n%.2f A' % (self.M.Ia))

    def sample(self) -> None:
        self.data['n'] = np.append(self.data['n'], self.M.n)
        self.data['Ia'] = np.append(self.data['Ia'], self.M.Ia)

    def plot(self) -> None:
        self.figure = Figure((6, 6))
        self.draw = self.figure.add_subplot(1, 1, 1)
        self.draw.scatter(self.data['Ia'], self.data['n'])
        self.draw.set_xlim((0, 150))
        self.draw.set_ylim((2500, 3300))
        self.draw.set_xlabel('Ia/A')
        self.draw.set_ylabel('n/(r/min)')
        self.canvas_plot = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas_plot.get_tk_widget().grid(row=0, column=4, rowspan=5)

    def fit(self) -> None:
        A = np.vstack(
            [self.data['Ia'], np.ones(len(self.data['Ia']))]
        ).T
        # n = a * Ia + b
        a, b = np.linalg.lstsq(A, self.data['n'], rcond=None)[0]
        x = np.linspace(0, 150, 151)
        self.draw.plot(x, x * a + b)
        self.draw.set_title('n = %.2f * Ia + %.2f' % (a, b))
        self.canvas_plot = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas_plot.get_tk_widget().grid(row=0, column=4, rowspan=5)

    def clear(self) -> None:
        self.data['n'] = np.array([])
        self.data['Ia'] = np.array([])
        self.plot()


if __name__ == '__main__':
    app = Ui()
