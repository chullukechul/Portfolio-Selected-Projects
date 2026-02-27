
from manim import *

class PointsAndLinesScene(Scene):
    def construct(self):
        points = {
            "A": [-2.5, -2.0, 0],
            "B": [-1.5, 0.5, 0],
            "C": [2.5, 0.5, 0],
            "D": [1.5, -2.0, 0],
            "E": [2.8805988906743063, 1.4514972266857653, 0],
            "F": [1.4164043238914263, 0.5122591252657687, 0]
        }

        A = Dot(points["A"], color=WHITE)
        B = Dot(points["B"], color=WHITE)
        C = Dot(points["C"], color=WHITE)
        D = Dot(points["D"], color=WHITE)
        E = Dot(points["E"], color=WHITE)
        F = Dot(points["F"], color=WHITE)

        label_A = Text("A").next_to(A, DOWN)
        label_B = Text("B").next_to(B, UP)
        label_C = Text("C").next_to(C, RIGHT)
        label_D = Text("D").next_to(D, RIGHT)
        label_E = Text("E").next_to(E, RIGHT)
        label_F = Text("F").next_to(F, DOWN)

        AB = Line(points["A"], points["B"], color=WHITE)
        AD = Line(points["A"], points["D"], color=WHITE)
        AF = Line(points["A"], points["F"], color=WHITE)
        BF = Line(points["B"], points["F"], color=WHITE)
        CF = Line(points["C"], points["F"], color=WHITE)
        CE = Line(points["C"], points["E"], color=WHITE)
        CD = Line(points["C"], points["D"], color=WHITE)
        EF = Line(points["E"], points["F"], color=WHITE)
        x00 = Tex("製作給興安小朋友學習使用",fill_color=WHITE,fill_opacity=0.05).next_to([-6,-3.5,0])
        x0 = Tex("AF是角平分線  ABCD是平行四邊形",font_size=60).next_to([-5,1.5,0])
        x01 = Tex("找找看畫面中有幾個等腰三角形",font_size=60).next_to(x0,DOWN)
        self.add(x00)
        self.play(AnimationGroup(Write(x0),Write(x01)))
        self.wait(2.5)
        self.play(AnimationGroup(Unwrite(x0),Unwrite(x01)),run_time = 0.6)
        self.play(FadeIn(VGroup(A, B, C, D, E, F, label_A, label_B, label_C, label_D, label_E, label_F)),run_time=1.4)
        self.play(DrawBorderThenFill(VGroup(AB, AD, AF, BF, CF, CE, CD, EF)),run_time = 3)
        self.wait(1.5)

        BAF = Angle.from_three_points(points["B"], points["A"], points["F"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        FAD = Angle.from_three_points(points["F"], points["A"], points["D"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        BFA = Angle.from_three_points(points["B"], points["F"], points["A"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=False)
        EFC = Angle.from_three_points(points["E"], points["F"], points["C"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=True)
        FEC = Angle.from_three_points(points["F"], points["E"], points["C"], color=YELLOW, dot=True, quadrant=(1, 1),
                                      other_angle=False)
        self.play(Create(BAF))
        x2 = Tex("AF 是角平分線").next_to([-3,3,0])
        self.play(Write(x2))
        self.play(ShowPassingFlash(AF))
        self.add(AF)
        self.play(Create(FAD))
        self.wait(0.5)
        self.play(Unwrite(x2),run_time = 0.6)
        self.wait()

        x3 = Tex("AB 平行 CE",color=YELLOW).next_to([-3,3,0])
        x4 = Tex("AE 是截線").next_to(x3,DOWN)
        self.play(AnimationGroup(Write(x3),Write(x4)))
        self.play(AnimationGroup(Indicate(AB),Indicate(CD),Indicate(CE)),run_time = 1.5)
        self.play(AnimationGroup(ApplyWave(AF,amplitude=0.5),ApplyWave(EF,amplitude=0.5,direction=DOWN)))
        self.play(AnimationGroup(Flash(BAF),Flash(FEC)))
        self.play(Create(FEC))
        self.play(AnimationGroup(Unwrite(x3),Unwrite(x4)),run_time = 0.6)
        self.wait(0.5)
        #另一組平行邊
        x5 = Tex("AD 平行 BC", color=YELLOW).next_to([-3, 3, 0])
        x6 = Tex("AF 是截線").next_to(x5, DOWN)
        self.play(AnimationGroup(Write(x5), Write(x6)))
        self.play(AnimationGroup(Indicate(BF), Indicate(CF), Indicate(AD)),run_time = 1.5)
        self.play( ApplyWave(AF,amplitude=0.5))
        self.play(AnimationGroup(Flash(FAD),Flash(BFA)))
        self.play(Create(BFA))
        self.play(AnimationGroup(Unwrite(x5), Unwrite(x6)),run_time = 0.6)
        self.wait(0.5)
        #對頂角
        x7 = Tex("對頂角相等").next_to([-3,3,0])
        self.play(Write(x7))
        self.play(AnimationGroup(Flash(BFA),Flash(EFC)))
        self.play(Create(EFC))
        self.play(Unwrite(x7),run_time = 0.6)

        self.play(AnimationGroup(AB.animate.set_color(ORANGE),BF.animate.set_color(ORANGE)))
        self.play(AnimationGroup(CE.animate.set_color(GREEN), CF.animate.set_color(GREEN)))
        x8 = Tex("AB = BF",color=ORANGE).next_to([-3,3,0])
        x9 = Tex("CF = CE",color=GREEN).next_to(x8,RIGHT)
        self.play(AnimationGroup(Write(x8),Write(x9)))
        p1 = Polygon(A.get_center(),B.get_center(),F.get_center(),color=ORANGE,fill_color=ORANGE,fill_opacity=0.3)
        p2 = Polygon(C.get_center(), E.get_center(), F.get_center(), color=GREEN, fill_color=GREEN, fill_opacity=0.3)
        self.play(AnimationGroup(Create(p1),Create(p2)),run_time = 1.2)
        self.wait(1)

        self.play(AnimationGroup(Unwrite(x8),Unwrite(x9)),run_time = 0.6)
        self.play(Uncreate(p1),Uncreate(p2))
        self.play(AnimationGroup(AB.animate.set_color(WHITE), BF.animate.set_color(WHITE),CE.animate.set_color(WHITE), CF.animate.set_color(WHITE)))

        x10 = Tex("AD = DE", color=BLUE).next_to([-3, 3, 0])
        self.play(AnimationGroup(CD.animate.set_color(BLUE), CE.animate.set_color(BLUE), AD.animate.set_color(BLUE)))
        self.play(Write(x10))
        p3 = Polygon(A.get_center(), E.get_center(), D.get_center(), color=BLUE, fill_color=BLUE, fill_opacity=0.3)
        self.play(Create(p3),run_time = 1.5)
        self.wait(1.5)
        self.play(AnimationGroup(Unwrite(p3),Unwrite(x10)))
        x11 = Tex("一共三組等腰三角形",font_size=60).next_to([-3,3,0])
        self.play(FadeIn(x11))
        self.wait(4)