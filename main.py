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
        stack: deque[Chain] = deque([self])
        while stack:
            chain = stack.popleft()
            if not chain.content:
                continue
            if isinstance(chain.content[0], Chain):
                enter_chain = Chain(chain.content[0].content.copy())  # type:ignore
                enter_chain.content.append(Chain(chain.content[1:].copy()))
                chain_str = str(enter_chain)
                if chain_str not in visualizations:
                    visualizations.add(chain_str)
                    stack.append(enter_chain)
            if len(chain.content) <= 1:
                continue
            rotate_chain = Chain(chain.content.copy())
            rotate_chain.content.append(rotate_chain.content.pop(0))
            chain_str = str(rotate_chain)
            if chain_str not in visualizations:
                visualizations.add(chain_str)
                stack.append(rotate_chain)
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
        previous_chains = initial_chains
        if level < start_level - 1:
            continue
        explore_keys(initial_chains)
        if level >= end_level:
            break

if __name__ == "__main__":
    import cProfile
    cProfile.run("main()")