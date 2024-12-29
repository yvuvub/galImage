from PIL import Image
import sys
import csv
import os

def csv_to_array(csvPath : str):
    array : list[list[int]]
    try:
        with open(csvPath,'r',encoding="utf8") as f:
            content = csv.reader(f)
            array = [row for row in content]
    except:
        with open(csvPath,'r',encoding="shiftjis") as f:
            content = csv.reader(f)
            array = [row for row in content]
    return array

def combine(imageDes : Image.Image,imageSrc : Image.Image) -> Image.Image:

    imageDes = imageDes.convert("RGBA")
    imageSrc = imageSrc.convert("RGBA")

    if imageDes.size != imageSrc.size:
        raise ValueError("unmatched size")
    
    imageDes.alpha_composite(imageSrc)
    return imageDes


args = sys.argv
if len(args) == 1:
    print("usage : please enter evimage path")
    sys.exit(1)
if len(args) == 2:
    root_dir = args[1]
    output_dir = os.path.join(root_dir,"output") 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
if len(args) == 3:
    root_dir = args[1]
    output_dir = args[2]

csv_flag = False
for root,_,files in os.walk(root_dir):
    if csv_flag == False:
        print("try to find evdiff.csv...")
    for file in files:
        if file == "evdiff.csv":
           print("get evdiff.csv")
           csv_flag = True
           csv_path = os.path.join(root,file)
           map = csv_to_array(csv_path)

if csv_flag == False:
    print("cannot find evdiff.csv")
    sys.exit(1)


for index in range(len(map)):
    if not len(map[index]) == 7:
        print(f"file {file},line {index},cannot create an image")
        continue
    line = map[index]
    outName = line[0]
    srcName = line[1]
    srcDiffName = line[2]
    diffTop = int(line[3])
    diffLeft = int(line[4])
    diffWidth = int(line[5])
    diffHeight = int(line[6])
    print(f"try combine {outName}") 
    try:
        srcImage = Image.open(os.path.join(root_dir,srcName + ".png"))
    except Exception as e:
        print(f"file {file},line {index},cannot open {srcName}.only support png files.\nerror: {e}")
        continue
    try:
        diffImage = Image.open(os.path.join(root_dir,"diff",srcDiffName + ".png"))
    except Exception as e:
        print(f"file {file},line {index},cannot open{srcDiffName}.only support png files.\nerror: {e}")
        continue 
    srcImage = srcImage.convert("RGBA")
    diffImage = diffImage.convert("RGBA")

    blankLayer = Image.new("RGBA",(srcImage.width,srcImage.height),(0,0,0,0)) #创建一个空白图层用于合成
    diffImage = diffImage.resize((diffWidth,diffHeight))        
    blankLayer.paste(diffImage,(diffTop,diffLeft))
    srcImage.alpha_composite(blankLayer)
    srcImage.save(os.path.join(output_dir,outName + ".png"))

    
print("done")
