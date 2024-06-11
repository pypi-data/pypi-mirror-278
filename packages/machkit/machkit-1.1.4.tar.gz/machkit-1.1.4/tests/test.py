
import os
os.environ['HOME'] = os.path.abspath(".")
os.environ["DATAPP_KIT_DEBUG"] = 'off'

if __name__ == "__main__":
    from machkit.machkit import Datapp
    datapp = Datapp()
    res,data = datapp.login('17600206307', 'tf123456')
    print(res,data)
    res, d = datapp.get_batch(1920086)
    print(res, d)