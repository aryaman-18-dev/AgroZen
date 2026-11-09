from PIL import Image
p=r'C:\Users\KIIT0001\AppData\Local\Temp\codex-clipboard-45522556-5729-4098-b676-0eabc2555f69.png'
im=Image.open(p)
im.crop((1140,28,1637,402)).save('tmp\leaf_from_user_screenshot.png')
