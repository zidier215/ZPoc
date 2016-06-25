__author__ = 'MR.SJ'
import zoomeye


if __name__ == "__main__":
    z =zoomeye.ZoomEye("ghost@163.com","ghost")
    z._login()
    z._search(21,1,'app,os')