import py_dss_interface
from config.general import dss_file, opendss_path

dss = py_dss_interface.DSSDLL(opendss_path)
dss.text('compile [{}]'.format(dss_file))
