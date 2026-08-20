import time
from typing import Literal

ChainTypes = Literal["Chain", "Key"]
LETTERS = "ABCDEZXYWT"


class Chain:
    category: ChainTypes

    def __init__(
        self,
        category: ChainTypes,
        content: "list[Chain]|None" = None,
        name: str = ""
    ) -> None:
        self.name = name
        self.category = category
        if content is None:
            self.content: list[Chain] = []
        else:
            self.content = content
        self.visualizations: set[str] | None = None
        self.has_all_vis = False
        self.string = ""

    def get_visualizations(self) -> set[str]:
        if self.visualizations is None:
            self.visualizations = {str(self)}
        return self.visualizations

    def append_visualization(self, chain: "Chain") -> None:
        if self.visualizations is None:
            self.visualizations = {str(self)}
        self.visualizations.add(str(chain))

    def copy(self) -> "Chain":
        new_content: list[Chain] = [chain.copy() for chain in self.content]
        chain = Chain(self.category, new_content)
        chain.visualizations = self.get_visualizations().copy()
        return chain

    def rotate(self) -> "Chain":
        new_chain = Chain(self.category, self.content.copy())
        new_chain.content.append(new_chain.content.pop(0))
        return new_chain

    def enter(self) -> "Chain":
        new_chain = Chain(
            self.content[0].category, [c.copy() for c in self.content[0].content]
        )
        new_chain.content.append(
            Chain(self.category, [c.copy() for c in self.content[1:]])
        )
        new_chain.append_visualization(new_chain)
        return new_chain

    def __str__(self) -> str:
        if self.category == "Key":
            return self.name
        if self.string != "":
            return self.string
        text = ""
        if self.content:
            for chain in self.content:
                text += str(chain)
        return f"[{text}]"

    def print_visualizations(self) -> None:
        vis_sort = sorted(self.get_visualizations())
        for n, vis in enumerate(vis_sort):
            print(f"    {n + 1}. `{vis}`")

    def list_visualizations(self) -> str:
        text = ""
        vis_sort = sorted(self.get_visualizations())
        for n, vis in enumerate(vis_sort):
            text += f"    {n + 1}. `{vis}`\n"
        return text

    def find_all_visualizations(self) -> None:
        if self.has_all_vis:
            return
        stack: list[Chain] = [self]
        while stack:
            chain = stack.pop(0)
            if not chain.content:
                continue
            if chain.content[0].category != "Key":
                enter_chain = chain.enter()
                if str(enter_chain) not in self.get_visualizations():
                    self.append_visualization(enter_chain)
                    stack.append(enter_chain)
            if chain.category == "Key":
                continue
            if len(chain.content) <= 1:
                continue
            rotate_chain = chain.rotate()
            if str(rotate_chain) not in self.get_visualizations():
                self.append_visualization(rotate_chain)
                stack.append(rotate_chain)
        self.has_all_vis = True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chain):
            raise NotImplementedError("only comparable with chains")
        if self.has_all_vis:
            return str(other) in self.get_visualizations()
        if other.has_all_vis:
            return str(self) in other.get_visualizations()
        self.find_all_visualizations()
        return str(other) in self.get_visualizations()

    def unique_str(self) -> str:
        self.find_all_visualizations()
        vis_sort = sorted(self.get_visualizations(), reverse=True)
        return str(vis_sort[0])

    def __hash__(self) -> int:
        return hash(self.unique_str())

    def __repr__(self) -> str:
        return (f"{self.category} : {self.name} : {self.content}")


def convert_it(text: str, index: int) -> tuple[Chain, int]:
    chain = Chain("Chain")
    char = text[index]
    index += 1
    if char in ["[","]"]:
        chain.category = "Chain"
    else:
        chain.category = "Key"
        chain.name = char
        chain.string = char
        return chain, index
    text_size = len(text)
    while index < text_size:
        char = text[index]
        if char == "]":
            chain.string = ""
            chain.visualizations = {str(chain)}
            index += 1
            return chain, index
        new_chain, index = convert_it(text, index)
        chain.content.append(new_chain)
    chain.string = ""
    chain.visualizations = {str(chain)}
    return chain, index


def convert_text_to_chain(text: str) -> Chain:
    chain, _ = convert_it(text, 0)
    return chain


def explore_keys(initial_chains: set[Chain]) -> str:
    begin = time.time()
    text = ""
    previous_chains: set[Chain] = initial_chains
    for level in range(10):
        message = f"## KEY {level + 1}\n\n"
        text += message
        print(message)
        all_chains: set[Chain] = set()
        for chain in previous_chains:
            for vis in chain.get_visualizations():
                for letter in LETTERS:
                    sub_chain = convert_text_to_chain(f"{vis[:-1]}{letter}{vis[-1:]}")
                    all_chains.add(sub_chain)
                    if letter not in vis:
                        break
        message = f"{level + 1} : {len(all_chains)}\n"
        print(message)
        text += message
        previous_chains = all_chains
        if len(previous_chains) >= 50000:
            return text
    print(time.time() - begin)
    return text


def main() -> None:
    start_level = 1
    end_level = 10
    previous_chains: set[Chain] = set()
    text = ""
    for level in range(end_level):
        message = f"\n## CHAINS {level + 1}\n\n"
        text += message
        print(message)
        initial_chains: set[Chain] = set()
        if len(previous_chains) == 0:
            initial_chains.add(convert_text_to_chain("[]"))
        else:
            for chain in previous_chains:
                for vis in chain.get_visualizations():
                    if vis[0] == "(":
                        continue
                    sub_chain = convert_text_to_chain(f"{vis[:-1]}[]{vis[-1:]}")
                    initial_chains.add(sub_chain)
        for n, chain in enumerate(initial_chains):
            text += f"{n + 1}. `{chain}`\n"
        previous_chains = initial_chains
        if level < start_level - 1:
            continue
        text += explore_keys(initial_chains)
    with open("output.md", "w") as file:
        file.write(text)


if __name__ == "__main__":
    main()
