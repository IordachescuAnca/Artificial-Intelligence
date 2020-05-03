import reversi_consola
import reversi_interfata
import argparse
import sys

if __name__ == '__main__':

    if len(sys.argv) == 1:
        reversi_consola.main()
    else:
        if sys.argv[1] == '-gui':
            reversi_interfata.main()
        else:
            print("Nu exista acest program")
