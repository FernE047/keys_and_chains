import time


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

    def copy(self) -> "Chain":
        new_content: list[Chain | str] = [
            chain.copy() if isinstance(chain, Chain) else chain
            for chain in self.content
        ]
        chain = Chain(new_content)
        return chain

    def rotate(self) -> "Chain":
        new_chain = Chain(self.content.copy())
        new_chain.content.append(new_chain.content.pop(0))
        return new_chain

    def enter(self) -> "Chain":
        new_chain = Chain(
            [
                chain.copy() if isinstance(chain, Chain) else chain
                for chain in self.content[0].content  # type:ignore
            ]
        )
        new_chain.content.append(
            Chain(
                [
                    chain.copy() if isinstance(chain, Chain) else chain
                    for chain in self.content[1:]  # type:ignore
                ]
            )
        )
        return new_chain

    def __str__(self) -> str:
        if self.string != "":
            return self.string
        text = ""
        if self.content:
            for chain in self.content:
                text += str(chain)
        return f"[{text}]"

    def get_visualizations(self) -> "list[str]":
        visualizations: list[str] = [str(self)]
        stack: list[Chain] = [self]
        while stack:
            chain = stack.pop(0)
            if not chain.content:
                continue
            if isinstance(chain.content[0], Chain):
                enter_chain = chain.enter()
                if str(enter_chain) not in visualizations:
                    visualizations.append(str(enter_chain))
                    stack.append(enter_chain)
            if len(chain.content) <= 1:
                continue
            rotate_chain = chain.rotate()
            if str(rotate_chain) not in visualizations:
                visualizations.append(str(rotate_chain))
                stack.append(rotate_chain)
        return visualizations

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chain):
            raise NotImplementedError("only comparable with chains")
        return self.unique_str() == other.unique_str()

    def unique_str(self) -> str:
        if self.string:
            return self.string
        vis_sort = sorted(self.get_visualizations(), reverse=True)
        self.string = vis_sort[0]
        self.visualizations = None
        return self.string

    def __hash__(self) -> int:
        return hash(self.unique_str())


def convert_it(text: str, index: int) -> tuple[Chain | str, int]:
    chain = Chain()
    char = text[index]
    index += 1
    if char not in ["[", "]"]:
        return char, index
    text_size = len(text)
    while index < text_size:
        char = text[index]
        if char == "]":
            index += 1
            return chain, index
        new_chain, index = convert_it(text, index)
        chain.content.append(new_chain)
    return chain, index


def convert_text_to_chain(text: str) -> Chain:
    chain, _ = convert_it(text, 0)
    assert isinstance(chain, Chain)
    return chain


def explore_keys(initial_chains: set[Chain]) -> None:
    begin = time.time()
    previous_chains: set[Chain] = initial_chains
    for level in range(10):
        print(f"## KEY {level + 1}\n")
        all_chains: set[Chain] = set()
        for chain in previous_chains:
            chain_str = str(chain)
            for index in range(1,len(chain_str)):
                sub_chain = convert_text_to_chain(
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
            initial_chains.add(convert_text_to_chain("[]"))
        for chain in previous_chains:
            chain_str = str(chain)
            for index in range(1,len(chain_str)):
                sub_chain = convert_text_to_chain(
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