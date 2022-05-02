from function import *
import os

input_template = './inputs/input_'
output_template = './outputs/output_'
extension = '.txt'

i = 1
while os.path.exists(input_template + str(i) + extension):
        pl_res = PL_RESOLUTION()
        pl_res.read_file(input_template + str(i) + extension)
        pl_res.pl_resolution()
        pl_res.write_file(output_template + str(i) + extension)
        i += 1

