import random
from typing import Tuple, List, Dict, Any

class Question:
    def __init__(self, qid: int, question_type: str, content: str, options: List[int], correct_answer: int, hint: str = ""):
        self.qid = qid
        self.question_type = question_type
        self.content = content
        self.options = options
        self.correct_answer = correct_answer
        self.hint = hint
        self.user_answer = None
        self.is_correct = False
        self.time_spent = 0

class QuestionGenerator:
    PATTERNS = ["🍎", "🍊", "🍋", "🍇", "🍓", "🌸", "🌺", "🐱", "🐶", "🐰", "🐼", "🦋", "⭐", "🌙", "🌈"]
    
    def __init__(self):
        self.used_patterns = []
        self.question_id = 0
    
    def generate_question(self, difficulty: int) -> Question:
        self.question_id += 1
        
        question_type = self._select_question_type(difficulty)
        
        if question_type == "counting":
            return self._generate_counting_question(difficulty)
        elif question_type == "addition":
            return self._generate_addition_question(difficulty)
        elif question_type == "subtraction":
            return self._generate_subtraction_question(difficulty)
        elif question_type == "multiplication":
            return self._generate_multiplication_question(difficulty)
        elif question_type == "division":
            return self._generate_division_question(difficulty)
        elif question_type == "compare":
            return self._generate_compare_question(difficulty)
        elif question_type == "mixed":
            return self._generate_mixed_question(difficulty)
        
        return self._generate_counting_question(difficulty)
    
    def _select_question_type(self, difficulty: int) -> str:
        if difficulty == 1:
            return "counting"
        elif difficulty == 2:
            return random.choice(["addition", "subtraction"])
        elif difficulty == 3:
            return random.choice(["addition", "subtraction", "multiplication"])
        else:
            return random.choice(["addition", "subtraction", "multiplication", "division", "compare", "mixed"])
    
    def _generate_counting_question(self, difficulty: int) -> Question:
        min_count, max_count = self._get_count_range(difficulty)
        
        available_patterns = [p for p in self.PATTERNS if p not in self.used_patterns]
        if not available_patterns:
            self.used_patterns.clear()
            available_patterns = self.PATTERNS
        
        pattern = random.choice(available_patterns)
        self.used_patterns.append(pattern)
        
        count = random.randint(min_count, max_count)
        
        content = f"{pattern} " * count
        options = self._generate_options(count, min_count, max_count)
        
        return Question(
            qid=self.question_id,
            question_type="counting",
            content=content,
            options=options,
            correct_answer=count,
            hint="数一数有几个图案"
        )
    
    def _generate_addition_question(self, difficulty: int) -> Question:
        if difficulty <= 2:
            max_num = 20
            no_carry = difficulty == 2
        else:
            max_num = 100
            no_carry = False
        
        if no_carry:
            a = random.randint(1, 9)
            b = random.randint(1, 9)
        else:
            a = random.randint(1, max_num // 2)
            b = random.randint(1, max_num // 2)
        
        answer = a + b
        content = f"{a} + {b} = ?"
        options = self._generate_options(answer, max(1, answer - 10), min(max_num, answer + 10))
        
        return Question(
            qid=self.question_id,
            question_type="addition",
            content=content,
            options=options,
            correct_answer=answer,
            hint=f"可以先数{a}个，再数{b}个"
        )
    
    def _generate_subtraction_question(self, difficulty: int) -> Question:
        if difficulty <= 2:
            max_num = 20
            no_borrow = difficulty == 2
        else:
            max_num = 100
            no_borrow = False
        
        if no_borrow:
            a = random.randint(10, max_num)
            b = random.randint(1, a // 2)
        else:
            a = random.randint(10, max_num)
            b = random.randint(1, a - 1)
        
        answer = a - b
        content = f"{a} - {b} = ?"
        options = self._generate_options(answer, max(0, answer - 10), min(max_num, answer + 10))
        
        return Question(
            qid=self.question_id,
            question_type="subtraction",
            content=content,
            options=options,
            correct_answer=answer,
            hint=f"从{a}里面拿走{b}个"
        )
    
    def _generate_multiplication_question(self, difficulty: int) -> Question:
        max_factor = min(difficulty + 4, 9)
        a = random.randint(2, max_factor)
        b = random.randint(2, max_factor)
        answer = a * b
        
        content = f"{a} × {b} = ?"
        options = self._generate_options(answer, max(1, answer - 15), min(81, answer + 15))
        
        return Question(
            qid=self.question_id,
            question_type="multiplication",
            content=content,
            options=options,
            correct_answer=answer,
            hint=f"乘法口诀：{a}×{b}等于多少？"
        )
    
    def _generate_division_question(self, difficulty: int) -> Question:
        max_divisor = min(difficulty + 3, 9)
        divisor = random.randint(2, max_divisor)
        quotient = random.randint(2, max_divisor)
        dividend = divisor * quotient
        
        content = f"{dividend} ÷ {divisor} = ?"
        options = self._generate_options(quotient, max(1, quotient - 5), min(9, quotient + 5))
        
        return Question(
            qid=self.question_id,
            question_type="division",
            content=content,
            options=options,
            correct_answer=quotient,
            hint=f"想乘法算除法：{divisor}乘多少等于{dividend}？"
        )
    
    def _generate_compare_question(self, difficulty: int) -> Question:
        if difficulty <= 3:
            max_num = 50
        else:
            max_num = 100
        
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        
        if a > b:
            answer = 1
            content = f"{a} > {b}"
        elif a < b:
            answer = 2
            content = f"{a} < {b}"
        else:
            answer = 3
            content = f"{a} = {b}"
        
        options = [1, 2, 3]
        random.shuffle(options)
        
        return Question(
            qid=self.question_id,
            question_type="compare",
            content=content,
            options=options,
            correct_answer=answer,
            hint="比较两个数的大小"
        )
    
    def _generate_mixed_question(self, difficulty: int) -> Question:
        operations = [
            lambda: self._generate_two_step_add_sub(),
            lambda: self._generate_add_mul(),
            lambda: self._generate_sub_mul(),
        ]
        
        func = random.choice(operations)
        return func()
    
    def _generate_two_step_add_sub(self) -> Question:
        a = random.randint(1, 20)
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        
        if random.choice([True, False]):
            answer = a + b - c
            content = f"{a} + {b} - {c} = ?"
        else:
            answer = a - b + c
            content = f"{a} - {b} + {c} = ?"
        
        options = self._generate_options(answer, max(1, answer - 10), min(50, answer + 10))
        
        return Question(
            qid=self.question_id,
            question_type="mixed",
            content=content,
            options=options,
            correct_answer=answer,
            hint="按照从左到右的顺序计算"
        )
    
    def _generate_add_mul(self) -> Question:
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        c = random.randint(1, 10)
        
        answer = a * b + c
        content = f"{a} × {b} + {c} = ?"
        options = self._generate_options(answer, max(1, answer - 10), min(40, answer + 10))
        
        return Question(
            qid=self.question_id,
            question_type="mixed",
            content=content,
            options=options,
            correct_answer=answer,
            hint="先算乘法，再算加法"
        )
    
    def _generate_sub_mul(self) -> Question:
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        c = random.randint(1, 10)
        
        answer = a * b - c
        content = f"{a} × {b} - {c} = ?"
        options = self._generate_options(answer, max(1, answer - 10), min(30, answer + 10))
        
        return Question(
            qid=self.question_id,
            question_type="mixed",
            content=content,
            options=options,
            correct_answer=answer,
            hint="先算乘法，再算减法"
        )
    
    def _get_count_range(self, difficulty: int) -> Tuple[int, int]:
        ranges = {
            1: (1, 10),
            2: (5, 20),
            3: (10, 30),
            4: (15, 50),
        }
        return ranges.get(difficulty, (1, 10))
    
    def _generate_options(self, correct_answer: int, min_option: int, max_option: int) -> List[int]:
        options = {correct_answer}
        
        while len(options) < 4:
            option = random.randint(min_option, max_option)
            if option != correct_answer:
                options.add(option)
        
        options = list(options)
        random.shuffle(options)
        return options
    
    def generate_positions(self, count: int, canvas_width: int, canvas_height: int, pattern_size: int) -> List[Tuple[int, int]]:
        positions = []
        padding = pattern_size // 2 + 20
        
        for _ in range(count):
            while True:
                x = random.randint(padding, canvas_width - padding)
                y = random.randint(padding, canvas_height - padding)
                
                overlap = False
                for (px, py) in positions:
                    distance = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
                    if distance < pattern_size + 10:
                        overlap = True
                        break
                
                if not overlap:
                    positions.append((x, y))
                    break
        
        return positions
    
    def reset(self):
        self.used_patterns.clear()
        self.question_id = 0