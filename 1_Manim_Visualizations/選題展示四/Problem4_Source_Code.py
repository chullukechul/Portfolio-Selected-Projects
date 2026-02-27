from manim import *

class PointsScene(Scene):
    def construct(self):
        points = {
            "A": [-3.0, -2.0, 0],
            "B": [2.0, -2.0, 0],
            "C": [4.0, 2.0, 0],
            "D": [-1.0, 2.0, 0],
            "E": [3.0, 2.0, 0],
            "F": [1.0, -2.0, 0],
            "G": [0.0, 2.0, 0],
            "H": [-2.0, -2.0, 0],
            "I": [0.0, 0.0, 0],
            "J": [0.25, -0.5, 0],
            "K": [0.75, 0.5, 0],
            "L": [1, 0, 0]
        }

        # 定義點
        A = Dot(points["A"], color=WHITE)
        B = Dot(points["B"], color=WHITE)
        C = Dot(points["C"], color=WHITE)
        D = Dot(points["D"], color=WHITE)
        E = Dot(points["E"], color=WHITE)
        F = Dot(points["F"], color=WHITE)
        G = Dot(points["G"], color=WHITE)
        H = Dot(points["H"], color=WHITE)
        I = Dot(points["I"], color=WHITE)
        J = Dot(points["J"], color=WHITE)
        K = Dot(points["K"], color=WHITE)
        L = Dot(points["L"], color=WHITE)

        # 定義標籤
        label_A = Text("A").next_to(A, DOWN)
        label_B = Text("B").next_to(B, RIGHT)
        label_C = Text("C").next_to(C, RIGHT)
        label_D = Text("D").next_to(D, UP)
        label_E = Text("E").next_to(E, RIGHT)
        label_F = Text("F").next_to(F, RIGHT)
        label_G = Text("G").next_to(G, RIGHT)
        label_H = Text("H").next_to(H, RIGHT)
        label_I = Text("I").next_to(I, UP)
        label_J = Text("J").next_to(J, RIGHT)
        label_K = Text("K").next_to(K, RIGHT)
        label_L = Text("L").next_to(L, RIGHT)

        # 定義線段
        AE = Line(points["A"], points["E"], color=WHITE)
        DF = Line(points["D"], points["F"], color=WHITE)
        GK = Line(points["B"], points["G"], color=RED)
        CH = Line(points["C"], points["H"], color=WHITE)
        AD = Line(points["A"], points["D"], color=WHITE)
        AH = Line(points["A"], points["H"], color=WHITE)
        FH = Line(points["F"], points["H"], color=WHITE)
        BF = Line(points["B"], points["F"], color=WHITE)
        BC = Line(points["B"], points["C"], color=WHITE)
        CE = Line(points["C"], points["E"], color=WHITE)
        EG = Line(points["E"], points["G"], color=WHITE)
        DG = Line(points["D"], points["G"], color=WHITE)
        DI = Line(points["D"], points["I"], color=RED)
        IJ = Line(points["I"], points["J"], color=RED)
        FJ = Line(points["F"], points["J"], color=RED)
        KL = Line(points["K"], points["L"], color=RED)
        BL = Line(points["B"], points["L"], color=RED)
        AI = Line(points["A"], points["I"], color=RED)
        IK = Line(points["I"], points["K"], color=RED)
        EK = Line(points["E"], points["K"], color=RED)
        CL = Line(points["C"], points["L"], color=RED)
        HJ = Line(points["H"], points["J"], color=RED)
        JL = Line(points["J"], points["L"], color=RED)

        # 定義角度
        DAI = Angle.from_three_points(points["D"], points["A"], points["I"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        IAH = Angle.from_three_points(points["I"], points["A"], points["H"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        FBL = Angle.from_three_points(points["F"], points["B"], points["L"], color=GREEN, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        LBC = Angle.from_three_points(points["L"], points["B"], points["C"], color=GREEN, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        BCL = Angle.from_three_points(points["B"], points["C"], points["L"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        LCE = Angle.from_three_points(points["L"], points["C"], points["E"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        GDI = Angle.from_three_points(points["G"], points["D"], points["I"], color=GREEN, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        IDA = Angle.from_three_points(points["I"], points["D"], points["A"], color=GREEN, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        DIA = Angle.from_three_points(points["D"], points["I"], points["A"], color=WHITE, dot=False, quadrant=(1, 1),
                                      other_angle=False,elbow = True,radius = 0.2)
        HJF = Angle.from_three_points(points["H"], points["J"], points["F"], color=WHITE, dot=False, quadrant=(1, 1),
                                      other_angle=False,elbow = True,radius = 0.2)
        BLC = Angle.from_three_points(points["B"], points["L"], points["C"], color=WHITE, dot=False, quadrant=(1, 1),
                                      other_angle=False,elbow = True,radius = 0.2)
        GKE = Angle.from_three_points(points["G"], points["K"], points["E"], color=WHITE, dot=False, quadrant=(1, 1),
                                      other_angle=True,elbow = True,radius = 0.2)
        KIJ = Angle.from_three_points(points["K"], points["I"], points["J"], color=WHITE, dot=False, quadrant=(1, 1),
                                      other_angle=True,elbow = True,radius = 0.2)
        IJL = Angle.from_three_points(points["I"], points["J"], points["L"], color=WHITE, dot=False, quadrant=(1, 1),
                                      other_angle=True,elbow = True,radius = 0.2)
        JLK = Angle.from_three_points(points["J"], points["L"], points["K"], color=WHITE, dot=False, quadrant=(1, 1),
                                      other_angle=True,elbow = True,radius = 0.2)
        LKI = Angle.from_three_points(points["L"], points["K"], points["I"], color=WHITE, dot=False, quadrant=(1, 1),
                                      other_angle=True,elbow = True,radius = 0.2)
        CDA = Angle.from_three_points(points["C"], points["D"], points["A"], color=GREEN, dot=False, quadrant=(1, 1),
                                      other_angle=True)
        DAB = Angle.from_three_points(points["D"], points["A"], points["B"], color=YELLOW, dot=False, quadrant=(1, 1),
                                      other_angle=True)
        p1 = Polygon(I.get_center(), J.get_center(), L.get_center(), K.get_center(), color=BLUE, fill_color=BLUE,
                     fill_opacity=0.5)
        # 將所有點和標籤組合進一個 VGroup
        dots1 = VGroup(A, B, C, D,  label_A, label_B, label_C, label_D)
        dots2 = VGroup( I,  label_I)
        dots3 = VGroup( E, F, G, H, J, K, L, label_E, label_F,
                       label_G, label_H, label_J, label_K, label_L)
        # 將所有線段組合進一個 VGroup
        lines1 = VGroup(AD, AH, FH, BF, BC, CE, EG, DG)
        lines2 = VGroup(DI, IJ, FJ, AI, IK, EK)
        lines3 = VGroup(AE, DF, GK, CH, KL, BL, CL, HJ, JL,DI, IJ, FJ, AI, IK, EK)
        x0 = Tex("供興安校的小朋友學習使用",color=WHITE,fill_color=WHITE,fill_opacity=0.06).next_to([-4,-3,0])
        x1 = Tex("平行四邊形對角線交出的形狀是甚麼").next_to([-3,3.5,0])
        self.add(x0)
        self.play(FadeIn(x1))
        self.play(AnimationGroup(FadeIn(dots1),FadeIn(dots2),FadeIn(dots3)))
        self.play(AnimationGroup(DrawBorderThenFill(lines1),DrawBorderThenFill(lines2.copy().set_color(WHITE)),DrawBorderThenFill(lines3.copy().set_color(WHITE))))
        self.play(Create(p1),run_time = 0.8)
        self.wait(3)
        self.clear()
        self.wait()
        # 動畫顯示所有點和標籤
        self.play(FadeIn(dots1), run_time=1.4)
        x2 = Tex("鄰角會互補").next_to([-3,3.5,0])
        self.play(FadeIn(x2))
        # 動畫顯示所有線段
        self.play(DrawBorderThenFill(lines1), run_time=2)
        self.play(AnimationGroup(Create(CDA),Create(DAB)))
        self.play(Unwrite(x2),run_time = 0.6)
        x3 = Tex("紅色的線條是各角的平分線",color=RED).next_to([-3,3.5,0])
        self.play(FadeIn(x3))
        #將所有角度組合進一個 VGroup
        angles1 = VGroup(DAI, IAH, IDA, GDI)
        angles2 = VGroup(DIA)
        angles3 = VGroup( KIJ)
        angles4 = VGroup(FBL, LBC, BCL, LCE)
        angles5 = VGroup(HJF, BLC, GKE)
        angles6 = VGroup(IJL, JLK, LKI)
        self.play(Create(lines2))
        self.wait()

        self.add(dots2)
        self.wait()
        self.play(AnimationGroup(Unwrite(CDA),Unwrite(DAB)))
        self.play(Create(angles1))

        self.play(Unwrite(x3),run_time =0.6)
        x41 = Tex("2綠+",color=GREEN).next_to([-3,3.5,0])
        x42 = Tex("2黃",color=YELLOW).next_to(x41,RIGHT)
        x43 = Tex("=180度", color=WHITE).next_to(x42, RIGHT)
        self.play(Write(x41),Write(x42),Write(x43))
        self.wait(1.5)
        self.play(AnimationGroup(Unwrite(x41),Unwrite(x42),Unwrite(x43)))
        x51 = Tex("1綠+", color=GREEN).next_to([-3, 3.5, 0])
        x52 = Tex("1黃", color=YELLOW).next_to(x51, RIGHT)
        x53 = Tex("=90度", color=WHITE).next_to(x52, RIGHT)
        self.play(Write(x51), Write(x52), Write(x53))
        self.wait(1.5)
        self.play(AnimationGroup(Unwrite(x51), Unwrite(x52), Unwrite(x53)))
        self.play(AnimationGroup(Unwrite(x41), Unwrite(x42), Unwrite(x43)))

        p2 = Polygon(D.get_center(),I.get_center(),A.get_center(),color=ORANGE,fill_color=ORANGE,fill_opacity=0.5)
        x6 = Tex("橘色三角形內角和=180",color=ORANGE).next_to([-3,3.5,0])
        self.play(AnimationGroup(Create(p2),Write(x6)))
        self.wait(1.5)
        self.play(Uncreate(p2))
        self.play(FadeOut(x6))


        x7 = Tex("扣除 1綠1橘剩下90度").next_to([-3,3.5,0])
        self.play(Create(angles2),Write(x3))
        self.wait()
        #加入90度的角
        self.play(Unwrite(x3),run_time =0.6)
        self.wait()
        x8 = Tex("對頂角相等",color=YELLOW).next_to([-3,3.5,0])
        self.play(FadeIn(x8))
        self.play(AnimationGroup(Flash(KIJ),Flash(DIA)))
        self.play(Create(angles3))
        self.play(FadeOut(x8))
        self.wait()
        #加入所有角平分線
        x9 = Tex("其他四角按照同樣做法").next_to([-3,3.5,0])
        self.play(Write(x9))
        self.play(Create(lines3))
        self.play(Create(angles4))
        self.wait()
        self.play(Create(angles5))
        self.wait()
        self.play(AnimationGroup(FadeOut(angles5),FadeOut(angles2)))
        self.wait()
        self.play(Create(angles6))
        self.play(FadeOut(x9))
        self.wait()

        x10 =Tex("交出的形狀四角90度為 長方形",color=BLUE).next_to([-4,3.5,0])
        self.play(Create(p1))
        self.play(Write(x10))
        self.wait(4)
        #說明所有交矩形