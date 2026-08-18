import time
from typing import Literal

ChainTypes = Literal["Chain", "Key"]


class Chain:
    category: ChainTypes

    def __init__(
        self,
        category: ChainTypes,
        content: "list[Chain]|None" = None,
    ) -> None:
        self.category = category
        if content is None:
            self.content: list[Chain] = []
        else:
            self.content = content
        self.visualizations: set[str]|None = None
        self.has_all_vis = False
        self.string = ""

    def get_visualizations(self) -> set[str]:
        if self.visualizations is None:
            self.visualizations = {str(self)}
        return self.visualizations

    def append_visualization(self, chain:"Chain") -> None:
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
        new_chain = Chain(self.content[0].category, self.content[0].content)
        new_chain.content.append(Chain(self.category,self.content[1:])) # maybe this is a problem because we don't copy
        new_chain.append_visualization(new_chain)
        return new_chain

    def __str__(self) -> str:
        if self.string != "":
            return self.string
        text = ""
        if self.content:
            text += ",".join([str(chain) for chain in self.content])
        if self.category == "Chain":
            self.string = f"[{text}]"
        else:
            self.string = f"({text})"
        return self.string

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


def convert_it(text: str, index:int) -> tuple[Chain, int]:
    chain = Chain("Chain")
    char = text[index]
    if char == "[":
        chain.category = "Chain"
    elif char == "(":
        chain.category = "Key"
    index += 1
    text_size = len(text)
    while index < text_size:
        char = text[index]
        if char == ",":
            index += 1
            continue
        if char in ["[", "("]:
            new_chain, index = convert_it(text, index)
            chain.content.append(new_chain)
            index += 1
            continue
        chain.string = ""
        chain.visualizations = {str(chain)}
        return chain, index
    chain.string = ""
    chain.visualizations = {str(chain)}
    return chain, index


def convert_text_to_chain(text: str) -> Chain:
    chain, _ = convert_it(text, 0)
    return chain

def main() -> None:
    begin = time.time()
    initial_chains = {
        convert_text_to_chain("[[[[]]]]"),
        convert_text_to_chain("[[[],[]]]]"),
    }
    text = ""
    for n, chain in enumerate(initial_chains):
        text += f"{n + 1}. `{chain}`\n"
    previous_chains: set[Chain] = initial_chains
    for level in range(10):
        text += f"## KEY {level + 1}\n\n"
        all_chains: set[Chain] = set()
        for chain in previous_chains:
            for vis in chain.get_visualizations():
                if vis[0] == "(":
                    continue
                sub_chain = convert_text_to_chain(f"{vis[:-1]}(){vis[-1:]}")
                all_chains.add(sub_chain)
        print(f"{level + 1} : {len(all_chains)}")
        for n, chain in enumerate(all_chains):
            text += f"{n + 1}. `{chain.unique_str()}`\n"
            # text += chain.list_visualizations() + "\n"
        text += "\n"
        previous_chains = all_chains
    with open("output.md", "w") as file:
        file.write(text)
    print(time.time() - begin)

if __name__ == '__main__':
    main()
