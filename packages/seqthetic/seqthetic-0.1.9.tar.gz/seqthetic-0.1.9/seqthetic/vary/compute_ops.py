from typing import Literal

from pydantic import BaseModel, Field


class BaseComputeOp(BaseModel):
    op: str = ''
    value: float

    def __init__(self, x: float, op: str) -> None:
        super().__init__(op=op, value=x)
    
    def __repr__(self) -> str:
        return f'{self.op.title()}({self.value})'

    

class Mul(BaseComputeOp):
    op: Literal["mul"] = "mul"

    def __init__(self, x: float) -> None:
        super().__init__(x, op="mul")
        
    def compute(self, y: float) -> int:
        return int(y * self.value)

class Add(BaseComputeOp):
    op: Literal["add"] = "add"

    def __init__(self, x: float) -> None:
        super().__init__(x, op="add")
        
    def compute(self, y: int) -> int:
        return y + self.value

class Sub(BaseComputeOp):
    op: Literal["sub"] = "sub"

    def __init__(self, x: float) -> None:
        super().__init__(x, op="sub")
    
    def compute(self, y: int) -> int:
        return y - self.value

class Div(BaseComputeOp):
    op: Literal["div"] = "div"

    def __init__(self, x: float) -> None:
        super().__init__(x, op="div")
    
    def compute(self, y: float) -> int:
        return y // self.value

ComputeOp = Mul | Add | Sub | Div


# Additional methods like model_dump() and model_validate() are not standard Pydantic methods.
# If you're using custom methods, you should define them or ensure they are part of your environment.