__author__ = 'MR.SJ'
import zoomeye


if __name__ == "__main__":
    z =zoomeye.ZoomEye()
    z._login()
    z._search(21,1,'app,os')