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
        self.unique_string = ""
        self.family = 0

    def __str__(self) -> str:
        if self.unique_string != "":
            return self.unique_string
        if self.string != "":
            return self.string
        text = ""
        if self.content:
            for chain in self.content:
                text += str(chain)
        self.string = f"[{text}]"
        return self.string

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chain):
            raise NotImplementedError("only comparable with chains")
        return self.unique_str() == other.unique_str()

    def get_family(self) -> int:
        if not self.family:
            self.unique_str()
        return self.family

    def unique_str(self) -> str:
        if self.unique_string != "":
            return self.unique_string
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
        self.unique_string = vis_sort[0]
        self.family = len(visualizations)
        return self.unique_string

    def __hash__(self) -> int:
        return hash(self.unique_str())


def convert(text: str) -> Chain:
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


def explore_keys(initial_chain: Chain) -> dict[int, int]:
    previous_chains: set[Chain] = {initial_chain}
    total = {l: 0 for l in range(11)}
    for level in range(10):
        all_chains: set[Chain] = set()
        for chain in previous_chains:
            chain_str = str(chain)
            for index in range(1, len(chain_str)):
                sub_chain = convert(f"{chain_str[:index]}K{chain_str[index:]}")
                all_chains.add(sub_chain)
        total[level + 1] = len(all_chains)
        previous_chains = all_chains
    return total


def process_chain(chain: Chain) -> tuple[Chain, dict[int, int], float]:
    begin = time.time()
    new_total = explore_keys(chain)
    return chain, new_total, time.time() - begin


def main() -> None:
    start_level = 8
    end_level = 10
    previous_chains: set[Chain] = set()
    for level in range(end_level):
        print(f"\n## CHAINS {level + 1}\n")
        initial_chains: set[Chain] = set()
        if len(previous_chains) == 0:
            initial_chains.add(convert("[]"))
        for chain in previous_chains:
            chain_str = str(chain)
            for index in range(1, len(chain_str)):
                sub_chain = convert(f"{chain_str[:index]}[]{chain_str[index:]}")
                initial_chains.add(sub_chain)
        previous_chains = initial_chains
        if level < start_level - 1:
            continue
        total = {l: 0 for l in range(11)}
        total[0] = len(initial_chains)
        families: dict[int, list[Chain]] = {}
        for chain in initial_chains:
            family = chain.get_family()
            if family not in families:
                families[family] = []
            families[family].append(chain)
        begin_total = time.time()
        for family, chains in sorted(families.items()):
            chain, new_total, elapsed = process_chain(chains[0])
            for key, value in new_total.items():
                total[key] += value * len(chains)
            print(
                f"⏱️ {elapsed:.2f}s | "
                f"🔗 {len(families)} | "
                f"🧬 {chain} | "
                f"✨ {new_total}"
            )
        print(f"\n🌸 TOTAL: {time.time() - begin_total:.2f}s")
        for key, value in total.items():
            print(f"{key} : {value}")
        if level >= end_level:
            break


if __name__ == "__main__":
    main()
