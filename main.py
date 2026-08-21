import time
from collections import deque


class Chain:
    def __init__(
        self,
        content: "list[Chain|str]|None" = None,
    ) -> None:
        if content is None:
            self.content: list[Chain | str] = []
        else:
            self.content = content
        self.string = ""

    def __str__(self) -> str:
        if self.string != "":
            return self.string
        text = ""
        if self.content:
            for chain in self.content:
                text += str(chain)
        return f"[{text}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chain):
            raise NotImplementedError("only comparable with chains")
        return self.unique_str() == other.unique_str()

    def unique_str(self) -> str:
        if self.string:
            return self.string
        visualizations: set[str] = {str(self)}
        stack: deque[Chain] = deque()
        if not self.content:
            return "[]"
        if isinstance(self.content[0],Chain):
            stack.append(self)
        rotate_chain = Chain(self.content.copy())
        for _ in range(len(self.content)-1):
            rotate_chain.content.append(rotate_chain.content.pop(0))
            chain_str = str(rotate_chain)
            if chain_str not in visualizations:
                if isinstance(rotate_chain.content[0],Chain):
                    stack.append(Chain(rotate_chain.content.copy()))
                visualizations.add(chain_str)
        while stack:
            chain = stack.popleft()
            enter_chain = Chain(chain.content[0].content.copy())  # type:ignore
            enter_chain.content.append(Chain(chain.content[1:].copy()))
            chain_str = str(enter_chain)
            if len(enter_chain.content) > 1 and isinstance(enter_chain.content[0], Chain):
                    stack.append(Chain(enter_chain.content.copy()))
            visualizations.add(chain_str)
            rotate_chain = Chain(enter_chain.content.copy())
            for _ in range(len(enter_chain.content) - 1):
                rotate_chain.content.append(rotate_chain.content.pop(0))
                chain_str = str(rotate_chain)
                if chain_str not in visualizations:
                    if isinstance(rotate_chain.content[0], Chain):
                        stack.append(Chain(rotate_chain.content.copy()))
                    visualizations.add(chain_str)
        vis_sort = sorted(visualizations, reverse=True)
        self.string = vis_sort[0]
        return self.string

    def __hash__(self) -> int:
        return hash(self.unique_str())

def convert(text:str) -> Chain:
    chain_stack: list[Chain] = [Chain()]
    for char in text[1:]:
        if char == "[":
            new_chain = Chain()
            chain_stack[-1].content.append(new_chain)
            chain_stack.append(new_chain)
        elif char == "]":
            if len(chain_stack) == 1:
                return chain_stack[0]
            chain_stack.pop()
        else:
            chain_stack[-1].content.append(char)
    return chain_stack[0]


def explore_keys(initial_chains: set[Chain]) -> None:
    begin = time.time()
    previous_chains: set[Chain] = initial_chains
    for level in range(10):
        print(f"## KEY {level + 1}\n")
        all_chains: set[Chain] = set()
        for chain in previous_chains:
            chain_str = str(chain)
            for index in range(1,len(chain_str)):
                sub_chain = convert(
                    f"{chain_str[:index]}K{chain_str[index:]}"
                )
                all_chains.add(sub_chain)
        print(f"{level + 1} : {len(all_chains)}")
        previous_chains = all_chains
        if len(previous_chains) >= 500000:
            return
    print(time.time() - begin)


def main() -> None:
    start_level = 1
    end_level = 5
    previous_chains: set[Chain] = set()
    for level in range(end_level):
        print(f"\n## CHAINS {level + 1}\n")
        initial_chains: set[Chain] = set()
        if len(previous_chains) == 0:
            initial_chains.add(convert("[]"))
        for chain in previous_chains:
            chain_str = str(chain)
            for index in range(1,len(chain_str)):
                sub_chain = convert(
                    f"{chain_str[:index]}[]{chain_str[index:]}"
                )
                initial_chains.add(sub_chain)
        print(f"{level + 1} : {len(initial_chains)}")
        previous_chains = initial_chains
        if level < start_level - 1:
            continue
        explore_keys(initial_chains)
        if level >= end_level:
            break

if __name__ == "__main__":
    import cProfile
    cProfile.run("main()")