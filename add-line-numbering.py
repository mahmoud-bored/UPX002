input_file = './Physio by Dr.Fawzy [Sensory].txt'
output_file = './Physio by Dr.Fawzy [Sensory] [NUMBERED].txt'

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    i = 0
    for line in f_in:
        i = i + 1
        f_out.write("[Line %d] %s" % (i, line))
    f_in.close()
    f_out.close()