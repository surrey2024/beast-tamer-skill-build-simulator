import sys, os
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QSizePolicy, QWidget, QPushButton, QSpinBox, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QApplication, QFileDialog)
from PyQt5.QtCore import  QObject, QSize, QPoint
import numpy as np
import cv2

class MyLabel(QWidget):
    def __init__(self, label, n, box) -> None:
        super().__init__()
        self.label = label
        self.label.leaveEvent = self.leave
        self.label.enterEvent = self.enter
        self.label.mouseMoveEvent = self.draw_box
        self.skill_box = box # 技能說明，隨著滑鼠移動
        self.act = 0 # 用來知道目前等級
        self.havepassive = False # 用來有沒有被動技能增加，如果有，是被動技能的說明框會變紅色背景
        self.max = False
        self.n = n
        self.windowSize = (0, 0)
        self.passive = [1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,1,0,0,
                        1,0,1,1,1,0,0,0,1,1,1,0,1,1,1,1,0,0,
                        1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,0,1,0,
                        1,1,1,1,1,1,0,1,0,0,0,1,1,0,0,1,1,0]

    def leave(self, event):
        self.skill_box.setVisible(False)
        print("Mouse is leaving the label", self.n)
    
    def enter(self, event):
        self.skill_box.setVisible(True)
        print("Mouse is over the label", self.n)

    def draw_box(self, event):
        # print('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
        skill_cur, line = self.skillStr(self.act)
        if not self.max:
            skill_next, line = self.skillStr(self.act+1)
        if self.act > 0:
            if self.max: # 滿等
                self.skill_box.setText(" [現在等級 {}]\n{}".format(self.act, skill_cur))
                self.skill_box.resize(250,35+15*line)
            else:
                self.skill_box.setText(" [現在等級 {}]\n{}\n------------------------------------------------------------\n[下次等級: {}]\n{}". 
                    format(self.act, skill_cur, self.act+1, skill_next))
                self.skill_box.resize(250,60+30*line)
        else:  # 等級0
            self.skill_box.setText(" [下次等級: {}]\n{}".format(self.act+1, skill_next))
            self.skill_box.resize(250,35+15*line)

        move_x = self.label.geometry().topLeft().x() + event.x() + 5
        move_y = self.label.geometry().topLeft().y() + event.y() + 15
        if move_x + self.skill_box.width() > self.windowSize[0]:
            move_x = self.windowSize[0] - self.skill_box.width()
        if move_y + self.skill_box.height() > self.windowSize[1]:
            move_y = self.windowSize[1] - self.skill_box.height()
        self.skill_box.move(QPoint(move_x, move_y))
        if self.passive[self.n] and self.havepassive:
            self.skill_box.setStyleSheet("QLabel"
                                        "{"
                                        "color : white;"
                                        "border: 1px solid white;"
                                        "background-color : rgba(180,0,0,70%)"
                                        "}")
        else:
            self.skill_box.setStyleSheet("QLabel"
                                        "{"
                                        "color : white;"
                                        "border: 1px solid white;"
                                        "background-color : rgba(0,0,0,70%)"
                                        "}")
        
    def skillStr(self, level):
        # 熊 ################################################################
        if self.n == 0:
            return f"使用{360+3*level}%的傷害攻擊1次", 1
        elif self.n == 1:
            return f"{9+(level-1)//3}秒內，造成{150+3*level}%的傷害", 1
        elif self.n == 2:
            return f"增加最大HP{((level+1)//2)*10}%、智力{level*5}", 1
        elif self.n == 3:
            return f"格檔機率提升{25+7*level}%、防禦力增加{80+12*level}、被擊傷害減少{10+2*level}%", 2
        elif self.n == 4:
            return f"以{400+5*level}%的傷害進行攻擊", 1
        elif self.n == 5:
            return f"以{175+5*level}%的傷害，攻擊3次", 1
        elif self.n == 6:
            return f"增加無視防禦{2*level}%、攻速{level//10+1}個階段", 1
        elif self.n == 7:
            return f"以{200+10*level}%的傷害，攻擊4次\n波波揮擊技能傷害額外增加{50+2*level}%", 2
        elif self.n == 8:
            return f"增加爆擊機率{15+3*level}%、爆擊傷害{10+2*level}%、魔力{level}", 1
        elif self.n == 9:
            return f"以{550+6*level}%的傷害進行攻擊", 1
        elif self.n == 10:
            return f"召喚以{370+7*level}%的傷害攻擊4次的小波波", 1
        elif self.n == 11:
            return f"魔力增加{(level-1)//2+1}%", 1
        elif self.n == 12:
            return f"主動效果:傷害+{15+level}%、爆擊傷害+{(level-1)//2+1}%、最終傷害+{level}%\n被動效果:MaxHP+{level}%、MaxMP+{level}%、防禦力+{5*level}%、無視防禦+{level}%", 4
        elif self.n == 13:
            return f"以{230+4*level}%的傷害攻擊5次，持續{5+level//6*2}秒，冷卻30秒", 1
        elif self.n == 14:
            return f"發動後進行復活，之後無敵時間{5+level//2}秒。冷卻時間{2300-50*level}秒", 2
        elif self.n == 15:
            return f"魔力增加{2*level}，煙霧放屁的傷害增加{80+4*level}%", 1
        elif self.n == 16:
            return f"以{360+20*level}%的傷害進行10次攻擊", 1
        elif self.n == 17:
            return f"以{360+20*level}%的傷害進行10次攻擊", 1 
        # 豹 ################################################################
        elif self.n == 18:
            return f"以{140+3*level}%的傷害進行攻擊2次", 1
        elif self.n == 19:
            return f"以{200+3*level}%的傷害進行2次攻擊，冷卻時間{8-level//2}秒", 1
        elif self.n == 20:
            return f"透過{10+2*level}%的機率，恢復殺傷力{level//2+1}%的HP", 1
        elif self.n == 21:
            return f"以{180+5*level}%的傷害進行攻擊4次", 1
        elif self.n == 22:
            return f"增加魔力{20+level}、智力{20+level}、移動速度{5+2*level}、彈跳力{level//3+1}", 1
        elif self.n == 23:
            return f"以{160+4*level}%的傷害進行3次攻擊", 1
        elif self.n == 24:
            return f"以{200+5*level}%的傷害進行3次攻擊", 1
        elif self.n == 25:
            return f"技能持續{90+6*level}秒，以{15+level}%的機率召喚{10+2*level}秒內以傷害{150+10*level}%攻擊4次的小豹", 2
        elif self.n == 26:
            return f"以{300+10*level}%的傷害進行4次攻擊\n增加萊伊痛擊與萊伊衝擊的傷害{(level+1)//2+10}%，以及對象目標增加{1+level//10}位，攻擊一般怪物傷害增加{10+level}%", 3
        elif self.n == 27:
            return f"以{100+4*level}%的傷害進行攻擊，效果持續{2+(level-1)//5}秒", 1
        elif self.n == 28:
            return f"以{650+10*level}%的傷害進行攻擊，並以{20+4*level}%的機率產生暈眩效果\n紳士之舞與紳士的步伐的所攻擊的怪物增加{1+level//10}名，傷害增加{(level+1)//2+10}%", 4
        elif self.n == 29:
            return f"以{315+15*level}%的傷害進行4次攻擊，冷卻時間{12-level//2}秒", 1
        elif self.n == 30:
            return f"以{300+5*level}%的傷害進行攻擊{2+level//10}次，冷卻時間{5-level//6}秒", 1
        elif self.n == 31:
            return f"魔力提升{2*level}、最終傷害提升{5+level}%", 1
        elif self.n == 32:
            return f"萊伊痛擊、萊伊衝擊、咆哮、紳士之舞、紳士的步伐、萊伊的尾巴的傷害增加{20+2*level}%，對象目標增加{2+(level-1)//7}，無視防禦增加{2*level}%，攻擊一般怪物傷害增加{10+level}%", 4
        elif self.n == 33:
            return f"增加攻速{level//10+1}個階段、魔力{level//2+1}%、無視防禦{6*level}%", 2
        elif self.n == 34:
            return f"以{500+15*level}%的傷害進行8次攻擊，冷卻時間{25-level}秒", 1
        elif self.n == 35:
            return f"以{500+15*level}%的傷害進行8次攻擊，冷卻時間{25-level}秒", 1
        # 鳥 ################################################################
        elif self.n == 36:
            return f"以{80+3*level}%的傷害進行1次攻擊，擊中敵人時艾卡飛行技能冷卻時間減少0.5秒", 2
        elif self.n == 37:
            return f"消耗MP{20-level}，跳躍狀態中使用時可以朝前方再跳躍兩次", 2
        elif self.n == 38:
            return f"{650+100*level}超高跳躍", 1
        elif self.n == 39:
            return f"傳送點持續{20*level}秒，冷卻時間{400-20*level}秒\n[被動效果:爆擊傷害增加{level}%]", 2
        elif self.n == 40:
            return f"使用後持續飛行{10+level//3*2}秒，冷卻時間60秒", 1
        elif self.n == 41:
            return f"{30+10*level}秒間，增加移動速度{2*level}、跳躍力{level}\n[被動效果:移動速度上限增加{level}]", 2
        elif self.n == 42:
            return f"增加魔力{2*level}、攻速{level//10+1}個階段、無視防禦{2*level}%", 1
        elif self.n == 43:
            return f"以{30+4*level}%的傷害進行2次攻擊", 1
        elif self.n == 44:
            return f"跳躍或飛行狀態下按住，可轉換為滑翔狀態", 1
        elif self.n == 45:
            return f"跳躍力提升{level//5+1}、爆擊機率提升{level}%", 1
        elif self.n == 46:
            return f"召喚隊員，冷卻{3600-300*level}秒\n[被動效果:無視防禦力增加{2*level}%]", 2
        elif self.n == 47:
            return f"{30+10*level}秒間，魔力增加{4*level}\n[被動效果:攻擊時有{25+5*level}%的機率，產生每秒{190+10*level}%傷害維持{1+level//3}秒的出血效果]", 3
        elif self.n == 48:
            return f"以{225+10*level}%的傷害攻擊4次，冷卻時間{18-level//10*5}秒", 1
        elif self.n == 49:
            return f"{30*level}秒間，爆擊機率提升{level}%、防禦力提升{150+50*level}", 1
        elif self.n == 50:
            return f"隊伍攻擊、隊伍掩護、隊伍轟炸技能的傷害增加{60+3*level}%、隊伍攻擊技能攻擊次數提升{level//10}段", 2
        elif self.n == 51:
            return f"{90+6*level}秒內，物理和魔法攻擊力各增加{2*level}/{2*level}", 1
        elif self.n == 52:
            return f"移動速度增加{3*level}、爆擊傷害提升{level}%", 1
        elif self.n == 53:
            return f"以{500+30*level}%的傷害進行攻擊，冷卻時間{30-level//2}秒", 1
        # 貓 ################################################################
        elif self.n == 54:
            return f"以{150+5*level}%的傷害攻擊4次，攻擊第四次時最終攻擊以{300+10*level}%的傷害攻擊4次", 2
        elif self.n == 55:
            return f"被動效果:智力增加{10*level}", 1
        elif self.n == 56:
            return f"被動效果:攻擊力/魔力增加{20+level}", 1
        elif self.n == 57:
            return f"被動效果:最大HP增加{250+25*level}/最大MP增加{250+25*level}", 1
        elif self.n == 58:
            return f"被動效果:增加格檔機率{20+level}%，每4秒追加恢復HP{10*level}、MP{10*level}", 2
        elif self.n == 59:
            return f"被動效果:隊員的道具獲得機率增加{10+level//2}%", 1
        elif self.n == 60:
            return f"讓6名玩家恢復{10+level//2}%的HP", 1
        elif self.n == 61:
            return f"被動效果:增加爆擊機率{10+level}%、爆擊傷害{(level+1)//2}%", 1
        elif self.n == 62:
            return f"以{10*level}的機率來讓魔法無效化與治療狀態異常，冷卻時間5秒", 2
        elif self.n == 63:
            return f"給予範圍內的所有怪物{550+30*level}%的傷害，恢復夥伴們{250+20*level}HP，持續時間{15+level//2}秒，冷卻時間15秒", 2
        elif self.n == 64:
            return f"紅卡:傷害增加{20+level}%\n藍卡:防禦力增加{100+5*level}、最大HP/MP增加{5+level}%\n綠卡:攻擊速度增加{1+level//20}、移動速度增加{level}\n卡片持續時間{60+6*level}秒，冷卻時間{40-level//2}秒", 4
        elif self.n == 65:
            return f"增加朋友發射技能傷害{40+4*level}%", 1
        elif self.n == 66:
            return f"被動效果:防禦力/魔王防禦力無視{level}%", 1
        elif self.n == 67:
            return f"以{400+20*level}%的傷害進行攻擊3次，並使敵人防禦力減少{2*level}%，冷卻時間3秒", 2
        elif self.n == 68:
            return f"幫助範圍內的隊員復活，冷卻時間{1200-30*level}秒", 1
        elif self.n == 69:
            return f"被動效果:抽到阿樂卡牌的機率+{25+level*5}% 冷卻時間{40-level//2}秒", 2
        elif self.n == 70:
            return f"被動效果:隊員經驗值的獲得量增加{10+level}%", 1
        elif self.n == 71:
            return f"10秒間維持貓咪翻花繩，翻花繩內的敵人以一定間距用{700+30*level}%傷害攻擊1次，被翻花繩攻擊的敵人在20秒內受到的最終傷害提升{10+level}%", 3
        else:
            return None, 0

class Copyright(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        all = QHBoxLayout()
        text = QLabel()
        text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        text.setText("耳朵跟尾巴感謝繪師及月月提供，僅供此程式使用。其餘使用之圖片皆為原遊戲(新楓之谷)創作者、代理商所有，若有任何不當使用請來信告知，各位遊戲創作者及代理商辛苦了。\n\n聯絡信箱: 8937danny@gmail.com")
        text.setWordWrap(True)
        all.addWidget(text)
        self.setLayout(all)
        self.setGeometry(100, 90, 300, 120)
        self.setWindowTitle('版權聲明')

class Blow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.mylabels = []
        self.passive = [0,0,1,1,0,0,1,0,1,0,0,1,2,0,1,0,0,0,
                        0,0,0,0,1,0,0,2,0,0,0,0,0,1,0,1,0,0,
                        0,0,0,1,0,2,1,0,0,1,1,2,0,2,0,2,1,0,
                        0,1,1,1,1,1,0,1,0,0,0,0,1,0,0,0,1,0]
        self.skill_name = {0:["波波揮擊", "煙霧放屁", "波波的糧食儲存", "波波的耐心", "吸入", "波波的追擊", "波波的堅強",
                    "憤怒亂打", "波波的致命打擊", "強大的吸入", "小波波", "波波的勇猛", "集中打擊", "鮮魚龍捲風",
                    "波波的重生", "火焰臭屁彈", "打翻飯桌", ""],
                      1:["萊伊痛擊", "萊伊的尾巴", "萊伊的皮強化", "萊伊衝擊", "萊伊的筋力強化", "紳士之舞", "紳士的步伐",
                    "小豹呼喚", "咆哮", "雷火之地", "撼動震擊", "電光石火", "萊伊的尾巴強化", "萊伊的牙齒強化",
                    "萊伊的指甲強化", "萊伊的精神強化", "X怒吼", ""],
                      2:["隊伍攻擊", "艾卡飛躍", "艾卡跳躍", "設置艾卡碼頭", "艾卡飛行", "艾卡翅膀強化", "艾卡的敏捷身姿",
                    "隊伍掩護", "艾卡滑翔", "艾卡的羽毛披風", "帶朋友來", "艾卡腳趾強化", "隊伍轟炸", "艾卡眼睛強化",
                    "隊伍強化", "艾卡嘴強化", "艾卡的羽毛鞋", "旋風飛行"],
                      3:["朋友發射", "阿樂好可愛", "強化阿樂的魅力", "阿樂的飽足感", "阿樂的意志", "阿樂的竊取", "阿樂療癒",
                    "阿樂的指甲", "阿樂淨化", "阿樂區域", "阿樂卡牌", "朋友發射強化", "阿樂的弱點探索", "阿樂投擲",
                    "貓咪復活", "黃金卡牌", "阿樂的朋友們", "進擊!翻花繩"]}

    def update_(self):
        all = QHBoxLayout()
        container = []
        mode = []
        count_list = []
        count_max = 0
        
        for i in range(4):
            count = 0
            container.append(QWidget())
            mode.append(QVBoxLayout(container[i]))
            for j in range(18):
                if self.passive[i*18+j] and self.mylabels[i*18+j].act > 0:
                    count += 1
                    skill = QHBoxLayout()
                    img = QLabel()
                    img_path = './skill_img/{}.jpg'.format(i*18+j)
                    if os.path.isfile(img_path):
                        pixmap = QPixmap(img_path)
                    else:
                        pixmap = QPixmap("")
                    img.setPixmap(pixmap)
                    skill.addWidget(img)
                    lv = self.mylabels[i*18+j].act if not self.mylabels[i*18+j].max else "最大"
                    if self.passive[i*18+j] == 2:
                        skill.addWidget(QLabel(f"{self.skill_name[i][j]} [等級：{lv}]\n(需在吹哨子期間施放該技能)"))
                    else:
                        skill.addWidget(QLabel(self.skill_name[i][j]+f" [等級：{lv}]"))
                    skill.setStretch(0,1)
                    skill.setStretch(1,100)
                    mode[i].addLayout(skill)
                    text = QLabel()
                    text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
                    skill_str = self.mylabels[i*18+j].skillStr(self.mylabels[i*18+j].act)[0]
                    if j == 11 and i == 2:
                        text.setText(skill_str.split()[0])
                    else:
                        text.setText(skill_str)
                    text.setWordWrap(True)
                    text.resize(200,50)
                    mode[i].addWidget(text)

            if count == 0:
                d = {0:"熊", 1:"豹", 2:"鳥", 3:"貓"}
                text = QLabel("無法從{}模式獲得效果".format(d[i]))
                text.setStyleSheet("QLabel"
                    "{"
                    "color : red;"
                    "}")
                
                mode[i].addWidget(text)
                count = 1

            if count > count_max:
                count_max = count

            count_list.append(count)

        for i in range(4):
            for _ in range(count_max - count_list[i]):
                space1 = QLabel(" ")
                space2 = QLabel(" ")
                space3 = QLabel(" ")
                mode[i].addWidget(space1)
                mode[i].addWidget(space2)
                mode[i].addWidget(space3)

        color = {0:"rgba(255,180,180,100%)", 1:"rgba(190,230,255,100%)", 2:"rgba(225,190,255,100%)", 3:"rgba(255,195,160,100%)"}
        for i in range(4):
            container[i].setStyleSheet(f"background-color:{color[i]};")
            all.addWidget(container[i])
            all.setStretch(i, 1)

        self.setLayout(all)
        self.setGeometry(100, 90, 1000, 100*count_max)
        self.setWindowTitle('全集中守護效果')

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.labels = []
        self.spinbox = []
        self.skill_limit = [20,20,10,10,10,20,15,25,15,20,15,20,20,25,10,15,10,0,
                            20,10,15,20,15,20,20,15,20,15,20,20,20,15,15,10,10,0,
                            10,5,10,10,30,15,15,30,1,15,10,15,30,15,30,15,15,10,
                            10,10,15,15,10,20,20,20,10,15,20,15,20,20,15,15,20,10]
        self.skill_need = [0,7,15,24,39,47,62,73,93,105,120,130,140,155,175,183,190,0,
                           0,9,18,27,39,48,60,72,87,96,107,116,123,129,138,149,190,0,
                           0,0,8,14,20,27,40,50,70,71,81,82,103,126,137,145,150,170,
                           0,0,8,15,27,39,51,60,70,83,95,104,113,125,137,147,160,170]
        self.passive = [1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,1,0,0,
                        1,0,1,1,1,0,0,0,1,1,1,0,1,1,1,1,0,0,
                        1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,0,1,0,
                        1,1,1,1,1,1,0,1,0,0,0,1,1,0,0,1,1,0]
        self.point_label = []
        self.used_point = [0,0,0,0]
        self.total_point = [0,0,0,0]
        self.combo1 = QComboBox()
        self.combo2 = QComboBox()
        self.clear = QComboBox()
        self.remain_point = QLabel("剩餘點數: 593")
        # self.setMouseTracking(True)
        self.initUI()
        self.update_(0)
        self.setMouseTracking(True)

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                if isinstance(child, QSpinBox):
                    continue
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)
        QWidget.setMouseTracking(self, flag)
        recursive_set(self)
        

    def initUI(self):
        skill_name = {0:["波波揮擊", "煙霧放屁", "波波的糧食儲存", "波波的耐心", "吸入", "波波的追擊", "波波的堅強",
                    "憤怒亂打", "波波的致命打擊", "強大的吸入", "小波波", "波波的勇猛", "集中打擊", "鮮魚龍捲風",
                    "波波的重生", "火焰臭屁彈", "打翻飯桌", ""],
                      1:["萊伊痛擊", "萊伊的尾巴", "萊伊的皮強化", "萊伊衝擊", "萊伊的筋力強化", "紳士之舞", "紳士的步伐",
                    "小豹呼喚", "咆哮", "雷火之地", "撼動震擊", "電光石火", "萊伊的尾巴強化", "萊伊的牙齒強化",
                    "萊伊的指甲強化", "萊伊的精神強化", "X怒吼", ""],
                      2:["隊伍攻擊", "艾卡飛躍", "艾卡跳躍", "設置艾卡碼頭", "艾卡飛行", "艾卡翅膀強化", "艾卡的敏捷身姿",
                    "隊伍掩護", "艾卡滑翔", "艾卡的羽毛披風", "帶朋友來", "艾卡腳趾強化", "隊伍轟炸", "艾卡眼睛強化",
                    "隊伍強化", "艾卡嘴強化", "艾卡的羽毛鞋", "旋風飛行"],
                      3:["朋友發射", "阿樂好可愛", "強化阿樂的魅力", "阿樂的飽足感", "阿樂的意志", "阿樂的竊取", "阿樂療癒",
                    "阿樂的指甲", "阿樂淨化", "阿樂區域", "阿樂卡牌", "朋友發射強化", "阿樂的弱點探索", "阿樂投擲",
                    "貓咪復活", "黃金卡牌", "阿樂的朋友們", "進擊!翻花繩"]}
        box = []
        points = []
        img = []

        for i in range(4):
            self.point_label.append(QLabel("花費點數: 0，實際點數: 0"))
            points.append([])
            box.append(QVBoxLayout())
            for j in range(18):
                skill = QHBoxLayout()
                img.append(QLabel())
                img_path = './skill_img/{}.jpg'.format(i*18+j)
                if os.path.isfile(img_path):
                    pixmap = QPixmap(img_path)
                else:
                    pixmap = QPixmap("")
                img[i*18+j].setPixmap(pixmap)
                skill.addWidget(img[i*18+j])
                content = QVBoxLayout()
                if i == 0 and j == 11:
                    self.bobo_b = QLabel(skill_name[i][j])
                    content.addWidget(self.bobo_b)
                else:
                    content.addWidget(QLabel(skill_name[i][j]))

                points[i].append(QHBoxLayout())
                points[i][j].addWidget(QLabel("(需要: {})".format(self.skill_need[i*18+j])))
                
                self.spinbox.append(QSpinBox())
                self.spinbox[i*18+j].setRange(0, self.skill_limit[i*18+j])
                self.spinbox[i*18+j].setWrapping(True)
                if j == 0 or (j == 1 and i >= 2):
                    self.spinbox[i*18+j].setDisabled(False)
                else: 
                    self.spinbox[i*18+j].setDisabled(True)
                self.spinbox[i*18+j].valueChanged.connect(self.update_)
                points[i][j].addWidget(self.spinbox[i*18+j])

                self.labels.append(QLabel("0 / {}".format(self.skill_limit[i*18+j])))
                points[i][j].addWidget(self.labels[i*18+j])
                
                points[i][j].setStretch(0, 3)
                points[i][j].setStretch(1, 3)
                points[i][j].setStretch(2, 2)
                if i < 2 and j == 17:
                    continue # 不加layout
                content.addLayout(points[i][j])
                skill.addLayout(content)
                box[i].addLayout(skill)
            box[i].addWidget(self.point_label[i])
        
        # 第一行
        self.head = QHBoxLayout()

        self.copyright_button = QPushButton('版權聲明')
        self.copyright_button.clicked.connect(self.handleCopyright)
        self.head.addWidget(self.copyright_button)

        for i in range(13):
            self.combo1.addItem("所有技能等級加 {}".format(i))
        self.combo1.currentTextChanged.connect(self.update_)
        for i in range(7):
            self.combo2.addItem("被動技能等級加 {}".format(i))
        self.combo1.currentTextChanged.connect(self.update_)
        self.combo2.currentTextChanged.connect(self.update_)
        self.head.addWidget(self.combo1)
        self.head.addWidget(self.combo2)
        # self.head.addStretch(1)

        self.blow_button = QPushButton('', self)
        self.blow_button.clicked.connect(self.handleBlow)
        self.blow_button.setIcon(QIcon('./skill_img/blow.jpg'))
        self.blow_button.setFixedWidth(40)
        self.blow_button.setFixedHeight(40)
        self.blow_button.setIconSize(QSize(50,50))
        self.head.addWidget(self.blow_button)
        self.head.addWidget(QLabel("查看全集中守護效果"))

        self.head.addStretch(1)
        self.head.addWidget(self.remain_point)
        self.clear.addItems(["","重置熊模式","重置豹模式","重置鳥模式","重置貓模式", "重置全部模式"])
        self.head.addWidget(self.clear)
        clear = QPushButton("確定重置")
        self.head.addWidget(clear)
        clear.clicked.connect(self.clear_points)
        self.head.setStretch(0, 1)
        self.head.setStretch(1, 2)
        self.head.setStretch(2, 2)
        self.head.setStretch(3, 1)
        self.head.setStretch(4, 1)

        # 中間
        self.hbox = QHBoxLayout()
        for i in range(4):
            self.hbox.addLayout(box[i])

        # 最下面
        self.button = QHBoxLayout()
        btn_name = ["儲存檔案","選擇檔案","生成圖片"]
        btn1 = QPushButton(btn_name[0])
        btn1.clicked.connect(self.save_data)
        self.button.addWidget(btn1)
        btn2 = QPushButton(btn_name[1])
        btn2.clicked.connect(self.read_data)
        self.button.addWidget(btn2)
        btn3 = QPushButton(btn_name[2])
        btn3.clicked.connect(self.gen_image)
        self.button.addWidget(btn3)
        
        widget = QWidget()
        self.setCentralWidget(widget)

        self.all = QVBoxLayout(widget)
        self.all.addLayout(self.head)
        self.all.addLayout(self.hbox)
        self.all.addLayout(self.button)

        # self.setLayout(self.all)

        self.skill_box = QLabel(widget)
        self.skill_box.setVisible(False)
        self.skill_box.setText(" ")
        self.skill_box.setStyleSheet("QLabel"
                                    "{"
                                    "color : white;"
                                    "border: 1px solid white;"
                                    "background-color : rgba(40,0,0,70%)"
                                    "}")
        self.skill_box.resize(250,50)
        self.skill_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.skill_box.setWordWrap(True)
        

        self.mylabels = []
        for i in range(72):
            self.mylabels.append(MyLabel(img[i], i, self.skill_box))

        self.setGeometry(100, 60, 1000, 940)
        self.setWindowTitle('幻獸師模擬配點 v3.1 作者:棉花糖')
        # self.show()

    def resizeEvent(self, event):
        for i in range(72):
            self.mylabels[i].windowSize = (self.geometry().width(), self.geometry().height())
        print("resize ", self.geometry().width(), self.geometry().height())
        QMainWindow.resizeEvent(self, event)

    def handleBlow(self):
        self.blow = Blow()
        self.blow.mylabels = self.mylabels
        self.blow.update_()
        self.blow.show()
        print("blow!!")

    def handleCopyright(self):
        self.w = Copyright()
        self.w.show()

    # def mouseMoveEvent(self, event):
        # print('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
    
    def update_(self, value_as_unicode):
        print('value changed:', value_as_unicode)
        add = int(str(self.combo1.currentText())[8:])
        p_add = int(str(self.combo2.currentText())[8:])
        if p_add > 0:
            self.combo2.setStyleSheet("QComboBox"
                                    "{"
                                    "color : white;"
                                    "background-color : rgba(180,0,0,70%);"
                                    "}")
            for i in range(72):
                self.mylabels[i].havepassive = True
        else:
            self.combo2.setStyleSheet("QComboBox"
                                    "{"
                                    "background-color : native;"
                                    "}")
            for i in range(72):
                self.mylabels[i].havepassive = False
                
        bobo_b = False
        for i in range(4):
            used, total = 0, 0
            pre_zero = False
            pre_red = False
            for j in range(18):
                if self.spinbox[i*18+j].value() == 0:
                    act = 0
                else:
                    act = min(self.spinbox[i*18+j].value()+add+self.passive[i*18+j]*p_add, self.skill_limit[i*18+j])
                if act == self.skill_limit[i*18+j]:
                    self.mylabels[i*18+j].max = True
                else:
                    self.mylabels[i*18+j].max = False
                self.mylabels[i*18+j].act = act

                if i == 0 and j == 11 and act == 20:
                    bobo_b = True
                
                if used >= self.skill_need[i*18+j] and (not pre_zero or i*18+j==26) and not pre_red:
                    self.spinbox[i*18+j].setDisabled(False)
                    self.spinbox[i*18+j].setStyleSheet("QSpinBox"
                                    "{"
                                    "background-color : white;"
                                    "}")
                else:
                    self.spinbox[i*18+j].setDisabled(True)
                    if self.spinbox[i*18+j].value() > 0 or pre_red:
                        self.spinbox[i*18+j].setStyleSheet("QSpinBox"
                                    "{"
                                    "background-color : pink;"
                                    "}")
                        pre_red = True
                    else:
                        self.spinbox[i*18+j].setStyleSheet("QSpinBox"
                                    "{"
                                    "background-color : native;"
                                    "}")
                used += self.spinbox[i*18+j].value()
                total += act
                
                self.labels[i*18+j].setText("{} / {}".format(act, self.skill_limit[i*18+j]))
                if i >= 2 and j == 0:
                    continue
                if self.spinbox[i*18+j].value() == 0:
                    pre_zero = True
                    if i >= 2 and j == 1:
                        if self.spinbox[i*18+j].value() + self.spinbox[i*18+j-1].value() == 0:
                            pre_zero = True
                        else:
                            pre_zero = False
                if i*18+j==26 and self.spinbox[i*18+j].value() > 0:
                    pre_zero = False


            self.used_point[i] = used
            self.total_point[i] = total
            self.point_label[i].setText("投入點數: {}，實際點數: {}".format(used, total))
        remain = 593-self.used_point[0]-self.used_point[1]-self.used_point[2]-self.used_point[3]
        if remain < 0:
            self.remain_point.setStyleSheet("QLabel"
                                    "{"
                                    "color : red;"
                                    "}")
            self.remain_point.setText("剩餘點數: {}".format(remain))
        else:
            self.remain_point.setStyleSheet("QLabel"
                                    "{"
                                    "color : native;"
                                    "}")
            self.remain_point.setText("剩餘點數: {}".format(remain))
        
        if bobo_b:
            self.bobo_b.setStyleSheet("QLabel"
                    "{"
                    "color : red;"
                    "}")
            self.bobo_b.setText("波波的勇猛(19跟20效果相同)")
        else:
            self.bobo_b.setStyleSheet("QLabel"
                    "{"
                    "color : native;"
                    "}")
            self.bobo_b.setText("波波的勇猛")
        
    def clear_points(self):
        dct = {"":-1,"重置熊模式":0,"重置豹模式":1,"重置鳥模式":2,"重置貓模式":3, "重置全部模式":4}
        a = str(self.clear.currentText())
        if a == "":
            pass
        elif a[0] == "重" and a[2] != "全":
            for j in range(18):
                self.spinbox[dct[a]*18+j].setValue(0)
        else:
            print(a)
            for j in range(18*4):
                self.spinbox[j].setValue(0)

    def save_data(self):
        try:
            fileName, filetype = QFileDialog.getSaveFileName(self,"另存新檔","./","ccdy (*.ccdy)")
            with open(fileName, "w") as f:
                f.write("{}\n".format(self.combo1.currentText()[8:]))
                for i in range(4):
                    for j in range(18):
                        f.write("{}\n".format(self.spinbox[i*18+j].value()))
                f.write("{}\n".format(self.combo2.currentText()[8:]))
        except Exception:
            pass

    def read_data(self):
        try:
            fileName, filetype = QFileDialog.getOpenFileName(self,"選擇檔案","./","ccdy (*.ccdy)")
            self.setWindowTitle(f'幻獸師模擬配點 v3.1 作者:棉花糖 讀取檔案: {fileName}')
            with open(fileName, "r") as f:
                self.combo1.setCurrentText("所有技能等級加 "+f.readline()[:-1])
                for i in range(4):
                    for j in range(18):
                        self.spinbox[i*18+j].setValue(int(f.readline()))
                self.combo2.setCurrentText("被動技能等級加 "+f.readline()[:-1])
        except Exception:
            pass

    def gen_image(self):
        try:
            fileName, filetype = QFileDialog.getSaveFileName(self,"另存新檔","./","jpg (*.jpg)")
            img = np.zeros((15 + 32 * 18 + 14, 91 * 4 + 2, 3), np.uint8)
            img.fill(255)

            cat1 = cv2.imread("./skill_img/ear.png")  
            cat2 = cv2.imread("./skill_img/tail.png")  

            img[2:20, 13:31, :] = cat1
            img[14:32, 150:168, :] = cat2

            color = {0:(80,80,155), 1:(155,130,90), 2:(125,90,155), 3:(60,95,155)}
            for i in range(4):
                up = 32 if i <= 1 else 0
                img[up:, 91*i:91*(i+1)+2, :] = color[i] 
                img[up:, 91*i:91*(i+1)+2, :] += 100

                for j in range(18):
                    if i <= 1 and j == 17:
                        continue
                    cost = self.spinbox[i*18+j].value()  # 花費點數
                    act = self.mylabels[i*18+j].act  # 實際點數
                    lcorner = i * 91 + 2
                    ucorner = 32 * j + 10 if i >= 2 else 32 * (j+1) + 10
                    if cost == 0:
                        skill_img = cv2.imread(f"./skill_img/{i*18+j}.jpg", 0) 
                        img[ucorner:ucorner+32, lcorner:lcorner+32] = np.repeat(skill_img[:, :, np.newaxis], 3, axis=2)
                    else:
                        skill_img = cv2.imread(f"./skill_img/{i*18+j}.jpg") 
                        img[ucorner:ucorner+32, lcorner:lcorner+32] = skill_img
                    
                    text = f'{cost}'
                    if cost >= 10:
                        cv2.putText(img, text, (lcorner+35, ucorner+24), cv2.FONT_HERSHEY_DUPLEX,
                                0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(img, text, (lcorner+41, ucorner+24), cv2.FONT_HERSHEY_DUPLEX,
                                0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    text = f'{act}'
                    if act >= 10:
                        cv2.putText(img, text, (lcorner+65, ucorner+24), cv2.FONT_HERSHEY_DUPLEX,
                                0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(img, text, (lcorner+71, ucorner+24), cv2.FONT_HERSHEY_DUPLEX,
                                0.5, (0, 0, 0), 1, cv2.LINE_AA)

            add = int(str(self.combo1.currentText())[8:])
            text = f"Skill Level +{add}"
            cv2.putText(img, text, (35, 12), cv2.FONT_HERSHEY_DUPLEX,
                                            0.4, (205, 55, 105), 1, cv2.LINE_AA)

            p_add = int(str(self.combo2.currentText())[8:])
            text = f"Passive Level +{p_add}"
            cv2.putText(img, text, (35, 27), cv2.FONT_HERSHEY_DUPLEX,
                                            0.4, (205, 55, 105), 1, cv2.LINE_AA)
            
            img[32*18+10:32*18+29, :91*2, :] = color[0]
            img[32*18+10:32*18+29, 91*2:, :] = color[3]
            for i in range(4):
                img[32*18+10:32*18+29, 91*i+2:91*(i+1)+2, :] = color[i]

                if i <= 1:
                    text = "before"
                    cv2.putText(img, text, (91*i+29, 39), cv2.FONT_HERSHEY_DUPLEX,
                                            0.3, (5, 5, 5), 1, cv2.LINE_AA)
                    text = "after"
                    cv2.putText(img, text, (91*i+66, 39), cv2.FONT_HERSHEY_DUPLEX,
                                            0.3, (5, 5, 5), 1, cv2.LINE_AA)
                    cv2.line(img, (91*i+63, 42), (91*i+63, 32*18+29), (180, 180, 180), 2)
                else:
                    text = "before"
                    cv2.putText(img, text, (91*i+29, 7), cv2.FONT_HERSHEY_DUPLEX,
                                            0.3, (5, 5, 5), 1, cv2.LINE_AA)
                    text = "after"
                    cv2.putText(img, text, (91*i+66, 7), cv2.FONT_HERSHEY_DUPLEX,
                                            0.3, (5, 5, 5), 1, cv2.LINE_AA)
                    cv2.line(img, (91*i+63, 10), (91*i+63, 32*18+29), (180, 180, 180), 2)
                    

                text = "total"
                cv2.putText(img, text, (91*i+7, 32*18+23), cv2.FONT_HERSHEY_DUPLEX,
                                        0.3, (250, 250, 250), 1, cv2.LINE_AA)

                text = f'{self.used_point[i]}'
                if self.used_point[i] >= 100:
                    cv2.putText(img, text, (91*i+36, 32*18+24), cv2.FONT_HERSHEY_DUPLEX,
                            0.4, (250, 250, 250), 1, cv2.LINE_AA)
                elif 10 <= self.used_point[i] <= 99:
                    cv2.putText(img, text, (91*i+40, 32*18+24), cv2.FONT_HERSHEY_DUPLEX,
                            0.4, (250, 250, 250), 1, cv2.LINE_AA)
                else:
                    cv2.putText(img, text, (91*i+44, 32*18+24), cv2.FONT_HERSHEY_DUPLEX,
                            0.4, (250, 250, 250), 1, cv2.LINE_AA)

                text = f'{self.total_point[i]}'
                if self.total_point[i] >= 100:
                    cv2.putText(img, text, (91*i+67, 32*18+24), cv2.FONT_HERSHEY_DUPLEX,
                            0.4, (250, 250, 250), 1, cv2.LINE_AA)
                elif 10 <= self.total_point[i] <= 99:
                    cv2.putText(img, text, (91*i+70, 32*18+24), cv2.FONT_HERSHEY_DUPLEX,
                            0.4, (250, 250, 250), 1, cv2.LINE_AA)
                else:
                    cv2.putText(img, text, (91*i+74, 32*18+24), cv2.FONT_HERSHEY_DUPLEX,
                            0.4, (250, 250, 250), 1, cv2.LINE_AA)

            # cv2.imwrite(fileName, img)
            cv2.imencode('.jpg', img)[1].tofile(fileName)
        except Exception:
            pass
        

app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
