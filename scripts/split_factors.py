import sys

file_in = sys.argv[1]
text_out=file_in + ".txt"
factor1_out=file_in + ".factor1"
factor2_out=file_in + ".factor2"



with open(file_in, "r") as f, open(text_out, "w") as t_out, open(factor1_out, "w") as f1_out, open(factor2_out, "w") as f2_out:
    for line in f.readlines():
        words = line.rstrip().split(' ')
        for w in words:
            try:
                (text, factor1, factor2) = w.split('|')
                # print(f"{text} ",end="")
                t_out.write(f"{text} ")
                # print(f"{text} ",end="")
                f1_out.write(f"{factor1} ")
                f2_out.write(f"{factor2} ")
                #print(f"{text} ",end="")
            except:
                print(w)
        t_out.write("\n")
        f1_out.write("\n")
        f2_out.write("\n")
        #print()
