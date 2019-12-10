from tkinter import Tk, messagebox, Canvas, ALL
import random
import socket
import sys
from Tetris import Tetris


class Client(Tk):
    def __init__(self, *args, **kw):
        super().__init__()
        self.title("Tetris")
        self.configure(background='white')
        self.geometry("320x480")
        self.resizable(0, 0)
        self.cv = Canvas(self, bg='white')
        self.cv.pack(fill='both', expand='yes')

        self.net = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = int(args[0])
        self.server = '127.0.0.1'

        self.bind(sequence='<Left>', func=self.key_event)
        self.bind(sequence='<Right>', func=self.key_event)
        self.bind(sequence='<Up>', func=self.key_event)
        self.bind(sequence='<Down>', func=self.key_event)

        self.b_width = 20
        self.l_shift = 15
        self.t_shift = 20
        self.l_margin = 15
        self.tt_margin = 20
        self.sp_limit = 30

        self.net.sendto(b'Pending', (self.server, self.port))
        print("Pending...")
        res = self.net.recv(1024)
        if res == b'Start':
            print("Start!")
        self.net.setblocking(False)

        self.tetris = Tetris()
        self.fc = 0
        self.score = 0

        self.tetris.drop(False)
        self.refresh()

        self.mainloop()

    def refresh(self):
        self.after(10, self.refresh)
        self.cv.delete(ALL)

        for x in range(10):
            for y in range(20):
                fill = 'white'
                if self.tetris.map[x][y] == 1:
                    fill = 'black'
                self.cv.create_rectangle(
                    x * self.b_width + self.l_shift,
                    y * self.b_width + self.t_shift,
                    (x + 1) * self.b_width + self.l_shift,
                    (y + 1) * self.b_width + self.t_shift,
                    fill=fill
                )
        for x in range(4):
            for y in range(4):
                fill = 'white'
                if self.tetris.next.mat[y][x] == 1:
                    fill = 'black'
                self.cv.create_rectangle(
                    (x + 10) * self.b_width + self.l_shift + self.l_margin,
                    y * self.b_width + self.t_shift,
                    (x + 11) * self.b_width + self.l_shift + self.l_margin,
                    (y + 1) * self.b_width + self.t_shift,
                    fill=fill
                )

        self.cv.create_text(
            10 * self.b_width + self.l_shift + self.l_margin * 2,
            4 * self.b_width + self.t_shift + self.tt_margin,
            text=str(self.tetris.next.bottom()) + ' ' + str(self.tetris.next.left()) + ' ' + str(
                self.tetris.next.right())
        )

        self.cv.create_text(
            10 * self.b_width + self.l_shift + self.l_margin * 2,
            4 * self.b_width + self.t_shift + self.tt_margin * 2,
            text=str(self.tetris.get_score())
        )

        self.fc += 1
        datarecv = None
        if self.tetris.get_over():
            self.net.sendto(
                b'Over',
                (self.server, self.port))
            print("You lose.")
            exit(0)
            messagebox.showinfo(
                title="Tetris",
                message="You lose."
            )
        try:
            datarecv = self.net.recv(1024)
        except Exception as _:
            pass
        if datarecv is not None:
            if datarecv == b'Over':
                print("You win.")
                exit(0)
                messagebox.showinfo(
                    title='Tetris',
                    message='You win.')
            for _ in range(int(datarecv[5:])):
                self.tetris.add()
        if self.tetris.get_score() > self.score:
            self.net.sendto(
                b'Score' + str.encode(str(self.tetris.get_score()-self.score)),
                (self.server, self.port))
            self.score = self.tetris.get_score()
        if self.fc >= self.sp_limit:
            self.tetris.drop(False)
            self.fc = 0
            if self.sp_limit > 15:
                self.sp_limit -= int(random.choice("012"))
            else:
                self.sp_limit += int(random.choice("0123"))

    def key_event(self, key):
        self.tetris.move(key.keysym)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python Client.py [port]")
        exit(0)
    main = Client(int(sys.argv[1]))
