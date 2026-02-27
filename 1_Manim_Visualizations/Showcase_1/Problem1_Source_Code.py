# -*- coding: utf-8 -*-
from manim import *

class PointAndLineScene(Scene):
    def construct(self):
        # 定義點的位置
        points = {
            'A': [-0.5, 1.0, 0],
            'B': [1.5, 1.0, 0],
            'C': [0.5, -0.5, 0],
            'D': [-1.5, -0.5, 0],
            'E': [0.0, 2.0, 0],
            'F': [-1.0, -0.5, 0],
            'G': [0.4, 1.0, 0],
            'H': [0.8, 1.0, 0],
            'I': [-0.86, -0.08, 0],
            'J': [-0.82, 0.04, 0]
        }

        # 創建並顯示點
        dots = {key: Dot(point) for key, point in points.items()}


        # 創建連線字典，並顯示連線
        lines = {}
        for key1 in points:
            for key2 in points:
                if key1 < key2:  # 確保每個連線只被創建一次
                    line_key = f"{key1}{key2}"
                    line = Line(points[key1], points[key2])
                    lines[line_key] = line
        x00 = Tex("提供興安小朋友學習使用",fill_color=WHITE,fill_opacity=0.07).next_to([-3.5,-2,0])
        x0 = Tex("畫面中的綠色與橘色三角形誰比較大").next_to([-3,3,0])
        p1 = Polygon(points["A"], points["B"], points["C"], points["D"], color=BLUE_D)
        IHF = Polygon(points["I"], points["H"], points["F"], color=GREEN, fill_color=GREEN, fill_opacity=0.3)
        JGF = Polygon(points["J"], points["G"], points["F"], color=ORANGE, fill_color=ORANGE, fill_opacity=0.3)
        self.play(AnimationGroup(DrawBorderThenFill(VGroup(dots["A"],dots["B"],dots["C"],dots["D"],p1,dots["G"],dots["H"],dots["F"],lines["AF"],IHF,JGF)),Write(x0)),run_time = 2)
        self.wait(3)
        self.clear()

        #加入四邊形與兩三角
        self.add(x00)
        x01 = Tex("藍色是平行四邊形").next_to([-3, 3, 0])
        self.play(Create(p1),run_time = 2)
        self.play(Write(x01))
        self.play(FadeIn(dots["A"],dots["B"],dots["C"],dots["D"],),scale = 1.5)
        self.play(FadeIn(dots["G"],dots["H"],dots["F"]))
        self.wait(0.5)
        self.play(Unwrite(x01),run_time = 0.6)


        #定義並創建三角形
        K = Dot([0.4, -0.5, 0])
        L = Dot([0.8, -0.5, 0])
        CL = Line(points["C"], [0.8, -0.5, 0], color=BLUE_D)
        GK = Line([0.4, 1, 0], [0.4, -0.5, 0], color=RED)
        HL = Line([0.8, 1, 0], [0.8, -0.5, 0], color=RED)
        DGF = Polygon(points["D"], points["G"], points["F"], color=ORANGE)
        DHF = Polygon(points["D"], points["H"], points["F"], color=GREEN)
        self.play(*[Create(DGF), Create(DHF)], run_time=2, lag_time=0.5)

        x02 = Tex("讓我們觀察這兩個三角形的面積").next_to([-3,3,0])
        self.play(FadeIn(x02))
        self.wait(1.5)
        #同底
        xDF =Tex("同底").next_to(lines["DF"],DOWN)
        self.play(Write(xDF))
        self.play(Flash(lines["DF"]))

        #同高
        a1 = Angle(GK,lines["CF"],color=RED,radius=0.2,quadrant=(-1,1),elbow=True)
        a2 = Angle(HL,CL,color=RED,radius=0.2,quadrant=(-1,-1),elbow=True)
        self.wait(1)
        self.play(AnimationGroup(Create(GK),Create(HL)),Create(CL))
        self.play(*[Write(a1),Write(a2)])
        x2 = Tex("同高", color=RED).next_to(HL, RIGHT)
        self.play(Write(x2))
        self.play(Flash(HL))
        self.wait()
        self.play(FadeOut(x02))
        #加入文字:描述同底同高橘綠三角型等面積
        x11 = Tex("綠三角",color=GREEN).next_to([-3,3,0])
        x12= Tex(" = ").next_to(x11,RIGHT)
        x13= Tex("橘三角",color=ORANGE).next_to(x12,RIGHT)
        self.play(Write(x11), Write(x12),Write(x13) ,target_position = points["A"])
        self.wait(2)
        self.play(*[Unwrite(GK),Unwrite(HL),Unwrite(x11),Unwrite(x12),Unwrite(x13),Unwrite(x2),Unwrite(xDF),Unwrite(CL),Unwrite(a2),Unwrite(a1)])
        self.wait()
        self.add(lines["AF"])

        DIF = Polygon(points["D"], points["I"], points["F"], color=WHITE, fill_color=WHITE,fill_opacity=1)
        self.play((Create(DIF)))
        label1 = Tex("扣除較小",color=WHITE).move_to([-1,-1.5,0])
        self.play(Write(label1))
        self.wait()

        self.play((Create(IHF)))
        self.wait()
        label3 = Tex("剩下綠色部分較多",color=GREEN).move_to([-1,2,0])
        self.play(Write(label3))
        self.wait(2)
        self.play(*[FadeOut(label1),FadeOut(label3),FadeOut(DIF),FadeOut(IHF)])


        #x3 = Tex("x3",color=Write).next_to([3,3,0])
        #self.play(Write(x3))
        DJF = Polygon(points["D"], points["J"], points["F"], color=WHITE, fill_color=WHITE,fill_opacity=1)
        self.play((Create(DJF)))
        label2 = Tex("扣除較大",color=WHITE).move_to([-1,-1.5,0])
        self.play(Write(label2))
        self.wait()

        self.play((Create(JGF)))
        self.wait()
        label4 = Tex("剩下橘色部分較少",color=ORANGE).move_to([-1,2,0])
        self.play(Write(label4))
        self.wait(3)
        self.play(*[FadeOut(label4), FadeOut(label2), FadeOut(DJF), FadeOut(JGF)])
        x21 = Tex("綠三角", color=GREEN).next_to([-3, 3, 0])
        x22 = Tex("  $>$ ").next_to(x21, RIGHT)
        x23 = Tex("橘三角", color=ORANGE).next_to(x22, RIGHT)
        self.play(Write(x21), Write(x22), Write(x23), target_position=points["A"])
        self.wait(2)
        self.clear()
        self.wait()
