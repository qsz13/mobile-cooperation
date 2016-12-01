
import numpy as np
input_dir="output_everyday/"
output_dir = "output_average/"
node=1000
iteration=6000
landmark = range(1,6)
repeat_times = 5

for lm in landmark:
    for enhancement in np.arange(35.0,116.0,10.0):
        input_data = []
        for repeat in range(repeat_times):
            input_filename = input_dir+"Cooperation_Rate_%iNode_%iLmk_%iiter_enhance%.1f_repeat_%i.txt" \
            %(node,lm, iteration, enhancement,repeat)
            f = open(input_filename,"r")
            input_data.append([float(line.strip()) for line in f])
            f.close()
        result = []
        for i in range(iteration):
            s = 0.0
            for repeat in range(repeat_times):
                s+=input_data[repeat][i]
            result.append(s/repeat_times)
        outfile = output_dir+"Cooperation_Rate_%iNode_%iLmk_%iiter_enhance%.1f_avg.txt" \
            %(node,lm, iteration, enhancement)
        f = open(outfile,"w")
        for i in result:
            f.write("%f\n" % i)
        f.close()
