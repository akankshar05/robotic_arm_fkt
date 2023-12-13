# robotic_arm

1. clone this : git clone https://github.com/WongKinYiu/yolov7.git
2. replace these files : detect.py , utils/datasets.py , utils/plots.py present in yolov7 folder by the files present in the folder yolo_files
3. pip install -r requirements.txt
4. add best.pt in yolov7 folder
5. use this to run: python3 ./detect.py --weights 'best.pt' --device 'cpu' --save-txt --view-img --source 0
6. search for - GET CENTER FROM HERE in detect.py to get the centers of the packages.
