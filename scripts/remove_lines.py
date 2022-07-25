#script to remove empty lines in source and target

sourcefile = open('dev.es', 'r').readlines()
targetfile = open('test.txt', 'r').readlines()
source_new = open('dev_out.es', 'w')
target_new = open('test_out.txt', 'w')

zipped = zip(sourcefile, targetfile) #pairs of source and target

#if either source or target is empty
#delete the empty lines in both pairs
#so that the sentence alignments are preserved
zippedFiltered = [(source,target) for source, target in zipped if not source.isspace()]
zippedFiltered = [(source,target) for source, target in zippedFiltered if not target.isspace()]
sourceFiltered, targetFiltered = zip(*zippedFiltered)

#write in new file
for i in sourceFiltered:
    source_new.write(i)
for i in targetFiltered:
    target_new.write(i)