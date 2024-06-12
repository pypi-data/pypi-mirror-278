from data.result.Class_text import Class_text


class Label_area:
    def __init__(self):
        self.labels = dict(
            {
                        Class_text.number : ('', 0.0),
                        Class_text.prod : ('', 0.0),
                        Class_text.year : ('', 0.0)
            }
        )


