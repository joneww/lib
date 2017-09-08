#!/usr/bin/env python
import numpy
import string
import os

#########################################################################
#file name:train_dataset.py
#file description:this file define a train dataset class,aimed to record
#dataset information of each train
#struct:train_dataset_A.csv:slide_name  patch_num(each group)
#author:joneww
#start date:20170907
#########################################################################


#########################################################################
#class name:train_dataset
#class description:this class is aimed for record train dataset information
#date:20170908
#########################################################################
class train_dataset(object):
    # func description:init record file name and path
    def __init__(self, base_path, project_name, train_name):
        self.path = os.path.join(base_path, project_name)
        self.file = os.path.join(self.path, train_name + ".csv")
        if(not os.path.exists(self.path)):
            os.makedirs(self.path)
            print("%s is not exists, and creat it"%self.path)
        self.slide_info = []
        self.patch_info = []


    # func description:add slide and patch info
    def record_slide_info(self, slide_name, patch_stat):
        self.slide_info.append(slide_name)
        self.patch_info.append(patch_stat)


    # func description:write record into file
    def write_record(self):
        with open(self.file, 'a+') as opf:
            for i in range(0, len(self.slide_info)):
                csv_data = '%5s' % (self.slide_info[i])
                for j in range(0, len(self.patch_info[0])):
                    csv_data = csv_data + ',' + '%5s' % (self.patch_info[i][j])
                opf.write(csv_data + '\n')
            opf.close()


# if __name__ == "__main__":
#     tct_train_dataset_A = train_dataset("./", "tct", "train_dataset_A")
#     for i in range(4):
#         slide_name = "%d.kfb"%i
#         patch_stat = [123,0,567,0]
#         tct_train_dataset_A.record_slide_info(slide_name, patch_stat)
#     tct_train_dataset_A.write_record()

