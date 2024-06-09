from manim import *

def paragraph(*strs, alignment=LEFT, direction=DOWN, **kwargs):
    
    if kwargs.pop('math', False):
        texts = VGroup(*[MathTex(s, **kwargs) for s in strs]).arrange(direction)
    else:
        texts = VGroup(*[Text(s, **kwargs) for s in strs]).arrange(direction)

    if len(strs) > 1:
        for text in texts[1:]:
            text.align_to(texts[0], direction=alignment)

    return texts


def highlighted_paragraph(self, *strs, explanations, explanation_positions, highlights, alignment=LEFT, direction=DOWN, **kwargs):
    
    texts = paragraph(*strs, alignment=alignment, direction=direction, **kwargs)
    

    highlights_vgroup = VGroup()
    for j, (pos, line) in enumerate(highlights):
        part = texts[line]
        char_box = SurroundingRectangle(texts[line][0][pos], color=RED, buff=0.1)
        highlight = Circle(radius=0.3, color=RED).move_to(char_box.get_center())
        text_explanation = Text(explanations[j], color=RED).scale(0.5)
        if explanation_positions[j] == 'above':
            text_explanation.next_to(highlight, UP*2)
        elif explanation_positions[j] == 'below':
            text_explanation.next_to(highlight, DOWN*2)
        highlights_vgroup.add(VGroup(highlight, text_explanation))
                    

    self.play(Write(texts, run_time=0.05))
    self.wait(2)
    for highlight in highlights_vgroup:
        self.next_slide()
        self.play(Create(highlight))  # Show the highlight
        self.next_slide()
        self.wait(2)
        self.play(FadeOut(highlight))  # Hide the highlight

    return texts


